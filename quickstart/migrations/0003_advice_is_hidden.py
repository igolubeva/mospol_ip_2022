# Generated by Django 3.2.12 on 2022-04-09 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0002_advice_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='advice',
            name='is_hidden',
            field=models.BooleanField(default=False, verbose_name='Скрыт'),
        ),
    ]
