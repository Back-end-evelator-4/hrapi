# Generated by Django 4.2.5 on 2023-09-27 15:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_job_created_date_job_modified_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='company',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='job',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='responsibility',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='responsibility',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='responsibility',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='skill',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skill',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='skill',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
