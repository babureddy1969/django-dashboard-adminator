# Generated by Django 2.2.10 on 2020-09-13 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20200913_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='baseline_payment_dte',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='check_encashment_date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='document_date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='entry_date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='posting_date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='run_date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='value_date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='voided_check_date',
            field=models.CharField(max_length=10),
        ),
    ]