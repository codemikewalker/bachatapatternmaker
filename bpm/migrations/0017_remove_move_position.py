# Generated by Django 5.1.1 on 2024-09-15 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bpm', '0016_movematrix_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='move',
            name='position',
        ),
    ]
