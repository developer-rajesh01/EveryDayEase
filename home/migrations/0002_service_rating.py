# Generated by Django 5.1.6 on 2025-02-13 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='rating',
            field=models.FloatField(default=0.0),
        ),
    ]
