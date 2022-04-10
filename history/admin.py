import json

from django.contrib import admin
from django.utils.html import format_html

from history.models import History


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'content_type', 'object_id')
    list_filter = ('action',)
    raw_id_fields = ('user', 'content_type')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'id', 'object_id')
    list_select_related = ('user', 'content_type')
    exclude = ['fields_json']
    readonly_fields = ('fields_json_formatted',)

    def fields_json_formatted(self, obj):
        return format_html(
            '<pre style="margin: 4px 0;word-break: break-word;padding: 0;white-space: pre-wrap;">{}</pre>',
            json.dumps(json.loads(obj.fields_json), indent=2, ensure_ascii=False)
        )

    fields_json_formatted.short_description = 'Значения полей'


admin.site.register(History, HistoryAdmin)

