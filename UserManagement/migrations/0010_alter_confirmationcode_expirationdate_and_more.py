# Generated by Django 4.1 on 2022-08-29 00:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0009_alter_confirmationcode_expirationdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationcode',
            name='expirationDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 29, 0, 9, 26, 852389, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='passwordresetcode',
            name='expirationDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 29, 0, 9, 26, 856503, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='twofactorauthcode',
            name='expirationDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 29, 0, 9, 26, 858050, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='LocationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=255, unique=True)),
                ('expirationDate', models.DateTimeField(default=datetime.datetime(2022, 8, 29, 0, 9, 26, 859453, tzinfo=datetime.timezone.utc))),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='UserManagement.user')),
            ],
        ),
    ]
