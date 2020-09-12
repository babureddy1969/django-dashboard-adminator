# Generated by Django 2.2.10 on 2020-09-12 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20200912_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='check',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='check_void_reason_code',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_reference',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='paid_check',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='reverse_clearing',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='run_id',
            field=models.CharField(default='', max_length=4),
        ),
    ]