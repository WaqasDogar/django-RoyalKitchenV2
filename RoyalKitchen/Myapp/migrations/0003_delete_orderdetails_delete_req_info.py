# Generated by Django 4.0.2 on 2022-05-25 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0002_usertype'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderDetails',
        ),
        migrations.DeleteModel(
            name='Req_info',
        ),
    ]
