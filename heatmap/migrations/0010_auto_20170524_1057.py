# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0009_auto_20170524_1045'),
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
    ]
