# Generated by Django 4.0.2 on 2022-05-25 22:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Myapp', '0003_delete_orderdetails_delete_req_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Req_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='Pending', max_length=255)),
                ('GrandTotal', models.FloatField(default='0.00', null=True)),
                ('Address', models.CharField(max_length=255, null=True)),
                ('Phone', models.CharField(max_length=15, null=True)),
                ('EntryDate', models.DateTimeField(auto_now=True)),
                ('CustomerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('RestuarantID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.restuarant')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Foodname', models.CharField(max_length=150)),
                ('FoodSize', models.CharField(max_length=100)),
                ('Foodprice', models.FloatField()),
                ('Foodquantity', models.FloatField()),
                ('EntryDate', models.DateTimeField(auto_now=True)),
                ('orderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Myapp.req_info')),
            ],
        ),
    ]
