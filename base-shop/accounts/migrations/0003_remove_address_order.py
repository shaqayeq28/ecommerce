# Generated by Django 4.0.4 on 2022-06-01 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='order',
        ),
    ]
