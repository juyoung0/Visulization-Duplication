from django.db import models
from django.utils import timezone

# Create your models here.
class geromicsData(models.Model):
	GeneSymbol = models.CharField(max_length=100, null=True)
	GSM1076965 = models.CharField(max_length=100, null=True)
	GSM1076966 = models.CharField(max_length=100, null=True)
	GSM1076967 = models.CharField(max_length=100, null=True)
	GSM1076968 = models.CharField(max_length=100, null=True)
	
	def __str__(self):
        	return self.GeneSymbol

	class Meta:
		app_label = 'heatmap'

class member(models.Model):
	user_id = models.CharField(max_length=30, primary_key=True)
	user_pw = models.CharField(max_length=30, null=True)
	email = models.CharField(max_length=30, null=True)

	class Meta:
		app_label = 'heatmap'

class project(models.Model):
	project_id = models.AutoField(primary_key=True)
	project_name = models.CharField(max_length=255, null=True)
	user_id = models.CharField(max_length=30)
	last_date = models.DateTimeField(default=timezone.now)
	project_annotation = models.TextField(null=True)

	class Meta:
		app_label = 'heatmap'

class session(models.Model):
	session_id = models.AutoField(primary_key=True)
	session_name = models.CharField(max_length=255, default="")
	session_ver = models.IntegerField(default=0)
	user_id = models.CharField(max_length=30, null=True)
	project_name = models.CharField(max_length=255, null=True)
	last_date = models.DateTimeField(default=timezone.now)
	creatation_date = models.DateTimeField(default=timezone.now)
	parent_session_name = models.CharField(max_length=255, default="")
	parent_session_ver = models.IntegerField(default=0)
	branched_date = models.DateTimeField(default=timezone.now)
	session_annotation = models.TextField(null=True)
	is_first = models.BooleanField(default=False)

	class Meta:
		app_label = 'heatmap'

class block(models.Model):
	block_id = models.AutoField(primary_key=True)
	user_id = models.CharField(max_length=30, null=True)
	project_name = models.CharField(max_length=255, null=True)
	session_name = models.CharField(max_length=255, null=True)
	session_ver = models.IntegerField(default=0)
	block_iden = models.CharField(max_length=30, null=True)
	block_name = models.CharField(max_length=30, null=True)
	block_ver = models.IntegerField(default=0)
	parent_block_iden = models.CharField(max_length=30, null=True)
	parent_block_ver = models.IntegerField(default=0)
	clusterType = models.CharField(max_length=20, null=True)
	clusterParam = models.CharField(max_length=20, null=True)
	colors = models.CharField(max_length=50, null=True)
	data = models.TextField()
	last_date = models.DateTimeField(default=timezone.now)
	creatation_date = models.DateTimeField(default=timezone.now)
	position_top = models.IntegerField(default=0)
	position_left = models.IntegerField(default=0)
	position_width = models.IntegerField(default=0)
	position_height = models.IntegerField(default=0)
	is_closed = models.BooleanField(default=False)
	data_annotation = models.TextField(null=True)
	data_name = models.CharField(max_length=100, null=True)
	is_save = models.BooleanField(default=False)
	save_ver = models.IntegerField(blank=True, null=True)
	is_undo = models.BooleanField(default=False)
	is_broken = models.BooleanField(default=False)
	vis_types = models.CharField(max_length=100, null=True)
	pcp_id = models.IntegerField(null=True)
	scm_id = models.IntegerField(null=True)
	sp_id = models.IntegerField(null=True)
	is_graph = models.BooleanField(default=False)
	is_first = models.BooleanField(default=False)
	ori_p_block_iden = models.CharField(max_length=30, null=True)
	ori_p_block_ver = models.IntegerField(default=0)

	class Meta:
		app_label = 'heatmap'

