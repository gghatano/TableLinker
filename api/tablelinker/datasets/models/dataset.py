import codecs
import collections
import csv
import io
import json
from logging import getLogger
import tempfile
import traceback
import uuid
from enum import IntEnum
import jwt
import boto3

import nkf

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile, File
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from inflector import Inflector
from mtab.mtab import MTabAnnotate
from shared.models import TimeStampedModel
from shared.utils import gen_csv_reader, get_encode
from shared.csv_cleaner import CSVCleaner

from .mixins.dataset_annotates import DatasetAnnotatesMixin
from .mixins.dataset_similar_search import DatasetSimilarSearchMixin
from .dataset_group import DatasetGroup

logger = getLogger(__name__)
User = get_user_model()


def content_file_name_by_data(instance, filename):
    return "/".join([slugify(Inflector().pluralize(instance.__class__.__name__)), str(instance.id), "data.csv", ])


def mtab_file_name_by_data(instance, filename):
    return "/".join([slugify(Inflector().pluralize(instance.__class__.__name__)), str(instance.id), "mtab.json", ])


class DatasetQuerySet(models.QuerySet):
    def search(self, keyword):
        return self.icontains_keyword_with_attr_name(keyword).distinct()

    def icontains_keyword_with_attr_name(self, keyword):
        return self.filter(Q(attr_set__name__icontains=keyword) | Q(name__icontains=keyword))

    def icontains_keyword(self, keyword):
        return self.filter(name__icontains=keyword)

    def analyzed(self):
        return self.filter(analyzed_at__isnull=False)

    def latest(self):
        return self.order_by("-updated_at")

    def with_attrs(self):
        return self.prefetch_related("attr_set")

    def with_created_by(self):
        return self.prefetch_related("created_by")

    def with_stared(self, user):
        return self.prefetch_related("stared_users")

    def by_user(self, user):
        return self.filter(created_by_id=user.id)


class DatasetManager(models.Manager):
    def get_queryset(self):
        return DatasetQuerySet(self.model, using=self._db)

    def search(self, keyword):
        return self.get_queryset().search(keyword)


class DatasetStatus(IntEnum):
    UPLOADED = 0  #
    ANALYZE_REQUEST = 10
    ANALYZE_PROCESSING = 20
    ANALYZE_SUCCESS = 50
    ANALYZE_ANNOTATE = 60
    ANALYZE_FAIL = 90


