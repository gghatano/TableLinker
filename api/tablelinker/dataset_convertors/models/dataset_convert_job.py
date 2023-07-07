from celery.result import AsyncResult

# from convertors.core import LocalJob
from convertors.core import filter_find_by

from convertors.celery import CeleryAsyncJob
from datasets.models import Dataset

from ..convertor_extends import DatasetCollectionProxy, DatasetInputCollection, DatasetOutputCollection


class DatasetConvertJob(object):
    def __init__(self, dataset_id, filter_key, filter_params, created_by, dataset_group_id):
        self.dataset_id = dataset_id
        self.dataset_group_id = dataset_group_id
        self.filter_key = filter_key
        self.filter_params = filter_params
        self.created_by = created_by

        self.input = None
        self.output = None
        self.task_id = None
        self._errors = None
        self.status = None

        self.job = None

    def task_result(self):
        return AsyncResult(self.task_id)

    def get_filter(self):
        return filter_find_by(self.filter_key)

    def get_dataset(self):
        return Dataset.objects.get(pk=self.dataset_id)

    def create(self):
        filter = self.get_filter()
        dataset = self.get_dataset()

        self.input = DatasetInputCollection(dataset)
        self.output = DatasetOutputCollection(
            dataset.id, self.created_by.id, self.dataset_group_id, self.filter_key, self.filter_params
        )

        # self.job = LocalJob(filter, self.filter_params, self.input, self.output, proxy=DatasetCollectionProxy,)
        self.job = CeleryAsyncJob(filter, self.filter_params, self.input, self.output, proxy=DatasetCollectionProxy,)

        if self.job.run():
            self.status = "success"
        else:
            self._errors = self.job.errors()
            self.status = "invalid"

    @property
    def errors(self):
        return self._errors.error_messages if self._errors is not None else {}

    @property
    def error_messages(self):
        return (
            [message for _, messages in self.errors.items() for message in messages]
            if self._errors is not None and self._errors.has_error()
            else []
        )

    @property
    def has_error(self):
        return self._errors.has_error() if self._errors is not None else False

    def is_invalid(self):
        return self.status == "invalid"

    @property
    def result(self):
        return self.job.get_result().get_data()

    def is_owner(self, user):
        return True
