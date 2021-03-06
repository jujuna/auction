# Generated by Django 4.0.4 on 2022-06-10 13:15

import User.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_alter_user_passport_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'ეს მაილი უკვე გამოყენებულია'}, max_length=254, unique=True, verbose_name='მეილი'),
        ),
        migrations.AlterField(
            model_name='user',
            name='passport_id',
            field=models.BigIntegerField(validators=[User.models.validate_length], verbose_name='პირადი ნომერი'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='უნდა იწყებოდეს 5-ზე და იყოს 9 ციფრიანი', regex='^[5]\\d{8}')], verbose_name='ტელეფონის ნომერი'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'ასეთი მეტსახელი არსებობს'}, max_length=30, unique=True, verbose_name='მეტსახელი'),
        ),
    ]
