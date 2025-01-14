# Generated by Django 5.1.1 on 2024-09-26 09:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0008_alter_assetinfo_service_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100, unique=True, verbose_name='账户名')),
                ('fullname', models.CharField(blank=True, max_length=100, null=True, verbose_name='姓名')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='property.department', verbose_name='所属部门')),
            ],
            options={
                'verbose_name': '员工用户',
                'verbose_name_plural': '员工用户列表',
            },
        ),
    ]
