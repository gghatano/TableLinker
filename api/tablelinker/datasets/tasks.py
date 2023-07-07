from config.celery import app
from .models import Dataset


@app.task(name="analyze_dataset_task")
def analyze_dataset_task(dataset_id, convert=False):

    print("analyze_dataset_task", flush=True)
    dataset = Dataset.objects.get(pk=dataset_id)
    dataset.analyze(convert=convert)
    print("analyze_dataset_task end", flush=True)
    return True
