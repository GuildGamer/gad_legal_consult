# Generated by Django 3.2.5 on 2021-10-16 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_rename_title_apost_heading'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apost',
            name='heading',
            field=models.TextField(default='New Blog Post'),
        ),
    ]