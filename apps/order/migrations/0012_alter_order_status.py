# Generated by Django 4.1.3 on 2022-12-04 09:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0011_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ordered', 'Ordered'), ('shipped', 'Shipped'), ('arrived', 'Arrived')],
                                   default='ordered', max_length=20),
        ),
    ]