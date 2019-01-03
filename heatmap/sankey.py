from heatmap import *

def count_values(data, is_session, info_set):
    for i in data['children']:
        if "children" in i:
            count_values(i, is_session, info_set)
        #print(i['parent'])
        #print(i['id'])
        info_set['action_values'][info_set['ids'].index(i['parent'])] += info_set['action_values'][info_set['ids'].index(i['id'])]
        info_set['apply_values'][info_set['ids'].index(i['parent'])] += info_set['apply_values'][info_set['ids'].index(i['id'])]
        info_set['anno_values'][info_set['ids'].index(i['parent'])] += info_set['anno_values'][info_set['ids'].index(i['id'])]
        if is_session == True:
            info_set['save_values'][info_set['ids'].index(i['parent'])] += info_set['save_values'][info_set['ids'].index(i['id'])]

def erase_hypon(data, is_session, info_set):
    for i in data['children']:
        if "children" in i:
            erase_hypon(i, is_session, info_set)
        i['total_action_num'] = info_set['action_values'][info_set['ids'].index(i['id'])]
        i['total_apply_num'] = info_set['apply_values'][info_set['ids'].index(i['id'])]
        if is_session == True:
            i['total_save_num'] = info_set['save_values'][info_set['ids'].index(i['id'])]
            i['name'] = i['name'][:i['name'].rfind("-")]
        i['total_anno_num'] = info_set['anno_values'][info_set['ids'].index(i['id'])]
        i['id'] = i['id'][:i['id'].rfind("-")]


@ensure_csrf_cookie
def get_session_history(request):
    errors = []
    username = ""
    if request.method == 'POST':
        param_list = ['username', 'project_name']
        errors = param_checker(request, errors, param_list)
        if not errors:
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            info = {}
            info['username'] = username
            info['project_name'] = project_name
            info['is_analysis'] = False
            return run_session_history(info)
    else:
        return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

def run_session_history(ses_info):
    if not ses_info['project_name'] == None:
        ses = []
        links = []
        ses = session.objects.filter(user_id=ses_info['username'], project_name=ses_info['project_name'])
        action_values = []
        action_values.append(0)
        apply_values = []
        apply_values.append(0)
        save_values = []
        save_values.append(0)
        anno_values = []
        anno_values.append(0)

        ids = []
        ids.append(ses_info['project_name'])
        total_action = 0
        total_anno_num = 0
        total_apply_num = 0
        total_save_num = 0
        tree_info = []

        #standard_date = datetime.date(2017, 4, 20)

        for i in ses:
            for count in range(0, int(i.session_ver) + 1):
                stat = {}
                stat_list = []
                logs = []
                """
                none_logs = log_history.objects.filter(user_id=ses_info['username'], project_name=ses_info['project_name'],
                                                  session_name=i.session_name, session_ver=None,
                                                  is_event=False, is_closed = False, creatation_date__lte = standard_date).values('action_id', 'action', 'scope', 'user_id',
                                                                         'project_name', 'session_name', 'session_ver',
                                                                         'block_iden', 'block_name', 'block_ver',
                                                                         'clusterType', 'clusterParam', 'colors',
                                                                         'data', 'data_name', 'data_annotation',
                                                                         'position_top', 'position_left',
                                                                         'position_width', 'position_height',
                                                                         'is_closed', 'creatation_date',
                                                                         'parent_block_iden', 'parent_block_ver',
                                                                         'save_ver', 'is_save')
                """
                none_logs = log_history.objects.filter(user_id=ses_info['username'],
                                                       project_name=ses_info['project_name'],
                                                       session_name=i.session_name, session_ver=None,
                                                       is_event=False, is_closed=False).values('action_id', 'action',
                                                                                                  'scope', 'user_id',
                                                                                                  'project_name',
                                                                                                  'session_name',
                                                                                                  'session_ver',
                                                                                                  'block_iden',
                                                                                                  'block_name',
                                                                                                  'block_ver',
                                                                                                  'clusterType',
                                                                                                  'clusterParam',
                                                                                                  'colors',
                                                                                                  'data', 'data_name',
                                                                                                  'data_annotation',
                                                                                                  'position_top',
                                                                                                  'position_left',
                                                                                                  'position_width',
                                                                                                  'position_height',
                                                                                                  'is_closed',
                                                                                                  'creatation_date',
                                                                                                  'parent_block_iden',
                                                                                                  'parent_block_ver',
                                                                                                  'save_ver', 'is_save')
                logs.extend(none_logs)
                """
                total_logs = log_history.objects.filter(user_id=ses_info['username'], project_name=ses_info['project_name'],
                                                  session_name=i.session_name, session_ver=count,
                                                  is_event=False, is_closed = False, creatation_date__lte = standard_date).values('action_id', 'action', 'scope', 'user_id',
                                                                         'project_name', 'session_name', 'session_ver',
                                                                         'block_iden', 'block_name', 'block_ver',
                                                                         'clusterType', 'clusterParam', 'colors',
                                                                         'data', 'data_name', 'data_annotation',
                                                                         'position_top', 'position_left',
                                                                         'position_width', 'position_height',
                                                                         'is_closed', 'creatation_date',
                                                                         'parent_block_iden', 'parent_block_ver',
                                                                         'save_ver', 'is_save')
                """
                total_logs = log_history.objects.filter(user_id=ses_info['username'],
                                                        project_name=ses_info['project_name'],
                                                        session_name=i.session_name, session_ver=count,
                                                        is_event=False, is_closed=False).values('action_id',
                                                                                                   'action', 'scope',
                                                                                                   'user_id',
                                                                                                   'project_name',
                                                                                                   'session_name',
                                                                                                   'session_ver',
                                                                                                   'block_iden',
                                                                                                   'block_name',
                                                                                                   'block_ver',
                                                                                                   'clusterType',
                                                                                                   'clusterParam',
                                                                                                   'colors',
                                                                                                   'data', 'data_name',
                                                                                                   'data_annotation',
                                                                                                   'position_top',
                                                                                                   'position_left',
                                                                                                   'position_width',
                                                                                                   'position_height',
                                                                                                   'is_closed',
                                                                                                   'creatation_date',
                                                                                                   'parent_block_iden',
                                                                                                   'parent_block_ver',
                                                                                                   'save_ver',
                                                                                                   'is_save')
                logs.extend(total_logs)
                action_list = []
                anno_path = ""
                for j in logs:
                    action_elem = {}
                    action_elem['action'] = j['action']
                    action_elem['action_id'] = j['action_id']
                    parameter = {}
                    position = {}

                    if not list_checker(j['action'], action_check_list,
                                    [3, 7, 8, 37, 38, 39]):

                        if list_checker(j['action'], action_check_list,
                                        [0, 1, 2, 4, 5, 6, 14, 15, 17, 21, 27, 28, 29, 36]): # 3, 7
                            parameter['block_iden'] = j['block_iden']
                            parameter['block_name'] = j['block_name']
                            parameter['block_ver'] = j['block_ver']
                            parameter['save_ver'] = j['save_ver']
                            if list_checker(j['action'], action_check_list, [4]):
                                parameter['data_name'] = j['data_name']
                            elif list_checker(j['action'], action_check_list, [5]):
                                parameter['clusterType'] = j['clusterType']
                            elif list_checker(j['action'], action_check_list, [6]):
                                parameter['clusterParam'] = j['clusterParam']
                            elif list_checker(j['action'], action_check_list, [7]):
                                position['position_top'] = j['position_top']
                                position['position_left'] = j['position_left']
                                position['position_width'] = j['position_width']
                                position['position_height'] = j['position_height']
                                parameter['position'] = position
                            elif list_checker(j['action'], action_check_list, [14]):
                                parameter['data_annotation'] = j['data_annotation']
                            elif list_checker(j['action'], action_check_list, [15]):
                                parameter['block_annotation'] = j['block_annotation']
                            elif list_checker(j['action'], action_check_list, [19]):
                                parameter['parent_block_iden'] = j['parent_block_iden']
                                parameter['parent_block_ver'] = j['parent_block_ver']
                            elif list_checker(j['action'], action_check_list, [21]):
                                parameter['color_type'] = j['colors']
                            elif list_checker(j['action'], action_check_list, [27]):
                                # get pcp_id
                                pcp_bl = block.objects.filter(user_id=j['user_id'], project_name=j['project_name'],
                                                              session_name=j['session_name'],
                                                              session_ver=int(j['session_ver']),
                                                              block_iden=j['block_iden'],
                                                              block_ver=int(j['block_ver']))
                                if len(pcp_bl) > 0:
                                    if pcp_bl[0].pcp_id is not None:
                                        pcp_obj = pcp.objects.filter(pcp_id=pcp_bl[0].pcp_id)
                                        parameter['column_order'] = pcp_obj[0].column_order
                            elif list_checker(j['action'], action_check_list, [28]):
                                # get pcp_id
                                pcp_bl = block.objects.filter(user_id=j['user_id'], project_name=j['project_name'],
                                                              session_name=j['session_name'],
                                                              session_ver=int(j['session_ver']),
                                                              block_iden=j['block_iden'],
                                                              block_ver=int(j['block_ver']))
                                if len(pcp_bl) > 0:
                                    if pcp_bl[0].pcp_id is not None:
                                        pcp_obj = pcp.objects.filter(pcp_id=pcp_bl[0].pcp_id)
                                        parameter['selected_index'] = pcp_obj[0].selected_index
                                        parameter['brushed_axis'] = pcp_obj[0].brushed_axis
                                        parameter['brushed_range'] = pcp_obj[0].brushed_range
                            elif list_checker(j['action'], action_check_list, [29]):
                                # get scm_id
                                scm_bl = block.objects.filter(user_id=j['user_id'], project_name=j['project_name'],
                                                              session_name=j['session_name'],
                                                              session_ver=int(j['session_ver']),
                                                              block_iden=j['block_iden'],
                                                              block_ver=int(j['block_ver']))
                                if len(scm_bl) > 0:
                                    if scm_bl[0].scm_id is not None:
                                        scm_obj = scm.objects.filter(scm_id=scm_bl[0].scm_id)
                                        parameter['selected_index'] = scm_obj[0].selected_index
                                        parameter['brushed_axis'] = scm_obj[0].brushed_axis
                                        parameter['brushed_range'] = scm_obj[0].brushed_range
                            elif list_checker(j['action'], action_check_list, [30]):
                                # get scm_id
                                sp_bl = block.objects.filter(user_id=j['user_id'], project_name=j['project_name'],
                                                          session_name=j['session_name'],
                                                          session_ver=int(j['session_ver']),
                                                          block_iden=j['block_iden'],
                                                          block_ver=int(j['block_ver']))
                                if len(sp_bl) > 0:
                                    if sp_bl[0].sp_id is not None:
                                        sp_obj = sp.objects.filter(sp_id=sp_bl[0].sp_id)
                                        parameter['brushed_range'] = sp_obj[0].brushed_range
                        elif list_checker(j['action'], action_check_list, [9, 10, 11, 18]): # 8
                            parameter['username'] = ses_info['username']
                            parameter['project_name'] = j['project_name']
                            parameter['session_name'] = j['session_name']
                            parameter['session_ver'] = j['session_ver']
                        elif list_checker(j['action'], action_check_list, [12]):
                            parameter['project_name'] = j['project_name']
                            parameter['project_annotation'] = j['project_annotation']
                        elif list_checker(j['action'], action_check_list, [13]):
                            parameter['project_name'] = j['project_name']

                        action_elem['parameter'] = parameter
                        action_elem['date'] = j['creatation_date'].strftime("%Y-%m-%d %H:%M:%S")
                        action_list.append(action_elem)
                action_num = len(logs)

                for log in logs:
                    if log['action'] in stat_list:
                        stat[log['action']] += 1
                    else:
                        stat_list.append(log['action'])
                        stat[log['action']] = 1
                total_block_anno_num = 0
                bl = block.objects.filter(user_id=ses_info['username'], project_name=ses_info['project_name'], session_name=i.session_name,
                                          session_ver=count).values_list('block_iden', 'block_ver', 'clusterType',
                                                                         'is_save').annotate(
                    last_date=Max('last_date')).order_by('-block_ver').distinct()
                bl_list = []
                for j in bl:
                    bl_list.append(j)
                du_list = []
                result_list = []
                for j in bl_list:
                    if du_list.count(j[0]) == 0:
                        result_list.append(j)
                        du_list.append(j[0])
                    else:
                        pass
                for k in result_list:
                    get_anno_num = block_annotation_history.objects.all().filter(user_id=ses_info['username'],
                                                                                 project_name=ses_info['project_name'],
                                                                                 session_name=i.session_name,
                                                                                 session_ver=count, block_iden=k[0],
                                                                                 block_ver=0,
                                                                                 is_removed=False).aggregate(
                        Max('annotation_num'))
                    max_anno_num = get_anno_num['annotation_num__max']
                    if max_anno_num is not None:  # null
                        annotation_num = max_anno_num + 1
                    else:
                        annotation_num = 0
                    total_block_anno_num += annotation_num
                anno_values.append(total_block_anno_num)
                total_anno_num += total_block_anno_num
                total_action += action_num
                s_apply_num = 0
                s_save_num = 0
                for j in bl:
                    s_apply_num = s_apply_num + 1
                    if j[3] == True:
                        s_save_num = s_save_num + 1
                total_apply_num = total_apply_num + s_apply_num
                total_save_num = total_save_num + s_save_num
                bookmark_ses = session_history.objects.filter(user_id=ses_info['username'], project_name=ses_info['project_name'],
                                                              session_name=i.session_name, session_ver=int(count))
                if count == 0:
                    if i.parent_session_name == "" or i.is_first == True:
                        tree_info.append([ses_info['project_name'], i.session_name + "-" + str(0), 0, i.last_date, action_num,
                                          total_block_anno_num, s_apply_num, s_save_num, stat, action_list,
                                          bookmark_ses[0].is_bookmarked])
                    else:
                        tree_info.append(
                            [i.parent_session_name + "-" + str(i.parent_session_ver), i.session_name + "-" + str(0), 0,
                             i.last_date, action_num, total_block_anno_num, s_apply_num, s_save_num, stat, action_list,
                             bookmark_ses[0].is_bookmarked])
                    ids.append(i.session_name + "-" + str(0))
                else:
                    tree_info.append(
                        [i.session_name + "-" + str(int(count) - 1), i.session_name + "-" + str(int(count)), count,
                         i.last_date, action_num, total_block_anno_num, s_apply_num, s_save_num, stat, action_list,
                         bookmark_ses[0].is_bookmarked])
                    ids.append(i.session_name + "-" + str(int(count)))
                action_values.append(action_num)
                apply_values.append(s_apply_num)
                save_values.append(s_save_num)

        info_set = {}
        info_set['action_values'] = action_values
        info_set['apply_values'] = apply_values
        info_set['save_values'] = save_values
        info_set['anno_values'] = anno_values
        info_set['ids'] = ids

        name_to_node = {}
        proj = project.objects.filter(user_id=ses_info['username'], project_name=ses_info['project_name'])
        root = {'id': ses_info['project_name'], 'name': ses_info['project_name'], 'children': [], 'ver': None,
                'last_date': proj[0].last_date.strftime("%Y-%m-%d %H:%M:%S"), 'parent': None, 'action_num': 0,
                'total_action_num': total_action, 'anno_num': 0, 'total_anno_num': total_anno_num, 'apply_num': 0,
                'total_apply_num': total_apply_num, 'save_num': 0, 'total_save_num': total_save_num, "stat": None,
                'bookmark': False}
        for parent, child, ver, last_date, action_num, total_block_anno_num, s_apply_num, s_save_num, stat, action_list, is_bookmarked in tree_info:
            parent_node = name_to_node.get(parent)
            if not parent_node:
                parent_node = root
            name_to_node[child] = child_node = {'id': child, 'name': child, 'ver': ver,
                                                'last_date': last_date.strftime("%Y-%m-%d %H:%M:%S"), 'parent': parent,
                                                'action_num': action_num, 'total_action_num': 0,
                                                'anno_num': total_block_anno_num, 'total_action_num': 0,
                                                'apply_num': s_apply_num, 'total_apply_num': 0, 'save_num': s_save_num,
                                                'total_save_num': 0, "stat": stat, "action_list": action_list,
                                                'bookmark': is_bookmarked}
            parent_node.setdefault('children', []).append(child_node)
        count_values(root, True, info_set)
        erase_hypon(root, True, info_set)
        if ses_info['is_analysis'] == False:
            return HttpResponse(json.dumps({'success': True, 'detail': "Get session history.", 'output': root}),
                                content_type="application/json")
        else:
            return json.dumps({'success': True, 'detail': "Get session history.", 'output': root})
    else:
        return HttpResponse(json.dumps({'success': True, 'detail': "No project.", 'output': ""}),
                            content_type="application/json")

