from django.forms import ModelForm

from shared.forms import BulamFormMixin

from .models import DatasetGroup, DatasetSource


class DatasetCreateForm(BulamFormMixin, ModelForm):
    class Meta:
        model = DatasetGroup
        fields = ("original_file", "name")


class DatasetSourceForm(BulamFormMixin, ModelForm):
    class Meta:
        model = DatasetSource
        fields = ("site_name", "site_url")

        # def __init__(self, *args, **kwargs):
        #     super(My_Form, self).__init__(*args, **kwargs)
        #     self.fields['site_name'].required = False
        #     self.fields['site_url'].required = False


class DatasetUpdateForm(BulamFormMixin, ModelForm):
    class Meta:
        model = DatasetGroup
        fields = ("name",)
        # fields = ("name", "public_level")
