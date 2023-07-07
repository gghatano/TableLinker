import json
import os
import traceback
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Dataset

User = get_user_model()


class Resource:
    def __init__(self, resource_json, base_path):
        self.id = str(resource_json["id"])
        self.name = str(resource_json["name"])
        self.url = str(resource_json["url"])
        self.format = str(resource_json["format"]).lower()

        self.base_path = os.path.dirname(base_path)

    @property
    def filename(self):
        return os.path.join(self.base_path, self.id + "." + self.format)

    def __str__(self):
        return ",".join([self.id, self.name, self.url])


class Command(BaseCommand):
    SYSTEM_USER_ID = "94010a7d-ef2f-4732-8382-cc3ce6fa2b3b"
    help = "データIMPORT"

    def add_arguments(self, parser):
        parser.add_argument("--datapath", nargs="*", default=["db/seed/selection/"], type=str)

    def handle(self, *args, **options):

        data_paths = options["datapath"]

        # TODO：引数化
        system_user = self.get_system_user(self.SYSTEM_USER_ID)
        for path in data_paths:
            self._load_dataset_from(path, system_user)

    def _load_dataset_from(self, path, system_user):

        catalog_file_paths = self.catalog_file_paths(path)

        resources = []
        for catalog_file_path in catalog_file_paths:
            with open(catalog_file_path, "r") as file:
                catalog_json = json.load(file)
                resources_json = catalog_json["result"]["resources"]
                resources.extend([Resource(resource_json, catalog_file_path) for resource_json in resources_json])

        resources = [resource for resource in resources if os.path.exists(os.path.join(os.path.abspath(resource.filename)))]

        resources_count = len(resources)
        print("count{resources_count}".format(resources_count=resources_count))

        # open log file
        try:
            log = open("import.log", "w")

            counter = {
                "total": 0,
                "success": 0,
                "failure": 0,
            }
            for idx, resource in enumerate(resources):
                name = resource.name
                url = resource.url
                csv_abs_path = os.path.join(os.path.abspath(resource.filename))

                if os.path.exists(csv_abs_path) is False:
                    continue

                error_message = ""
                log_text = None
                print(csv_abs_path, flush=True)

                try:
                    dataset = self.import_dataset(name, url, csv_abs_path, system_user)
                    log_text = "{filepath},{dataset_id},{dataset_status},{encoding},{error_message}\n".format(  # noqa: E501
                        filepath=resource.filename,
                        dataset_id=dataset.id,
                        dataset_status=dataset.status,
                        encoding=dataset.dataset_group.encoding,
                        error_message=error_message,
                    )

                except Exception as e:
                    error_message = "{type}:{message}".format(type=type(e), message=str(e))
                    print(error_message)
                    print(traceback.format_exc())

                    log_text = "{filepath},{dataset_id},{dataset_status},{encoding},{error_message}\n".format(  # noqa: E501
                        filepath=resource.filename,
                        dataset_id=None,
                        dataset_status=None,
                        encoding=None,
                        error_message=error_message,
                    )

                    counter["failure"] += 1
                else:
                    counter["success"] += 1
                finally:
                    counter["total"] += 1
                    log.write(log_text)
                    print("{count}/{total}:{log_text}".format(log_text=log_text, total=resources_count, count=(idx + 1),))

        finally:
            log.flush()
            log.close()
            print(
                "summary total: {total_count} ok:{success_count} error:{failer_count}".format(
                    total_count=counter["total"], success_count=counter["success"], failer_count=counter["failure"],
                )
            )

    @transaction.atomic()
    def import_dataset(self, name, url, csvpath, system_user):
        with open(csvpath, mode="rb") as file:
            dataset = Dataset(name=name, created_by=system_user)
            dataset.original_file.save(csvpath, File(file), save=False)
            dataset.save()
            dataset.analyze(save=True)

            if not dataset.has_annotates:
                dataset.dataset_group.set_publish()
                dataset.dataset_group.save()
            return dataset

    def catalog_file_paths(self, path, filename=".catalog.json"):
        return Path(path).glob("**/" + filename)

    def get_system_user(self, system_user_id=SYSTEM_USER_ID):
        return User.objects.get(pk=system_user_id)
