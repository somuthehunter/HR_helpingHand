# Generated by Django 5.0.6 on 2025-01-18 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume_hr_side', '0006_alter_professional_resume_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professional',
            name='resume_content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
