# Generated by Django 4.2.5 on 2023-11-27 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0002_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='amount',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]