# Generated by Django 4.1.4 on 2023-02-06 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_productimage_is_resized'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='is_resized',
        ),
    ]