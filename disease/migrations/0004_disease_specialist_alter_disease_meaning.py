# Generated by Django 4.1.4 on 2023-12-28 20:34

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('specialist', '0004_alter_category_options'),
        ('disease', '0003_symptom_disease'),
    ]

    operations = [
        migrations.AddField(
            model_name='disease',
            name='specialist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='diseases_specialized', to='specialist.category'),
        ),
        migrations.AlterField(
            model_name='disease',
            name='meaning',
            field=tinymce.models.HTMLField(blank=True),
        ),
    ]