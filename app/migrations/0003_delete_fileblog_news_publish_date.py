# Generated by Django 5.1.1 on 2024-09-26 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_is_timer_news_is_timer_enabled_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FileBlog',
        ),
        migrations.AddField(
            model_name='news',
            name='publish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