def erase_hypon_bl(data):
    for i in data['children']:
        if "children" in i:
            erase_hypon_bl(i)
        i['block_iden'] = i['block_iden'][:i['block_iden'].rfind("-")]

@ensure_csrf_cookie
def action_history(request):
    errors = []
    username = ""
    session_name = ""
    session_ver = 0
    if request.method == 'POST':
        param_list = ['username', 'project_name', 'session_name', 'session_ver']
        errors = param_checker(request, errors, param_list)
        if not errors:
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            info = {}
            info['username'] = username
            info['project_name'] = project_name
            info['session_name'] = session_name
            info['session_ver'] = int(session_ver)
            info['is_analysis'] = False
            return run_unit_history(info)
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

def run_unit_history(unit_info):
    # get all blocks
    action_values = []
    action_values.append(0)
    apply_values = []
    apply_values.append(0)
    anno_values = []
    anno_values.append(0)
    ids = []
    ids.append(unit_info['session_name'] + "-" + str(unit_info['session_ver']))
    total_action = 0
    total_anno_num = 0
    total_apply_num = 0

    save_bls = block.objects.filter(user_id=unit_info['username'], project_name=unit_info['project_name'], session_name=unit_info['session_name'],
                                    session_ver=int(unit_info['session_ver']), is_save=True).order_by('last_date')
    node = []
    pre_ver = 0
    pre_id_list = []
    pre_ver_list = []

    #standard_date = datetime.date(2017, 4, 20)

    tree_info = []
    for j in save_bls:
        logs = []
        u_apply_num = 0
        node_elem = {}

        """
        none_logs = log_history.objects.filter(user_id=unit_info['username'],
                                               project_name=unit_info['project_name'],
                                               session_name=unit_info['session_name'], session_ver=int(unit_info['session_ver']),
                                               is_event=False, is_closed=False).values('action_id', 'action',
                                                                                       'scope', 'user_id',
                                                                                       'project_name',
                                                                                       'session_name',
                                                                                       'session_ver',
                                                                                       'block_iden',
                                                                                       'block_name',
                                                                                       'block_ver',
                                                                                       'clusterType',
                                                                                       'clusterParam',
                                                                                       'colors',
                                                                                       'data', 'data_name',
                                                                                       'data_annotation',
                                                                                       'position_top',
                                                                                       'position_left',
                                                                                       'position_width',
                                                                                       'position_height',
                                                                                       'is_closed',
                                                                                       'creatation_date',
                                                                                       'parent_block_iden',
                                                                                       'parent_block_ver',
                                                                                       'save_ver', 'is_save')
        logs.extend(none_logs)
        """

        if j.block_iden in pre_id_list:  # not first saved unit
            new_bl_list = []
            """
            ran_logs = log_history.objects.filter(scope="unit", user_id=unit_info['username'], project_name=unit_info['project_name'],
                                                  session_name=unit_info['session_name'], session_ver=int(unit_info['session_ver']),
                                                  block_iden=j.block_iden, block_ver__range=(
                    int(pre_ver_list[pre_id_list.index(j.block_iden)]) + 1, int(j.block_ver)),
                                                  is_event=False, is_closed = False, creatation_date__lte = standard_date).values('action_id', 'action', 'scope',
                                                                         'user_id', 'project_name',
                                                                         'session_name', 'session_ver',
                                                                         'block_iden', 'block_name',
                                                                         'block_ver', 'clusterType',
                                                                         'clusterParam', 'colors', 'data',
                                                                         'data_name', 'data_annotation',
                                                                         'position_top', 'position_left',
                                                                         'position_width', 'position_height',
                                                                         'is_closed', 'creatation_date',
                                                                         'parent_block_iden',
                                                                         'parent_block_ver', 'save_ver',
                                                                         'is_save').order_by(
                ("creatation_date"))
            """
            ran_logs = log_history.objects.filter(scope="unit", user_id=unit_info['username'],
                                                  project_name=unit_info['project_name'],
                                                  session_name=unit_info['session_name'],
                                                  session_ver=int(unit_info['session_ver']),
                                                  block_iden=j.block_iden, block_ver__range=(
                    int(pre_ver_list[pre_id_list.index(j.block_iden)]) + 1, int(j.block_ver)),
                                                  is_event=False, is_closed=False,).values('action_id', 'action',
                                                                                             'scope',
                                                                                             'user_id', 'project_name',
                                                                                             'session_name',
                                                                                             'session_ver',
                                                                                             'block_iden', 'block_name',
                                                                                             'block_ver', 'clusterType',
                                                                                             'clusterParam', 'colors',
                                                                                             'data',
                                                                                             'data_name',
                                                                                             'data_annotation',
                                                                                             'position_top',
                                                                                             'position_left',
                                                                                             'position_width',
                                                                                             'position_height',
                                                                                             'is_closed',
                                                                                             'creatation_date',
                                                                                             'parent_block_iden',
                                                                                             'parent_block_ver',
                                                                                             'save_ver',
                                                                                             'is_save').order_by(
                ("creatation_date"))

            for k in ran_logs:
                new_bl_list.append(k)
            logs.extend(new_bl_list)
            u_apply_num = j.block_ver - (pre_ver_list[pre_id_list.index(j.block_iden)])
        else:  # first saved unit
            if j.block_ver == 0:  # not applied unit, only saved
                if j.parent_block_iden == None:  # not branched unit
                    """
                    bs_logs = log_history.objects.filter(scope="unit", user_id=unit_info['username'], project_name=unit_info['project_name'],
                                                         session_name=unit_info['session_name'], session_ver=int(unit_info['session_ver']),
                                                         block_iden=j.block_iden, block_ver=0, is_event=False, is_closed = False, creatation_date__lte = standard_date).values(
                        'action_id', 'action', 'scope', 'user_id', 'project_name', 'session_name', 'session_ver',
                        'block_iden', 'block_name', 'block_ver', 'clusterType', 'clusterParam', 'colors', 'data',
                        'data_name', 'data_annotation', 'position_top', 'position_left', 'position_width',
                        'position_height', 'is_closed', 'creatation_date', 'parent_block_iden', 'parent_block_ver',
                        'save_ver', 'is_save').order_by("creatation_date")
                    """
                    bs_logs = log_history.objects.filter(scope="unit", user_id=unit_info['username'],
                                                         project_name=unit_info['project_name'],
                                                         session_name=unit_info['session_name'],
                                                         session_ver=int(unit_info['session_ver']),
                                                         block_iden=j.block_iden, block_ver=0, is_event=False,
                                                         is_closed=False).values(
                        'action_id', 'action', 'scope', 'user_id', 'project_name', 'session_name', 'session_ver',
                        'block_iden', 'block_name', 'block_ver', 'clusterType', 'clusterParam', 'colors', 'data',
                        'data_name', 'data_annotation', 'position_top', 'position_left', 'position_width',
                        'position_height', 'is_closed', 'creatation_date', 'parent_block_iden', 'parent_block_ver',
                        'save_ver', 'is_save').order_by("creatation_date")
                    new_bl_list = []
                    for k in bs_logs:
                        new_bl_list.append(k)
                    logs.extend(new_bl_list)
                    u_apply_num = 1

                else:  # branched unit

                    # last_bl_ver : None case
                    """
                    recent_bl = block.objects.filter(user_id=unit_info['username'], project_name=unit_info['project_name'],
                                                     session_name=unit_info['session_name'], session_ver=int(unit_info['session_ver']),
                                                     block_iden=j.parent_block_iden,
                                                     block_ver__lte=int(j.parent_block_ver), is_save=True, creatation_date__lte = standard_date).aggregate(
                        Max('block_ver'))
                    """
                    recent_bl = block.objects.filter(user_id=unit_info['username'],
                                                     project_name=unit_info['project_name'],
                                                     session_name=unit_info['session_name'],
                                                     session_ver=int(unit_info['session_ver']),
                                                     block_iden=j.parent_block_iden,
                                                     block_ver__lte=int(j.parent_block_ver), is_save=True,).aggregate(
                        Max('block_ver'))
                    last_bl_ver = recent_bl['block_ver__max']
                    new_bl_list = []
                    if last_bl_ver != None:  # branched unit after save
                        """
                        ran_logs = log_history.objects.filter(scope="unit", user_id=unit_info['username'],
                                                              project_name=unit_info['project_name'],
                                                              session_name=unit_info['session_name'],
                                                              session_ver=int(unit_info['session_ver']),
                                                              block_iden=j.block_iden, block_ver__range=(
                                last_bl_ver + 1, int(j.parent_block_ver)), is_event=False, is_closed = False, creatation_date__lte = standard_date).values('action_id',
                                                                                                  'action',
                                                                                                  'scope',
                                                                                                  'user_id',
                                                                                                  'project_name',
                                                                                                  'session_name',
                                                                                                  'session_ver',
                                                                                                  'block_iden',
                                                                                                  'block_name',
                                                                                                  'block_ver',
                                                                                                  'clusterType',
                                                                                                  'clusterParam',
                                                                                                  'colors',
                                                                                                  'data',
                                                                                                  'data_name',
                                                                                                  'data_annotation',
                                                                                                  'position_top',
                                                                                                  'position_left',
                                                                                                  'position_width',
                                                                                                  'position_height',
                                                                                                  'is_closed',
                                                                                                  'creatation_date',
                                                                                                  'parent_block_iden',
                                                                                                  'parent_block_ver',
                                                                                                  'save_ver',
                                                                                                  'is_save').order_by(
                            "creatation_date")
                        """
                        ran_logs = log_history.objects.filter(scope="unit", user_id=unit_info['username'],
                                                              project_name=unit_info['project_name'],
                                                              session_name=unit_info['session_name'],
                                                              session_ver=int(unit_info['session_ver']),
                                                              block_iden=j.block_iden, block_ver__range=(
                                last_bl_ver + 1, int(j.parent_block_ver)), is_event=False, is_closed=False,).values('action_id',
                                                                                                         'action',
                                                                                                         'scope',
                                                                                                         'user_id',
                                                                                                         'project_name',
                                                                                                         'session_name',
                                                                                                         'session_ver',
                                                                                                         'block_iden',
                                                                                                         'block_name',
                                                                                                         'block_ver',
                                                                                                         'clusterType',
                                                                                                         'clusterParam',
                                                                                                         'colors',
                                                                                                         'data',
                                                                                                         'data_name',
                                                                                                         'data_annotation',
                                                                                                         'position_top',
                                                                                                         'position_left',
                                                                                                         'position_width',
                                                                                                         'position_height',
                                                                                                         'is_closed',
                                                                                                         'creatation_date',
                                                                                                         'parent_block_iden',
                                                                                                         'parent_block_ver',
                                                                                                         'save_ver',
                                                                                                         'is_save').order_by(
                            "creatation_date")
                        for k in ran_logs:
                            new_bl_list.append(k)
                        logs.extend(new_bl_list)
                        u_apply_num = int(j.parent_block_ver) - last_bl_ver + 1
                    else:  # branched unit, not after save
                        """
                        ran_logs = log_history.objects.filter(scope="unit", user_id=unit_info['username'], project_name=unit_info['project_name'],
                                                              session_name=unit_info['session_name'], session_ver=int(unit_info['session_ver']),
                                                              block_iden=j.block_iden,
                                                              block_ver__range=(0, int(j.parent_block_ver)),
                                                              is_event=False, is_closed = False, creatation_date__lte = standard_date).values('action_id', 'action', 'scope',
                                                                                     'user_id', 'project_name',
                                                                                     'session_name', 'session_ver',
                                                                                     'block_iden', 'block_name',
                                                                                     'block_ver', 'clusterType',
                                                                                     'clusterParam', 'colors', 'data',
                                                                                     'data_name', 'data_annotation',
                                                                                     'position_top', 'position_left',
                                                                                     'position_width',
                                                                                     'position_height', 'is_closed',
                                                                                     'creatation_date',
                                                                                     'parent_block_iden',
                                                                                     'parent_block_ver', 'save_ver',
                                                                                     'is_save').order_by(
                            "creatation_date")
                        """
                        ran_logs = log_history.objects.filter(scope="unit", user_id=unit_info['username'],
                                                              project_name=unit_info['project_name'],
                                                              session_name=unit_info['session_name'],
                                                              session_ver=int(unit_info['session_ver']),
                                                              block_iden=j.block_iden,
                                                              block_ver__range=(0, int(j.parent_block_ver)),
                                                              is_event=False, is_closed=False).values('action_id',
                                                                                                         'action',
                                                                                                         'scope',
                                                                                                         'user_id',
                                                                                                         'project_name',
                                                                                                         'session_name',
                                                                                                         'session_ver',
                                                                                                         'block_iden',
                                                                                                         'block_name',
                                                                                                         'block_ver',
                                                                                                         'clusterType',
                                                                                                         'clusterParam',
                                                                                                         'colors',
                                                                                                         'data',
                                                                                                         'data_name',
                                                                                                         'data_annotation',
                                                                                                         'position_top',
                                                                                                         'position_left',
                                                                                                         'position_width',
                                                                                                         'position_height',
                                                                                                         'is_closed',
                                                                                                         'creatation_date',
                                                                                                         'parent_block_iden',
                                                                                                         'parent_block_ver',
                                                                                                         'save_ver',
                                                                                                         'is_save').order_by(
                            "creatation_date")
                        for k in ran_logs:
                            new_bl_list.append(k)
                        logs.extend(new_bl_list)
                        u_apply_num = int(j.parent_block_ver) + 1
                    """
                    bs_logs = log_history.objects.filter(scope="unit", user_id=unit_info['username'], project_name=unit_info['project_name'],
                                                         session_name=unit_info['session_name'], session_ver=int(unit_info['session_ver']),
                                                         block_iden=j.block_iden, block_ver=j.block_ver,
                                                         is_event=False, is_closed = False, creatation_date__lte = standard_date).values('action_id', 'action', 'scope',
                                                                                'user_id', 'project_name',
                                                                                'session_name', 'session_ver',
                                                                                'block_iden', 'block_name', 'block_ver',
                                                                                'clusterType', 'clusterParam', 'colors',
                                                                                'data', 'data_name', 'data_annotation',
                                                                                'position_top', 'position_left',
                                                                                'position_width', 'position_height',
                                                                                'is_closed', 'creatation_date',
                                                                                'parent_block_iden', 'parent_block_ver',
                                                                                'save_ver', 'is_save').order_by(
                        "creatation_date")
                    """
                    bs_logs = log_history.objects.filter(scope="unit", user_id=unit_info['username'],
                                                         project_name=unit_info['project_name'],
                                                         session_name=unit_info['session_name'],
                                                         session_ver=int(unit_info['session_ver']),
                                                         block_iden=j.block_iden, block_ver=j.block_ver,
                                                         is_event=False, is_closed=False).values('action_id',
                                                                                                    'action', 'scope',
                                                                                                    'user_id',
                                                                                                    'project_name',
                                                                                                    'session_name',
                                                                                                    'session_ver',
                                                                                                    'block_iden',
                                                                                                    'block_name',
                                                                                                    'block_ver',
                                                                                                    'clusterType',
                                                                                                    'clusterParam',
                                                                                                    'colors',
                                                                                                    'data', 'data_name',
                                                                                                    'data_annotation',
                                                                                                    'position_top',
                                                                                                    'position_left',
                                                                                                    'position_width',
                                                                                                    'position_height',
                                                                                                    'is_closed',
                                                                                                    'creatation_date',
                                                                                                    'parent_block_iden',
                                                                                                    'parent_block_ver',
                                                                                                    'save_ver',
                                                                                                    'is_save').order_by(
                        "creatation_date")
                    for k in bs_logs:
                        new_bl_list.append(k)
                    logs.extend(new_bl_list)

            else:  # saved unit after applied
                """
                ran_logs = log_history.objects.filter(scope="unit", user_id=unit_info['username'], project_name=unit_info['project_name'],
                                                      session_name=unit_info['session_name'], session_ver=int(unit_info['session_ver']),
                                                      block_iden=j.block_iden, block_ver__range=(-1, int(j.block_ver)),
                                                      is_event=False, is_closed = False, creatation_date__lte = standard_date).values('action_id', 'action', 'scope', 'user_id',
                                                                             'project_name', 'session_name',
                                                                             'session_ver', 'block_iden', 'block_name',
                                                                             'block_ver', 'clusterType', 'clusterParam',
                                                                             'colors', 'data', 'data_name',
                                                                             'data_annotation', 'position_top',
                                                                             'position_left', 'position_width',
                                                                             'position_height', 'is_closed',
                                                                             'creatation_date', 'parent_block_iden',
                                                                             'parent_block_ver', 'save_ver',
                                                                             'is_save').order_by("creatation_date")
                """
                ran_logs = log_history.objects.filter(scope="unit", user_id=unit_info['username'],
                                                      project_name=unit_info['project_name'],
                                                      session_name=unit_info['session_name'],
                                                      session_ver=int(unit_info['session_ver']),
                                                      block_iden=j.block_iden, block_ver__range=(-1, int(j.block_ver)),
                                                      is_event=False, is_closed=False).values('action_id', 'action',
                                                                                                 'scope', 'user_id',
                                                                                                 'project_name',
                                                                                                 'session_name',
                                                                                                 'session_ver',
                                                                                                 'block_iden',
                                                                                                 'block_name',
                                                                                                 'block_ver',
                                                                                                 'clusterType',
                                                                                                 'clusterParam',
                                                                                                 'colors', 'data',
                                                                                                 'data_name',
                                                                                                 'data_annotation',
                                                                                                 'position_top',
                                                                                                 'position_left',
                                                                                                 'position_width',
                                                                                                 'position_height',
                                                                                                 'is_closed',
                                                                                                 'creatation_date',
                                                                                                 'parent_block_iden',
                                                                                                 'parent_block_ver',
                                                                                                 'save_ver',
                                                                                                 'is_save').order_by(
                    "creatation_date")
                new_bl_list = []
                for k in ran_logs:
                    new_bl_list.append(k)
                logs.extend(new_bl_list)
                u_apply_num = int(j.block_ver)

        action_num = len(logs)
        annotation_num = 0
        total_action += action_num
        total_apply_num += u_apply_num
        action_list = []
        anno_path = ""
        for i in logs:
            action_elem = {}
            action_elem['action'] = i['action']
            action_elem['action_id'] = i['action_id']
            parameter = {}
            position = {}
            if list_checker(i['action'], action_check_list,
                            [0, 1, 2, 3, 4, 5, 6, 7, 14, 15, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 36]):
                parameter['block_iden'] = i['block_iden']
                parameter['block_name'] = i['block_name']
                parameter['block_ver'] = i['block_ver']
                parameter['save_ver'] = i['save_ver']
                if list_checker(i['action'], action_check_list, [4]):
                    parameter['data_name'] = i['data_name']
                elif list_checker(i['action'], action_check_list, [5]):
                    parameter['clusterType'] = i['clusterType']
                elif list_checker(i['action'], action_check_list, [6]):
                    parameter['clusterParam'] = i['clusterParam']
                elif list_checker(i['action'], action_check_list, [7]):
                    position['position_top'] = i['position_top']
                    position['position_left'] = i['position_left']
                    position['position_width'] = i['position_width']
                    position['position_height'] = i['position_height']
                    parameter['position'] = position
                elif list_checker(i['action'], action_check_list, [14]):
                    parameter['data_annotation'] = i['data_annotation']
                elif list_checker(i['action'], action_check_list, [15]):
                    parameter['block_annotation'] = i['block_annotation']
                elif list_checker(i['action'], action_check_list, [19]):
                    parameter['parent_block_iden'] = i['parent_block_iden']
                    parameter['parent_block_ver'] = i['parent_block_ver']
                elif list_checker(i['action'], action_check_list, [21]):
                    parameter['color_type'] = i['colors']
                    if list_checker(i['action'], action_check_list, [27]):
                        # get pcp_id
                        pcp_bl = block.objects.filter(user_id=i['user_id'], project_name=i['project_name'],
                                                      session_name=i['session_name'],
                                                      session_ver=int(i['session_ver']),
                                                      block_iden=i['block_iden'], block_ver=int(i['block_ver']))
                        pcp_obj = pcp.objects.filter(pcp_id=pcp_bl[0].pcp_id)
                        parameter['column_order'] = pcp_obj[0].column_order
                    elif list_checker(i['action'], action_check_list, [28]):
                        # get pcp_id
                        pcp_bl = block.objects.filter(user_id=i['user_id'], project_name=i['project_name'],
                                                      session_name=i['session_name'],
                                                      session_ver=int(i['session_ver']),
                                                      block_iden=i['block_iden'], block_ver=int(i['block_ver']))
                        pcp_obj = pcp.objects.filter(pcp_id=pcp_bl[0].pcp_id)
                        parameter['selected_index'] = pcp_obj[0].selected_index
                        parameter['brushed_axis'] = pcp_obj[0].brushed_axis
                        parameter['brushed_range'] = pcp_obj[0].brushed_range
                    elif list_checker(i['action'], action_check_list, [29]):
                        # get scm_id
                        scm_bl = block.objects.filter(user_id=i['user_id'], project_name=i['project_name'],
                                                      session_name=i['session_name'],
                                                      session_ver=int(i['session_ver']),
                                                      block_iden=i['block_iden'], block_ver=int(i['block_ver']))
                        scm_obj = scm.objects.filter(scm_id=scm_bl[0].scm_id)
                        parameter['selected_index'] = scm_obj[0].selected_index
                        parameter['brushed_axis'] = scm_obj[0].brushed_axis
                        parameter['brushed_range'] = scm_obj[0].brushed_range
                    elif list_checker(i['action'], action_check_list, [30]):
                        # get scm_id
                        sp_bl = block.objects.filter(user_id=i['user_id'], project_name=i['project_name'],
                                                     session_name=i['session_name'],
                                                     session_ver=int(i['session_ver']),
                                                     block_iden=i['block_iden'], block_ver=int(i['block_ver']))
                        sp_obj = sp.objects.filter(sp_id=sp_bl[0].sp_id)
                        parameter['brushed_range'] = sp_obj[0].brushed_range
            action_elem['parameter'] = parameter
            action_elem['date'] = i['creatation_date'].strftime("%Y-%m-%d %H:%M:%S")
            action_list.append(action_elem)
            get_anno_num = block_annotation_history.objects.all().filter(user_id=j.user_id, project_name=j.project_name,
                                                                         session_name=j.session_name,
                                                                         session_ver=int(j.session_ver),
                                                                         block_iden=j.block_iden, block_ver=0,
                                                                         is_removed=False).aggregate(
                Max('annotation_num'))
            max_anno_num = get_anno_num['annotation_num__max']
            if max_anno_num is not None:  # null
                annotation_num = max_anno_num + 1
            else:
                annotation_num = 0
            total_anno_num += annotation_num
        if j.save_ver == 0:  # first save
            if j.is_first == True:  # Not branched
                #print(1)
                #print(unit_info['session_name'] + "-" + str(unit_info['session_ver']) + " : " + j.block_iden + "-" + str(j.block_ver))
                anno_path = os.path.join('static', 'member', str(unit_info['username']), str(unit_info['project_name']), str(unit_info['session_name']),
                                         str(unit_info['session_ver']), str(j.block_iden), "annotation.json")
                tree_info.append(
                    [unit_info['session_name'] + "-" + str(unit_info['session_ver']), j.block_iden + "-" + str(j.block_ver), j.block_ver,
                     j.block_name, j.last_date, action_num, annotation_num, u_apply_num, anno_path, action_list,
                     j.save_ver, j.is_broken, j.vis_types, j.is_graph])
            else:  # bracned
                recent_bl = block.objects.filter(user_id=unit_info['username'], project_name=unit_info['project_name'], session_name=unit_info['session_name'],
                                                 session_ver=int(unit_info['session_ver']), block_iden=j.parent_block_iden,
                                                 block_ver__lte=int(j.parent_block_ver), is_save=True).aggregate(
                    Max('block_ver'))
                last_bl_ver = recent_bl['block_ver__max']
                if last_bl_ver == None:  # Not saved in previous unit
                    #print(2)
                    #print(str(j.parent_block_iden) + "-" + str(j.parent_block_ver) + " : " +j.block_iden + "-" + str(j.block_ver))
                    tree_info.append([str(j.parent_block_iden) + "-" + str(j.parent_block_ver),
                                      j.block_iden + "-" + str(j.block_ver), j.block_ver, j.block_name, j.last_date,
                                      action_num, annotation_num, u_apply_num, anno_path, action_list, j.save_ver,
                                      j.is_broken, j.vis_types, j.is_graph])
                else:  # Saved in previous block
                    #print(3)
                    #print(str(j.parent_block_iden) + "-" + str(last_bl_ver) + " : " + j.block_iden + "-" + str(j.block_ver))
                    tree_info.append(
                        [str(j.parent_block_iden) + "-" + str(last_bl_ver), j.block_iden + "-" + str(j.block_ver),
                         j.block_ver, j.block_name, j.last_date, action_num, annotation_num, u_apply_num, anno_path,
                         action_list, j.save_ver, j.is_broken, j.vis_types, j.is_graph])
                anno_path = os.path.join('static', 'member', str(unit_info['username']), str(unit_info['project_name']), str(unit_info['session_name']),
                                         str(unit_info['session_ver']), str(j.block_iden), "annotation.json")
        else:  # exist previous save
            #print(4)
            if j.block_iden in pre_id_list:
                #print(j.block_iden + "-" + str(int(pre_ver_list[pre_id_list.index(j.block_iden)])) + " : " +j.block_iden + "-" + str(j.block_ver))
                tree_info.append([j.block_iden + "-" + str(int(pre_ver_list[pre_id_list.index(j.block_iden)])),
                                  j.block_iden + "-" + str(j.block_ver), int(j.block_ver), j.block_name, j.last_date,
                                  action_num, annotation_num, u_apply_num, anno_path, action_list, j.save_ver,
                                  j.is_broken, j.vis_types, j.is_graph])
                anno_path = os.path.join('static', 'member', str(unit_info['username']), str(unit_info['project_name']), str(unit_info['session_name']),
                                         str(unit_info['session_ver']), str(j.block_iden), "annotation.json")
        ids.append(j.block_iden + "-" + str(j.block_ver))
        anno_values.append(annotation_num)
        apply_values.append(u_apply_num)
        action_values.append(len(logs))

        if j.block_iden in pre_id_list:
            pre_ver_list[pre_id_list.index(j.block_iden)] = j.block_ver
        else:
            pre_id_list.append(j.block_iden)
            pre_ver_list.append(j.block_ver)

    info_set = {}
    info_set['action_values'] = action_values
    info_set['apply_values'] = apply_values
    info_set['anno_values'] = anno_values
    info_set['ids'] = ids
    name_to_node = {}
    root = {'id': unit_info['session_name'] + "-" + str(unit_info['session_ver']), 'name': unit_info['session_name'], 'children': [], 'ver': unit_info['session_ver'],
            'last_date': None, 'parent': None, 'action_num': 0, 'total_action_num': total_action, 'anno_num': 0,
            'total_anno_num': total_anno_num, 'apply_num': 0, 'total_apply_num': total_apply_num, 'anno_path': None,
            'action_list': None, 'save_ver': None, "vis_type":None}
    for parent, child, ver, name, last_date, action_num, anno_num, u_apply_num, anno_path, action_list, u_save_ver, is_broken, vis_type, is_graph in tree_info:
        parent_node = name_to_node.get(parent)
        if not parent_node:
            parent_node = root
        name_to_node[child] = child_node = {'id': child, 'name': name, 'ver': ver,
                                            'last_date': last_date.strftime("%Y-%m-%d %H:%M:%S"), 'parent': parent,
                                            'action_num': action_num, 'total_action_num': 0, 'anno_num': anno_num,
                                            'total_anno_num': 0, 'apply_num': u_apply_num, 'total_apply_num': 0,
                                            'anno_path': anno_path, 'action_list': action_list, 'save_ver': u_save_ver,
                                            'is_broken': is_broken, "vis_type":vis_type, "is_graph" : is_graph}
        parent_node.setdefault('children', []).append(child_node)
    count_values(root, False, info_set)
    erase_hypon(root, False, info_set)
    return HttpResponse(json.dumps({'success': True, 'detail': "Action History.", 'output': root}),
                        content_type="application/json")

