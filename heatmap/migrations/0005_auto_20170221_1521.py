# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0004_auto_20170221_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log_history',
            name='is_undo',
            field=models.BooleanField(default=False),
        ),
    ]
