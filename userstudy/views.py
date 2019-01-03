from heatmap import *
from userstudy import *

# Create your views here.
@gzip_page
def sankey_overview(request, filename):
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

def sankey_list(request):
    """
    get sankey list
    :param request:
    :return: sankey list
    """
    errors = []
    if request.method == 'POST':
        # check information
        #param_list = ['username']
        #errors = param_checker(request, errors, param_list)
        output_list = []
        if not errors:
            static_str = "static"
            sankey_str = "sankey"
            # get parameter
            userlist = json.loads(request.POST.get('userlist'))
            for i in userlist:
                output = {}
                sankeys = []
                if 'username' not in i.keys():
                    username = None
                else:
                    username = i['username']
                if 'project_name' not in i.keys():
                    project_name = None
                else:
                    project_name = i['project_name']
                if 'session_name' not in i.keys():
                    session_name = None
                else:
                    session_name = i['session_name']

                if project_name == None and session_name == None:
                    user_dir = os.path.join(os.getcwd(), 'static', 'sankey', username)
                    if os.path.exists(user_dir) is False:
                        return HttpResponse(
                            json.dumps({'success': False, 'detail': "No user", 'output': username}),
                            content_type="application/json")
                    else:
                        for proj in os.listdir(user_dir):
                            if os.path.exists(os.path.join(user_dir, proj)) is False:
                                continue
                            proj_dir = os.path.join(user_dir, proj)
                            for ses in os.listdir(proj_dir):
                                ses_file = ses.lower()
                                if ses_file.endswith("png") or ses_file.endswith("svg") or ses_file.endswith("jpg"):
                                    sankeys.append(os.path.join(static_str, sankey_str, username, proj, ses))
                                    continue
                                if os.path.exists(os.path.join(proj_dir, ses)) is False:
                                    continue
                                ses_dir = os.path.join(proj_dir, ses)
                                for ses_sankey in os.listdir(ses_dir):
                                    if os.path.exists(os.path.join(ses_dir, ses_sankey)) is False:
                                        continue
                                    sankeys.append(os.path.join(static_str, sankey_str, username, proj, ses, ses_sankey))
                elif project_name != None and session_name == None:
                    proj_dir = os.path.join(os.getcwd(), 'static', 'sankey', username, project_name)
                    if os.path.exists(proj_dir) is False:
                        return HttpResponse(
                            json.dumps({'success': False, 'detail': "No project", 'output': project_name}),
                            content_type="application/json")
                    else:
                        for ses in os.listdir(proj_dir):
                            ses_file = ses.lower()
                            if ses_file.endswith("png") or ses_file.endswith("svg") or ses_file.endswith("jpg"):
                                sankeys.append(os.path.join(static_str, sankey_str, username, project_name, ses))
                                continue
                            if os.path.exists(os.path.join(proj_dir, ses)) is False:
                                continue
                            ses_dir = os.path.join(proj_dir, ses)
                            for ses_sankey in os.listdir(ses_dir):
                                if os.path.exists(os.path.join(ses_dir, ses_sankey)) is False:
                                    continue
                                sankeys.append(os.path.join(static_str, sankey_str, username, project_name, ses, ses_sankey))

                elif project_name != None and session_name != None:
                    ses_dir = os.path.join(os.getcwd(), 'static', 'sankey', username, project_name, session_name)
                    if os.path.exists(ses_dir) is False:
                        return HttpResponse(
                            json.dumps({'success': False, 'detail': "No session", 'output': session_name}),
                            content_type="application/json")
                    else:
                        for ses in os.listdir(ses_dir):
                            ses_file = ses.lower()
                            if ses_file.endswith("png") or ses_file.endswith("svg") or ses_file.endswith("jpg"):
                                sankeys.append(os.path.join(static_str, sankey_str, username, project_name, session_name, ses))
                                continue
                else:
                    return HttpResponse(
                        json.dumps({'success': False, 'detail': "Please enter project name", 'output': None}),
                        content_type="application/json")

                output['username'] = username
                output['project_name'] = project_name
                output['session_name'] = session_name
                output['sankeys'] = sankeys
                output_list.append(output)
            return HttpResponse(
                json.dumps({'success': True, 'detail': "Got sankeys", 'output': output_list}),
                content_type="application/json")

        else:
            return HttpResponse(json.dumps({'success': False, 'detail': errors, 'output': None}),
                                content_type="application/json")

