# Generated by Django 5.1.3 on 2024-12-16 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_completed_total_activity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='certificate',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='certificate_no',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='completed_total_activity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='completed_total_mod',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='completed_total_task',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='final_marks',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_Certificate_issued',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_completed_total_tasks',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_payment_completed',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='module_marks',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='task_marks',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
