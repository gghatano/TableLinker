import csv
import enum
import graphene
import io
import logging
import nkf
import requests
from time import sleep

from datasets.models import Dataset, DatasetGroup, DatasetAttr, DatasetCurrentVersion, DatasetSource
from datasets.tasks import analyze_dataset_task
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from graphql_jwt.decorators import login_required
from graphql_schema.types.objects import (
    DatasetGroupType,
    CreateDatasetGroupInputType,
    UpdateDatasetGroupInputType,
    AnalyzeDatasetGroupInputType,
    UpdateDatasetAttrInputType,
    DatasetAttrType,
)
from users.models import User
from shared.csv_cleaner import CSVCleaner

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "インポートコマンド"

    def add_arguments(self, parser):
        parser.add_argument('--email', nargs='?', default='', type=str, required=True)
        parser.add_argument('--script-args', nargs='?', default='', type=str)

    def handle(self, *args, **options):
        email = options["email"]
        user = User.objects.get(email=email)  # may raise no user exception

        # "サイト名","データセット名","リソース名","サイトURL"
        with open(options["script_args"], 'r', newline='') as f:
            reader = csv.DictReader(f)

            for num, row in enumerate(reader):
                site_name = row["サイト名"].replace(" ", "")
                site_url = row["サイトURL"].replace(" ", "")
                dataset_name = "{}-{}".format(
                    row["データセット名"], row["リソース名"])[0:40]
                source_data = {'site_name': site_name, 'site_url': site_url}
                directory_list = source_data['site_url'].split("/")
                file_name = directory_list[len(directory_list) - 1]

                if file_name.rfind("csv") < 0:  # CSV 以外今のところ非対応
                    continue

                dataset = None
                with transaction.atomic():

                    dataset_group = DatasetGroup()
                    dataset_group.name = dataset_name
                    dataset_group.created_by_id = str(user.id)
                    dataset_group.created_by = user
                    try:

                        if source_data['site_url'].count("http"):
                            # HTTPでの指定
                            response = requests.get(source_data['site_url'])
                            data = response.content
                        else:
                            with open(source_data['site_url'], "rb") as input_original_file:
                                data = input_original_file.read()

                        with CSVCleaner(data, useDictReader=False) as cc, \
                                io.StringIO(newline="") as fout:
                            writer = csv.writer(fout, quoting=csv.QUOTE_MINIMAL)
                            for row in cc:
                                writer.writerow(row)

                            dataset_group.original_file.save(
                                file_name,
                                ContentFile(fout.getvalue().encode("utf-8")))

                    except Exception as e:
                        print(f"{dataset_name} を処理中に例外発生（スキップ）")
                        logger.error(e)
                        continue

                    logger.error(f"{file_name} を処理中...")
                    dataset_group.save()

                    dataset = Dataset()
                    dataset.name = "アップロードしました。"
                    dataset.created_by = user
                    dataset.dataset_group = dataset_group
                    dataset.save()

                    current_version = DatasetCurrentVersion(dataset_group=dataset_group, dataset=dataset)
                    current_version.save()

                    if source_data is not None:
                        source_data = {
                            'site_name': site_name[0:40],
                            'site_url': site_url[0:60]
                        }
                        DatasetSource.objects.create(dataset_group=dataset_group, **source_data)

                    # 同期実行
                    dataset.analyze()

                    # 非同期実行
                    # dataset.set_analyze_request()

                    dataset.save()
