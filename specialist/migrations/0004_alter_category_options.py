# Generated by Django 4.1.4 on 2023-12-27 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('specialist', '0003_workhours_appointment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
    ]
