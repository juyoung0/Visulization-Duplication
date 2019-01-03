# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0006_auto_20170221_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='undo_block',
            name='block_list',
            field=models.TextField(null=True),
        ),
    ]
