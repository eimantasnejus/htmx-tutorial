# Generated by Django 5.0.3 on 2024-03-09 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gdp',
            name='gdp',
            field=models.FloatField(),
        ),
    ]