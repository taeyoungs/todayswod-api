# Generated by Django 3.1.2 on 2020-10-14 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(choices=[('term', 'Term'), ('count', 'Count')], max_length=80)),
                ('state', models.CharField(choices=[('progress', 'Progress'), ('expired', 'Expired')], default='progress', max_length=80)),
                ('cnt', models.IntegerField(blank=True, null=True)),
                ('start_term', models.DateField(blank=True, null=True)),
                ('end_term', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
