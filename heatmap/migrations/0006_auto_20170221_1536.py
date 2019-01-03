# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0005_auto_20170221_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log_history',
            name='is_save',
            field=models.BooleanField(default=False),
        ),
    ]
