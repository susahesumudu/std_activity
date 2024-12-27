# Generated by Django 5.1.3 on 2024-12-27 13:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_mainactivity_commonefficacyquestion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='activity_code',
            field=models.CharField(default=1, max_length=10, unique=True, verbose_name='Activity Code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(choices=[('Technical Knowledge', 'Technical Knowledge'), ('Skill Development', 'Skill Development'), ('Workplace Readiness', 'Workplace Readiness'), ('Assessment', 'Assessment'), ('Problem-Solving', 'Problem-Solving'), ('Industry-Specific', 'Industry-Specific'), ('Creative and Design', 'Creative and Design'), ('Self-Learning', 'Self-Learning'), ('Collaborative', 'Collaborative'), ('Reflective and Feedback', 'Reflective and Feedback')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='no_of_sessions',
            field=models.PositiveIntegerField(default=1, verbose_name='Number of Sessions'),
        ),
        migrations.AddField(
            model_name='activity',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
