# Generated by Django 5.0.6 on 2025-01-18 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_hr_side', '0005_professional_resume_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professional',
            name='resume_content',
            field=models.CharField(blank=True, default='', max_length=1000000),
        ),
    ]
