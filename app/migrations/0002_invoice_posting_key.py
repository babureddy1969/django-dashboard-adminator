# Generated by Django 2.2.10 on 2020-09-12 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='posting_key',
            field=models.CharField(default='', max_length=2),
            preserve_default=False,
        ),
    ]
