# Generated by Django 5.1.1 on 2024-09-26 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0009_userinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetinfo',
            name='user_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.userinfo', verbose_name='使用用户'),
        ),
    ]
