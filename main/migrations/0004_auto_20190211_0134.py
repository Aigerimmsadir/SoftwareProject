# Generated by Django 2.1.1 on 2019-02-10 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20181125_0021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='dish',
            name='num_of_orders',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