def playback(request):
    errors = []
    if request.method == 'POST':
        # check information
        param_list = []
        errors = param_checker(request, errors, param_list)

        if not errors:
            with open('static/csv/final_5.csv', 'r') as f:
                reader = csv.reader(f, delimiter=',')
                first_row = True
                f = open(os.path.join(os.getcwd(), "userstudy/final_5.json"), 'w')
                final_list = []
                for row in reader:
                    if first_row :
                        first_row = False
                    else :
                        #username = '%r' % request.POST['username']
                        username = row[2]
                        username = username.replace('\'', '')
                        #project_name = '%r' % request.POST['project_name']
                        project_name = row[16]
                        project_name = project_name.replace('\'', '')
                        #session_name = '%r' % request.POST['session_name']
                        session_name = row[14]
                        session_name = session_name.replace('\'', '')
                        #session_ver = '%r' % request.POST['session_ver']
                        session_ver = 0
                        #session_ver = session_ver.replace('\'', '')
                        session_ver = int(session_ver)

                        path_list = []
                        path_elem = {}
                        inform_elem = {}
                        user_elem = {}
                        action_list = []

                        scope_list = ["tab", "table"]
                        query_list = []

                        user_elem['username'] = username
                        user_elem['project_name'] = "experiment"
                        user_elem['session_name'] = "Problem5"
                        """
                        if '1' in session_name:
                            user_elem['session_name'] = "Problem1"
                        elif '2' in session_name:
                            user_elem['session_name'] = "Problem2"
                        elif '3' in session_name:
                            user_elem['session_name'] = "Problem3"
                        elif '4' in session_name:
                            user_elem['session_name'] = "Problem4"
                        elif '5' in session_name:
                            user_elem['session_name'] = "Problem5"
                            """
                        user_elem['session_ver'] = session_ver

                        path_list.append(user_elem)

                        for i in scope_list:
                            query_list.append(
                                Q(user_id=username, project_name=project_name, session_name=session_name,
                                  session_ver=int(session_ver),
                                  scope=i))
                        logs = log_history.objects.filter(reduce(operator.or_, query_list)).values('action_id', 'action',
                                                                                                   'scope', 'user_id',
                                                                                                   'project_name',
                                                                                                   'session_name', 'session_ver',
                                                                                                   'page', 'column',
                                                                                                   'creatation_date').order_by('creatation_date')
                        for j in logs:
                            action_elem = {}
                            #if j['action'] == "Select-Unit":
                            #    continue
                            action_elem['action'] = j['action']
                            action_elem['action_id'] = j['action_id']
                            parameter = {}
                            position = {}
                            """
                            if list_checker(j['action'], action_check_list, [37, 38, 39, 42, 43]):
                                parameter['username'] = j['user_id']
                                parameter['project_name'] = j['project_name']
                                parameter['session_name'] = j['session_name']
                                parameter['session_ver'] = j['session_ver']
                                if list_checker(j['action'], action_check_list, [42]):
                                    parameter['column'] = j['column']
                                if list_checker(j['action'], action_check_list, [43]):
                                    parameter['page'] = j['page']
                        #    action_elem['parameter'] = parameter
                        """
                            action_elem['date'] = j['creatation_date'].strftime("%Y-%m-%d %H:%M:%S")
                            action_list.append(action_elem)
                            """
                        path_elem['username'] = username
                        path_elem['project_name'] = "experiment"
                        if '1' in session_name:
                            path_elem['session_name'] = "Problem1"
                        elif '2' in session_name:
                            path_elem['session_name'] = "Problem2"
                        elif '3' in session_name:
                            path_elem['session_name'] = "Problem3"
                        elif '4' in session_name:
                            path_elem['session_name'] = "Problem4"
                        elif '5' in session_name:
                            path_elem['session_name'] = "Problem5"
                        path_elem['session_ver'] = session_ver

                        """
                        path_elem['action_list'] = action_list
                        path_elem['block_iden'] = "U-"
                        path_list.append(path_elem)

                        bls = block.objects.filter(user_id=username, project_name=project_name, session_name=session_name,
                                                  session_ver=int(session_ver))
                        for bl in bls:
                            path = os.path.join("static", "member", str(username), str(project_name), str(session_name),
                                                str(session_ver), str(bl.block_iden), str(bl.block_ver))
                            anno_path = os.path.join("static", "member", str(username), str(project_name), str(session_name),
                                                     str(session_ver), str(bl.block_iden))
                            path_elem = {}
                            """
                            if bl.vis_types == 'Parallel Coordinate Plot':
                                path_elem['pcp_path'] = os.path.join(path, "pcp.json")
                                path_elem['annotation_path'] = os.path.join(anno_path, "annotation.json")
                            elif bl.vis_types == 'Scatterplot Matrix':
                                path_elem['scm_path'] = os.path.join(path, "scm.json")
                                path_elem['annotation_path'] = os.path.join(anno_path, "annotation.json")
                            elif bl.vis_types == 'Scatter Plot':
                                path_elem['sp_path'] = os.path.join(path, "sp.json")
                                path_elem['annotation_path'] = os.path.join(anno_path, "annotation.json")
                            else:
                                path_elem['heatmap_path'] = os.path.join(path, "clusters.json")
                                path_elem['annotation_path'] = os.path.join(anno_path, "annotation.json")
                                if bl.clusterType == "Hierarchy":
                                    path_elem['dendro_path'] = os.path.join(path, str(bl.clusterType) + ".csv")
                                    path_elem['dendro_col_path'] = os.path.join(path, str(bl.clusterType) + "Col.csv")
                                else:
                                    path_elem['dendro_path'] = None
                                    path_elem['dendro_col_path'] = None

                            path_elem['username'] = username
                            path_elem['project_name'] = "experiment"
                            if '1' in session_name:
                                path_elem['session_name'] = "Problem1"
                            elif '2' in session_name:
                                path_elem['session_name'] = "Problem2"
                            elif '3' in session_name:
                                path_elem['session_name'] = "Problem3"
                            elif '4' in session_name:
                                path_elem['session_name'] = "Problem4"
                            elif '5' in session_name:
                                path_elem['session_name'] = "Problem5"
                            path_elem['session_ver'] = session_ver
                            path_elem['block_iden'] = bl.block_iden
                            path_elem['block_name'] = bl.block_name
                            path_elem['block_ver'] = bl.block_ver
                            path_elem['vis_types'] = bl.vis_types
                            """
                            action_list = []
                            logs = log_history.objects.filter(user_id=username, project_name=project_name,
                                                                   session_name=session_name, session_ver=int(session_ver),
                                                                   block_iden=bl.block_iden, block_ver=int(bl.block_ver))


                            anno_path = ""
                            for j in logs:
                                action_elem = {}
                            #    if j.action == "Select-Unit":
                            #        continue
                                if j.action == "Branch-Unit":
                                    action_list = []


                                action_elem['action'] = j.action
                                action_elem['action_id'] = j.action_id
                                parameter = {}
                                position = {}
                                """
                                if list_checker(j.action, action_check_list,
                                                [0, 1, 2, 3, 4, 5, 6, 7, 14, 15, 17, 19, 21, 27, 28, 29, 30, 33, 36, 40, 41, 37, 38, 39, 42, 43]):
                                    parameter['block_iden'] = bl.block_iden
                                    parameter['block_name'] = bl.block_name
                                    parameter['block_ver'] = bl.block_ver
                                    parameter['save_ver'] = bl.save_ver
                                    if list_checker(j.action, action_check_list, [4]):
                                        parameter['data_name'] = j.data_name
                                    elif list_checker(j.action, action_check_list, [5]):
                                        parameter['clusterType'] = j.clusterType
                                    elif list_checker(j.action, action_check_list, [6]):
                                        parameter['clusterParam'] = j.clusterParam
                                    elif list_checker(j.action, action_check_list, [7]):
                                        position['position_top'] = j.position_top
                                        position['position_left'] = j.position_left
                                        position['position_width'] = j.position_width
                                        position['position_height'] = j.position_height
                                        parameter['position'] = position
                                    elif list_checker(j.action, action_check_list, [14]):
                                        parameter['data_annotation'] = j.data_annotation
                                    elif list_checker(j.action, action_check_list, [15]):
                                        parameter['block_annotation'] = j.block_annotation
                                    elif list_checker(j.action, action_check_list, [19]):
                                        parameter['parent_block_iden'] = j.parent_block_iden
                                        parameter['parent_block_ver'] = j.parent_block_ver
                                    elif list_checker(j.action, action_check_list, [21]):
                                        parameter['color_type'] = j.colors
                                    elif list_checker(j.action, action_check_list, [27]):
                                        # get pcp_id
                                        pcp_obj = pcp.objects.filter(pcp_id=j.pcp_id)
                                        if len(pcp_obj) > 0:
                                            parameter['column_order'] = pcp_obj[0].column_order
                                    elif list_checker(j.action, action_check_list, [28]):
                                        # get pcp_id
                                        pcp_obj = pcp.objects.filter(pcp_id=j.pcp_id)
                                        if len(pcp_obj) > 0:
                                            parameter['selected_index'] = pcp_obj[0].selected_index
                                            parameter['brushed_axis'] = pcp_obj[0].brushed_axis
                                            parameter['brushed_range'] = pcp_obj[0].brushed_range
                                    elif list_checker(j.action, action_check_list, [29]):
                                        # get scm_id
                                        scm_obj = scm.objects.filter(scm_id=j.scm_id)
                                        if len(scm_obj) > 0:
                                            parameter['selected_index'] = scm_obj[0].selected_index
                                            parameter['brushed_axis'] = scm_obj[0].brushed_axis
                                            parameter['brushed_range'] = scm_obj[0].brushed_range
                                    elif list_checker(j.action, action_check_list, [30]):
                                        # get sp_id
                                        sp_obj = sp.objects.filter(sp_id=j.sp_id)
                                        if len(sp_obj) > 0:
                                            parameter['x_axis'] = sp_obj[0].x_axis
                                            parameter['y_axis'] = sp_obj[0].y_axis
                                            parameter['brushed_range'] = sp_obj[0].brushed_range
                                            parameter['selected_index'] = sp_obj[0].selected_index
                                    elif list_checker(j.action, action_check_list, [42]):
                                        parameter['column'] = j.column
                                    elif list_checker(j.action, action_check_list, [43]):
                                        parameter['page'] = j.page
                                elif list_checker(j.action, action_check_list, [8, 9, 10, 11, 18, 37, 38, 39, 42, 43]):
                                    parameter['username'] = ses_info['username']
                                    parameter['project_name'] = project_name
                                    parameter['session_name'] = session_name
                                    parameter['session_ver'] = session_ver
                                    if list_checker(j.action, action_check_list, [42]):
                                        parameter['column'] = j.column
                                    if list_checker(j.action, action_check_list, [43]):
                                        parameter['page'] = j.page
                                elif list_checker(j.action, action_check_list, [12]):
                                    parameter['project_name'] = j.project_name
                                    parameter['project_annotation'] = j.project_annotation
                                elif list_checker(j.action, action_check_list, [13]):
                                    parameter['username'] = ses_info['username']
                                    parameter['project_name'] = j.project_name
                                action_elem['parameter'] = parameter
                                """
                                action_elem['date'] = j.creatation_date.strftime("%Y-%m-%d %H:%M:%S")
                                action_list.append(action_elem)
                            path_elem['block_iden'] = bl.block_iden
                            path_elem['block_name'] = bl.block_name
                            path_elem['block_ver'] = bl.block_ver
                            path_elem['save_ver'] = bl.save_ver
                            path_elem['action_list'] = action_list
                            path_list.append(path_elem)
                        final_list.append(path_list)


                f.write(json.dumps(final_list))
                f.close()


            return HttpResponse(json.dumps({'success': True, 'detail': "Get Unit information.", 'output': None}),
                                    content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success': False, 'detail': errors, 'output': None}),
                                content_type="application/json")

