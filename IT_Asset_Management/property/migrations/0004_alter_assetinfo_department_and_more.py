# Generated by Django 5.1.1 on 2024-09-24 08:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_remove_assetinfo_dept_assetinfo_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetinfo',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.department', verbose_name='所属部门'),
        ),
        migrations.AlterField(
            model_name='hostmodellist',
            name='asset_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='host_models', to='property.assettypelist', verbose_name='设备类别'),
        ),
        migrations.AlterField(
            model_name='software',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='softwares', to='property.department', verbose_name='所属部门'),
        ),
    ]
