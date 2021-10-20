# Generated by Django 3.2.7 on 2021-10-16 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naturescall', '0002_alter_restroom_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='restroom',
            name='Accessible',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='restroom',
            name='FamilyFriendly',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='restroom',
            name='TransactionRequired',
            field=models.BooleanField(default=True),
        ),
    ]
