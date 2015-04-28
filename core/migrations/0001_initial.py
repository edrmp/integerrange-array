# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import django.contrib.postgres.fields.ranges


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IntegerRangeArrayModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('field', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ranges.IntegerRangeField(), size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
