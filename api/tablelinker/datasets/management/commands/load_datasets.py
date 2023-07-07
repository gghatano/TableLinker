import csv
import os

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Dataset

User = get_user_model()


class Command(BaseCommand):
    help = "初期データの投入"

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **kwargs):
        system_user_id = "94010a7d-ef2f-4732-8382-cc3ce6fa2b3b"

        # TODO：引数化
        opendata_path = "db/seed/opendata/"

        list_path = self._opendata_listfile_path(opendata_path=opendata_path)

        total_count = 0
        success_count = 0
        failer_count = 0

        system_user = self._get_system_user(system_user_id)
        for name, url, csvpath in self._open_opendata_list(list_path=list_path):
            csv_abs_path = os.path.join(os.path.abspath(opendata_path), csvpath)
            print("load %s(%s)" % (name, csv_abs_path))
            try:

                self._create_dataset(name, url, csv_abs_path, system_user)
                # ログ出力

            except Exception as err:
                print(err)
                print("failure. ()\n")
                failer_count += 1
            else:
                print("success.\n")
                success_count += 1
            finally:
                total_count += 1

        print(
            "summary total: {total_count} ok:{success_count} error:{failer_count}".format(
                total_count=total_count, success_count=success_count, failer_count=failer_count,
            )
        )

    @transaction.atomic()
    def _create_dataset(self, name, url, csvpath, system_user):
        with open(csvpath, mode="rb") as file:
            dataset = Dataset(name=name, created_by=system_user)
            dataset.original_file.save(csvpath, File(file), save=False)
            dataset.set_publish()
            dataset.dataset_group.set_publish()
            dataset.dataset_group.save()
            dataset.save()
            dataset.analyze(save=True)

    def _opendata_listfile_path(self, opendata_path="db/seed/opendata/", list_filename="list.csv"):
        return os.path.join(os.path.abspath(opendata_path), list_filename)

    def _open_opendata_list(self, list_path):
        print("open file: {list_path}".format(list_path=list_path))
        with open(list_path) as file:
            csv_reader = self._gen_csv_reader(file)

            next(csv_reader)  # headerは、捨てる

            for index, row in enumerate(csv_reader):
                name, url, csvpath = row
                yield (name, url, csvpath)

    def _get_system_user(self, system_user_id):
        return User.objects.get(pk=system_user_id)

    def _gen_csv_reader(self, file):
        return csv.reader(file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True,)


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
