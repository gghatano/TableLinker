from factory import DjangoModelFactory, LazyFunction, Sequence
from faker import Factory

from datasets.models import DatasetAttr

f = Factory.create("ja_JP")


def dataset_attr_name():
    return f.job()


class DatasetAttrFactory(DjangoModelFactory):
    class Meta:
        model = DatasetAttr

    name = LazyFunction(dataset_attr_name)
    index = Sequence(lambda n: n)