def stat(request):
    """
    get sankey list
    :param request:
    :return: sankey list
    """
    if request.method == 'POST':
        user_list = ["A", "B"]
        number_list = [23, 50]

        f = open(os.path.join(os.getcwd(), "userstudy", "stat2.json"), 'w')
        stat_list = {}
        user_stat_list = []
        for usr in user_list:
            for num in range(1, number_list[user_list.index(usr)]):
                user_stat = {}
                user_name = usr + str(num)
                projs = project.objects.filter(user_id = user_name)
                if len(projs) == 0:
                    continue
                user_stat['user'] = user_name
                for proj in projs:
                    low_proj_name = str(proj.project_name).lower()
                    if "ex" in low_proj_name:
                        user_stat['project_name'] = proj.project_name
                        session_stat_list = []
                        proj_block_vis_list = []
                        proj_log = 0
                        proj_anno = 0
                        proj_branch = 0
                        sess = session.objects.filter(user_id = user_name, project_name = proj.project_name)
                        for ses in sess:
                            session_stat = {}
                            session_stat['session_name'] = ses.session_name
                            ses_branch = 0
                            block_vis_list = []
                            bls = block.objects.filter(user_id = user_name, project_name = proj.project_name, session_name = ses.session_name)
                            bl_du_list = []
                            total_anno_num = 0
                            for bl in bls:
                                if bl.block_iden not in bl_du_list:
                                    bl_du_list.append(bl.block_iden)
                                    block_vis_list.append(bl.vis_types)
                                    proj_block_vis_list.append(bl.vis_types)
                                 #   session_stat['vis_types'] = block_vis_list
                                    get_block_ver = block.objects.all().filter(user_id=user_name,
                                                                               project_name=proj.project_name,
                                                                               session_name=ses.session_name,
                                                                               block_iden=bl.block_iden).aggregate(
                                        Max('block_ver'))
                                    max_block_ver = get_block_ver['block_ver__max']
                                    annos = block_annotation_history.objects.filter(user_id=user_name,
                                                                                    project_name=proj.project_name,
                                                                                    session_name=ses.session_name,
                                                                                    block_iden=bl.block_iden,
                                                                                    block_ver=int(max_block_ver))
                                    total_anno_num += len(annos)
                            logs = log_history.objects.filter(user_id = user_name, project_name = proj.project_name, session_name = ses.session_name)
                            for log in logs:
                                if log.action == "Branch-Unit":
                                    ses_branch = ses_branch + 1
                         #   session_stat["log"] = len(logs)
                            proj_log = proj_log + len(logs)
                          #  session_stat["annotation"] = total_anno_num
                          #  session_stat["branch"] = ses_branch
                            session_stat["units"] = len(bl_du_list)
                            proj_anno = proj_anno + total_anno_num
                            proj_branch = proj_branch + ses_branch
                            session_stat_list.append(session_stat)
                    #    user_stat["proj_log"] = proj_log
                    #    user_stat["proj_annotation"] = proj_anno
                        user_stat["session"] = session_stat_list
                     #   user_stat["proj_vis_types"] = proj_block_vis_list
                    #    user_stat["proj_branch"] = proj_branch

                user_stat_list.append(user_stat)
        stat_list['stat'] = user_stat_list
        f.write(json.dumps(stat_list))
        f.close()
        return HttpResponse(json.dumps({'success': True, 'detail': "Get Unit information.", 'output': None}),
                            content_type="application/json")

