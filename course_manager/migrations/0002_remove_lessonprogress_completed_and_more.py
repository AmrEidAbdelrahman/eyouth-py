# Generated by Django 5.0.2 on 2025-05-03 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonprogress',
            name='completed',
        ),
        migrations.AlterField(
            model_name='certificate',
            name='certificate_file',
            field=models.FileField(blank=True, null=True, upload_to='certificates/'),
        ),
    ]
