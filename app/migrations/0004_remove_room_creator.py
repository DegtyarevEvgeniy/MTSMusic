# Generated by Django 4.0.2 on 2023-11-24 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_room_delete_homework_delete_homework_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='creator',
        ),
    ]