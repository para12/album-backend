# Generated by Django 3.2.6 on 2021-08-30 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210830_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='title',
            field=models.CharField(default='', max_length=256),
        ),
    ]
