# Generated by Django 3.1.2 on 2020-11-30 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0005_alert_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='content',
            field=models.TextField(),
        ),
    ]
