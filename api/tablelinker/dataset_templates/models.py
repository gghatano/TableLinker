import csv
import io
import json
import tempfile
import uuid

from celery.result import AsyncResult
from datasets.models.attr_type import AttrType
from datasets.models import Dataset, DataType
from datasets.tasks import analyze_dataset_task
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from shared.models import TimeStampedModel

User = get_user_model()


class DatasetTemplateQuerySet(models.QuerySet):
    def search(self, keyword):
        return self.icontains_keyword_with_attr_name(keyword).distinct()

    def icontains_keyword_with_attr_name(self, keyword):
        return self.filter(Q(attr_set__name__icontains=keyword) | Q(name__icontains=keyword))

    def icontains_keyword(self, keyword):
        return self.filter(name__icontains=keyword)

    def latest(self):
        return self.order_by("-updated_at")

    def with_attrs(self):
        return self.prefetch_related("attr_set")


class DatasetTemplateManager(models.Manager):
    def get_queryset(self):
        return DatasetTemplateQuerySet(self.model, using=self._db)


class DatasetTemplate(TimeStampedModel):
    """データセットテンプレートモデル"""

    class Meta:
        ordering = ["id"]

    objects = DatasetTemplateManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="名前", max_length=128, db_index=True)
    desc = models.TextField(verbose_name="説明", max_length=1024, null=True)

    source_dataset = models.ForeignKey(
        Dataset,
        verbose_name="作成元データソース",
        on_delete=models.SET_NULL,
        related_name="created_dataset_template_set",
        db_index=True,
        null=True,
    )

    created_by = models.ForeignKey(
        User,
        verbose_name="作成者",
        on_delete=models.CASCADE,
        related_name="created_dataset_template_set",
        db_index=True,
        null=True,
    )

    def __unicode__(self):
        return self.name

    @property
    def attr_names(self):
        sorted_attrs = sorted(self.attrs, key=lambda x: x.index)
        return [attr.name for attr in sorted_attrs]

    @property
    def attrs(self):
        return self.attr_set.all().order_by("index")

    @classmethod
    def create_by_dataset(cls, dataset, user=None, name=None):
        """
        データセットからテンプレートを生成する
        :param dataset:
        :param save:
        :return:
        """
        new_name = "%sテンプレート" % dataset.dataset_group.name if name is None else name

        template = cls(name=new_name, source_dataset=dataset, created_by=user)
        for attr in dataset.attr_set.all():
            template.attr_set.create(
                name=attr.name,
                index=attr.index,
                attr_type=attr.attr_type,
                data_type=attr.data_type,
                sample_values=attr.sample_values,
            )
        template.source_dataset = dataset

        return template


