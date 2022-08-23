# Generated by Django 4.0.4 on 2022-08-23 20:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0003_alter_confirmationcode_expirationdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationcode',
            name='expirationDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 23, 20, 40, 46, 111715, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='passwordresetcode',
            name='expirationDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 23, 20, 40, 46, 112209, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='twofactorauthcode',
            name='expirationDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 23, 20, 40, 46, 112601, tzinfo=utc)),
        ),
    ]
