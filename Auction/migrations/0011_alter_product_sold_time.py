# Generated by Django 4.0.4 on 2022-06-26 21:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auction', '0010_product_sold_time_alter_bid_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sold_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 21, 9, 4, 385740)),
        ),
    ]
