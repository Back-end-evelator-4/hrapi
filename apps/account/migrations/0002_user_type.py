# Generated by Django 4.2.5 on 2023-09-22 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.IntegerField(blank=True, choices=[(0, 'Hr'), (1, 'Candidate')], null=True),
        ),
    ]
