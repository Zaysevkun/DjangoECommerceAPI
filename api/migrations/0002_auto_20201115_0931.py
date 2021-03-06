# Generated by Django 3.1.3 on 2020-11-15 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.PositiveIntegerField(default=0, max_length=10, verbose_name='Сумма заказа'),
        ),
        migrations.AddField(
            model_name='productsinorder',
            name='sum',
            field=models.PositiveIntegerField(default=0, max_length=8, verbose_name='Сумма по строке'),
        ),
    ]
