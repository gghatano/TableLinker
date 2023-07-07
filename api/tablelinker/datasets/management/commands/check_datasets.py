import json
import os
import traceback
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from shared.utils import get_encode

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
    help = "データチェック"

    def add_arguments(self, parser):
        parser.add_argument("--datapath", nargs="*", default=["db/seed/selection/"], type=str)

    def handle(self, *args, **options):

        data_paths = options["datapath"]

        # TODO：引数化
        system_user = self._get_system_user(self.SYSTEM_USER_ID)
        for path in data_paths:
            self._load_dataset_from(path, system_user)

    def _load_dataset_from(self, path, system_user):

        catalog_file_paths = self._catalog_file_paths(path)

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
                if os.path.exists(csv_abs_path):
                    error_message = ""
                    try:
                        analyzed_status = self._check_dataset(name, url, csv_abs_path, system_user)
                    except Exception as e:
                        error_message = "{type}:{message}".format(type=type(e), message=str(e))
                        print(error_message)
                        print(traceback.format_exc())
                        analyzed_status = 9
                        counter["failure"] += 1
                    else:
                        counter["success"] += 1
                    finally:
                        counter["total"] += 1

                    log_str = "{analyzed_status},{encoding},{csv_abs_path},{error_message}\n".format(  # noqa: E501
                        encoding=get_encode(csv_abs_path),
                        analyzed_status=str(int(analyzed_status)),
                        csv_abs_path=resource.filename,
                        error_message=error_message,
                    )
                    log.write(log_str)
                    log.flush()
                    print("{count}/{total}:{log_str}".format(log_str=log_str, total=resources_count, count=(idx + 1),))
        finally:
            log.close()
            print(
                "summary total: {total_count} ok:{success_count} error:{failer_count}".format(
                    total_count=counter["total"], success_count=counter["success"], failer_count=counter["failure"],
                )
            )

    @transaction.atomic()
    def _check_dataset(self, name, url, csvpath, system_user):
        with open(csvpath, mode="rb") as file:
            dataset = Dataset(name=name, created_by=system_user)
            status = dataset.check_file(original_file=file)
            return status

    def _catalog_file_paths(self, path, filename=".catalog.json"):
        return Path(path).glob("**/" + filename)

    def _get_system_user(self, system_user_id=SYSTEM_USER_ID):
        return User.objects.get(pk=system_user_id)


# @seed_cli.command('purge', help="purge seeds data.")
# @with_appcontext
# def seed_purge():
#     try:
#         system_user = User.query.filter(User.name == "system").first()
#         [db.session.delete(dataset) for dataset in Dataset.query.filter(
#             Dataset.owner_id == system_user.id)]
#         [db.session.delete(user)
#          for user in User.query.filter(User.name == "system")]
#         db.session.commit()
#         print("complete purge")
#     except:
#         db.session.rollback()
#         print("failer purge")
#         raise
