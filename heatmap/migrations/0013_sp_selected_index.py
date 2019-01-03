# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0012_auto_20170710_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='sp',
            name='selected_index',
            field=models.TextField(null=True),
        ),
    ]
