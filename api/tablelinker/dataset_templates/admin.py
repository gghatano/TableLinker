from django.contrib import admin

from .models import DatasetTemplate, DatasetTemplateAttr


class DatasetTemplateAttrAdmin(admin.TabularInline):
    model = DatasetTemplateAttr

    ordering = ("index",)

    list_display = (
        "name",
        "index",
    )

    fields = (
        "name",
        "index",
    )


class DatasetTemplateAdmin(admin.ModelAdmin):
    inlines = [
        DatasetTemplateAttrAdmin,
    ]

    list_display = (
        "name",
        "created_at",
        "updated_at",
    )

    fields = (
        "name",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


admin.site.register(DatasetTemplate, DatasetTemplateAdmin)
# admin.site.register(DatasetTemplateAttr, DatasetTemplateAttrAdmin)