def regroup(request):
    """
    get sankey list
    :param request:
    :return: sankey list
    """
    if request.method == 'POST':
        user_list = ["S"]
        number_list = [4]
        #number_list = [23, 50]
        f = open(os.path.join(os.getcwd(), "userstudy", "GroupA2.json"), 'w')
        user_stat_list = []
        log_list = []
        for usr in user_list:
            for num in range(1, number_list[user_list.index(usr)]):
                user_stat = {}
                user_name = usr + str(num+49)

                log_list.append(user_name)
                projs = project.objects.filter(user_id = user_name)
                if len(projs) == 0:
                    continue

                for proj in projs:
                    low_proj_name = str(proj.project_name).lower()
                    if "exp" in low_proj_name:
                        user_stat['project_name'] = proj.project_name
                        sess = session.objects.filter(user_id = user_name, project_name = proj.project_name)
                        for ses in sess:
                            log_list.append(ses.session_name + " : ")
                            user_stat['user'] = user_name
                            user_stat['problem'] = ses.session_name
                            ses_branch = 0
                            unit_branch = 0
                            restore_unit = 0

                            bls = block.objects.filter(user_id = user_name, project_name = proj.project_name, session_name = ses.session_name)
                            user_stat["Parallel Coordinate Plot"] = 0
                            user_stat["Scatter Plot"] = 0
                            user_stat["Scatterplot Matrix"] = 0

                            log_before_branch = []
                            anno_before_branch = []

                            bl_list = []
                            for bl in bls:
                                #block logs
                                logs = log_history.objects.filter(user_id = user_name, project_name = proj.project_name, session_name = ses.session_name, block_iden = bl.block_iden)

                                block_logs = 0
                                for log in logs:
                                    block_logs += 1
                                    if log.action == "Branch-Unit":
                                        log_before_branch.append(block_logs)


                                if bl.block_iden not in bl_list:
                                    if bl.vis_types == "Parallel Coordinate Plot":
                                        user_stat["Parallel Coordinate Plot"] += 1
                                    elif bl.vis_types == "Scatter Plot":
                                        user_stat["Scatter Plot"] += 1
                                    elif bl.vis_types == "Scatterplot Matrix":
                                        user_stat["Scatterplot Matrix"] += 1
                                    bl_list.append(bl.block_iden)


                            # session logs
                            logs = log_history.objects.filter(user_id=user_name, project_name=proj.project_name, session_name=ses.session_name)

                            branch_num = 0
                            log_num = 0
                            anno_num = 0
                            for log in logs:
                                log_num += 1
                                log_list.append(log.action + " : " + str(log_num))
                                if log.action == "Branch-Unit":
                                    unit_branch += 1
                                    log_num -= log_before_branch[branch_num]
                                    branch_num += 1

                                if log.action == "Branch-Session":
                                    ses_branch += 1
                                    log_num = 1
                                    anno_num = 0
                                if log.action == "Restore-Unit":
                                    restore_unit += 1
                                if log.action == "Show-Session":
                                    log_num -= 1
                                if log.action == "Create-Unit-Annotation":
                                    anno_num += 1
                                #if log.action == "Delete-Unit-Annotation":
                                #    anno_num -= 1


                            if unit_branch == 0 & ses_branch == 0:
                                user_stat["group"] = "A"
                            elif unit_branch > 0 & ses_branch == 0:
                                user_stat["group"] = "B"
                            if ses_branch > 0:
                                user_stat["group"] = "C"
                            if restore_unit > 0:
                                user_stat["group"] = "D"
                            user_stat["restore"] = restore_unit
                            user_stat["units"] = len(bl_list)
                            user_stat["logs"] = log_num
                            annos = block_annotation_history.objects.filter(user_id = user_name, project_name = proj.project_name, session_name = ses.session_name)
                            user_stat["unit branch"] = unit_branch
                            user_stat["session branch"] = ses_branch
                            user_stat["annotation"] = anno_num # len(annos) #anno_num
                            user_stat_list.append(user_stat)
                            user_stat = {}

            #stat_list['stat'] = user_stat_list
        f.write(json.dumps(user_stat_list))
        f.close()

        return HttpResponse(json.dumps({'success': True, 'detail': "Get User information.", 'output': []}),
                            content_type="application/json")
