# Generated by Django 3.1.2 on 2020-10-16 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0002_membership_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='hold_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='state',
            field=models.CharField(choices=[('progress', 'Progress'), ('expired', 'Expired'), ('holding', 'Holding')], default='progress', max_length=80),
        ),
    ]
