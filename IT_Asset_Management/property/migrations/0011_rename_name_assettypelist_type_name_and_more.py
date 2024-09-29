# Generated by Django 5.1.1 on 2024-09-27 03:23

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0010_alter_assetinfo_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assettypelist',
            old_name='name',
            new_name='type_name',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='name',
            new_name='dept_name',
        ),
        migrations.RenameField(
            model_name='software',
            old_name='name',
            new_name='soft_name',
        ),
        migrations.RemoveField(
            model_name='assetinfo',
            name='department',
        ),
        migrations.RemoveField(
            model_name='assetinfo',
            name='user_name',
        ),
        migrations.AddField(
            model_name='assetinfo',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.userinfo', verbose_name='使用用户'),
        ),
        migrations.AlterField(
            model_name='assetinfo',
            name='receive_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='采购日期'),
        ),
    ]
