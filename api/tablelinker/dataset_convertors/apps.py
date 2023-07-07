from django.apps import AppConfig
from django.conf import settings

from convertors.core import loader


class DatasetConvertorsConfig(AppConfig):
    name = "dataset_convertors"

    def ready(self):
        loader.load_dirs(settings.CONV_FILTES_DIRS)
