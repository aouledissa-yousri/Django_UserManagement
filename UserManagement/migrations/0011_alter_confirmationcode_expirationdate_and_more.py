# Generated by Django 4.1 on 2022-08-30 23:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0010_alter_confirmationcode_expirationdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationcode',
            name='expirationDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 30, 23, 5, 38, 248102)),
        ),
        migrations.AlterField(
            model_name='locationcode',
            name='expirationDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 30, 23, 5, 38, 254055, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='passwordresetcode',
            name='expirationDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 30, 23, 5, 38, 251729)),
        ),
        migrations.AlterField(
            model_name='twofactorauthcode',
            name='expirationDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 30, 23, 5, 38, 252949)),
        ),
    ]
