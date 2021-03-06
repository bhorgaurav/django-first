# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 05:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_remove_studentrecord_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentClasses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='studentrecord',
            name='class_name',
        ),
        migrations.AddField(
            model_name='studentclasses',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.StudentRecord'),
        ),
    ]
