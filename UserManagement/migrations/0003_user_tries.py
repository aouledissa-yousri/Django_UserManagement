# Generated by Django 4.0.5 on 2022-06-20 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0002_user_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tries',
            field=models.IntegerField(default=3),
        ),
    ]
