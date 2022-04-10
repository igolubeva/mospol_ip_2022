from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Advice(models.Model):
    title = models.CharField(u'Заголовок', max_length=256, blank=True, null=True)
    author = models.ForeignKey(User, verbose_name=u'автор', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    text = models.TextField('Текст совета', blank=True, null=True)
    is_published = models.BooleanField('Опубликован', default=False)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    is_hidden = models.BooleanField('Скрыт', default=False)

    def __str__(self):
        if not self.text:
            return ''
        if len(self.text) < 100:
            return self.text
        return self.text[:97] + '...'

    class Meta:
        verbose_name = 'совет'
        verbose_name_plural = 'советы'
        permissions = (
            ('moderate_advices', 'право модерировать советы'),
        )

    def extra_count(self):
        return 10

