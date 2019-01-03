from django.views.decorators.gzip import gzip_page

# list of action in order to check action from client
action_check_list = ['Create-Unit', 'Delete-Unit', 'Save-Unit',
                     'Select-Unit', 'Change-Data', 'Change-Cluster-Type',
                     'Change-Cluster-Parameter', 'Locate-Unit', 'Show-Session',
                     'Create-Session', 'Branch-Session', 'Delete-Session',
                     'Create-Project', 'Delete-Project', 'Change-Data-Annotation',
                     'Change-Unit-Annotation' ,'Change-Session-Annotation', 'Change-Unit-Name',
                     'Save-Session', 'Branch-Unit', 'Apply-Unit',
                     'Change-Color', 'Create-Unit-Annotation', 'Delete-Unit-Annotation',
                     'Update-Unit-Annotation', 'Copy-Unit', 'Move-Unit',
                     'Change-PCP-Column', 'Brush-PCP-Axis', 'Brush-SCM-Axis',
                     'Brush-SP-Axis', 'Search-Table', 'Search-Table-Row',
                     'Restore-Unit', 'Unit-Workflow', 'Session-Workflow',
                     'Create-Unit-Graph', 'Click-Sankey-Tab', 'Click-Table-Tab',
                     'Click-Menu-Tab', 'Pin-Unit', 'Unpin-Unit',
                     'Change_Table_Order', 'Change_Table_Page']