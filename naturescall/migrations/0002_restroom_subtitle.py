# Generated by Django 3.2.9 on 2021-11-07 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naturescall', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restroom',
            name='subtitle',
            field=models.CharField(default='Subtitle', max_length=255),
        ),
    ]
