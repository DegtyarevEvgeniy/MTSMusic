# Generated by Django 4.0.2 on 2023-09-18 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(default='', max_length=1000)),
                ('email', models.EmailField(default='', max_length=254, unique=True)),
                ('first_name', models.CharField(default='', max_length=1000)),
                ('last_name', models.CharField(default='', max_length=1000)),
                ('phone', models.IntegerField(default='1')),
                ('city', models.CharField(default='', max_length=1000)),
                ('userImage', models.ImageField(default='https://i.ibb.co/s3QmZrw/default.png', upload_to='')),
                ('prevUserImage', models.ImageField(default='', upload_to='')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('payment_account', models.IntegerField(default=0)),
                ('checking_account', models.IntegerField(default=0)),
                ('fiz_adress', models.CharField(default='', max_length=1000)),
                ('street', models.CharField(default='', max_length=1000)),
                ('is_partner', models.BooleanField(default=False)),
                ('confirmed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
