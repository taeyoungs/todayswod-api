# Generated by Django 3.1.2 on 2020-10-14 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=120)),
                ('address', models.CharField(max_length=240)),
                ('certification_code', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Boxes',
            },
        ),
    ]
