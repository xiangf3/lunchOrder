# Generated by Django 3.0.7 on 2020-06-26 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_preference_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='budget',
            field=models.IntegerField(default=0),
        ),
    ]
