import datetime

from factory import DjangoModelFactory, LazyFunction, SubFactory, django, post_generation
from faker import Factory

from users.factory import UserFactory

from datasets.models import Dataset
from datasets.factory import DatasetAttrFactory

f = Factory.create("ja_JP")


def dataset_name():
    return "%s%s利用データ" % (f.city(), f.company_category())


class DatasetFactory(DjangoModelFactory):
    class Meta:
        model = Dataset

    name = LazyFunction(dataset_name)

    original_file = django.FileField(from_path="datasets/fixtures/tests/datasets/default.csv", filename="data.csv")
    # data_file = None

    analyzed_at = datetime.datetime.now()
    created_by = SubFactory(UserFactory)

    @post_generation
    def attr_sets(self, create, extracted, **kwargs):
        return DatasetAttrFactory.create_batch(4, dataset_id=self.id)
