# Generated by Django 4.0.4 on 2022-04-21 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_ad_slider_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'active'), ('', 'default')], max_length=25),
        ),
    ]
