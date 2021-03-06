# Generated by Django 4.0.2 on 2022-05-26 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0006_restuarant_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webresources',
            name='ClosingTime',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='webresources',
            name='Day',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='webresources',
            name='FbLink',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='webresources',
            name='GitLink',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='webresources',
            name='LinkedInLink',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='webresources',
            name='OpeningTime',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='webresources',
            name='TwitterLink',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
