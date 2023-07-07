from django.contrib import admin

from dataset_templates.models import DatasetTemplate

from .models import Dataset


class DatasetAdmin(admin.ModelAdmin):
    list_display = (
        "encoding",
        "num_records",
        "num_columns",
        "created_by",
        "created_at",
        "updated_at",
    )

    fields = (
        "encoding",
        "num_records",
        "num_columns",
        "created_by",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "encoding",
        "num_records",
        "num_columns",
        "created_at",
        "updated_at",
    )

    actions = ["make_template"]

    def make_template(self, request, queryset):
        for dataset in queryset.all():
            DatasetTemplate.create_by_dataset(dataset)
        self.message_user(request, "テンプレートを生成しました。.")

    make_template.short_description = "テンプレート生成"


admin.site.site_title = "TableLinker管理画面"
admin.site.site_header = "TableLinker管理画面"
admin.site.index_title = "メニュー"

admin.site.register(Dataset, DatasetAdmin)
