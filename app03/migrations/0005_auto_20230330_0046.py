# Generated by Django 3.2.18 on 2023-03-30 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app03', '0004_admin_alter_account_level_alter_account_mobile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(max_length=32, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='admin',
            name='username',
            field=models.CharField(max_length=32, verbose_name='username'),
        ),
    ]
