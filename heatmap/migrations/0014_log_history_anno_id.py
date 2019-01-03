# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0013_sp_selected_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='log_history',
            name='anno_id',
            field=models.IntegerField(null=True),
        ),
    ]
