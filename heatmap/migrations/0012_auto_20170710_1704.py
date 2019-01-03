# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0011_auto_20170524_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='axisOption',
        ),
        migrations.RemoveField(
            model_name='block',
            name='isSub',
        ),
        migrations.AddField(
            model_name='log_history',
            name='column',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='log_history',
            name='page',
            field=models.IntegerField(null=True),
        ),
    ]
