import json

from celery.result import AsyncResult

from convertors.core import ArrayOutputCollection, LocalJob, filter_find_by
from datasets.models import Dataset

from ..convertor_extends import DatasetCollectionProxy, DatasetInputCollection


class DatasetPreview(object):
    def __init__(self, dataset_id, filter_key, filter_params):
        self.dataset_id = dataset_id
        self.filter_key = filter_key
        self.filter_params = filter_params

        self.task_id = None
        self._result = None
        self._errors = None
        self.status = None
        self.job = None

        self._filter = filter_find_by(self.filter_key)
        self._dataset = self.get_dataset()

    def task_result(self):
        return AsyncResult(self.task_id)

    def get_dataset(self):
        return Dataset.objects.get(pk=self.dataset_id)

    def create(self):
        """
        プレビューのデータを処理をします。
        返還との違いは、Outputとして、配列を出力するようにしていることです。
        ArrayOutputCollection()
        :return:
        """
        self.input = DatasetInputCollection(self._dataset)
        self.output = ArrayOutputCollection()
        self.job = LocalJob(self._filter, self.filter_params, self.input, self.output, proxy=DatasetCollectionProxy,)

        # self.job = CeleryAsyncJob(
        #     filter,
        #     self.filter_params,
        #     self.input,
        #     self.output,
        #     proxy=DatasetCollectionProxy,
        # )

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
        return self._errors.has_error()

    def is_invalid(self):
        return self.status == "invalid"

    @property
    def result(self):
        return json.dumps(self.job.get_result().get_data())

    def is_owner(self, user):
        return True
