import csv
import io
from logging import getLogger
import tempfile

from convertors.core import CollectionProxy, filter_find_by
from convertors.core.input import CsvInputCollection, registry_input
from convertors.core.output import CsvOutputCollection, registry_output
from convertors.core.proxy import registry_proxy
from datasets.models import Dataset, DatasetGroup
from django.core.files import File
from django.db import transaction
from shared.utils import gen_csv_reader
from users.models import User

logger = getLogger(__name__)


class DatasetInputCollection(CsvInputCollection):
    def __init__(self, dataset):
        self._dataset = dataset
        self.filepath = dataset.data_file.path
        self._file = None
        self._reader = None

    def file(self):
        return self._file

    def encode(self):
        return [self._dataset.id]

    @classmethod
    def decode(cls, args):
        dataset = Dataset.objects.get(id=args[0])
        return cls(dataset)


class DatasetOutputCollection(CsvOutputCollection):
    def __init__(self, dataset_id=None, user_id=None, dataset_group_id=None, filter_key=None, filter_params=None):
        super(DatasetOutputCollection, self).__init__(None)
        self.dataset_id = dataset_id
        self.dataset_group_id = dataset_group_id
        self.user_id = user_id
        self._dataset = None
        self.filter_key = filter_key
        self.filter_params = filter_params

    def open_file(self):
        return tempfile.NamedTemporaryFile(mode="r+", suffix=".csv")

    def get_filter(self):
        print(self.filter_key)
        return filter_find_by(self.filter_key)

    def get_filter_message(self):
        return self.get_filter().get_message(self.filter_params)

    def close(self):
        self._file.flush()  # これがないと反映されない

        with transaction.atomic():
            user = User.objects.get(pk=self.user_id)
            dataset_group = DatasetGroup.objects.get(pk=self.dataset_group_id)

            # データセットの生成
            new_dataset = Dataset.create_new_version(dataset_group, user)
            new_dataset.name = self.get_filter_message()
            new_dataset.filter_json = {
                "key": self.filter_key,
                "params": self.filter_params,
            }
            new_dataset.data_file.save(None, File(open(self._file.name, "rb")), save=False)
            new_dataset.save()
            self._dataset = new_dataset

            # io close
            super().close()

            # 解析
            new_dataset.analyze(convert=True)

            # カレントの設定
            new_dataset.refresh_from_db()
            if new_dataset.is_analyzed:
                dataset_group.set_current_version(new_dataset)
            else:
                new_dataset.delete()

    def get_data(self):
        return self._dataset.id if self._dataset else self.dataset_id

    def getInput(self):
        # TOOD:
        return None

    def encode(self):
        dataset_id = self._dataset.id if self._dataset is not None else None
        return [dataset_id, self.user_id, self.dataset_group_id, self.filter_key, self.filter_params]

    @classmethod
    def decode(cls, args):
        return cls(args[0], args[1], args[2], args[3], args[4])


class DatasetCollectionProxy(CollectionProxy):
    @property
    def filepath(self):
        return self.value

    @property
    def dataset(self):
        dataset_group = DatasetGroup.objects.get(pk=self.value)
        return dataset_group.current_dataset

    def data_read(self, with_headers=False):
        with io.TextIOWrapper(
                self.dataset.data_file.open(mode="rb"), 'utf-8') as file:
            reader = gen_csv_reader(file)
            if with_headers is False:
                reader.__next__()
            for record in reader:
                yield record


registry_input(DatasetInputCollection)
registry_output(DatasetOutputCollection)
registry_proxy(DatasetCollectionProxy)
