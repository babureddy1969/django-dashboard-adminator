# Generated by Django 2.2.10 on 2020-09-12 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200912_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='trade_code',
            field=models.CharField(default='', max_length=1),
        ),
    ]
