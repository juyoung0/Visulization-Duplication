# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0010_auto_20170524_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='axisOption',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='block',
            name='isSub',
            field=models.BooleanField(default=False),
        ),
    ]
