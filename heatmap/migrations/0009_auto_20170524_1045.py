# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heatmap', '0008_auto_20170304_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='pcp',
            fields=[
                ('pcp_id', models.AutoField(serialize=False, primary_key=True)),
                ('column_order', models.CharField(max_length=255, null=True)),
                ('selected_index', models.TextField(null=True)),
                ('brushed_axis', models.CharField(max_length=255, null=True)),
                ('brushed_range', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='scm',
            fields=[
                ('scm_id', models.AutoField(serialize=False, primary_key=True)),
                ('selected_index', models.TextField(null=True)),
                ('brushed_axis', models.CharField(max_length=255, null=True)),
                ('brushed_range', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='sp',
            fields=[
                ('sp_id', models.AutoField(serialize=False, primary_key=True)),
                ('x_axis', models.CharField(max_length=30, null=True)),
                ('y_axis', models.CharField(max_length=30, null=True)),
                ('brushed_range', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='goa_human',
            old_name='gene_ontology_pathway',
            new_name='pathway',
        ),
        migrations.RenameField(
            model_name='goa_human',
            old_name='synonym_genes',
            new_name='synonym',
        ),
        migrations.RenameField(
            model_name='log_history',
            old_name='is_action',
            new_name='is_event',
        ),
        migrations.RemoveField(
            model_name='goa_human',
            name='species',
        ),
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
        migrations.AddField(
            model_name='block',
            name='is_broken',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='block',
            name='is_first',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='block',
            name='is_graph',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='block',
            name='ori_p_block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='block',
            name='ori_p_block_ver',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='block',
            name='pcp_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='block',
            name='scm_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='block',
            name='sp_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='block',
            name='vis_types',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='block_annotation_history',
            name='experiment_type',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='block_annotation_history',
            name='organism',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='block_annotation_history',
            name='platform_name',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='closed_block',
            name='is_first',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='closed_block',
            name='ori_p_block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='closed_block',
            name='ori_p_block_ver',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='log_history',
            name='copy_block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='log_history',
            name='copy_block_ver',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='log_history',
            name='is_first',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='log_history',
            name='is_graph',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='log_history',
            name='pcp_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='log_history',
            name='scm_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='log_history',
            name='selected_index',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='log_history',
            name='sp_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='log_history',
            name='vis_types',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='is_first',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='session_history',
            name='is_bookmarked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='session_history',
            name='is_first',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='session_history',
            name='ori_p_block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='session_history',
            name='ori_p_block_ver',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='session_history',
            name='prev_block_list',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='undo_block',
            name='is_first',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='undo_block',
            name='is_graph',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='undo_block',
            name='ori_p_block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='undo_block',
            name='ori_p_block_ver',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='undo_block',
            name='pcp_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='undo_block',
            name='scm_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='undo_block',
            name='sp_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='undo_block',
            name='vis_types',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='block_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='data_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='parent_block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='project_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='session_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='block_annotation_history',
            name='block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='block_annotation_history',
            name='project_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='block_annotation_history',
            name='session_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='closed_block',
            name='block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='closed_block',
            name='project_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='closed_block',
            name='session_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='log_history',
            name='block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='log_history',
            name='data_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='log_history',
            name='parent_block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='log_history',
            name='project_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='log_history',
            name='session_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='parent_session_name',
            field=models.CharField(max_length=255, default=''),
        ),
        migrations.AlterField(
            model_name='session',
            name='project_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_name',
            field=models.CharField(max_length=255, default=''),
        ),
        migrations.AlterField(
            model_name='session_history',
            name='project_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='session_history',
            name='session_name',
            field=models.CharField(max_length=255, default=''),
        ),
        migrations.AlterField(
            model_name='undo_block',
            name='block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='undo_block',
            name='data_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='undo_block',
            name='parent_block_iden',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='undo_block',
            name='project_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='undo_block',
            name='session_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
