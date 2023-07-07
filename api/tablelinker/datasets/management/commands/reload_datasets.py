from django.core.management.base import BaseCommand

from shared.utils import batch_qs

from ...models import Dataset


class Command(BaseCommand):
    help = "初期データの投入"

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **kwargs):

        datasets = Dataset.objects.all().analyzed().published().latest()
        for _, _, _, qs in batch_qs(datasets):
            for dataset in qs:
                dataset.analyze(save=True)
