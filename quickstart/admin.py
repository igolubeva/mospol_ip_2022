from django.contrib import admin, messages
from quickstart.models import Advice
from import_export import resources, fields
from import_export.admin import ExportMixin, ExportActionMixin


class AdviceResource(resources.ModelResource):
    item_count = fields.Field(attribute='item_count', column_name='count')
    item_author = fields.Field(attribute='item_author', column_name='Автор')

    class Meta:
        model = Advice
        fields = (
            'item_author',
            'text',
            'is_published',
            'created_at',
            'is_hidden'
        )
        export_order = fields

    def dehydrate_item_count(self, advice):
        return advice.extra_count()

    def dehydrate_item_author(self, advice):
        return advice.author.username


class AdviceAdmin(ExportActionMixin, ExportMixin, admin.ModelAdmin):
    resource_class = AdviceResource


admin.site.register(Advice, AdviceAdmin)