"""
from heatmap.models import *
user_stat = {}
logs0 = log_history.objects.filter(user_id="B22", project_name="experiment", session_name="Problem 3", session_ver=int(0))
logs1 = log_history.objects.filter(user_id="B22", project_name="experiment", session_name="Problem 3", session_ver=int(1))
brch_block_log = log_history.objects.filter(user_id="B22", project_name="experiment", session_name="Problem 3", session_ver=int(0), scope="unit")
num, log_num, unit_branch, restore_unit, ses_branch = 0, 0, 0, 0, 0
for log in logs1:
    if num < len(logs0):
        num += 1
        continue
    if log.action == "Show-Session":
        continue
    elif log.action == "Branch-Unit":
        prev_bl = log_history.objects.filter(user_id="B22", project_name="experiment", session_name="Problem 3", session_ver=int(1), block_iden = log.parent_block_iden, block_ver = int(log.parent_block_ver))
        log_num -= len(prev_bl)
        unit_branch += 1
    elif log.action == "Branch-Session":
        ses_branch += 1
    elif log.action == "Restore-Unit":
        restore_unit += 1
    log_num += 1
print(log_num)
user_stat['logs'] = log_num
user_stat["restore"] = restore_unit
user_stat["unit branch"] = unit_branch
user_stat["session branch"] = ses_branch
dif_logs_list = list_difference(list(logs1), list(logs0))

bl_ses0 = block.objects.filter(user_id="B22", project_name="experiment", session_name="Problem 3", session_ver=int(0))
bl_ses1 = block.objects.filter(user_id="B22", project_name="experiment", session_name="Problem 3", session_ver=int(1))
user_stat['units'] = len(bl_ses1) - len(bl_ses0)
anno0 = block_annotation_history.objects.filter(user_id="B22", project_name="experiment", session_name="Problem 3", session_ver=int(0))
anno1 = block_annotation_history.objects.filter(user_id="B22", project_name="experiment", session_name="Problem 3", session_ver=int(1))
user_stat['annotation'] = 1

print(user_stat)

"""