@ensure_csrf_cookie
def from_to_session(request):
    errors = []
    username = ""
    session_list = ""
    if request.method == 'POST':
        param_list = ['username', 'project_name', 'session_list']
        errors = param_checker(request, errors, param_list)
        if not errors:
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            session_list = json.loads(request.POST.get('session_list'))
            query_list = []
            for i in session_list:
                query_list.append(Q(user_id=username, project_name=project_name, session_name=i['session_name'], session_ver=None,is_event=False, is_closed = False))
                query_list.append(Q(user_id = username, project_name = project_name, session_name = i['session_name'], session_ver = i['session_ver'], is_event=False, is_closed = False))
            bls = log_history.objects.filter(reduce(operator.or_, query_list)).values('action_id', 'action', 'scope', 'user_id','project_name', 'session_name', 'session_ver', 'block_iden', 'block_name', 'block_ver',  'clusterType', 'clusterParam', 'colors', 'data', 'data_name', 'data_annotation', 'position_top', 'position_left', 'position_width', 'position_height', 'is_closed', 'creatation_date', 'parent_block_iden', 'parent_block_ver', 'save_ver', 'is_save', 'is_undo', 'selected_index', 'anno_id').order_by('creatation_date')
            bls = sorted(bls, key=lambda o: o['creatation_date'])
            output_list = []
            for i in bls:
                output_elem = {}
                output_elem['scope'] = i['scope']
                output_elem['action'] = i['action']
                output_elem['action_id'] = i['action_id']
                parameter = {}
                position = {}
                if list_checker(i['action'], action_check_list, [0, 1, 2, 3, 17, 22, 27, 28, 29, 36]):
                    parameter['block_iden'] = i['block_iden']
                    parameter['block_name'] = i['block_name']
                    parameter['block_ver'] = i['block_ver']
                    if list_checker(i['action'], action_check_list, [27]):
                        # get pcp_id
                        pcp_bl = log_history.objects.filter(action_id = i['action_id'])
                        pcp_obj = pcp.objects.filter(pcp_id = pcp_bl[0].pcp_id)
                        parameter['column_order'] = pcp_obj[0].column_order
                    elif list_checker(i['action'], action_check_list, [28]):
                        # get pcp_id
                        pcp_bl = log_history.objects.filter(action_id=i['action_id'])
                        pcp_obj = pcp.objects.filter(pcp_id=pcp_bl[0].pcp_id)
                        parameter['selected_index'] = pcp_obj[0].selected_index
                        parameter['brushed_axis'] = pcp_obj[0].brushed_axis
                        parameter['brushed_range'] = pcp_obj[0].brushed_range
                    elif list_checker(i['action'], action_check_list, [29]):
                        # get scm_id
                        scm_bl = log_history.objects.filter(action_id=i['action_id'])
                        scm_obj = scm.objects.filter(scm_id=scm_bl[0].scm_id)
                        parameter['selected_index'] = scm_obj[0].selected_index
                        parameter['brushed_axis'] = scm_obj[0].brushed_axis
                        parameter['brushed_range'] = scm_obj[0].brushed_range
                    elif list_checker(i['action'], action_check_list, [30]):
                        # get sp_id
                        sp_bl = log_history.objects.filter(action_id=i['action_id'])
                        sp_obj = sp.objects.filter(sp_id=sp_bl[0].sp_id)
                        parameter['brushed_range'] = sp_obj[0].brushed_range
                    elif list_checker(i['action'], action_check_list, [22]):
                        bl_anno = block_annotation_history.objects.filter(annotation_id = i['anno_id'])
                        parameter['answer'] = bl_anno[0].data_annotation
                        parameter['confidence_level'] = bl_anno[0].research_annotation
                elif list_checker(i['action'], action_check_list, [4]):
                    parameter['data'] = i['data']
                    parameter['data_name'] = i['data_name']
                elif list_checker(i['action'], action_check_list, [5]):
                    parameter['clusterType'] = i['clusterType']
                elif list_checker(i['action'], action_check_list, [6]):
                    parameter['clusterParam'] = i['clusterParam']
                elif list_checker(i['action'], action_check_list, [7]):
                    parameter['top'] = i['position_top']
                    parameter['left'] = i['position_left']
                    parameter['width'] = i['position_width']
                    parameter['height'] = i['position_height']
                elif list_checker(i['action'], action_check_list, [8, 9, 10, 11, 18]):
                    parameter['username'] = username
                    parameter['project_name'] = i['project_name']
                    parameter['session_name'] = i['session_name']
                    parameter['session_ver'] = i['session_ver']
                elif list_checker(i['action'], action_check_list, [12]):
                    parameter['project_name'] = i['project_name']
                    parameter['project_annotation'] = i['project_annotation']
                elif list_checker(i['action'], action_check_list, [13]):
                    parameter['project_name'] = i['project_name']
                elif list_checker(i['action'], action_check_list, [14]):
                    parameter['data_annotation'] = i['data_annotation']
                elif list_checker(i['action'], action_check_list, [15]):
                    parameter['block_annotation'] = i['block_annotation']
                elif list_checker(i['action'], action_check_list, [16]):
                    parameter['session_annotation'] = i['session_annotation']
                elif list_checker(i['action'], action_check_list, [19]):
                    parameter['block_iden'] = i['block_iden']
                    parameter['block_name'] = i['block_name']
                    parameter['block_ver'] = i['block_ver']
                    parameter['parent_block_iden'] = i['parent_block_iden']
                    parameter['parent_block_ver'] = i['parent_block_ver']
                elif list_checker(i['action'], action_check_list, [21]):
                    parameter['color_type'] = i['colors']
                elif list_checker(i['action'], action_check_list, [37, 38, 39]):
                    parameter['project_name'] = i['project_name']
                elif list_checker(i['action'], action_check_list, [42, 43]):
                    parameter['project_name'] = i['project_name']
                    parameter['session_name'] = i['session_name']
                    parameter['block_iden'] = i['block_iden']
                elif list_checker(i['action'], action_check_list, [31]):
                    parameter['block_iden'] = i['block_iden']
                    parameter['selected_index'] = i['selected_index']
                elif list_checker(i['action'], action_check_list, [32]):
                    parameter['block_iden'] = i['block_iden']
                    parameter['selected_index'] = i['selected_index']

                output_elem['parameter'] = parameter
                output_elem['date'] = i['creatation_date'].strftime("%Y-%m-%d %H:%M:%S")
                output_elem['is_undo'] = i['is_undo']
                output_list.append(output_elem)

            return HttpResponse(json.dumps({'success' : True, 'detail' : "From to session.", 'output' : output_list}) ,content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

@ensure_csrf_cookie
def from_to_unit(request):
    errors = []
    username = ""
    session_list = ""
    if request.method == 'POST':
        param_list = ['username', 'project_name', 'session_name', 'session_ver', 'block_list']
        errors = param_checker(request, errors, param_list)
        if not errors:
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            block_list = json.loads(request.POST.get('block_list'))
            query_list = []
            for i in block_list:
                query_list.append(Q(user_id = username, project_name = project_name, session_name = session_name, session_ver = session_ver, block_iden = i['block_iden'], block_ver = i['block_ver'], scope='unit', is_event=False, is_closed = False))
            bls = log_history.objects.filter(reduce(operator.or_, query_list)).values('action_id', 'action', 'scope', 'user_id', 'project_name', 'session_name', 'session_ver', 'block_iden', 'block_name', 'block_ver',  'clusterType', 'clusterParam', 'colors', 'data', 'data_name', 'data_annotation', 'position_top', 'position_left', 'position_width', 'position_height', 'is_closed', 'creatation_date', 'parent_block_iden', 'parent_block_ver', 'is_undo', 'selected_index', 'anno_id').order_by('creatation_date')
            output_list = []
            for i in bls:
                output_elem = {}
                output_elem['scope'] = i['scope']
                output_elem['action'] = i['action']
                output_elem['action_id'] = i['action_id']
                parameter = {}
                position = {}
                if list_checker(i['action'], action_check_list, [0, 1, 2, 3, 17, 22, 27, 28, 29, 30, 36, 40, 41]):
                    parameter['block_iden'] = i['block_iden']
                    parameter['block_name'] = i['block_name']
                    parameter['block_ver'] = i['block_ver']
                    if list_checker(i['action'], action_check_list, [27]):
                        # get pcp_id
                        pcp_bl = log_history.objects.filter(action_id=i['action_id'])
                        pcp_obj = pcp.objects.filter(pcp_id = pcp_bl[0].pcp_id)
                        parameter['column_order'] = pcp_obj[0].column_order
                    elif list_checker(i['action'], action_check_list, [28]):
                        # get pcp_id
                        pcp_bl = log_history.objects.filter(action_id=i['action_id'])
                        pcp_obj = pcp.objects.filter(pcp_id=pcp_bl[0].pcp_id)
                        parameter['selected_index'] = pcp_obj[0].selected_index
                        parameter['brushed_axis'] = pcp_obj[0].brushed_axis
                        parameter['brushed_range'] = pcp_obj[0].brushed_range
                    elif list_checker(i['action'], action_check_list, [29]):
                        # get scm_id
                        scm_bl = log_history.objects.filter(action_id=i['action_id'])
                        scm_obj = scm.objects.filter(scm_id=scm_bl[0].scm_id)
                        parameter['selected_index'] = scm_obj[0].selected_index
                        parameter['brushed_axis'] = scm_obj[0].brushed_axis
                        parameter['brushed_range'] = scm_obj[0].brushed_range
                    elif list_checker(i['action'], action_check_list, [30]):
                        # get sp_id
                        sp_bl = log_history.objects.filter(action_id=i['action_id'])
                        sp_obj = sp.objects.filter(sp_id=sp_bl[0].sp_id)
                        parameter['x_axis'] = sp_obj[0].x_axis
                        parameter['y_axis'] = sp_obj[0].y_axis
                        parameter['brushed_range'] = sp_obj[0].brushed_range
                    elif list_checker(i['action'], action_check_list, [22]):
                        bl_anno = block_annotation_history.objects.filter(annotation_id = i['anno_id'])
                        if len(bl_anno) != 0:
                            parameter['answer'] = bl_anno[0].data_annotation
                            parameter['confidence_level'] = bl_anno[0].research_annotation
                elif list_checker(i['action'], action_check_list, [31]):
                    parameter['block_iden'] = i['block_iden']
                    parameter['selected_index'] = i['selected_index']
                elif list_checker(i['action'], action_check_list, [32]):
                    parameter['block_iden'] = i['block_iden']
                    parameter['selected_index'] = i['selected_index']
                elif list_checker(i['action'], action_check_list, [4]):
                    parameter['data'] = i['data']
                    parameter['data_name'] = i['data_name']
                elif list_checker(i['action'], action_check_list, [5]):
                    parameter['clusterType'] = i['clusterType']
                elif list_checker(i['action'], action_check_list, [6]):
                    parameter['clusterParam'] = i['clusterParam']
                elif list_checker(i['action'], action_check_list, [7]):
                    #position['position_top'] = i['position_top']
                    #position['position_left'] = i['position_left']
                    #position['position_width'] = i['position_width']
                    #position['position_height'] = i['position_height']
                    #parameter['position'] = position
                    parameter['top'] = i['position_top']
                    parameter['left'] = i['position_left']
                    parameter['width'] = i['position_width']
                    parameter['height'] = i['position_height']
                #elif list_checker(i['action'], action_check_list, [8, 9, 10, 11, 18]):
                  #  parameter['username'] = username
                  #  parameter['project_name'] = i['project_name']
                   # parameter['session_name'] = i['session_name']
                   # parameter['session_ver'] = i['session_ver']
                elif list_checker(i['action'], action_check_list, [12]):
                    parameter['project_name'] = i['project_name']
                    parameter['project_annotation'] = i['project_annotation']
                elif list_checker(i['action'], action_check_list, [13]):
                    parameter['project_name'] = i['project_name']
                elif list_checker(i['action'], action_check_list, [14]):
                    parameter['data_annotation'] = i['data_annotation']
                elif list_checker(i['action'], action_check_list, [15]):
                    parameter['block_annotation'] = i['block_annotation']
                elif list_checker(i['action'], action_check_list, [16]):
                    parameter['session_annotation'] = i['session_annotation']
                elif list_checker(i['action'], action_check_list, [19]):
                    parameter['block_iden'] = i['block_iden']
                    parameter['block_name'] = i['block_name']
                    parameter['block_ver'] = i['block_ver']
                    parameter['parent_block_iden'] = i['parent_block_iden']
                    parameter['parent_block_ver'] = i['parent_block_ver']
                elif list_checker(i['action'], action_check_list, [21]):
                    parameter['color_type'] = i['colors']
                elif list_checker(i['action'], action_check_list, [37, 38, 39]):
                    parameter['project_name'] = i['project_name']
                elif list_checker(i['action'], action_check_list, [42, 43]):
                    parameter['project_name'] = i['project_name']
                    parameter['session_name'] = i['session_name']
                    parameter['block_iden'] = i['block_iden']
                output_elem['parameter'] = parameter
                output_elem['date'] = i['creatation_date'].strftime("%Y-%m-%d %H:%M:%S")
                output_elem['is_undo'] = i['is_undo']
                output_list.append(output_elem)

            return HttpResponse(json.dumps({'success' : True, 'detail' : "From to unit.", 'output' : output_list}) ,content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

@ensure_csrf_cookie
def action_move(request):
    errors = []
    if request.method == 'POST':
        # check necessary information
        param_list = ['username', 'project_name', 'session_name', 'session_ver', 'block_iden', 'block_ver', 'action_list']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get necessary information
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            block_iden = '%r' % request.POST['block_iden']
            block_iden = block_iden.replace('\'', '')
            block_ver = '%r' % request.POST['block_ver']
            block_ver = block_ver.replace('\'', '')
            action_list = request.POST.get('action_list')
            action_list = eval(json.loads(json.dumps(action_list)))
            depen_list = ['Change-Data-Annotation', 'Change-Unit-Annotation', 'Change-Unit-Name',
                          'Locate-Unit', 'Change-Color', 'Change-Data',
                          'Change-Cluster-Type', 'Change-Cluster-Parameter']

            add_bl = []
            for i in action_list:
                ori_lho = log_history.objects.get(action_id = i['action_id'])
                ori_bl = block.objects.filter(user_id = ori_lho.user_id, project_name = ori_lho.project_name,
                                              session_name = ori_lho.session_name, session_ver = int(ori_lho.session_ver),
                                              block_iden = ori_lho.block_iden, block_ver = int(ori_lho.block_ver))
                new_lho = ori_lho
                new_lho.action_id = None
                new_lho.save()
                new_lho = log_history.objects.filter(action_id = new_lho.action_id)
                new_lho.update(block_iden = block_iden, block_ver = block_ver, creatation_date = datetime.datetime.now())
                move_bl = block.objects.filter(user_id = username, project_name = project_name,
                                                session_name = session_name, session_ver = int(session_ver),
                                                block_iden = block_iden, block_ver = int(block_ver))
                if list_checker(ori_lho.action, depen_list, [2]):
                    move_bl.update(block_name = ori_bl[0].block_name)
                elif list_checker(ori_lho.action, depen_list, [4]):
                    move_bl.update(colors = ori_bl[0].colors)
                elif list_checker(ori_lho.action, depen_list, [5]):
                    move_bl.update(data = ori_bl[0].data)
                elif list_checker(ori_lho.action, depen_list, [6]):
                    move_bl.update(clusterType = ori_bl[0].clusterType)
                elif list_checker(ori_lho.action, depen_list, [7]):
                    move_bl.update(clusterParam = ori_bl[0].clusterParam)
                move_bl.update(data = ori_bl[0].data)
                add_bl = move_bl

            request_json = []
            rj_elem = {}
            bl_info = {}
            rj_elem['username'] = bl_info['username'] = add_bl[0].user_id
            rj_elem['project_name'] = bl_info['project_name'] = add_bl[0].project_name
            rj_elem['session_name'] = bl_info['session_name'] = add_bl[0].session_name
            rj_elem['session_ver'] = bl_info['session_ver'] = int(add_bl[0].session_ver)
            rj_elem['block_iden'] = bl_info['block_iden'] = add_bl[0].block_iden
            rj_elem['block_name'] = add_bl[0].block_name
            rj_elem['block_ver'] = bl_info['block_ver'] = int(add_bl[0].block_ver)
            rj_elem['parent_block_iden'] = add_bl[0].parent_block_iden
            rj_elem['parent_block_ver'] = int(add_bl[0].parent_block_ver)
            rj_elem['cluster_type'] =  bl_info['cluster_type'] = add_bl[0].clusterType
            rj_elem['cluster_param'] = bl_info['cluster_param'] = add_bl[0].clusterParam
            rj_elem['color_type'] = bl_info['color_type'] = add_bl[0].colors
            rj_elem['data'] = bl_info['data'] = add_bl[0].data
            rj_elem['data_annotation'] = add_bl[0].data_annotation
            rj_elem['data_name'] = add_bl[0].data_name
            request_json.append(rj_elem)
            position_json = []
            position = {}
            position['top'] = add_bl[0].position_top
            position['left'] = add_bl[0].position_left
            position['height'] = add_bl[0].position_height
            position['width'] = add_bl[0].position_width
            position_json.append(position)

            bl_info['request_json'] = request_json
            bl_info['position_json'] = position
            bl_info['is_cluster'] = False
            bl_info['vis_types'] = add_bl[0].vis_types
            data_type = rj_elem['data_name'][rj_elem['data_name'].find(".") + 1:rj_elem['data_name'].find(" (")]
            bl_info['data_type'] = data_type
            bl_info['vis_types'] = add_bl[0].vis_types
            if bl_info['vis_types'] == "Heatmap":
                bl_info['cluster_type'] = add_bl[0].clusterType
                bl_info['cluster_param'] = add_bl[0].clusterParam
                bl_info['color_type'] = add_bl[0].colors
            elif bl_info['vis_types'] == "Parallel Coordinate Plot":
                pcp_bl = block.objects.filter(user_id = username, project_name = project_name,
                                              session_name = session_name, session_ver = int(session_ver),
                                              block_iden = block_iden, block_ver = int(block_ver))
                pcp_obj = pcp.objects.filter(pcp_id = pcp_bl[0].pcp_id)
                bl_info['column_order'] = pcp_obj[0].column_order
                bl_info['selected_index'] = pcp_obj[0].selected_index
                bl_info['brushed_axis'] = pcp_obj[0].brushed_axis
                bl_info['brushed_range'] = pcp_obj[0].brushed_range
            elif bl_info['vis_types'] == "Scatterplot Matrix":
                scm_bl = block.objects.filter(user_id=username, project_name=project_name,
                                              session_name=session_name, session_ver=int(session_ver),
                                              block_iden=block_iden, block_ver=int(block_ver))
                scm_obj = scm.objects.filter(scm_id=scm_bl[0].scm_id)
                bl_info['selected_index'] = scm_obj[0].selected_index
                bl_info['brushed_axis'] = scm_obj[0].brushed_axis
                bl_info['brushed_range'] = scm_obj[0].brushed_range
            elif bl_info['vis_types'] == "Scatter Plot":
                sp_bl = block.objects.filter(user_id=username, project_name=project_name,
                                              session_name=session_name, session_ver=int(session_ver),
                                              block_iden=block_iden, block_ver=int(block_ver))
                sp_obj = sp.objects.filter(sp_id=sp_bl[0].sp_id)
                bl_info['brushed_range'] = sp_obj[0].brushed_range

            run_vis(bl_info)
            return HttpResponse(json.dumps({'success' : True, 'detail' : "From to unit.", 'output' : None}) ,content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

@ensure_csrf_cookie
def unit_copy(request):
    errors = []
    if request.method == 'POST':
        # check necessary information
        param_list = ['username', 'project_name', 'session_name', 'session_ver', 'block_iden', 'block_ver', 'target_block_iden', 'target_block_ver', 'target_session_name', 'target_session_ver']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get necessary information
            #req = get_params(request, ['username', 'project_name', 'session_name', 'session_ver', 'block_iden', 'block_ver', 'target_block_iden', 'target_block_ver'])
            # get necessary information
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            block_iden = '%r' % request.POST['block_iden']
            block_iden = block_iden.replace('\'', '')
            block_ver = '%r' % request.POST['block_ver']
            block_ver = block_ver.replace('\'', '')
            target_session_name = '%r' % request.POST['target_session_name']
            target_session_name = target_session_name.replace('\'', '')
            target_session_ver = '%r' % request.POST['target_session_ver']
            target_session_ver = target_session_ver.replace('\'', '')
            target_block_iden = '%r' % request.POST['target_block_iden']
            target_block_iden = target_block_iden.replace('\'', '')
            target_block_ver = '%r' % request.POST['target_block_ver']
            target_block_ver = target_block_ver.replace('\'', '')

            # it finds previous block version and saved block
            try:
                save_bl = block.objects.filter(user_id=username, project_name=project_name, session_name=session_name,
                                               session_ver=int(session_ver), block_iden=block_iden,
                                               block_ver__lte=int(block_ver), is_save=True).order_by('last_date')
            except block.DoesNotExist:
                save_bl = []
            saved_block_ver = 0
            if len(save_bl) != 0:
                saved_block_ver = save_bl[0].block_ver
            # find all block which made after this block version
            total_bls = []
            bl_info = {}
            bl_info['username'] = username
            bl_info['project_name'] = project_name
            bl_info['session_name'] = session_name
            bl_info['session_ver'] = session_ver
            bl_info['block_iden'] = block_iden
            bl_info['block_ver'] = int(block_ver)
            #print(int(saved_block_ver))
            total_bls = find_unit(total_bls, bl_info)
            new_bl_list = []
            old_bl_list = []
            copy_bl_list = []

            # get all block iden in this session
            bl_iden = block.objects.filter(user_id=username, project_name=project_name, session_name=target_session_name,
                                           session_ver=int(target_session_ver)).values('block_iden').distinct()

            is_copied = False

            num = 1
            for i in total_bls:
                # generate new block iden
                if i['block_iden'] not in old_bl_list:
                    temp_bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = i['block_iden'], block_ver = int(i['block_ver']))
                    old_bl_list.append(i['block_iden'])
                    # make new block iden
                    new_block_iden = "U-" + str(random_with_N_digits(13))
                    while (new_block_iden in bl_iden.values()):
                        new_block_iden = "U-" + str(random_with_N_digits(13))
                    new_bl_list.append(new_block_iden)
                    copy_bl_list.append(temp_bl[0].block_name + "-C" + str(num))
                    num = num + 1
                diff_bl_ver = int(target_block_ver) - int(block_ver) + 1

                # insert copy log
                if i['block_iden'] == block_iden and is_copied == False:
                    insert_copy_log = log_history(scope="unit", action="Copy-Unit",
                                                  intent="Session change Display change Unit change", user_id=username,
                                                  project_name=project_name, session_name=target_session_name,
                                                  session_ver=int(target_session_ver), parent_block_iden=target_block_iden,
                                                  parent_block_ver=int(target_block_ver),
                                                  block_iden=new_bl_list[old_bl_list.index(i['block_iden'])],
                                                  block_ver=0,
                                                  block_name=copy_bl_list[old_bl_list.index(i['block_iden'])],
                                                  creatation_date=datetime.datetime.now(), is_event=False,
                                                  is_save=True, is_new=False, is_used=True, copy_block_iden=block_iden,
                                                  copy_block_ver=int(block_ver), save_ver = 0, is_closed = False)
                    insert_copy_log.save()
                    is_copied = True

                # copy blocks
                bls = block.objects.filter(user_id=username, project_name=project_name,
                                           session_name=session_name, session_ver=int(session_ver),
                                           block_iden=i['block_iden'], block_ver=int(i['block_ver'])).order_by(
                    "creatation_date")

                get_block_ver = block.objects.all().filter(user_id=username, project_name=project_name,
                                                           session_name=target_session_name,
                                                           session_ver=int(target_session_ver),
                                                           block_iden=new_bl_list[
                                                               old_bl_list.index(i['block_iden'])]).aggregate(
                    Max('block_ver'))
                max_block_ver = get_block_ver['block_ver__max']
                if max_block_ver is None:
                    max_block_ver = 0
                else:
                    max_block_ver = int(max_block_ver) + 1

                # get block save ver
                get_save_ver = block.objects.filter(user_id=username, project_name=project_name,
                                                        session_name=session_name,
                                                        session_ver=int(session_ver), block_iden=new_bl_list[
                            old_bl_list.index(i['block_iden'])]).aggregate(
                        Max('save_ver'))
                max_save_ver = get_save_ver['save_ver__max']
                if max_save_ver is None:
                    max_save_ver = 0
                else:
                    max_save_ver = int(max_save_ver) + 1

                for j in bls:
                    new_obj = j
                    new_obj.block_id = None
                    new_obj.save()
                    new_obj = block.objects.filter(block_id=new_obj.block_id)
                    # root units part
                    if block_iden == i['block_iden']:
                        # applied unit
                        if new_obj[0].save_ver is not None:
                            new_obj.update(session_name = target_session_name, session_ver = int(target_session_ver), parent_block_iden=target_block_iden, parent_block_ver=int(target_block_ver),
                                           block_iden=new_bl_list[old_bl_list.index(i['block_iden'])],
                                           block_ver=int(max_block_ver), creatation_date=datetime.datetime.now(),
                                           block_name=copy_bl_list[old_bl_list.index(i['block_iden'])],
                                           last_date=datetime.datetime.now(),
                                           save_ver=max_save_ver, is_first = False)

                        # saved unit
                        else:
                            new_obj.update(session_name = target_session_name, session_ver = int(target_session_ver), parent_block_iden=target_block_iden, parent_block_ver=int(target_block_ver),
                                           block_iden=new_bl_list[old_bl_list.index(i['block_iden'])],
                                           block_ver=int(max_block_ver), creatation_date=datetime.datetime.now(),
                                           block_name=copy_bl_list[old_bl_list.index(i['block_iden'])],
                                           last_date=datetime.datetime.now(), is_first = False)

                    else:
                        # applied unit
                        if new_obj[0].save_ver is not None:
                            new_obj.update(session_name = target_session_name, session_ver = int(target_session_ver),block_iden=new_bl_list[old_bl_list.index(i['block_iden'])],
                                           block_ver=int(max_block_ver),
                                           creatation_date=datetime.datetime.now(),
                                           block_name=copy_bl_list[old_bl_list.index(i['block_iden'])],
                                           last_date=datetime.datetime.now(), save_ver=max_save_ver, is_first = False)
                        # saved unit
                        else:
                            new_obj.update(session_name = target_session_name, session_ver = int(target_session_ver),block_iden=new_bl_list[old_bl_list.index(i['block_iden'])],
                                           block_ver=int(max_block_ver),
                                           creatation_date=datetime.datetime.now(),
                                           block_name=copy_bl_list[old_bl_list.index(i['block_iden'])],
                                           last_date=datetime.datetime.now(), is_first = False)
                        if new_obj[0].parent_block_iden is not None:
                            new_obj.update(
                                parent_block_iden=new_bl_list[old_bl_list.index(new_obj[0].parent_block_iden)])
                            if old_bl_list[new_bl_list.index(new_obj[0].parent_block_iden)] == block_iden:
                                bls_save_ver = block.objects.filter(user_id=username, project_name=project_name,
                                                           session_name=session_name, session_ver=int(session_ver),
                                                           block_iden=block_iden, block_ver=int(block_ver))
                                tar_bls_save_ver = block.objects.filter(user_id=username, project_name=project_name,
                                                                        session_name=target_session_name,
                                                                        session_ver=int(target_session_ver),
                                                                    block_iden=target_block_iden, block_ver=int(target_block_ver))
                                new_obj.update(parent_block_ver=int(new_obj[0].parent_block_ver) - (int(bls_save_ver[0].save_ver) - int(tar_bls_save_ver[0].save_ver)), is_first = False)
                            else:
                                new_obj.update(parent_block_ver=int(new_obj[0].parent_block_ver), is_first = False)

                    # separated vis_type part
                    if new_obj[0].vis_types == "Parallel Coordinate Plot":
                        pcp_obj = pcp.objects.filter(pcp_id=new_obj[0].pcp_id)
                        for i in pcp_obj:
                            new_pcp_obj = i
                            new_pcp_obj.pcp_id = None
                            new_pcp_obj.save()
                            new_obj.update(pcp_id=new_pcp_obj.pcp_id)
                    elif new_obj[0].vis_types == "Scatterplot Matrix":
                        scm_obj = scm.objects.filter(scm_id=new_obj[0].scm_id)
                        for i in scm_obj:
                            new_scm_obj = i
                            new_scm_obj.scm_id = None
                            new_scm_obj.save()
                            new_obj.update(scm_id=new_scm_obj.scm_id)
                    elif new_obj[0].vis_types == "Scatter Plot":
                        sp_obj = sp.objects.filter(sp_id=new_obj[0].sp_id)
                        for i in sp_obj:
                            new_sp_obj = i
                            new_sp_obj.sp_id = None
                            new_sp_obj.save()
                            new_obj.update(sp_id=new_sp_obj.sp_id)

                    # run clusters
                    request_json = []
                    rj_elem = {}
                    bl_info = {}
                    rj_elem['username'] = bl_info['username'] = new_obj[0].user_id
                    rj_elem['project_name'] = bl_info['project_name'] = new_obj[0].project_name
                    rj_elem['session_name'] = bl_info['session_name'] = new_obj[0].session_name
                    rj_elem['session_ver'] = bl_info['session_ver'] = int(new_obj[0].session_ver)
                    rj_elem['block_iden'] = bl_info['block_iden'] = new_obj[0].block_iden
                    rj_elem['block_name'] = new_obj[0].block_name
                    rj_elem['block_ver'] = bl_info['block_ver'] = int(new_obj[0].block_ver)
                    rj_elem['parent_block_iden'] = new_obj[0].parent_block_iden
                    rj_elem['parent_block_ver'] = int(new_obj[0].parent_block_ver)
                    rj_elem['cluster_type'] = bl_info['cluster_type'] = new_obj[0].clusterType
                    rj_elem['cluster_param'] = bl_info['cluster_param'] = new_obj[0].clusterParam
                    rj_elem['color_type'] = bl_info['color_type'] = new_obj[0].colors
                    rj_elem['data'] = bl_info['data'] = new_obj[0].data
                    rj_elem['data_annotation'] = new_obj[0].data_annotation
                    rj_elem['data_name'] = new_obj[0].data_name
                    rj_elem['vis_types'] = new_obj[0].vis_types
                    request_json.append(rj_elem)
                    position_json = []
                    position = {}
                    position['top'] = new_obj[0].position_top
                    position['left'] = new_obj[0].position_left
                    position['height'] = new_obj[0].position_height
                    position['width'] = new_obj[0].position_width
                    position_json.append(position)

                    bl_info['request_json'] = request_json
                    bl_info['position_json'] = position
                    bl_info['is_cluster'] = True
                    data_type = rj_elem['data_name'][rj_elem['data_name'].find(".") + 1:rj_elem['data_name'].find(" (")]
                    bl_info['data_type'] = data_type
                    bl_info['vis_types'] = new_obj[0].vis_types
                    if bl_info['vis_types'] == "Heatmap":
                        bl_info['cluster_type'] = new_obj[0].clusterType
                        bl_info['cluster_param'] = new_obj[0].clusterParam
                        bl_info['color_type'] = new_obj[0].colors
                    elif bl_info['vis_types'] == "Parallel Coordinate Plot":
                        pcp_bl = block.objects.filter(user_id=new_obj[0].username, project_name=new_obj[0].project_name,
                                                      session_name=new_obj[0].session_name, session_ver=int(new_obj[0].session_ver),
                                                      block_iden=new_obj[0].block_iden, block_ver=int(new_obj[0].block_ver))
                        pcp_obj = pcp.objects.filter(pcp_id=pcp_bl[0].pcp_id)
                        bl_info['column_order'] = pcp_obj[0].column_order
                        bl_info['selected_index'] = pcp_obj[0].selected_index
                        bl_info['brushed_axis'] = pcp_obj[0].brushed_axis
                        bl_info['brushed_range'] = pcp_obj[0].brushed_range
                    elif bl_info['vis_types'] == "Scatterplot Matrix":
                        scm_bl = block.objects.filter(user_id=new_obj[0].username, project_name=new_obj[0].project_name,
                                                      session_name=new_obj[0].session_name,
                                                      session_ver=int(new_obj[0].session_ver),
                                                      block_iden=new_obj[0].block_iden,
                                                      block_ver=int(new_obj[0].block_ver))
                        scm_obj = scm.objects.filter(scm_id=scm_bl[0].scm_id)
                        bl_info['selected_index'] = scm_obj[0].selected_index
                        bl_info['brushed_axis'] = scm_obj[0].brushed_axis
                        bl_info['brushed_range'] = scm_obj[0].brushed_range
                    elif bl_info['vis_types'] == "Scatter Plot":
                        sp_bl = block.objects.filter(user_id=new_obj[0].username, project_name=new_obj[0].project_name,
                                                      session_name=new_obj[0].session_name,
                                                      session_ver=int(new_obj[0].session_ver),
                                                      block_iden=new_obj[0].block_iden,
                                                      block_ver=int(new_obj[0].block_ver))
                        sp_obj = sp.objects.filter(sp_id=sp_bl[0].sp_id)
                        bl_info['brushed_range'] = sp_obj[0].brushed_range

                    if os.path.exists(
                                    os.path.join(os.getcwd(), BASE_DIR, 'member', new_obj[0].user_id, new_obj[0].project_name, new_obj[0].session_name,
                                                     str(new_obj[0].session_ver), str(new_obj[0].block_iden))) is False:
                        os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', new_obj[0].user_id, new_obj[0].project_name, new_obj[0].session_name,
                                                     str(new_obj[0].session_ver), str(new_obj[0].block_iden)))
                    if os.path.exists(
                                        os.path.join(os.getcwd(), BASE_DIR, 'member', new_obj[0].user_id, new_obj[0].project_name, new_obj[0].session_name,
                                                     str(new_obj[0].session_ver), str(new_obj[0].block_iden), str(new_obj[0].block_ver))) is False:
                        os.mkdir(
                                        os.path.join(os.getcwd(), BASE_DIR, 'member', new_obj[0].user_id, new_obj[0].project_name, new_obj[0].session_name,
                                                     str(new_obj[0].session_ver), str(new_obj[0].block_iden), str(new_obj[0].block_ver)))
                    run_vis(bl_info)

                    bl_anno = block_annotation_history.objects.filter(user_id=username, project_name=project_name,
                                                                      session_name=session_name,
                                                                      session_ver=int(session_ver),
                                                                      block_iden=i['block_iden'],
                                                                      block_ver=0)
                    for anno in bl_anno:
                        new_anno_obj = anno
                        new_anno_obj.annotation_id = None
                        new_anno_obj.save()
                        new_anno_obj = block_annotation_history.objects.filter(
                            annotation_id=new_anno_obj.annotation_id)
                        new_anno_obj.update(session_name=target_session_name, session_ver=int(target_session_ver),
                                            block_iden=new_bl_list[old_bl_list.index(i['block_iden'])],
                                            block_ver=0, last_date = datetime.datetime.now())

                        # open annotation.json file
                        annotation_path = os.path.join(str(BASE_DIR), 'member', str(username), str(project_name),
                                                       str(session_name), str(session_ver), str(i['block_iden']),
                                                       'annotation.json')

                        rfile = open(annotation_path, 'r')
                        # get annotations
                        existing_json = rfile.readline()
                        if existing_json:
                            line = json.loads(existing_json)
                        rfile.close()
                        # add new annotation
                        new_annotation_path = os.path.join(str(BASE_DIR), 'member', str(username), str(project_name),
                                                       str(target_session_name), str(target_session_ver), str(new_bl_list[
                                                               old_bl_list.index(i['block_iden'])]),
                                                       'annotation.json')
                        wfile = open(new_annotation_path, 'w')
                        for k in line['annotation_list']:
                            k['annotation']['session_name'] = target_session_name
                            k['annotation']['session_ver'] = int(target_session_ver)
                            k['annotation']['block_iden'] = new_bl_list[old_bl_list.index(k['annotation']['block_iden'])]
                            k['annotation']['block_ver'] = max_block_ver
                            k['annotation']['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        wfile.write(json.dumps(line))
                        wfile.close()



                logs = []
                # copy log_history
                if i['block_iden'] is not block_iden or i['block_ver'] is not block_ver:
                    logs = log_history.objects.filter(user_id=username, project_name=project_name,
                                                      session_name=session_name, session_ver=int(session_ver),
                                                      block_iden=i['block_iden'],
                                                      block_ver=int(i['block_ver']), is_event=False, is_closed = False).order_by("creatation_date")

                for j in logs:
                    new_obj = j
                    new_obj.action_id = None
                    new_obj.save()
                    new_obj = log_history.objects.filter(action_id=new_obj.action_id)
                    if block_iden == i['block_iden']:
                        # The version added when call save api
                        if new_obj[0].save_ver is not None:
                            new_obj.update(session_name = target_session_name, session_ver = int(target_session_ver), parent_block_iden=target_block_iden, parent_block_ver=int(target_block_ver),
                                           block_iden=new_bl_list[old_bl_list.index(i['block_iden'])],
                                           block_ver=int(max_block_ver),
                                           creatation_date=datetime.datetime.now(),
                                           block_name=new_bl_list[old_bl_list.index(i['block_iden'])],
                                           save_ver=max_save_ver)
                        else:
                            new_obj.update(session_name = target_session_name, session_ver = int(target_session_ver), parent_block_iden=target_block_iden, parent_block_ver=int(target_block_ver),
                                           block_iden=new_bl_list[old_bl_list.index(i['block_iden'])],
                                           block_ver=int(max_block_ver),
                                           creatation_date=datetime.datetime.now(),
                                           block_name=new_bl_list[old_bl_list.index(i['block_iden'])])
                    else:
                        new_obj.update(session_name = target_session_name, session_ver = int(target_session_ver),block_iden=new_bl_list[old_bl_list.index(i['block_iden'])],
                                       block_ver=max_block_ver,
                                       creatation_date=datetime.datetime.now(),
                                       block_name=new_bl_list[old_bl_list.index(i['block_iden'])])
                        if new_obj[0].parent_block_iden is not None:
                            new_obj.update(
                                session_name=target_session_name, session_ver=int(target_session_ver),parent_block_iden=new_bl_list[old_bl_list.index(new_obj[0].parent_block_iden)],
                                creatation_date=datetime.datetime.now())
                            if old_bl_list[new_bl_list.index(new_obj[0].parent_block_iden)] == block_iden:
                                new_obj.update(parent_block_ver=int(new_obj[0].parent_block_ver) - int(block_ver))
                            else:
                                new_obj.update(parent_block_ver=int(new_obj[0].parent_block_ver))

            return HttpResponse(json.dumps({'success' : True, 'detail' : "From to unit.", 'output' : total_bls}) ,content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

@ensure_csrf_cookie
def bookmark(request):
    errors = []
    username = ""
    if request.method == 'POST':
        # check information
        param_list = ['username', 'project_name', 'session_name', 'session_ver']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get parameter
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            ses = session_history.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
            ses.update(is_bookmarked = True)
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Bookmark.", 'output' : None}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

@ensure_csrf_cookie
def delete_bookmark(request):
    errors = []
    username = ""
    if request.method == 'POST':
        # check information
        param_list = ['username', 'project_name', 'session_name', 'session_ver']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get parameter
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            ses = session_history.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
            ses.update(is_bookmarked = False)
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Delete Bookmark.", 'output' : None}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

"""
@ensure_csrf_cookie
def session_copy(request):
    errors = []
    if request.method == 'POST':
        # check necessary information
        param_list = ['username', 'project_name', 'session_name', 'session_ver', 'target_session_name', 'target_session_ver']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get necessary information
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            target_session_name = '%r' % request.POST['target_session_name']
            target_session_name = target_session_name.replace('\'', '')
            target_session_ver = '%r' % request.POST['target_session_ver']
            target_session_ver = target_session_ver.replace('\'', '')
            # find all block which made after this block version
            ses_info = {}
            ses_info['username'] = username
            ses_info['project_name'] = project_name
            ses_info['session_name'] = session_name
            ses_info['session_ver'] = session_ver
            logs = log_history.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
            for i in logs:
                new_obj = i
                new_obj.action_id = None
                new_obj.save()
                new_obj = log_history.objects.filter(action_id = new_obj.action_id)
                new_obj.update(session_name = target_session_name, )
                # get max block ver
                get_sesion_ver = session.objects.filter(user_id = username, project_name = project_name,
                                                           session_name = session_name, session_ver = int(session_ver)).aggregate(Max('block_ver'))
                max_session_ver = get_session_ver['session_ver__max']
                diff_ses_ver = int(target_session_ver) - int(session_ver) + 1
                if session_name == i['session_name']:
                    new_obj.update()


                    # run clusters
                    request_json = []
                    rj_elem = {}
                    bl_info = {}
                    rj_elem['username'] = bl_info['username'] = new_obj[0].user_id
                    rj_elem['project_name'] = bl_info['project_name'] = new_obj[0].project_name
                    rj_elem['session_name'] = bl_info['session_name'] = new_obj[0].session_name
                    rj_elem['session_ver'] = bl_info['session_ver'] = int(new_obj[0].session_ver)
                    rj_elem['block_iden'] = bl_info['block_iden'] = new_obj[0].block_iden
                    rj_elem['block_name'] = new_obj[0].block_name
                    rj_elem['block_ver'] = bl_info['block_ver'] = int(new_obj[0].block_ver)
                    rj_elem['parent_block_iden'] = new_obj[0].parent_block_iden
                    rj_elem['parent_block_ver'] = int(new_obj[0].parent_block_ver)
                    rj_elem['cluster_type'] =  bl_info['cluster_type'] = new_obj[0].clusterType
                    rj_elem['cluster_param'] = bl_info['cluster_param'] = new_obj[0].clusterParam
                    rj_elem['color_type'] = bl_info['color_type'] = new_obj[0].colors
                    rj_elem['data'] = bl_info['data'] = new_obj[0].data
                    rj_elem['data_annotation'] = new_obj[0].data_annotation
                    rj_elem['data_name'] = new_obj[0].data_name
                    request_json.append(rj_elem)
                    position_json = []
                    position = {}
                    position['top'] = new_obj[0].position_top
                    position['left'] = new_obj[0].position_left
                    position['height'] = new_obj[0].position_height
                    position['width'] = new_obj[0].position_width
                    position_json.append(position)

                    bl_info['request_json'] = request_json
                    bl_info['position_json'] = position
                    bl_info['is_cluster'] = False
                    run_clusters(bl_info)

            return HttpResponse(json.dumps({'success' : True, 'detail' : "From to unit.", 'output' : total_bls}) ,content_type="application/json")
    else:
        return HttpResponse(json.dumps({"errors" : errors}))
"""

@ensure_csrf_cookie
def set_first(request):
    errors = []
    username = ""
    if request.method == 'POST':
        # check information
        param_list = ['username', 'project_name', 'session_name', 'session_ver']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get parameter
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            bls = block.objects.filter(user_id=username, project_name=project_name,
                                       session_name=session_name, session_ver=int(session_ver))
            for i in bls:
                if i.parent_block_iden is None and i.ori_p_block_iden is None:
                    i.__dict__.update(is_first = True)
                    i.save()
            return HttpResponse(json.dumps({'success' : True, 'detail' : "set_first.", 'output' : None}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")