class Dataset(DatasetSimilarSearchMixin, DatasetAnnotatesMixin, TimeStampedModel):
    """データセットモデル"""

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["dataset_group_id", "version"], name="version_unique"),
        ]

    objects = DatasetManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name="名前", max_length=128, null=True, db_index=False)

    dataset_group = models.ForeignKey(
        DatasetGroup, on_delete=models.CASCADE, related_name="dataset_set", default=None, null=True
    )
    filter_json = models.TextField(verbose_name="フィルタ情報", null=True)

    mtab_file = models.FileField(verbose_name="mtab情報", upload_to=mtab_file_name_by_data, blank=True, null=True,)
    file_size = models.IntegerField(verbose_name="ファイルサイズ", null=True, default=None)

    version = models.IntegerField(verbose_name="バージョン", null=False, default=1)

    encoding = models.CharField(verbose_name="文字コード", max_length=128, null=True)
    num_records = models.IntegerField(verbose_name="レコード件数", null=True)
    num_columns = models.IntegerField(verbose_name="列数", null=True)

    data_file = models.FileField(
        verbose_name="データファイル",
        upload_to=content_file_name_by_data,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["csv", "tsv"])],
    )

    analyzed_at = models.DateTimeField(verbose_name="解析完了日時", null=True, db_index=True)

    status = models.IntegerField(verbose_name="ステータス", null=True, default=0)

    analyzed_status = models.IntegerField(verbose_name="解析結果のステータス", null=True,)

    created_by = models.ForeignKey(
        User, verbose_name="作成者", on_delete=models.CASCADE, related_name="created_dataset_set", db_index=True,
    )

    stared_users = models.ManyToManyField("users.User", through="DatasetUserStar", related_name="star_datasets")

    @property
    def filter_detail(self):
        if self.filter_json is None:
            return ""
        # TODO
        return self.filter_json

    @property
    def attr_names(self):
        sorted_attrs = sorted(self.attrs, key=lambda x: x.index)
        return [attr.name for attr in sorted_attrs]

    @property
    def attrs(self):
        return self.attr_set.all().order_by("index")

    @property
    def data_file_url(self):
        if not self.data_file:
            return None
        else:
            secret = settings.SECRET_KEY
            token = jwt.encode(
                {"sub": self.id, "dataset_id": self.id, }, secret, algorithm="HS256", headers={"alg": "HS256", "typ": "JWT"}
            )
            return "/download/datasets/" + token

    @property
    def is_analyzed(self):
        return self.analyzed_at is not None

    @property
    def created_by_name(self):
        return self.self.created_by.name

    def is_stared(self, user):
        return self.stared_users.filter(pk=user.id).exists()

    def is_owner(self, resource):
        return self.created_by == resource

    def similar_search_text(self):
        """
        カラム名をカンマで結合した文字列を返す
        """
        return ",".join([attr.name for attr in self.attrs])

    def analyze(self, save=True, convert=False):  # noqa: C901
        """オリジナルファイルの解析処理"""
        try:
            self.status = DatasetStatus.ANALYZE_PROCESSING
            if save:
                self.save()

            self.set_encoding()

            if not self.dataset_group.encoding:
                self.dataset_group.encoding = self.encoding
                self.dataset_group.save()

            if bool(self.dataset_group.original_file) and not convert:
                self.set_data_file_from_original_file()

            # 止まっているっぽいので一旦中止
            # self.mtab_annotate()

            if not self.has_annotates:
                self.analyze_csv_file()
                self.set_word_vec()

            if self.has_annotates:
                self.status = DatasetStatus.ANALYZE_ANNOTATE
            else:
                self.status = DatasetStatus.ANALYZE_SUCCESS

            self.analyzed_at = timezone.now()

            if save:
                self.save()

            if self.has_annotates:
                self.save()

        except Exception as e:
            print("error.")
            print(traceback.format_exc())
            try:
                dataset = Dataset.objects.get(pk=self.id)
                if dataset:
                    message = "不明なエラーです。({})".format(e)
                    dataset.add_annotate(message)
                    dataset.analyzed_at = timezone.now()
                    dataset.status = DatasetStatus.ANALYZE_FAIL
                    if save:
                        dataset.save()
            except Exception:
                print("analyze error in except")
                raise
            raise

    def mtab_annotate(self):
        try:
            mtab_client = MTabAnnotate()
            mtab_client.annotate(self.data_file)
            self.mtab_file.save(None, ContentFile(json.dumps(mtab_client.result, indent=4).encode("utf-8")))
        except Exception:
            self.add_annotate("mtabの解析でエラーが発生しました")
            print(traceback.format_exc())

    def set_analyze_request(self):
        self.status = DatasetStatus.ANALYZE_REQUEST
        self.save()

    def set_encoding(self):
        """文字コードの判定"""
        # original_fileが無い場合は、変換されたものなので、UTF−8とみなす
        # self.encoding = get_encode(self.dataset_group.original_file.file) if bool(
        #     self.dataset_group.original_file) else "UTF-8-SIG"
        self.encoding = "UTF-8"

    def set_data_file_from_original_file(self):
        bucket_name = getattr(settings, "AWS_STORAGE_BUCKET_NAME", None)
        access_key = getattr(settings, "AWS_ACCESS_KEY_ID", None)
        secret_key = getattr(settings, "AWS_SECRET_ACCESS_KEY", None)

        if bucket_name:
            # S3を使用する場合
            key = self.dataset_group.original_file.name
            temp_file = tempfile.NamedTemporaryFile()

            s3 = boto3.resource("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
            s3.Bucket(bucket_name).download_file(Filename=temp_file.name, Key=key)

            try:
                try:
                    info = codecs.lookup(self.encoding)
                except LookupError:
                    # バイナリ判定のエラーが出る場合は、UTF-8で読み込む
                    info = codecs.lookup("utf-8")

                with open(temp_file.name, mode="r+", encoding="UTF-8-SIG") as utf_bom_csv_file:
                    csv_writer = csv.writer(utf_bom_csv_file)
                    with self.dataset_group.original_file.open(mode="rb") as file:
                        with info.streamreader(file, "surrogateescape") as reader:
                            csv_reader = gen_csv_reader(reader)
                            for index, row in enumerate(csv_reader):
                                try:
                                    csv_writer.writerow(row)
                                except UnicodeError as e:
                                    max_size = len(e.object)  # TODO: memorize
                                    cutting_size = 5
                                    start = e.start - cutting_size if e.start > cutting_size else e.start
                                    end = e.end + cutting_size if e.end < max_size + cutting_size else e.end
                                    error_data = e.object[start: e.start] + "??" + e.object[e.end: end]
                                    message = "変換できない文字コードがありました。" + str(index) + "行目:" + error_data
                                    self.add_annotate(message)
                self.data_file.save(None, File(open(utf_bom_csv_file.name, "rb")), save=False)
            finally:
                temp_file.close()
        else:
            with self.dataset_group.original_file.open(mode="rb") as file:
                data = file.read()
                with CSVCleaner(data, useDictReader=False) as cc, \
                        io.StringIO(newline="") as fout:
                    writer = csv.writer(fout, quoting=csv.QUOTE_MINIMAL)
                    for row in cc:
                        writer.writerow(row)

                    self.data_file.save(
                        None, ContentFile(fout.getvalue().encode("utf-8")))

    def analyze_csv_file(self):
        """CSVファイルから以下の抽出を行います。
        - 列名
        - レコード数
        - ファイルサイズ
        """
        # info = codecs.lookup("UTF-8-SIG")
        with self.data_file.open(mode="r") as file:
            # with info.streamreader(file, "surrogateescape") as reader:
            csv_reader = gen_csv_reader(file)

            # ヘッダデータの作成
            header_str = next(csv_reader)
            header_names = [name for name in header_str]
            self.num_columns = len(header_names)

            # データセットの属性を生成
            # 既存のデータセットの名前と型の対応表を作成
            type_map = {
                attr.name: [attr.attr_type, attr.data_type]
                for attr in self.attrs.all()}

            self.attr_set.all().delete()
            # 新たに作成する属性に対し、属性名が既存のデータセットに
            # 存在する名前ならば、以前の型を付与する
            attrs = []
            for index, name in enumerate(header_names):
                new_attr = self.attr_set.create(name=name, index=index)
                if name in type_map:
                    new_attr.attr_type, new_attr.data_type = type_map[name]

                attrs.append(new_attr)

            # 型判定ロジックの生成
            data_type_resolvers = [attr.data_type_resolver() for attr in attrs]

            # mtabの解析自体をスキップ
            attr_type_resolvers = [attr.attr_type_resolver() for attr in attrs]

            # データのScan処理
            num_records = 0
            line_cols = []
            try:
                # Scan Line
                last_index = None  # エラーメッセージの行番号表示用
                for index, record in enumerate(csv_reader):
                    ncols = len(record)
                    if ncols == 0:
                        # 空行はスキップ
                        continue
                    elif len(''.join(record)) == 0:
                        # カンマだけの行もスキップ
                        continue
                    elif ncols < self.num_columns:
                        line = ','.join(record)
                        self.add_annotate(f"{index + 1}行目の列数が不一致({ncols}/{self.num_columns})")
                        continue

                    line_cols.append(ncols)
                    num_records += 1
                    last_index = index

                    # 属性データの収集
                    for record_index, resolver in enumerate(data_type_resolvers):
                        resolver.append(record, record_index)

                    # mtabの解析自体をスキップ
                    for record_index, resolver in enumerate(attr_type_resolvers):
                        resolver.append(record, record_index)

                # 型の決定
                for resolver in data_type_resolvers:
                    resolver.resolve()

                # 属性型の決定
                # mtabの解析自体をスキップ
                for resolver in attr_type_resolvers:
                    resolver.resolve()

            except UnicodeError:
                message = "変換できない文字コードがありました。" + str(last_index + 1) + "行目"
                self.add_annotate(message)

            # check coment line.
            line_cols_map = collections.Counter(line_cols)
            if len(line_cols_map.keys()) > 1:
                if line_cols[0] == 1:
                    self.add_annotate("コメント行が存在する可能性があります。")
                else:
                    self.add_annotate("列数の違うデータが含まれています。")

            self.num_records = num_records
            self.file_size = self.data_file.size

    @classmethod
    def create_new_version(self, dataset_group, user):
        new_dataset = Dataset()
        new_dataset.dataset_group = dataset_group
        new_dataset.version = dataset_group.max_version + 1
        new_dataset.created_by = user
        new_dataset.save()

        # 前のバージョンがあるなら、属性をコピーする
        current_dataset = dataset_group.current_dataset
        if current_dataset is not None:
            logger.debug("create_new_version: current_version={}".format(
                current_dataset.version))
            for attr in current_dataset.attrs.all():
                logger.debug((
                    f"{attr.index}:'{attr.name}','{attr.attr_type}',"
                    f"'{attr.data_type}','{attr.sample_values}'"))
                new_dataset.attr_set.create(
                    name=attr.name,
                    index=attr.index,
                    attr_type=attr.attr_type,
                    data_type=attr.data_type,
                    sample_values=attr.sample_values,
                )
        else:
            logger.debug("create_new_version: current_version=None")

        return new_dataset


class DatasetCurrentVersion(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    dataset = models.OneToOneField(
        Dataset,
        on_delete=models.CASCADE,
        related_name="current_version")
    dataset_group = models.OneToOneField(
        DatasetGroup,
        on_delete=models.CASCADE,
        related_name="current_version")
