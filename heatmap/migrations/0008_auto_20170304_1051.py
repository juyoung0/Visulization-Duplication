# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0007_undo_block_block_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log_history',
            name='block_ver',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='log_history',
            name='session_ver',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
