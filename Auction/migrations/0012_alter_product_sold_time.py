# Generated by Django 4.0.4 on 2022-06-26 21:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auction', '0011_alter_product_sold_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sold_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 26, 21, 12, 41, 345323), null=True),
        ),
    ]
