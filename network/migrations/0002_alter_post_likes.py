# Generated by Django 4.0.4 on 2022-07-17 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='network.like'),
        ),
    ]
