# Generated by Django 3.2.18 on 2023-04-04 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app02', '0010_alter_customer_birthdate'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Task',
        ),
    ]