def regroup2(request):
    """
    get sankey list
    :param request:
    :return: sankey list
    """
    if request.method == 'POST':
        user_list = ["S"]
        number_list = [2]
        #number_list = [23, 50]
        f = open(os.path.join(os.getcwd(), "userstudy", "s22group.json"), 'w')
        user_stat_list = []
        log_list = []
        for usr in user_list:
            for num in range(1, number_list[user_list.index(usr)]):
                user_stat = {}
                user_name = usr + str(num+22)

                log_list.append(user_name)
                projs = project.objects.filter(user_id = user_name)
                if len(projs) == 0:
                    continue

                for proj in projs:
                    low_proj_name = str(proj.project_name).lower()
                    if "2" in low_proj_name:
                        user_stat['project_name'] = proj.project_name
                        sess = session.objects.filter(user_id = user_name, project_name = proj.project_name)
                        for ses in sess:
                            log_list.append(ses.session_name + " : ")
                            user_stat['user'] = user_name
                            user_stat['problem'] = ses.session_name
                            ses_branch = 0
                            unit_branch = 0
                            restore_unit = 0

                            bls = block.objects.filter(user_id = user_name, project_name = proj.project_name, session_name = ses.session_name)
                            user_stat["Parallel Coordinate Plot"] = 0
                            user_stat["Scatter Plot"] = 0
                            user_stat["Scatterplot Matrix"] = 0

                            log_before_branch = []
                            anno_before_branch = []

                            bl_list = []
                            for bl in bls:
                                #block logs
                                logs = log_history.objects.filter(user_id = user_name, project_name = proj.project_name, session_name = ses.session_name, block_iden = bl.block_iden)

                                block_logs = 0
                                for log in logs:
                                    block_logs += 1
                                    if log.action == "Branch-Unit":
                                        log_before_branch.append(block_logs)


                                if bl.block_iden not in bl_list:
                                    if bl.vis_types == "Parallel Coordinate Plot":
                                        user_stat["Parallel Coordinate Plot"] += 1
                                    elif bl.vis_types == "Scatter Plot":
                                        user_stat["Scatter Plot"] += 1
                                    elif bl.vis_types == "Scatterplot Matrix":
                                        user_stat["Scatterplot Matrix"] += 1
                                    bl_list.append(bl.block_iden)


                            # session logs
                            logs = log_history.objects.filter(user_id=user_name, project_name=proj.project_name, session_name=ses.session_name)

                            branch_num = 0
                            log_num = 0
                            anno_num = 0
                            for log in logs:
                                log_num += 1
                                log_list.append(log.action + " : " + str(log_num))
                                if log.action == "Branch-Unit":
                                    unit_branch += 1
                                    log_num -= log_before_branch[branch_num]
                                    branch_num += 1

                                if log.action == "Branch-Session":
                                    ses_branch += 1
                                    log_num = 1
                                    anno_num = 0
                                if log.action == "Restore-Unit":
                                    restore_unit += 1
                                if log.action == "Show-Session":
                                    log_num -= 1
                                if log.action == "Create-Unit-Annotation":
                                    anno_num += 1
                                #if log.action == "Delete-Unit-Annotation":
                                #    anno_num -= 1


                            if unit_branch == 0 & ses_branch == 0:
                                user_stat["group"] = "A"
                            elif unit_branch > 0 & ses_branch == 0:
                                user_stat["group"] = "B"
                            if ses_branch > 0:
                                user_stat["group"] = "C"
                            if restore_unit > 0:
                                user_stat["group"] = "D"
                            user_stat["restore"] = restore_unit
                            user_stat["units"] = len(bl_list)
                            user_stat["logs"] = log_num
                            annos = block_annotation_history.objects.filter(user_id = user_name, project_name = proj.project_name, session_name = ses.session_name)
                            user_stat["unit branch"] = unit_branch
                            user_stat["session branch"] = ses_branch
                            user_stat["annotation"] = anno_num # len(annos) #anno_num
                            user_stat_list.append(user_stat)
                            user_stat = {}

            #stat_list['stat'] = user_stat_list
        f.write(json.dumps(user_stat_list))
        f.close()

        return HttpResponse(json.dumps({'success': True, 'detail': "Get User information.", 'output': []}),
                            content_type="application/json")


def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