class DatasetTemplateAttr(models.Model):
    """
    データセットテンプレートの属性データ
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset_template = models.ForeignKey(DatasetTemplate, on_delete=models.CASCADE, related_name="attr_set")
    name = models.CharField(verbose_name="名前", max_length=128)
    desc = models.TextField(verbose_name="説明", max_length=1024, null=True)
    index = models.IntegerField(verbose_name="順序", null=False)
    attr_type = models.CharField(verbose_name="意味型", max_length=128,
                                 choices=AttrType.choices(), null=True, default="unknown")
    data_type = models.CharField(verbose_name="データ型", max_length=128,
                                 choices=DataType.choices(), null=True, default="unknown")
    sample_values = models.TextField(verbose_name="サンプル値", max_length=1024, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def attr_type_name(self):
        for attr in AttrType:
            if attr.name == self.attr_type:
                return attr.value

    @property
    def data_type_name(self):
        for attr in DataType:
            if attr.name == self.data_type:
                return attr.value


def apply_template(attr_set, template_attr_set, input_stream, output_stream):
    """
    テンプレート適用のロジック
    attr_set: 変更するデータセットのattr_set
    template_attr_set: テンプレートのattr_set
    input_stream: 入力
    output_stream: 出力
    """
    template_attr_set_length = len(template_attr_set)

    writer = csv.writer(output_stream)
    reader = csv.reader(input_stream)

    # データセットの行を読み取ります。
    header_count = None
    for index, row in enumerate(reader):
        if index == 0:  # header
            header_count = len(row)
            # テンプレートの属性をそのままヘッダとして書き出します。
            headers = [attr.name for attr in template_attr_set]
            writer.writerow(headers)
        else:  # row
            # ヘッダ行と行に列の相違がある場合は、何もしない。
            if header_count != len(row):
                continue

            new_row = [None] * template_attr_set_length

            for template_index, dataset_index in attr_set.items():
                new_row[int(template_index)] = row[int(dataset_index)]

            writer.writerow(new_row)


class DatasetTemplateApplyJob(object):
    """
    テンプレートを適用するモデルです
    """

    def __init__(self, dataset_id, template_id, attr_set, output_name, created_by):
        self.dataset_id = dataset_id
        self.template_id = template_id
        self.attr_set = attr_set
        self.output_name = output_name
        self.created_by = created_by

        self._dataset = None
        self.task_id = None
        self._errros = None
        self.status = None

    def task_result(self):
        return AsyncResult(self.task_id)

    def get_dataset(self):
        return Dataset.objects.get(pk=self.dataset_id)

    def get_template(self):
        return DatasetTemplate.objects.get(pk=self.template_id)

    def create(self):
        """
        データセットテンプレートに合わせたデータセットを作る
        :return:
        """
        dataset = self.get_dataset()
        template = self.get_template()
        template_attr_set = template.attr_set.order_by("index")
        new_dataset = dataset.create_new_version()

        # 変換先の添付ファイルを生成します。
        with tempfile.NamedTemporaryFile(mode="r+", suffix=".csv", delete=False) as output_file:
            # info = codecs.lookup("UTF-8-SIG")
            with dataset.data_file.open(mode="rb") as input_file:
                # with info.streamreader(file, "surrogateescape") as input_file:
                apply_template(self.attr_set, template_attr_set, input_file, output_file)

            output_file.flush()
            output_file.seek(0)

            dataset.dataset_group.name = self.output_name
            dataset.dataset_group.save()

            new_dataset.data_file.save(None, open(output_file.name, "rb"), save=False)
            new_dataset.created_by = self.created_by
            new_dataset.save()
            analyze_dataset_task.delay(new_dataset.id, convert=True)
            self._dataset = new_dataset

    @property
    def errors(self):
        return self._errors.error_messages if self._errors is not None else {}

    @property
    def has_error(self):
        return self._errors.has_error() if self._errors is not None else False

    @property
    def result(self):
        return self._dataset.id

    def is_owner(self, user):
        return True


class DatasetTemplateApplyPreview(object):
    """
    テンプレート適用してプレビューします。
    """

    def __init__(self, dataset_id, template_id, attr_set, output_name, created_by):
        self.dataset_id = dataset_id
        self.template_id = template_id
        self.attr_set = attr_set
        self.output_name = output_name
        self.created_by = created_by

        self.output_string = None
        self.task_id = None
        self._errros = None
        self.status = None

    def task_result(self):
        return AsyncResult(self.task_id)

    def get_dataset(self):
        return Dataset.objects.get(pk=self.dataset_id)

    def get_template(self):
        return DatasetTemplate.objects.get(pk=self.template_id)

    def create(self):
        dataset = self.get_dataset()
        template = self.get_template()
        template_attr_set = template.attr_set.order_by("index")

        with io.StringIO() as output_string:
            with dataset.data_file.open(mode="r") as input_file:
                apply_template(self.attr_set, template_attr_set, input_file, output_string)
            self.output_string = output_string.getvalue()

    @property
    def errors(self):
        return self._errors.error_messages if self._errors is not None else {}

    @property
    def has_error(self):
        return self._errors.has_error() if self._errors is not None else False

    @property
    def result(self):
        return self.output_string

    def is_owner(self, user):
        return True


class DatasetApplyJob(object):
    """
    データセットに直接を適用するモデルです
    """

    def __init__(self, dataset_id, dataset_template_id, attr_set, output_name, created_by):
        self.dataset_id = dataset_id
        self.dataset_template_id = dataset_template_id
        self.attr_set = attr_set
        self.output_name = output_name
        self.created_by = created_by

        self._dataset = None
        self.task_id = None
        self._errros = None
        self.status = None

    def task_result(self):
        return AsyncResult(self.task_id)

    def get_dataset(self):
        return Dataset.objects.get(pk=self.dataset_id)

    def get_dataset_template(self):
        return Dataset.objects.get(pk=self.dataset_template_id)

    def create(self):
        """
        データセットテンプレートに合わせたデータセットを作る
        :return:
        """
        dataset = self.get_dataset()
        template = self.get_dataset_template()
        template_attr_set = template.attr_set.order_by("index")
        template_attr_set_length = len(template_attr_set)
        new_dataset = dataset.create_new_version()

        # 変換先の添付ファイルを生成します。
        with tempfile.NamedTemporaryFile(mode="r+", suffix=".csv", delete=False) as output_file:

            # データセットファイルを開いて処理をします。
            with dataset.data_file.open(mode="r") as input_file:
                writer = csv.writer(output_file)
                reader = csv.reader(input_file)

                # データセットの行を読み取ります。
                header_count = None
                for index, row in enumerate(reader):
                    if index == 0:  # header
                        header_count = len(row)
                        # テンプレートの属性をそのままヘッダとして書き出します。
                        headers = [attr.name for attr in template_attr_set]
                        writer.writerow(headers)
                    else:  # row

                        # ヘッダ行と行に列の相違がある場合は、何もしない。
                        if header_count != len(row):
                            continue

                        new_row = [None] * template_attr_set_length
                        for output_index, input_index in self.attr_set.items():
                            new_row[int(output_index)] = row[int(input_index)]

                        writer.writerow(new_row)

            dataset.dataset_group.name = self.output_name
            dataset.dataset_group.save()

            output_file.flush()
            output_file.seek(0)

            new_dataset.data_file.save(None, open(output_file.name, "rb"), save=False)

            new_dataset.created_by = self.created_by
            new_dataset.save()
            analyze_dataset_task.delay(str(new_dataset.id), convert=True)
            self._dataset = new_dataset

    @property
    def errors(self):
        return self._errors.error_messages if self._errors is not None else {}

    @property
    def has_error(self):
        return self._errors.has_error() if self._errors is not None else False

    @property
    def result(self):
        return self._dataset.id

    def is_owner(self, user):
        return True


class DatasetApplyPreview(object):
    """
    データセット適用してプレビューします。
    """

    def __init__(self, dataset_id, dataset_template_id, attr_set, output_name, created_by):
        self.dataset_id = dataset_id
        self.dataset_template_id = dataset_template_id
        self.attr_set = attr_set
        self.output_name = output_name
        self.created_by = created_by

        self.output_array = None
        self.task_id = None
        self._errros = None
        self.status = None

    def task_result(self):
        return AsyncResult(self.task_id)

    def get_dataset(self):
        return Dataset.objects.get(pk=self.dataset_id)

    def get_dataset_template(self):
        return Dataset.objects.get(pk=self.dataset_template_id)

    def create(self):
        dataset = self.get_dataset()
        template = self.get_dataset_template()
        template_attr_set = template.attr_set.order_by("index")
        template_attr_set_length = len(template_attr_set)

        output_array = []
        with dataset.data_file.open(mode="r") as input_file:
            reader = csv.reader(input_file)

            len_header = None
            for index, row in enumerate(reader):
                if index == 0:  # write header
                    len_header = len(row)
                    headers = [attr.name for attr in template_attr_set]
                    output_array.append(headers)

                else:  # apply row

                    # ヘッダ行と行に列の相違がある場合は、何もしない。
                    if len_header != len(row):
                        continue

                    new_row = [None] * template_attr_set_length
                    for output_index, input_index in self.attr_set.items():
                        new_row[int(output_index)] = row[int(input_index)]

                    output_array.append(new_row)
        self.output_array = output_array

    @property
    def errors(self):
        return self._errors.error_messages if self._errors is not None else {}

    @property
    def has_error(self):
        return self._errors.has_error() if self._errors is not None else False

    @property
    def result(self):
        return json.dumps(self.output_array)

    def is_owner(self, user):
        return True
