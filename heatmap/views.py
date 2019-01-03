from heatmap import *

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.

from django.middleware.gzip import GZipMiddleware

gzip_middleware = GZipMiddleware()

def gzip_compress(func):
    """
    Gzip compress an individual view rather than requiring the whole site to
    use the Gzip middleware.
    """
    @wraps(func)
    def dec(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        return gzip_middleware.process_response(request, response)
    return dec

def weka(request):
    """
    test for weka
    """
    return render(request, 'weka.html', {})

def cluster_list(request):
    """
    send cluster list json format
    """
    cluster_list = [{"ClusterType":"Hierarchy",
			"Parameter":["single", "complete", "average",
				"weighted", "centroid", "median", "ward"]},
		{"ClusterType":"KMeans", "Parameter":0},
		{"ClusterType":"Self Organizing Map", "Parameter":None},
		{"ClusterType":"Expectation Maximization", "Parameter":None},
		{"ClusterType":"Affinity Propagation", "Parameter":None},
		{"ClusterType":"Spectral", "Parameter":0},
		{"ClusterType":"Agglomerative Propagation", "Parameter":None},
		{"ClusterType":"DBSCAN", "Parameter":None}]
    return HttpResponse(json.dumps({'cluster_list' : cluster_list}), content_type="application/json")

def vis_types(request):
    """
    send cluster list json format
    """
    vis_types = [
		{ "visTypes" : "Parallel Coordinate Plot"},
        { "visTypes" : "Scatterplot Matrix"},
        { "visTypes": "Scatter Plot"}]

    return HttpResponse(json.dumps({'vis_types' : vis_types}), content_type="application/json")

def unav_undo(request):
    """
    unavailable undo list json format
    """
    unavailable_undo_list = [
		{ "action" : "Create-Unit"},
        { "action" : "Save-Unit"},
        {"action": "Select-Unit"},
        {"action": "Locate-Unit"},
        {"action": "Apply-Unit"},
        {"action": "Create-Unit-Annotation"},
        {"action": "Delete-Unit-Annotation"},
        {"action": "Update-Unit-Annotation"}]

    return HttpResponse(json.dumps({'unav_undo_list' : unavailable_undo_list}), content_type="application/json")

def species(request):
    """
    send species list json format
    """
    species_list = [
		{ "species" : "human"},
        { "species" : "rat"},
        { "species" : "mouse"}]

    return HttpResponse(json.dumps({'species_list' : species_list}), content_type="application/json")

def info1(request, start):
    """
    test for django
    """
    start = get_object_or_404(ContentType, pk=start)
    return render(request, 'info/info.html', {'start': start})

def hello(request):
    """
    test for django
    """
    return HttpResponse("Welcome to the page at %s" % request.path)

@gzip_compress
@ensure_csrf_cookie
def index(request):
    """
    index_value html
    """
    return render(request, 'index.html')

@gzip_compress
def user_study(request):
    """
    user_study html
    """
    return render(request, 'userStudy.html')

def seminar(request):
    return render(request, 'seminar.html')

def sankey_list(request):
    return render(request, 'sankeyList.html')

def final(request):
    """
    final html
    """
    return render(request, 'final.html')

@gzip_page
def file_name_download(request, filename):
    """
    download file (all path)
    """
    parse = filename.split("/")
    filepath = settings.STATIC_ROOT

    for i in parse:
        filepath = os.path.join(filepath, i)
    return_value = sendfile(request, filepath)
    if filepath[-4:] == "json":
        return_value['Content-Type'] = 'application/json'
    return return_value

def tool(request):
    """
    test for django
    """
    return render(request, 'tool.html', {})

def goobo(request):
    """
    test for goobo
    """
    html = urlopen('http://geneontology.org/ontology/go.obo')
    soup = BeautifulSoup(html, "html5lib")
#    soup = soup.split(' ')    
    return HttpResponse(soup)

def kegg(request):
    """
    test for kegg
    """
    return render(request, 'kegg.html', {})

def david(request):
    """
    test for david
    """
    return render(request, 'david.html', {})

def betarelease(request):
    """
    betarelease fucntion
    """
    return render(request, 'betarelease.html', {})


@ensure_csrf_cookie
def insert_log(request):
    errors = []
    username = ""
    session_name = ""
    session_ver = 0
    if request.method == 'POST':
        param_list = ['scope', 'action', 'username', 'project_name']
        errors = param_checker(request, errors, param_list)
        if not errors:
            scope = '%r' % request.POST['scope']
            scope = scope.replace('\'', '')
            action = '%r' % request.POST['action']
            action = action.replace('\'', '')
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            if request.POST.get('session_name', ''):
                session_name = '%r' % request.POST['session_name']
                session_name = session_name.replace('\'', '')
            else:
                session_name = None
            if request.POST.get('session_ver', ''):
                if action == "Create_Session":
                    session_ver = 0
                else:
                    session_ver = '%r' % request.POST['session_ver']
                    session_ver = session_ver.replace('\'', '')
            else:
                session_ver = None
            if request.POST.get('block_iden', ''):
                block_iden = '%r' % request.POST['block_iden']
                block_iden = block_iden.replace('\'', '')
            else:
                block_iden = None
            if request.POST.get('block_ver', ''):
                if action == "Create-Unit":
                    block_ver = 0
                else:
                    block_ver = '%r' % request.POST['block_ver']
                    block_ver = block_ver.replace('\'', '')
                """
                bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, block_iden = block_iden, block_ver = 0, is_save = True)
                if len(bl) == 0:
                    block_ver = -1
                """
            else:
                block_ver = None
            if request.POST.get('vis_types', ''):
                vis_types = '%r' % request.POST['vis_types']
                vis_types = vis_types.replace('\'', '')
            else:
                vis_types = None

            # define intent for acitons
            intent_list = ["Session change", "Display change", "Unit change",
                           "Project change", "Tab Change", "Table Change"]
            action_list = {}
            action_list['Create-Unit'] = [0, 1]
            action_list['Delete-Unit'] = [0, 1]
            action_list['Select-Unit'] = [1]
            action_list['Save-Unit'] = [0,1]
            action_list['Change-Data'] = [2]
            action_list['Change-Cluster-Type'] = [2]
            action_list['Change-Cluster-Parameter'] = [2]
            action_list['Locate-Unit'] = [1]
            action_list['Show-Session'] = [1]
            action_list['Create-Session'] = [1, 2]
            action_list['Branch-Session'] = [0, 1, 2]
            action_list['Delete-Session'] = [0, 1, 2]
            action_list['Create-Project'] = [3]
            action_list['Delete-Project'] = [3]
            action_list['Change-Unit-Name'] = [1, 2]
            action_list['Change-Data-Annotation'] = [2]
            action_list['Change-Unit-Annotation'] = [2]
            action_list['Change-Session-Annotation'] = [0]
            action_list['Change-Unit-Name'] = [1, 2]
            action_list['Save-Session'] = [0]
            action_list['Branch-Unit'] = [0, 1]
            action_list['Apply-Unit'] = [0, 1]
            action_list['Change-Color'] = [2]
            action_list['Create-Unit-Annotation'] = [0, 1, 2]
            action_list['Delete-Unit-Annotation'] = [0, 1, 2]
            action_list['Update-Unit-Annotation'] = [0, 1, 2]
            action_list['Copy-Unit'] = [0, 1, 2]
            action_list['Move-Unit'] = [0, 1, 2]
            action_list['Change-PCP-Column'] = [1, 2]
            action_list['Brush-PCP-Axis'] = [1, 2]
            action_list['Brush-SCM-Axis'] = [1, 2]
            action_list['Brush-SP-Axis'] = [1, 2]
            action_list['Search-Table'] = [1]
            action_list['Search-Table-Row'] = [1]
            action_list['Restore-Unit'] = [1, 2]
            action_list['Unit-Workflow'] = [1]
            action_list['Session-Workflow'] = [1]
            action_list['Create-Unit-Graph'] = [1]
            action_list['Click-Sankey-Tab'] = [4]
            action_list['Click-Table-Tab'] = [4]
            action_list['Click-Menu-Tab'] = [4]
            action_list['Pin-Unit'] = [1, 2]
            action_list['Unpin-Unit'] = [1, 2]
            action_list['Change_Table_Order'] = [5]
            action_list['Change_Table_Page'] = [5]

            if not action in action_check_list:
                return HttpResponse(json.dumps({'success' : False, 'detail' : "No Matching Action Name.", 'output' : str(action)}) ,content_type="application/json")
            intent_str = ""
            for i in action_list[action]:
                intent_str += intent_list[i] + " "

            # Unit-Workflow, Session-Workflow
            if action == action_check_list[34] or action == action_check_list[35]:
                lh = log_history(scope=scope, action=action, intent=intent_str, user_id=username,
                                project_name=project_name, is_event=True)
            else:
                lh = log_history(scope=scope, action=action, intent=intent_str, user_id=username,
                                 project_name=project_name)
            lh.save()
            # scope session
            if session_name is not None:
                lh = log_history.objects.filter(action_id = lh.action_id)
                lh.update(session_name=session_name)
                lho = log_history.objects.filter(action_id=lh[0].action_id)
                if session_ver is not None:
                    lh.update(session_ver = int(session_ver))
                    lho = log_history.objects.filter(action_id=lh[0].action_id)
            # scope unit
            if block_ver is not None:
                # get parent block information
                parent_bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_iden, block_ver = int(block_ver))
                if len(parent_bl) is not 0:
                    lh.update(block_iden = block_iden, block_ver = int(block_ver), parent_block_iden = parent_bl[0].parent_block_iden, parent_block_ver = int(parent_bl[0].parent_block_ver))
                else:
                    lh.update(block_iden = block_iden, block_ver = int(block_ver))
                lh.update(vis_types = vis_types)
                lho = log_history.objects.filter(action_id=lh[0].action_id)
            if action_check_list[18] == action:
                lho.update(session_ver = int(session_ver)+1)
            if request.POST.get('cluster_type', ''):
                cluster_type = '%r' % request.POST['cluster_type']
                cluster_type = cluster_type.replace('\'', '')
                lho.update(clusterType = cluster_type)
            if request.POST.get('cluster_param', ''):
                cluster_param = '%r' % request.POST['cluster_param']
                cluster_param = cluster_param.replace('\'', '')
                lho.update(clusterParam = cluster_param)
            if request.POST.get('data', ''):
                data = '%r' % request.POST['data']
                data = data.replace('\'', '')
                lho.update(data = data)
            if request.POST.get('color_type', ''):
                color_type = '%r' % request.POST['color_type']
                color_type = color_type.replace('\'', '')
                lho.update(colors = color_type)
            if request.POST.get('data_annotation', ''):
                data_annotation = '%r' % request.POST['data_annotation']
                data_annotation = data_annotation.replace('\'', '')
                lho.update(data_annotation = data_annotation)
            if request.POST.get('data_name', ''):
                data_name = '%r' % request.POST['data_name']
                data_name = data_name.replace('\'', '')
                lho.update(data_name = data_name)
            #if action_check_list[1] == action:
                #lho.update(is_closed = True)
            if request.POST.get('position', ''):
                position = json.loads(request.POST.get('position'))
                lho.update(position_top = position['top'], position_left = position['left'], position_width = position['width'], position_height = position['height'])
            if action == action_check_list[3]:
                lho.update(is_event = True)
            if action == action_check_list[33]:
                lho.update(is_event = True)
            if action == action_check_list[7]:
                lho.update(is_event = True)
                vis_bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_iden, block_ver = int(block_ver))
                if len(vis_bl) > 0:
                    file_path = os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name,
                                             str(session_ver),
                                             str(block_iden), str(block_ver))
                    if vis_bl[0].vis_types == "Heatmap":
                        file_path = os.path.join(file_path, "clusters.json")
                    elif vis_bl[0].vis_types == "Parallel Coordinate Plot":
                        file_path = os.path.join(file_path, "pcp.json")
                    elif vis_bl[0].vis_types == "Scatterplot Matrix":
                        file_path = os.path.join(file_path, "scm.json")
                    elif vis_bl[0].vis_types == "Scatter Plot":
                        file_path = os.path.join(file_path, "sp.json")
                    if os.path.exists(file_path) is True:
                        rfile = open(file_path, 'r')
                        content = json.loads(rfile.readline())
                        rfile.close()
                        wfile = open(file_path, 'w')
                        content['position']['top'] = position['top']
                        content['position']['left'] = position['left']
                        content['position']['width'] = position['width']
                        content['position']['height'] = position['height']
                        wfile.write(json.dumps(content))
                        wfile.close()
            if request.POST.get('block_name', ''):
                block_name = '%r' % request.POST['block_name']
                block_name = block_name.replace('\'', '')
                lho.update(block_name = block_name)
            if request.POST.get('parent_block_iden', ''):
                parent_block_iden = '%r' % request.POST['parent_block_iden']
                parent_block_iden = parent_block_iden.replace('\'', '')
                lho.update(parent_block_iden = parent_block_iden)
            if request.POST.get('parent_block_ver', ''):
                parent_block_ver = '%r' % request.POST['parent_block_ver']
                parent_block_ver = parent_block_ver.replace('\'', '')
                lho.update(parent_block_ver = parent_block_ver)
            if action_check_list[9] == action:
                lho.update(session_ver = 0)

            if action_check_list[42]:
                if request.POST.get('column', ''):
                    column = '%r' % request.POST['column']
                    column = column.replace('\'', '')
                    lho.update(column=int(column))
            if action_check_list[43]:
                if request.POST.get('page', ''):
                    page = '%r' % request.POST['page']
                    page = page.replace('\'', '')
                    lho.update(page=int(page))


            if action_check_list[27] == action:
                get_bl = block.objects.filter(user_id = username, project_name = project_name,
                                           session_name = session_name, session_ver = int(session_ver),
                                           block_iden = block_iden, block_ver = int(block_ver)).order_by("-last_date")
                if len(get_bl) > 0:
                    if request.POST.get('column_order', ''):
                        column_order = '%r' % request.POST['column_order']
                        column_order = column_order.replace('\'', '')
                    else:
                        column_order = None
                    #lho.update(pcp_id = get_bl.pcp_id, brushed_column = brushed_column)
                    pcp_obj = pcp.objects.filter(pcp_id = get_bl[0].pcp_id)
                    new_pcp_obj = pcp_obj[0]
                    new_pcp_obj.pcp_id = None
                    new_pcp_obj.save()
                    new_pcp_obj = pcp.objects.filter(pcp_id=new_pcp_obj.pcp_id)
                    new_pcp_obj.update(column_order = column_order)
                    lho.update(pcp_id=new_pcp_obj[0].pcp_id)
                    get_bl.update(pcp_id=new_pcp_obj[0].pcp_id)
                    file_path = os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name, str(session_ver),
                                 str(block_iden),str(block_ver), "pcp.json")
                    rfile = open(file_path, 'r')
                    pcp_content = json.loads(rfile.readline())
                    rfile.close()
                    wfile = open(file_path, 'w')
                    if column_order is None:
                        column_order = ""
                    pcp_content['request'][0]['column_order'] = column_order
                    pcp_content['response'][0]['column_order'] = column_order
                    wfile.write(json.dumps(pcp_content))
                    wfile.close()
            if  action_check_list[28] == action:
                get_bl = block.objects.filter(user_id=username, project_name=project_name, session_name=session_name,
                                           session_ver=int(session_ver), block_iden=block_iden,
                                           block_ver=int(block_ver)).order_by("-last_date")
                if len(get_bl) > 0:
                    if request.POST.get('selected_index', ''):
                        selected_index = '%r' % request.POST['selected_index']
                        selected_index = selected_index.replace('\'', '')
                    else:
                        selected_index = None

                    if request.POST.get('brushed_axis', ''):
                        brushed_axis = '%r' % request.POST['brushed_axis']
                        brushed_axis = brushed_axis.replace('\'', '')
                    else:
                        brushed_axis = None

                    if request.POST.get('brushed_range', ''):
                        brushed_range = '%r' % request.POST['brushed_range']
                        brushed_range = brushed_range.replace('\'', '')
                    else:
                        brushed_range = None
                    pcp_obj = pcp.objects.filter(pcp_id=get_bl[0].pcp_id)
                    new_pcp_obj = pcp_obj[0]
                    new_pcp_obj.pcp_id = None
                    new_pcp_obj.save()
                    new_pcp_obj = pcp.objects.filter(pcp_id=new_pcp_obj.pcp_id)
                    new_pcp_obj.update(selected_index=selected_index, brushed_axis=brushed_axis,
                                   brushed_range=brushed_range)
                    lho.update(pcp_id=new_pcp_obj[0].pcp_id)
                    get_bl.update(pcp_id=new_pcp_obj[0].pcp_id)
                    file_path = os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name,
                                             str(session_ver),
                                             str(block_iden), str(block_ver), "pcp.json")
                    rfile = open(file_path, 'r')
                    pcp_content = json.loads(rfile.readline())
                    rfile.close()
                    wfile = open(file_path, 'w')
                    if selected_index is None:
                        selected_index = ""
                    if brushed_axis is None:
                        brushed_axis = ""
                    if brushed_range is None:
                        brushed_range = ""
                    pcp_content['request'][0]['selected_index'] = selected_index
                    pcp_content['response'][0]['selected_index'] = selected_index
                    pcp_content['request'][0]['brushed_axis'] = brushed_axis
                    pcp_content['response'][0]['brushed_axis'] = brushed_axis
                    pcp_content['request'][0]['brushed_range'] = brushed_range
                    pcp_content['response'][0]['brushed_range'] = brushed_range
                    wfile.write(json.dumps(pcp_content))
                    wfile.close()
            if action_check_list[29] == action:
                get_bl = block.objects.filter(user_id=username, project_name=project_name, session_name=session_name,
                                           session_ver=int(session_ver), block_iden=block_iden,
                                           block_ver=int(block_ver)).order_by("-last_date")
                if len(get_bl) > 0:
                    if request.POST.get('selected_index', ''):
                        selected_index = '%r' % request.POST['selected_index']
                        selected_index = selected_index.replace('\'', '')
                    else:
                        selected_index = None

                    if request.POST.get('brushed_axis', ''):
                        brushed_axis = '%r' % request.POST['brushed_axis']
                        brushed_axis = brushed_axis.replace('\'', '')
                    else:
                        brushed_axis = None

                    if request.POST.get('brushed_range', ''):
                        brushed_range = '%r' % request.POST['brushed_range']
                        brushed_range = brushed_range.replace('\'', '')
                    else:
                        brushed_range = None

                    scm_obj = scm.objects.filter(scm_id=get_bl[0].scm_id)
                    new_scm_obj = scm_obj[0]
                    new_scm_obj.scm_id = None
                    new_scm_obj.save()
                    new_scm_obj = scm.objects.filter(scm_id=new_scm_obj.scm_id)
                    new_scm_obj.update(selected_index=selected_index, brushed_axis = brushed_axis, brushed_range = brushed_range)
                    lho.update(scm_id=new_scm_obj[0].scm_id)
                    get_bl.update(scm_id=new_scm_obj[0].scm_id)
                    file_path = os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name,
                                             str(session_ver),
                                             str(block_iden), str(block_ver), "scm.json")
                    rfile = open(file_path, 'r')
                    scm_content = json.loads(rfile.readline())
                    rfile.close()
                    wfile = open(file_path, 'w')
                    if selected_index is None:
                        selected_index = ""
                    if brushed_axis is None:
                        brushed_axis = ""
                    if brushed_range is None:
                        brushed_range = ""
                    scm_content['request'][0]['selected_index'] = selected_index
                    scm_content['response'][0]['selected_index'] = selected_index
                    scm_content['request'][0]['brushed_axis'] = brushed_axis
                    scm_content['response'][0]['brushed_axis'] = brushed_axis
                    scm_content['request'][0]['brushed_range'] = brushed_range
                    scm_content['response'][0]['brushed_range'] = brushed_range
                    wfile.write(json.dumps(scm_content))
                    wfile.close()
            if action_check_list[30] == action:
                get_bl = block.objects.filter(user_id=username, project_name=project_name, session_name=session_name,
                                           session_ver=int(session_ver), block_iden=block_iden,
                                           block_ver=int(block_ver)).order_by("-last_date")
                if len(get_bl) > 0:
                    if request.POST.get('brushed_range', ''):
                        brushed_range = '%r' % request.POST['brushed_range']
                        brushed_range = brushed_range.replace('\'', '')
                    else:
                        brushed_range = None
                    if request.POST.get('selected_index', ''):
                        selected_index = '%r' % request.POST['selected_index']
                        selected_index = selected_index.replace('\'', '')
                    else:
                        selected_index = None
                    sp_obj = sp.objects.filter(sp_id=get_bl[0].sp_id)
                    new_sp_obj = sp_obj[0]
                    new_sp_obj.sp_id = None
                    new_sp_obj.save()
                    new_sp_obj = sp.objects.filter(sp_id=new_sp_obj.sp_id)
                    new_sp_obj.update(brushed_range = brushed_range, selected_index = selected_index)
                    lho.update(sp_id = new_sp_obj[0].sp_id)
                    get_bl.update(sp_id=new_sp_obj[0].sp_id)
                    file_path = os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name,
                                             str(session_ver),
                                             str(block_iden), str(block_ver), "sp.json")
                    rfile = open(file_path, 'r')
                    sp_content = json.loads(rfile.readline())
                    rfile.close()
                    wfile = open(file_path, 'w')
                    if brushed_range is None:
                        brushed_range = ""
                    sp_content['request'][0]['brushed_range'] = brushed_range
                    sp_content['response'][0]['brushed_range'] = brushed_range
                    sp_content['request'][0]['selected_index'] = selected_index
                    sp_content['response'][0]['selected_index'] = selected_index
                    wfile.write(json.dumps(sp_content))
                    wfile.close()
            if action_check_list[31] == action or action_check_list[32] == action:
                if request.POST.get('selected_index', ''):
                    selected_index = '%r' % request.POST['selected_index']
                    selected_index = selected_index.replace('\'', '')
                else:
                    selected_index = None
                lho.update(selected_index = selected_index, is_event = False)

            # unit annotation id
            if action_check_list[22] == action:
                bl_anno = block_annotation_history.objects.filter(user_id=username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_iden).order_by("-last_date")
                lho.update(anno_id = bl_anno[0].annotation_id)

            # branched unit name update
            if action_check_list[19] == action:
                brch_log = log_history.objects.filter(user_id=username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_iden, block_ver = int(block_ver))
                for k in brch_log:
                    if action_check_list[19] == k.action:
                        if k.action_id == lho[0].action_id:
                            continue
                        else:
                            k.delete()
                    else:
                        brch_log_obj = log_history.objects.filter(action_id = k.action_id)
                        brch_log_obj.update(creatation_date = datetime.datetime.now(), block_name = block_name)


            # save version update
            if action_check_list[2] == action or action_check_list[19] == action:
                lho.update(is_save = True)
                get_save_ver = block.objects.all().filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_iden, is_save = True).aggregate(Max('save_ver'))
                save_ver = get_save_ver['save_ver__max']
                lho.update(save_ver = save_ver)

            if action_check_list[2] == action or action_check_list[19] == action:
                lho.update(is_used = True)

                if int(block_ver) != 0:
                    chk_used = log_history.objects.filter(scope = "unit", user_id=username, session_name=session_name, session_ver=int(session_ver), block_iden = block_iden, block_ver = int(block_ver)-1).order_by("-creatation_date")
                else:
                    chk_used = log_history.objects.filter(scope="unit", user_id=username, session_name=session_name,
                                                          session_ver=int(session_ver), block_iden=block_iden,
                                                          block_ver=int(block_ver)).order_by("-creatation_date")

                test_logs = log_history.objects.filter(scope="unit", user_id=username, session_name=session_name,
                                                       session_ver=int(session_ver), block_iden=block_iden,
                                                       )

                chk_du_unit_list = []
                # update is_used
                for i in chk_used:
                    if i.action not in chk_du_unit_list:
                        try:
                            used_lh = log_history.objects.get(action_id = i.action_id)
                            used_lh.__dict__.update(is_used = True)
                            used_lh.save()
                            chk_du_unit_list.append(i.action)
                        except log_history.DoesNotExist:
                            continue
                    if i.action == "Save-Unit" and int(block_ver) is not 0:
                        break

                if int(block_ver) != 0:
                    ver_up_logs = log_history.objects.filter(scope = "unit", user_id=username, session_name=session_name, session_ver=int(session_ver), block_iden = block_iden, block_ver = int(block_ver)-1).order_by("creatation_date")
                else:
                    ver_up_logs = log_history.objects.filter(scope="unit", user_id=username, session_name=session_name,
                                                          session_ver=int(session_ver), block_iden=block_iden,
                                                          block_ver=int(block_ver)).order_by("creatation_date")

                is_checked = False
                is_dbl_check = False

                # block_ver up
                if len(ver_up_logs) is not 0:
                    for i in ver_up_logs:
                        #if i.action == action_check_list[2]:
                            #break
                        if is_checked == True and is_dbl_check == False:
                            if list_checker(i.action, action_check_list, [27, 28, 29, 30]):
                                continue
                            ver_up_lh = log_history.objects.get(action_id=i.action_id)
                            ver_up_lh.__dict__.update(block_ver=int(i.block_ver) + 1)
                            ver_up_lh.save()
                        if i.action == action_check_list[2]: #or i.action == action_check_list[19]:
                            if is_checked == True:
                                is_dbl_check = True
                            is_checked = True

            if action_check_list[3] == action and block_ver is not None and block_iden is not None:
                path_bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_iden, block_ver = int(block_ver))
                if len(path_bl) > 0:
                    path = os.path.join('static', 'member', username, project_name, session_name, session_ver, block_iden, block_ver)
                    if path_bl[0].vis_types == "Heatmap":
                        path = os.path.join(path, 'clusters.json')
                    elif path_bl[0].vis_types == "Parallel Coordinate Plot":
                        path = os.path.join(path, 'pcp.json')
                    elif path_bl[0].vis_types == "Scatterplot Matrix":
                        path = os.path.join(path, 'scm.json')
                    elif path_bl[0].vis_types == "Scatter Plot":
                        path = os.path.join(path, 'sp.json')
                    lho.delete()
                    return HttpResponse(json.dumps(
                        {'success': True, 'detail': "Inserted Log.", 'output': path}),
                                        content_type="application/json")

            return HttpResponse(json.dumps({'success' : True, 'detail' : "Inserted Log.", 'output' : str(action) + " " + str(intent_str)}) ,content_type="application/json")
    else:
        return HttpResponse(json.dumps({"errors" : errors}))


