# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0002_log_history_is_used'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log_history',
            old_name='block_id',
            new_name='action_id',
        ),
    ]
