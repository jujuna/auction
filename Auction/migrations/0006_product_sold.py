# Generated by Django 4.0.4 on 2022-06-20 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auction', '0005_alter_bid_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold',
            field=models.IntegerField(default=False),
        ),
    ]
