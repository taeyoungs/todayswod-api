# Generated by Django 3.1.2 on 2020-10-05 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxes', '0002_auto_20201005_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='box',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
