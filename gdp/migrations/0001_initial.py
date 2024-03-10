# Generated by Django 5.0.3 on 2024-03-09 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GDP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('country_code', models.CharField(max_length=4)),
                ('year', models.IntegerField()),
                ('gdp', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
    ]
