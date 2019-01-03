# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0003_auto_20170220_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log_history',
            name='is_undo',
            field=models.IntegerField(default=False),
        ),
    ]
