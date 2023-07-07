from django.db import models


class DatasetAnnotatesMixin(models.Model):
    """
    注釈関連の実装
    """

    class Meta:
        abstract = True

    @property
    def annotate_messages(self):
        return [attr.message for attr in self.annotates]

    @property
    def annotates(self):
        return self.annotate_set.all()

    @property
    def has_annotates(self):
        return self.annotate_set.count() > 0

    def add_annotate(self, message):
        self.annotate_set.create(message=message)

    def clear_annotates(self):
        self.annotates.delete()
