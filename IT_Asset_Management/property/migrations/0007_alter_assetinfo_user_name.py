# Generated by Django 5.1.1 on 2024-09-25 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_alter_assetinfo_host_model_delete_hostmodellist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetinfo',
            name='user_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='使用用户'),
        ),
    ]
