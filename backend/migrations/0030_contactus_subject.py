# Generated by Django 4.2.16 on 2025-01-16 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0029_alter_admission_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='subject',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
