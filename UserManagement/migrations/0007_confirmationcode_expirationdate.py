# Generated by Django 4.0.4 on 2022-06-24 11:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0006_alter_confirmationcode_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmationcode',
            name='expirationDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 24, 11, 12, 42, 883959, tzinfo=utc)),
        ),
    ]