class undo_block(models.Model):
	block_id = models.AutoField(primary_key=True)
	user_id = models.CharField(max_length=30, null=True)
	project_name = models.CharField(max_length=255, null=True)
	session_name = models.CharField(max_length=255, null=True)
	session_ver = models.IntegerField(default=0)
	block_iden = models.CharField(max_length=30, null=True)
	block_name = models.CharField(max_length=20, null=True)
	block_ver = models.IntegerField(default=0)
	parent_block_iden = models.CharField(max_length=30, null=True)
	parent_block_ver = models.IntegerField(default=0)
	clusterType = models.CharField(max_length=20, null=True)
	clusterParam = models.CharField(max_length=20, null=True)
	colors = models.CharField(max_length=50, null=True)
	data = models.TextField()
	last_date = models.DateTimeField(default=timezone.now)
	position_top = models.IntegerField(null=True)
	position_left = models.IntegerField(null=True)
	position_width = models.IntegerField(null=True)
	position_height = models.IntegerField(null=True)
	is_closed = models.BooleanField(default=False)
	data_annotation = models.TextField(null=True)
	data_name = models.CharField(max_length=100, null=True)
	is_save = models.BooleanField(default=False)
	save_ver = models.IntegerField(blank=True, null=True)
	action = models.CharField(max_length=30, null=True)
	block_list = models.TextField(null=True)
	vis_types = models.CharField(max_length=100, null=True)
	pcp_id = models.IntegerField(null=True)
	scm_id = models.IntegerField(null=True)
	sp_id = models.IntegerField(null=True)
	is_graph = models.BooleanField(default=False)
	is_first = models.BooleanField(default=False)
	ori_p_block_iden = models.CharField(max_length=30, null=True)
	ori_p_block_ver = models.IntegerField(default=0)

	class Meta:
		app_label = 'heatmap'
	
class session_history(models.Model):
	session_id = models.AutoField(primary_key=True)
	session_name = models.CharField(max_length=255, default="")
	session_ver = models.IntegerField(default=0)
	user_id = models.CharField(max_length=30, null=True)
	project_name = models.CharField(max_length=255, null=True)
	last_date = models.DateTimeField(default=timezone.now)
	block_list = models.CharField(max_length=255, null=True)
	session_annotation = models.TextField(null=True)
	is_bookmarked = models.BooleanField(default=False)
	prev_block_list = models.TextField(null=True)
	is_first = models.BooleanField(default=False)
	ori_p_block_iden = models.CharField(max_length=30, null=True)
	ori_p_block_ver = models.IntegerField(default=0)

	class Meta:
		app_label = 'heatmap'

class closed_block(models.Model):
	block_id = models.AutoField(primary_key=True)
	user_id = models.CharField(max_length=30, null=True)
	project_name = models.CharField(max_length=255, null=True)
	session_name = models.CharField(max_length=255, null=True)
	session_ver = models.IntegerField(default=0)
	block_iden = models.CharField(max_length=30, null=True)
	last_date = models.DateTimeField(default=timezone.now)
	is_first = models.BooleanField(default=False)
	ori_p_block_iden = models.CharField(max_length=30, null=True)
	ori_p_block_ver = models.IntegerField(default=0)

	class Meta:
		app_label = 'heatmap'

class log_history(models.Model):
	action_id = models.AutoField(primary_key=True)
	scope = models.CharField(max_length=10, null=True)
	action = models.CharField(max_length=30, null=True)
	intent = models.CharField(max_length=30, null=True)
	user_id = models.CharField(max_length=30, null=True)  
	project_name = models.CharField(max_length=255, null=True)
	session_name = models.CharField(max_length=255, null=True)
	session_ver = models.IntegerField(blank=True, null=True)
	block_iden = models.CharField(max_length=30, null=True)
	block_name = models.CharField(max_length=20, null=True)
	block_ver = models.IntegerField(blank=True, null=True)
	parent_block_iden = models.CharField(max_length=30, null=True)
	parent_block_ver = models.IntegerField(default=0)
	copy_block_iden = models.CharField(max_length=30, null=True)
	copy_block_ver = models.IntegerField(default=0)
	clusterType = models.CharField(max_length=20, null=True)
	clusterParam = models.CharField(max_length=20, null=True)
	colors = models.CharField(max_length=50, null=True)
	data = models.TextField(null=True)
	creatation_date = models.DateTimeField(default=timezone.now)
	position_top = models.IntegerField(null=True)
	position_left = models.IntegerField(null=True)
	position_width = models.IntegerField(null=True)
	position_height = models.IntegerField(null=True)
	is_event = models.BooleanField(default=False)
	is_closed = models.BooleanField(default=False)
	data_annotation = models.TextField(null=True)
	data_name = models.CharField(max_length=100, null=True)
	is_save = models.BooleanField(default=False) 
	save_ver = models.IntegerField(blank=True, null=True)
	is_new = models.BooleanField(default=False)
	is_undo = models.BooleanField(default=False) 
	is_used = models.BooleanField(default=False)
	vis_types = models.CharField(max_length=100, null=True)
	pcp_id = models.IntegerField(null=True)
	scm_id = models.IntegerField(null=True)
	sp_id = models.IntegerField(null=True)
	is_graph = models.BooleanField(default=False)
	is_first = models.BooleanField(default=False)
	selected_index = models.TextField(null=True)
	column = models.IntegerField(null=True)
	page = models.IntegerField(null=True)
	anno_id = models.IntegerField(null=True)

	class Meta:
		app_label = 'heatmap'

