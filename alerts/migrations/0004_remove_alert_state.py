# Generated by Django 3.1.2 on 2020-10-14 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0003_auto_20201014_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alert',
            name='state',
        ),
    ]