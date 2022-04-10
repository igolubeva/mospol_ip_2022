from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone


class History(models.Model):
    ADD_FLAG = 'a'
    EDIT_FLAG = 'e'
    REMOVE_FLAG = 'r'
    PUBLISH_FLAG = 'p'

    ACTION_TYPE = (
        (ADD_FLAG, 'Добавление'),
        (EDIT_FLAG, 'Редактирование'),
        (REMOVE_FLAG, 'Удаление'),
        (PUBLISH_FLAG, 'Опубликовано'),
    )
    action = models.CharField(verbose_name='тип действия', max_length=1, choices=ACTION_TYPE)
    action_text = models.CharField(verbose_name='действие', max_length=50, null=True, blank=True)
    date = models.DateTimeField(verbose_name='дата', default=timezone.now, db_index=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='пользователь',
        null=True, blank=True, on_delete=models.CASCADE
    )
    fields_json = models.TextField(verbose_name='значения полей', null=True, blank=True)

    class Meta:
        verbose_name = 'Запись истории'
        verbose_name_plural = 'Записи истории'
        index_together = ('content_type', 'object_id')
        permissions = (
            ("view_history_entries", "просмотр истории"),
        )

    def __str__(self):
        return "[%s] [%s] %s.%s %s" % (
            self.date, self.get_action_display(), self.content_type, self.object_id, self.user
        )

    @staticmethod
    def get_history_link(obj):
        content_type_id = ContentType.objects.get_for_model(obj).pk
        return reverse(
            'show_object_history', kwargs={
                'content_type_id': content_type_id,
                'object_id': obj.pk
            })