@ensure_csrf_cookie
def get_time(request):
    errors = []
    Session_time = [];

    if request.method == 'POST':

        if not errors:
            time_file = os.path.join(os.getcwd(), "static", "file", "groupa_time2.csv")

            with open(time_file, 'w') as wf:
                #fieldnames = ['username', 'problem1', 'problem2', 'problem3', 'problem4', 'problem5']
                fieldnames = ['username', 'problem', 'sess', 'anno', 'time']
                csvw = csv.DictWriter(wf, fieldnames = fieldnames)
                csvw.writeheader()
                user_name_list = ["S"]
                user_num_list = 16
                user_list = []
                except_list = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 25, 30, 38, 47]
                for i in range(user_num_list):
                    user_list.append("S"+str(i+37))
                    """
                    for j in user_num_list:
                        if (j == 30 and i == "A") or (j==50 and i == "B"):
                            for k in range(1, int(j)+1):
                                if i == "B" and k in except_list:
                                    continue
                                user_list.append(i + str(k))
                    """
                for i in user_list:
                    user_name = str(i)
                    ses = session.objects.filter(user_id=user_name).order_by("creatation_date")
                    bl_anno = block_annotation_history.objects.filter(user_id=user_name).order_by("last_date")
                    ses_time_list, anno_time_list = [0 for i in range(0,5)], [0 for i in range(0, 5)]
                    #print(user_name)
                    for bl_a in bl_anno:
                        if "exp" in str(bl_a.project_name).lower().replace(" ", ""):
                            re_an = str(bl_a.research_annotation).lower().replace(" ", "")
                            da_an = str(bl_a.data_annotation).lower().replace(" ", "")
                            if re_an.find("ans") == 0 and isNumber(re_an[3]):
                                if anno_time_list[int(re_an[3])-1] != 0:
                                    continue
                                anno_time_list[int(re_an[3])-1] = bl_a.last_date
                            elif da_an.find("ans") == 0 and isNumber(da_an[3]):
                                if anno_time_list[int(da_an[3])-1] != 0:
                                    continue
                                anno_time_list[int(da_an[3])-1] = bl_a.last_date
                    #print(anno_time_list)
                    for s in ses:
                        if "exp" in str(s.project_name).lower().replace(" ", ""):
                            session_name = str(s.session_name).lower().replace(" ", "").replace("problem", "")
                            if i == "S44":
                                session_name = str(s.session_name).lower().replace(" ", "").replace("2017-08-14 15:20:47, Problem", "").replace(" - Ver. 0", "")
                            if session_name in ["1", "2", "3", "4", "5"]:
                                if isNumber(session_name) and ses_time_list[int(session_name)-1] == 0:
                                    ses_time_list[int(session_name)-1] = s.creatation_date
                    #print(ses_time_list)
                    time_dict = {}

                    for i in range(0, 5):
                        time_dict["username"] = user_name

                        if (anno_time_list[i] != 0 and ses_time_list[i] != 0):
                            diff_time = str(anno_time_list[i] - ses_time_list[i])
                            diff_time = diff_time[0:diff_time.index(".")]
                            time_dict["problem"] = "Problem" + str(i+1)
                            time_dict["sess"] = ses_time_list[i]
                            time_dict["anno"] = anno_time_list[i]
                            time_dict["time"] = diff_time
                           # time_dict["problem" + str(i + 1)] = diff_time
                           # print (user_name + " problem" + str(i + 1) + " sess : ")
                           # print(ses_time_list[i])
                           # print (user_name + " problem" + str(i + 1) + " anno : ")
                           # print(anno_time_list[i])

                        else:
                            time_dict["problem"] = "Problem" + str(i+1)
                            time_dict["sess"] = 0
                            time_dict["anno"] = anno_time_list[i]
                            time_dict["time"] = 0
                            #time_dict["problem" + str(i + 1)] = 0

                        csvw.writerow(time_dict)

            return HttpResponse(json.dumps({'success': True, 'detail': "Answer", 'output': None}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success': False, 'detail': "Duplicated username", 'output': None}),
                                content_type="application/json")


@ensure_csrf_cookie
def get_time2(request):
    errors = []
    Session_time = [];

    if request.method == 'POST':

        if not errors:
            time_file = os.path.join(os.getcwd(), "static", "file", "time2.txt")

            with open(time_file, 'w') as wf:
                fieldnames = ['username', 'problem1', 'problem2', 'problem3', 'problem4', 'problem5']
                csvw = csv.DictWriter(wf, fieldnames = fieldnames)
                csvw.writeheader()
                user_name_list = ["A", "B"]
                user_num_list = [30, 50]
                user_list = []
                except_list = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 25, 38, 47]
                for i in user_name_list:
                    for j in user_num_list:
                        if (j == 30 and i == "A") or (j==50 and i == "B"):
                            for k in range(1, int(j)+1):
                                if i == "B" and k in except_list:
                                    continue
                                user_list.append(i + str(k))
                for i in user_list:
                    user_name = str(i)
                    ses = session.objects.filter(user_id=user_name).order_by("creatation_date")
                    bl_anno = block_annotation_history.objects.filter(user_id=user_name).order_by("last_date")
                    ses_time_list = [0 for i in range(0,5)];
                    anno_time_list = [];
                    annos = [];
                    #print(user_name)
                    for bl_a in bl_anno:
                        if "exp" in str(bl_a.project_name).lower().replace(" ", ""):
                            re_an = str(bl_a.research_annotation).lower().replace(" ", "")
                            da_an = str(bl_a.data_annotation).lower().replace(" ", "")
                            if re_an.find("ans") == 0 :
                              #  if anno_time_list[int(re_an[3])-1] != 0:
                               #     continue
                                anno_time_list.append(bl_a.last_date)
                                annos.append(re_an)
                            elif da_an.find("ans") == 0 :
                               # if anno_time_list[int(da_an[3])-1] != 0:
                               #     continue

                                anno_time_list.append(bl_a.last_date)
                                annos.append(da_an)
                    #print(anno_time_list)
                    for s in ses:
                        if "exp" in str(s.project_name).lower().replace(" ", ""):
                            session_name = str(s.session_name).lower().replace(" ", "").replace("problem", "")
                            if i == "B40":
                                session_name = str(s.session_name).lower().replace(" ", "").replace("problem", "").replace("branch", "").replace("_branch", "").replace("_branch1", "").replace("branch4", "")
                            if session_name in ["1", "2", "3", "4", "5"]:
                                if isNumber(session_name) and ses_time_list[int(session_name)-1] == 0:
                                    ses_time_list[int(session_name)-1] = s.creatation_date
                    #print(ses_time_list)

                    if user_name == "B13":
                        for i in range(5):
                          #  diff_time = str(anno_time_list[i] - ses_time_list[i])
                          #  diff_time = diff_time[0:diff_time.index(".")]
                            print(annos)
                           # print(diff_time)
                            print(len(ses_time_list))




                    time_dict = {}
                    csvw.writerow(time_dict)

            return HttpResponse(json.dumps({'success': True, 'detail': "Answer", 'output': None}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success': False, 'detail': "Duplicated username", 'output': None}),
                                content_type="application/json")


def get_time3(request):
    errors = []
    Session_time = [];

    if request.method == 'POST':

        if not errors:
            time_file = os.path.join(os.getcwd(), "static", "file", "time.csv")

            with open(time_file, 'w') as wf:
                #fieldnames = ['username', 'problem1', 'problem2', 'problem3', 'problem4', 'problem5']
                fieldnames = ['username', 'problem', 'sess', 'anno', 'time']
                csvw = csv.DictWriter(wf, fieldnames = fieldnames)
                csvw.writeheader()
                user_name_list = ["S"]
                user_num_list = 37
                user_list = []
                except_list = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 25, 30, 38, 47]
                for i in range(user_num_list):
                    user_list.append("S"+str(i+1))
                    """
                    for j in user_num_list:
                        if (j == 30 and i == "A") or (j==50 and i == "B"):
                            for k in range(1, int(j)+1):
                                if i == "B" and k in except_list:
                                    continue
                                user_list.append(i + str(k))
                    """
                for i in user_list:
                    user_name = str(i)
                    ses = session.objects.filter(user_id=user_name).order_by("creatation_date")
                    bl_anno = block_annotation_history.objects.filter(user_id=user_name).order_by("last_date")
                    ses_time_list, anno_time_list = [0 for i in range(0,3)], [0 for i in range(0, 3)]
                    #print(user_name)
                    for bl_a in bl_anno:
                        if "2" in str(bl_a.project_name).lower().replace(" ", ""):
                            re_an = str(bl_a.research_annotation).lower().replace(" ", "")
                            da_an = str(bl_a.data_annotation).lower().replace(" ", "")
                            print (user_name)
                            print (re_an)
                            print (da_an)
                            if re_an.find("ans") == 0 and isNumber(re_an[3]):
                                if anno_time_list[int(re_an[3])-1] != 0:
                                    continue
                                anno_time_list[int(re_an[3])-1] = bl_a.last_date
                            elif da_an.find("ans") == 0 and isNumber(da_an[3]):
                                if anno_time_list[int(da_an[3])-1] != 0:
                                    continue
                                anno_time_list[int(da_an[3])-1] = bl_a.last_date
                    #print(anno_time_list)
                    for s in ses:
                        if "2" in str(s.project_name).lower().replace(" ", ""):
                            session_name = str(s.session_name).lower().replace(" ", "").replace("problem", "")
                            if i == "S44":
                                session_name = str(s.session_name).lower().replace(" ", "").replace("2017-08-14 15:20:47, Problem", "").replace(" - Ver. 0", "")
                            if session_name in ["1", "2", "3"]:
                                if isNumber(session_name) and ses_time_list[int(session_name)-1] == 0:
                                    ses_time_list[int(session_name)-1] = s.creatation_date
                    #print(ses_time_list)
                    time_dict = {}

                    for i in range(0, 3):
                        time_dict["username"] = user_name

                        if (anno_time_list[i] != 0 and ses_time_list[i] != 0):
                            diff_time = str(anno_time_list[i] - ses_time_list[i])
                            diff_time = diff_time[0:diff_time.index(".")]
                            time_dict["problem"] = "Problem" + str(i+1)
                            time_dict["sess"] = ses_time_list[i]
                            time_dict["anno"] = anno_time_list[i]
                            time_dict["time"] = diff_time
                           # time_dict["problem" + str(i + 1)] = diff_time
                           # print (user_name + " problem" + str(i + 1) + " sess : ")
                           # print(ses_time_list[i])
                           # print (user_name + " problem" + str(i + 1) + " anno : ")
                           # print(anno_time_list[i])

                        else:
                            time_dict["problem"] = "Problem" + str(i+1)
                            time_dict["sess"] = 0
                            time_dict["anno"] = anno_time_list[i]
                            time_dict["time"] = 0
                            #time_dict["problem" + str(i + 1)] = 0

                        csvw.writerow(time_dict)

            return HttpResponse(json.dumps({'success': True, 'detail': "Answer", 'output': None}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success': False, 'detail': "Duplicated username", 'output': None}),
                                content_type="application/json")



"""
def get_logs(request):

    if request.method == 'POST':
        user_list = ["A", "B"]
        number_list = [23, 50]

        f = open(os.path.join(os.getcwd(), "userstudy", "stat.json"), 'w')
        anno_list = {}

        for usr in user_list:
            for num in range(1, number_list[user_list.index(usr)]):
                user_stat = {}
                user_name = usr + str(num)
                projs = project.objects.filter(user_id = user_name)
                if len(projs) == 0:
                    continue
                user_stat['user'] = user_name
                for proj in projs:
                    low_proj_name = str(proj.project_name).lower()
                    if "ex" in low_proj_name:
                        user_stat['project_name'] = proj.project_name
                        proj_block_vis_list = []

                        sess = session.objects.filter(user_id = user_name, project_name = proj.project_name)
                        for ses in sess:
                            session_stat = {}
                            session_stat['session_name'] = ses.session_name
                            ses_branch = 0
                            block_vis_list = []
                            bls = block.objects.filter(user_id = user_name, project_name = proj.project_name, session_name = ses.session_name)
                            for bl in bls:
                                block_vis_list.append(bl.vis_types)
                                proj_block_vis_list.append(bl.vis_types)
                                session_stat['vis_types'] = block_vis_list

                            logs = log_history.objects.filter(user_id = user_name, project_name = proj.project_name, session_name = ses.session_name)
                            for log in logs:
                                if log.action == "Branch-Unit":
                                    ses_branch = ses_branch + 1


                user_stat_list.append(user_stat)
        stat_list['stat'] = user_stat_list
        f.write(json.dumps(stat_list))
        f.close()
        return HttpResponse(json.dumps({'success': True, 'detail': "Get Unit information.", 'output': None}),
                            content_type="application/json")
"""

@ensure_csrf_cookie
def sequence(request):
    """
    index_value html
    """
    return render(request, 'sequence.html')