@ensure_csrf_cookie
def goaHuman(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('gene_list', ''):
            errors.append("Enter an gene list.")
        if not errors:
            gene_list = json.loads(request.POST.get('gene_list'))
            query_list = []
            for i in gene_list:
                query_list.append(Q(synonym_genes__contains = i['gene']))
            output_gene_list = []
            gs = goa_human.objects.filter(reduce(operator.or_, query_list))
            go_name_list = []
            go_gene_list = []
            for i in gs:
                gene_elem = {}
                gene_elem['gene'] = i.gene
                gene_elem['gene_ontology_pathway'] = i.gene_ontology_pathway
                gene_elem['synonym_genes'] = i.synonym_genes
                gene_elem['species'] = i.species
                output_gene_list.append(gene_elem)
                if not i.gene_ontology_pathway in go_name_list:
                    go_name_list.append(i.gene_ontology_pathway)
                go_gene_list.append(i.gene)
            go_list = [[] for i in range(0, len(go_name_list))]
            for i in gs:
                go_list[go_name_list.index(i.gene_ontology_pathway)].append(i.gene)
            qlist = []
            for i in go_name_list:
                qlist.append(Q(pathway_id = i))
            go = go_obo.objects.filter(reduce(operator.or_, qlist))
            output_list = []
            for i in go:
                output_info = {}
                output_info['pathway_id'] = i.pathway_id
                output_info['pathway_name'] = i.pathway_name
                output_info['count'] = len(go_list[go_name_list.index(i.pathway_id)])
                output_list.append(output_info)
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Got gene list.", 'output' : output_list}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({"errors" : errors}))

def adminPage(request):
    """
    admin page
    :param request:
    :return:
    """
    return render(request, 'adminPage.html')

def map(request):
    """
    seminar(map)
    """
    return render(request, 'map.html')

@gzip_compress
def uitest(request):
    """
    ui test html
    """
    return render(request, 'uitest.html')

@gzip_compress
def color(request):
    """
    color html
    """
    return render(request, 'color.html')

@gzip_compress
def daehwa(request):
    """
    daehwa html
    """
    return render(request, 'daehwa.html')


