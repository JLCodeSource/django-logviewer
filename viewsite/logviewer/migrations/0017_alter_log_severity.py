# Generated by Django 4.0 on 2022-02-03 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logviewer', '0016_alter_asset_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='severity',
            field=models.CharField(blank=True, choices=[('Critical', 'Critical'), ('Warning', 'Warning'), ('Ok', 'Ok')], max_length=8),
        ),
    ]
