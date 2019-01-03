from django.contrib import admin
from heatmap.models import *
from import_export.admin import ImportExportModelAdmin, ImportMixin
from import_export import resources, fields

# Register your models here.

class GeromicsResource (resources.ModelResource):
	class Meta:
		model = geromicsData
		import_id_fields = ('GeneSymbol',)

class GeromicsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = GeromicsResource

class memberResource (resources.ModelResource):
	class Meta:
		model = member
		import_id_fields = ('user_id', )

class memberAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = memberResource
	list_display = ('user_id', 'email')

class sessionResource (resources.ModelResource):
	class Meta:
		model = session
		import_id_fields = ('session_id', )
		def __str__(self):
			return "Session: " + self.name

class sessionAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = sessionResource
	list_display = ('user_id', 'project_name', 'session_name', 'session_ver', 'last_date', 'parent_session_name', 'parent_session_ver', 'branched_date')
	search_fields = ('user_id', 'project_name', 'session_name', 'session_ver', 'last_date',)

class blockResource (resources.ModelResource):
	class Meta:
		model = block
		import_id_fields = ('block_id', )

class blockAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = blockResource
	list_display = ('user_id', 'project_name', 'session_name', 'session_ver', 'last_date', 'block_iden', 'block_name', 'block_ver', 'parent_block_iden', 'parent_block_ver', 'clusterType', 'clusterParam')
	search_fields = ('user_id', 'project_name', 'session_name', 'session_ver', 'last_date',)

class session_historyResource (resources.ModelResource):
	class Meta:
		model = session_history
		import_id_fields = ('session_id', )

class session_historyAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = session_historyResource
	list_display = list_display = ('user_id', 'project_name', 'session_name', 'session_ver', 'last_date', 'block_list')
	search_fields = ('user_id', 'project_name', 'session_name', 'session_ver', 'last_date',)

class closed_blockResource (resources.ModelResource):
	class Meta:
		model = closed_block
		import_id_fields = ('block_id', )

class closed_blockAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = closed_blockResource

class log_historyResource (resources.ModelResource):
	class Meta:
		model = log_history
		import_id_fields = ('block_id', )

class log_historyAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = log_historyResource
	list_display = ('action_id', 'action', 'scope', 'user_id', 'project_name', 'session_name', 'session_ver', 'creatation_date', 'block_iden', 'block_name', 'block_ver', 'parent_block_iden', 'parent_block_ver', 'copy_block_iden', 'copy_block_ver')
	search_fields = ('user_id', 'project_name', 'session_name', 'session_ver', 'creatation_date',)

class block_annotation_historyResource (resources.ModelResource):
	class Meta:
		model = block_annotation_history
		import_id_fields = ('annotation_id', )

class block_annotation_historyAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = block_annotation_historyResource
	list_display = ('user_id', 'project_name', 'session_name', 'session_ver', 'block_iden', 'block_ver', 'author', 'data_annotation', 'research_annotation', 'last_date', 'annotation_num', 'is_removed')
	search_fields = ('user_id', 'project_name', 'session_name', 'session_ver', 'last_date',)

class projectResource (resources.ModelResource):
        class Meta:
                model = project
                import_id_fields = ('project_id', )

class projectAdmin (ImportExportModelAdmin, admin.ModelAdmin):
        resource_class = projectResource
        list_display = ('user_id', 'project_name')

class goa_humanResource (resources.ModelResource):
	class Meta:
		model = goa_human
		import_id_fields = ('gene', )

class goa_humanAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = goa_humanResource
	list_display = ('gene', 'pathway')#'gene_ontology_pathway', 'synonym_genes', 'species')

class go_oboResource (resources.ModelResource):
	class Meta:
		model = go_obo
		import_id_fields = ('pathway_id', )

class go_oboAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = go_oboResource
	list_display = ('pathway_id', 'pathway_name', 'pathway_namespace', 'pathway_def', 'pathway_synonym', 'pathway_is_a', 'pathway_alt_id', 'pathway_subset', 'pathway_xref', 'pathway_comment')


class undo_blockResource (resources.ModelResource):
	class Meta:
		model = undo_block
		import_id_fields = ('block_id', )

class undo_blockAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = undo_blockResource
	list_display = ('action', 'user_id', 'session_name', 'session_ver', 'last_date', 'block_iden', 'block_name', 'block_ver', 'parent_block_iden', 'parent_block_ver', 'clusterType', 'clusterParam')

class pcpResource (resources.ModelResource):
	class Meta:
		model = pcp
		import_id_fields = ('pcp_id',)

class pcpAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = pcpResource
	list_display = ('pcp_id', 'column_order', 'selected_index', 'brushed_axis', 'brushed_range')

class scmResource (resources.ModelResource):
	class Meta:
		model = scm
		import_id_fields = ('scm_id',)

class scmAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = pcpResource
	list_display = ('scm_id', 'selected_index', 'brushed_axis', 'brushed_range')

class spResource (resources.ModelResource):
	class Meta:
		model = sp
		import_id_fields = ('sp_id',)

class spAdmin (ImportExportModelAdmin, admin.ModelAdmin):
	resource_class = spResource
	list_display = ('sp_id', 'x_axis', 'y_axis', 'brushed_range')

admin.site.register(geromicsData, GeromicsAdmin)
admin.site.register(member, memberAdmin)
admin.site.register(session, sessionAdmin)
admin.site.register(block, blockAdmin)
admin.site.register(session_history, session_historyAdmin)
admin.site.register(closed_block, closed_blockAdmin)
admin.site.register(log_history, log_historyAdmin)
admin.site.register(block_annotation_history, block_annotation_historyAdmin)
admin.site.register(project, projectAdmin)
admin.site.register(goa_human, goa_humanAdmin)
admin.site.register(go_obo, go_oboAdmin)
admin.site.register(undo_block, undo_blockAdmin)
admin.site.register(pcp, pcpAdmin)
admin.site.register(scm, scmAdmin)
admin.site.register(sp, spAdmin)
