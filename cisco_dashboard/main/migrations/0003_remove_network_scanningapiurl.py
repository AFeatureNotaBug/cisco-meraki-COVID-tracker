# Generated by Django 3.1.2 on 2021-01-27 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210119_2322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='network',
            name='scanningAPIURL',
        ),
    ]
