# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-15 01:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_ID', models.CharField(max_length=500)),
                ('Name', models.CharField(max_length=500)),
                ('Service', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_ID', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('department', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('image_url', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_ID', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('image_url', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry_ID', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('image_url', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('library_ID', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('image_url', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Mall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mall_ID', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('image_url', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Museum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('museum_ID', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('image_url', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Park',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('park_ID', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('image_url', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_ID', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('image_url', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.CharField(max_length=500)),
                ('name_first', models.CharField(max_length=250)),
                ('name_last', models.CharField(max_length=250)),
                ('user_type', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Zoo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zoo_ID', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('email', models.CharField(max_length=500)),
                ('image_url', models.CharField(max_length=500)),
            ],
        ),
    ]
