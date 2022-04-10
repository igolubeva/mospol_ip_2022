# Generated by Django 3.2.12 on 2022-03-28 03:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст совета')),
                ('is_published', models.BooleanField(default=False, verbose_name='Опубликован')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'совет',
                'verbose_name_plural': 'советы',
                'permissions': (('moderate_advices', 'право модерировать советы'),),
            },
        ),
    ]