class block_annotation_history(models.Model):
	annotation_id = models.AutoField(primary_key=True)
	user_id = models.CharField(max_length=30, null=True)
	project_name = models.CharField(max_length=255, null=True)
	session_name = models.CharField(max_length=255, null=True)
	session_ver = models.IntegerField(default=0)
	block_iden = models.CharField(max_length=30, null=True)
	block_ver = models.IntegerField(default=0)
	research_annotation = models.TextField(null=True)
	data_annotation = models.TextField(null=True)
	author = models.CharField(max_length=30, null=True)
	annotation_num = models.IntegerField(default=0)
	experiment_type = models.TextField(null=True)
	platform_name = models.TextField(null=True)
	organism = models.TextField(null=True)
	is_removed = models.BooleanField(default=False)
	last_date = models.DateTimeField(default=timezone.now)

	class Meta:
		app_label = 'heatmap'

class goa_human(models.Model):
	"""
	gene = models.CharField(max_length=30, null=True)
	gene_ontology_pathway = models.CharField(max_length=100, null=True)
	synonym_genes = models.CharField(max_length=100, null=True)
	species = models.CharField(max_length=30, null=True)
	"""
	gene = models.CharField(max_length=30, null=True)
	pathway = models.CharField(max_length=100, null=True)
	synonym = models.CharField(max_length=100, null=True)
	class Meta:
		app_label = 'heatmap'
        
class go_obo(models.Model):
	pathway_id = models.CharField(max_length=30, null=True)
	pathway_name = models.CharField(max_length=100, null=True)
	pathway_namespace = models.CharField(max_length=100, null=True)
	pathway_def = models.CharField(max_length=100, null=True)
	pathway_synonym = models.CharField(max_length=100, null=True)
	pathway_is_a = models.CharField(max_length=255, null=True)
	pathway_alt_id = models.CharField(max_length=100, null=True)
	pathway_subset = models.CharField(max_length=255, null=True)
	pathway_xref = models.TextField(null=True)
	pathway_comment = models.TextField(null=True)

	class Meta:
		app_label = 'heatmap'

class pcp(models.Model):
	pcp_id = models.AutoField(primary_key=True)
	column_order = models.CharField(max_length=255, null=True)
	selected_index = models.TextField(null=True)
	brushed_axis = models.CharField(max_length=255, null=True)
	brushed_range = models.CharField(max_length=255, null=True)


	class Meta:
		app_label = 'heatmap'


class scm(models.Model):
	scm_id = models.AutoField(primary_key=True)
	selected_index = models.TextField(null=True)
	brushed_axis = models.CharField(max_length=255, null=True)
	brushed_range = models.CharField(max_length=255, null=True)

	class Meta:
		app_label = 'heatmap'

class sp(models.Model):
	sp_id = models.AutoField(primary_key=True)
	x_axis = models.CharField(max_length=30, null=True)
	y_axis = models.CharField(max_length=30, null=True)
	brushed_range = models.CharField(max_length=255, null=True)
	selected_index = models.TextField(null=True)

	class Meta:
		app_label = 'heatmap'
