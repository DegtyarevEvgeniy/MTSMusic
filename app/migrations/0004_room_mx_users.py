# Generated by Django 4.0.4 on 2023-11-26 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_songn_song'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='mx_users',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]