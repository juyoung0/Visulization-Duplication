from heatmap import *

@ensure_csrf_cookie
def create_session(request):
    """
    New added session_name input
    """
    errors = []
    if request.method == 'POST':
        # check information
        param_list = ['username', 'project_name', 'session_name']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get parameter
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            # check existence
            try:
                user = member.objects.get(user_id = username)
            except member.DoesNotExist:
                user = None

            if not user:
                return HttpResponse(json.dumps({'success' : False, 'detail' : "No user.", 'output' : None}) ,content_type="application/json")
            # check existence
            try:
                proj = project.objects.get(user_id=username, project_name = project_name)
            except project.DoesNotExist:
                proj = None

            if not proj:
                return HttpResponse(json.dumps({'success' : False, 'detail' : "No project.", 'output' : None}) ,content_type="application/json")
            else:
                # check existence
                ses = session.objects.filter(user_id = username, project_name = project_name, session_name = session_name)
                if len(ses) > 0:
                    ses_info = []
                    ses_info_elem = {}
                    ses_info_elem['username'] = username
                    ses_info_elem['project_name'] = project_name
                    ses_info_elem['session_name'] = session_name
                    ses_info.append(ses_info_elem)
                    return HttpResponse(json.dumps({'success' : False, 'detail' : "Duplicated session.", 'output' : ses_info}) ,content_type="application/json")
                else:
                    if not request.POST.get('session_annotation', ''):
                        session_annotation = None
                        ses = session(user_id = user.user_id, project_name = project_name, session_name = session_name)
                        ses_his = session_history(user_id = user.user_id, project_name = project_name, session_name = session_name)
                    else:
                        session_annotation = '%r' % request.POST['session_annotation']
                        session_annotation = session_annotation.replace('\'', '')
                        ses = session(user_id = user.user_id, project_name = project_name, session_name = session_name, session_annotation = session_annotation)
                        ses_his = session_history(user_id = user.user_id, project_name = project_name, session_name = session_name, session_annotation = session_annotation)
                    now = datetime.datetime.now()
                    ses.save()
                    ses_his.save() 
                    ses_info = []
                    ses_info_elem = {}
                    ses_info_elem['username'] = username
                    ses_info_elem['project_name'] = project_name
                    ses_info_elem['session_name'] = session_name
                    ses_info_elem['date'] = now.strftime("%Y-%m-%d %H:%M:%S")
                    ses_info_elem['session_annotation'] = session_annotation
                    ses_info.append(ses_info_elem)
                    # create directory
                    try:
                        os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, str(session_name)))
                        os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, str(session_name), '0'))
                        #renew the last_date of project and session
                        proj_rn = project.objects.filter(user_id = username, project_name = project_name)
                        proj_rn.update(last_date = datetime.datetime.now())
                        ses_rn = session.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = 0)
                        ses_rn.update(last_date = datetime.datetime.now())
                        return HttpResponse(json.dumps({'success' : True, 'detail' : "Created session.", 'output' : ses_info}) ,content_type="application/json")
                    except OSError as e:
                        if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member')) is False:
                            os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member'))
                        if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username)) is False:
                            os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username))
                        if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name)) is False:
                            os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name))
                            os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, str(session_name)))
                            os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, str(session_name),'0'))
                        if e.errno == 17:
                            pass
                        return HttpResponse(json.dumps({'success' : False, 'detail' : "No path.", 'output' : ses_info}) ,content_type="application/json")

        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : "No user or No session name.", 'output' : errors}) ,content_type="application/json")

@ensure_csrf_cookie
def delete_session(request):
    """
    New added session_name input
    """
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
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            # delete sesion and block in the db
            try:
                ses = session.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
                ses_his = session_history.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
                blocks = block.objects.all().filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
                log_history.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), is_closed = False).update(is_closed = True)
                bl_anno = block_annotation_history.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver)).update(is_removed = True)
                blocks.delete()
                ses.delete()
                ses_his.delete()
                # delete directory
                shutil.rmtree(os.path.join(os.getcwd(), BASE_DIR, 'member', str(username), str(project_name), str(session_name), str(session_ver)))
                #renew the last_date of project and session
                proj_rn = project.objects.filter(user_id = username, project_name = project_name)
                proj_rn.update(last_date = datetime.datetime.now())
                ses_rn = session.objects.filter(user_id = username, project_name = project_name, session_name = session_name)
                ses_rn.update(last_date = datetime.datetime.now())
                return HttpResponse(json.dumps({'success' : True, 'detail' : "Deleted session.", 'output' : None}) ,content_type="application/json")

            except session.DoesNotExist:
                ses = None
                return HttpResponse(json.dumps({'success' : False, 'detail' : "No session.", 'output' : None}) ,content_type="application/json")


@ensure_csrf_cookie
@gzip_page
def get_session(request):
    errors = []
    username = ""
    if request.method == 'POST':
        # check information
        param_list = ['username', 'project_name']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get parameter
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            # get sessions
            ses = session_history.objects.filter(user_id=username, project_name = project_name).values('session_name', 'session_ver', 'session_annotation', 'last_date').order_by('-last_date')
            # check existence of session
            if ses.exists():
                sessions = []
                ses_name_list = []
                ses_ver_list = []
                ses_date_list = []
                ses_anno_list = []
                for i in ses:
                    try:
                        os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, str(i['session_name'])))
                        os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, str(i['session_name']), str(i['session_ver'])))
                    except OSError as e:
                        if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member')) is False:
                            os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member'))
                        if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username)) is False:
                            os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username))
                        if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name)) is False:
                            os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name))
                            os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, str(i['session_name'])))
                            os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, str(i['session_name']), str(i['session_ver'])))
                        if e.errno == 17:
                            pass
                    ses_elem = {}
                    ses_date = i['last_date'].strftime("%Y-%m-%d %H:%M:%S")
                    ses_elem['username'] = username
                    ses_elem['project_name'] = project_name
                    ses_elem['session_name'] = i['session_name']
                    ses_elem['session_ver'] = int(i['session_ver'])
                    ses_elem['session_annotation'] = i['session_annotation']
                    ses_elem['lastEdited'] = ses_date
                    sessions.append(ses_elem)
                    """
                    if i['session_name'] not in ses_name_list:
                        ses_name_list.append(i['session_name'])
                        ses_ver_list.append(int(i['session_ver']))
                        ses_date_list.append(i['last_date'].strftime("%Y-%m-%d %H:%M:%S"))
                        ses_anno_list.append(i['session_annotation'])
                    else:
                        if ses_ver_list[ses_name_list.index(i['session_name'])] < i['session_ver']:
                            ses_ver_list[ses_name_list.index(i['session_name'])] = i['session_ver']
                            ses_date_list.append(i['last_date'].strftime("%Y-%m-%d %H:%M:%S"))
                            ses_anno_list.append(i['session_annotation'])
                print(ses_name_list)
                print(ses_ver_list)
                print(ses_date_list)
                for i in ses_name_list:
                    print(ses_name_list.index(i))
                    ses_elem = {}
                    ses_date = ses_date_list[ses_name_list.index(i)]
                    ses_elem['username'] = username
                    ses_elem['project_name'] = project_name
                    ses_elem['session_name'] = i
                    ses_elem['session_ver'] = ses_ver_list[ses_name_list.index(i)]
                    ses_elem['session_annotation'] = ses_anno_list[ses_name_list.index(i)]
                    ses_elem['lastEdited'] = ses_date
                    sessions.append(ses_elem)
                """
                return HttpResponse(json.dumps({'success' : True, 'detail' : "Get session.", 'output' : sessions}) ,content_type="application/json")
            else:
                ses = None
                return HttpResponse(json.dumps({'success' : True, 'detail' : "No session.", 'output' : None}) ,content_type="application/json")

@ensure_csrf_cookie
def save_session(request):
    """
    Get session blocks
    """
    errors = []
    username = ""
    project_name = ""
    session_name = ""
    session_ver = 0
    if request.method == 'POST':
        # check information
        param_list = ['username', 'project_name','session_name', 'session_ver']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get parameter
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            if not request.POST.get('do_save'):
                do_save = True
            else:
                do_save = '%r' % request.POST['do_save']
                do_save = do_save.replace('\'', '')
            do_save = True
            if do_save is True:
                # check there is a block list or not
                if not request.POST.get('block_list'):
                    block_list = None
                else:
                    block_list = request.POST.get('block_list')
                    block_list = eval(block_list)
                now = datetime.datetime.now()

                get_ses = session.objects.filter(user_id=username, project_name=project_name,
                                              session_name=session_name).aggregate(Max('session_ver'))
                max_ses_ver = get_ses['session_ver__max']
                if int(session_ver) < max_ses_ver:
                    return HttpResponse(
                        json.dumps({'success': True, 'detail': "This is not last session.\n Save after session branch.", 'output': None}),
                        content_type="application/json")
                try:
                    du_ses = session.objects.get(user_id = username, project_name = project_name,
                                                 session_name = session_name, session_ver = int(session_ver)+1)
                    ses_info = []
                    ses_info_elem = {}
                    ses_info_elem['username'] = username
                    ses_info_elem['project_name'] = project_name
                    ses_info_elem['session_name'] = session_name
                    ses_info_elem['session_ver'] = session_ver
                    ses_info.append(ses_info_elem)
                    return HttpResponse(json.dumps({'success' : False, 'detail' : "Duplicated a session.", 'output' : ses_info}) ,content_type="application/json")
                except session.DoesNotExist:
                    du_ses = None
                # insert session and block in the session and session_history tables
                ses = session.objects.filter(user_id = username, project_name = project_name,
                                             session_name = session_name, session_ver = int(session_ver)).update(session_ver = int(session_ver)+1, last_date = now)
                cur_bls = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
                cur_bl_list = []
                for cur_bl in cur_bls:
                    cur_bl_elem = {}
                    cur_bl_elem['block_iden'] = cur_bl.block_iden
                    cur_bl_elem['block_ver'] = int(cur_bl.block_ver)
                    cur_bl_list.append(cur_bl_elem)
                ses_his = session_history(user_id = username, project_name = project_name,
                                             session_name = session_name, session_ver = int(session_ver)+1, last_date = now, block_list = block_list, prev_block_list = cur_bl_list)
                ses_his.save()

                # get blocks
                bl = block.objects.filter(user_id = username, project_name = project_name,
                                          session_name = session_name, session_ver = int(session_ver)).order_by('last_date')

                # update blocks
                for i in bl:
                    new_obj = i
                    new_obj.block_id = None
                    new_obj.save()
                    new_obj = block.objects.filter(block_id=new_obj.block_id)
                    # update several vis information according to vis_types
                    if new_obj[0].vis_types == "Parallel Coordinate Plot":
                        pcp_obj = pcp.objects.get(pcp_id = new_obj[0].pcp_id)
                        new_pcp_obj = pcp_obj
                        new_pcp_obj.pcp_id = None
                        new_pcp_obj.save()
                        new_obj.update(pcp_id = new_pcp_obj.pcp_id)
                    elif new_obj[0].vis_types == "Scatterplot Matrix":
                        scm_obj = scm.objects.get(scm_id = new_obj[0].scm_id)
                        new_scm_obj = scm_obj
                        new_scm_obj.scm_id = None
                        new_scm_obj.save()
                        new_obj.update(scm_id=new_scm_obj.scm_id)
                    elif new_obj[0].vis_types == "Scatter Plot":
                        sp_obj = sp.objects.get(sp_id=new_obj[0].sp_id)
                        new_sp_obj = sp_obj
                        new_sp_obj.sp_id = None
                        new_sp_obj.save()
                        new_obj.update(sp_id=new_sp_obj.sp_id)
                    new_obj.update(session_ver = int(session_ver)+1, last_date = datetime.datetime.now())

                bl_anno = block_annotation_history.objects.filter(user_id = username, project_name = project_name,
                                                                  session_name = session_name, session_ver = int(session_ver),
                                                                  is_removed = False)
                for i in bl_anno:
                    new_bl_anno = block_annotation_history(user_id = i.user_id, project_name = i.project_name,
                                                           session_name = i.session_name, session_ver = int(i.session_ver)+1,
                                                           block_iden = i.block_iden, block_ver = 0,
                                                           author = i.author, data_annotation = i.data_annotation,
                                                           research_annotation = i.research_annotation, annotation_num = i.annotation_num, experiment_type = i.experiment_type, platform_name = i.platform_name, organism = i.organism)
                    new_bl_anno.save()

                bl_log = log_history.objects.filter(scope='unit', user_id = username, project_name = project_name,
                                                    session_name = session_name, session_ver = int(session_ver)).exclude(action='Select-Unit')
                for i in bl_log:
                    new_bl_obj = i
                    new_bl_obj.action_id = None
                    new_bl_obj.save()
                    new_bl_obj = log_history.objects.filter(action_id=new_bl_obj.action_id)
                    new_bl_obj.update(creatation_date = datetime.datetime.now())
                    if new_bl_obj[0].block_iden is not None:
                        # get block in order to know pcp_id or scm_id
                        get_bl_vis_id = block.objects.filter(user_id = username, project_name = project_name,
                                                          session_name = session_name, session_ver = int(session_ver)+1,
                                                          block_iden = i.block_iden, block_ver = int(i.block_ver))
                        if len(get_bl_vis_id) > 0:
                            # update several vis information according to vis_types
                            if new_bl_obj[0].vis_types == "Parallel Coordinate Plot":
                                pcp_obj = pcp.objects.get(pcp_id = get_bl_vis_id[0].pcp_id)
                                new_bl_obj.update(pcp_id=pcp_obj.pcp_id, creatation_date = datetime.datetime.now())
                            elif new_bl_obj[0].vis_types == "Scatterplot Matrix":
                                scm_obj = scm.objects.get(scm_id = get_bl_vis_id[0].scm_id)
                                new_bl_obj.update(scm_id=scm_obj.scm_id, creatation_date = datetime.datetime.now())
                            elif new_bl_obj[0].vis_types == "Scatter Plot":
                                sp_obj = sp.objects.get(sp_id = get_bl_vis_id[0].sp_id)
                                new_bl_obj.update(sp_id=sp_obj.sp_id, creatation_date = datetime.datetime.now())
                            new_bl_obj.update(session_ver=int(session_ver) + 1)
                        else:
                            new_bl_obj.delete()

                # make preview units saved units
                if block_list is not None:
                    for j in block_list:
                        cur_get_bl = block.objects.filter(user_id=username, project_name=project_name,
                                                          session_name=session_name, session_ver=int(session_ver),
                                                          block_iden=j).aggregate(Max('block_ver'))
                        cur_max_bl_ver = cur_get_bl['block_ver__max']
                        cur_not_saved_bl = block.objects.filter(user_id=username, project_name=project_name,
                                                                session_name=session_name,
                                                                session_ver=int(session_ver),
                                                                block_iden=j, block_ver=int(cur_max_bl_ver)).update(
                            is_save=True, save_ver=0)
                        get_bl = block.objects.filter(user_id = username, project_name = project_name,
                                                      session_name = session_name, session_ver = int(session_ver) + 1,
                                                      block_iden = j).aggregate(Max('block_ver'))
                        max_bl_ver = get_bl['block_ver__max']
                        not_saved_bl = block.objects.filter(user_id = username, project_name = project_name,
                                                            session_name = session_name, session_ver = int(session_ver) + 1,
                                                            block_iden = j, block_ver = int(max_bl_ver)).update(is_save = True, save_ver = 0)


                ses_info = []
                ses_info_elem = {}
                ses_info_elem['username'] = username
                ses_info_elem['project_name'] = project_name
                ses_info_elem['session_name'] = session_name
                ses_info_elem['session_ver'] = session_ver
                ses_info_elem['date'] = now.strftime("%Y-%m-%d %H:%M:%S")
                ses_info_elem['block_list'] = block_list
                ses_info.append(ses_info_elem)
                src_path = os.path.join(BASE_DIR, "member", str(username), str(project_name),
                                                str(session_name), str(session_ver))
                dst_path = os.path.join(BASE_DIR, "member", str(username), str(project_name),
                                                str(session_name), str(int(session_ver)+1))
                shutil.copytree(src_path, dst_path)
                for i in bl:
                    file_path = os.path.join("static", "member", str(username), str(project_name),
                                                 str(session_name), str(int(session_ver)+1),
                                                 i.block_iden, str(i.block_ver))
                    anno_path = os.path.join("static", "member", str(username), str(project_name),
                                             str(session_name), str(int(session_ver) + 1),
                                             i.block_iden)
                    if i.vis_types == "Heatmap":
                        if os.path.exists(os.path.join(dst_path, i.block_iden, str(i.block_ver), "clusters.json")) is True:
                            infile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "clusters.json"), "r")
                            content = infile.readlines()
                            json_info = json.loads(content[0])
                            if not i.clusterType == "Hierarchy":
                                heatmap_path = os.path.join(file_path, "clusters.json")
                                annotation_path = os.path.join(anno_path, "annotation.json")
                                response_json = [{"cluster_data":json_info['response'][0]['cluster_data'], "label":json_info['response'][0]['label'],
                                                  "min":json_info['response'][0]['min'], "max":json_info['response'][0]["max"],
                                                  "name_data":json_info['response'][0]["name_data"], "heatmap_path":heatmap_path ,
                                                  "annotation_path":annotation_path , "block_ver" : json_info['response'][0]['block_ver'],
                                                  "vis_types": json_info['response'][0]['vis_types']}]
                            else:
                                heatmap_path = os.path.join(file_path, "clusters.json")
                                annotation_path = os.path.join(anno_path, "annotation.json")
                                dendro_path = os.path.join(file_path, i.clusterType + ".csv")
                                dendro_col_path = os.path.join(file_path, i.clusterType + "Col.csv")
                                response_json = [{"cluster_data":json_info['response'][0]['cluster_data'], "label":json_info['response'][0]['label'],
                                                  "min":json_info['response'][0]['min'], "max":json_info['response'][0]["max"],
                                                  "name_data":json_info['response'][0]["name_data"], "heatmap_path":heatmap_path ,
                                                  "dendro_data":json_info['response'][0]["dendro_data"], "dendro_path":dendro_path, "dendro_col_path":dendro_col_path,
                                                  "annotation_path":annotation_path , "block_ver" : json_info['response'][0]['block_ver'],
                                                  "vis_types": json_info['response'][0]['vis_types']}]
                            heatmap_json = json.dumps({"request" : json_info['request'], "response" : response_json, "position" : json_info['position']})
                            infile.close()
                            wfile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "clusters.json"), "w")
                            wfile.write(heatmap_json)
                    elif i.vis_types == "Parallel Coordinate Plot":
                        if os.path.exists(os.path.join(dst_path, i.block_iden, str(i.block_ver), "pcp.json")) is True:
                            infile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "pcp.json"), "r")
                            content = infile.readlines()
                            json_info = json.loads(content[0])
                            pcp_path = os.path.join(file_path, "pcp.json")
                            annotation_path = os.path.join(anno_path, "annotation.json")
                            response_json = [{"pcp_path": pcp_path,
                                              "column_order": json_info['response'][0]['column_order'],
                                              "brushed_axis": json_info['response'][0]['brushed_axis'],
                                              "brushed_range": json_info['response'][0]['brushed_range'],
                                              "annotation_path": annotation_path,
                                              "block_ver": json_info['response'][0]["block_ver"],
                                              "data": json_info['response'][0]["data"],
                                              "selected_index": "",
                                              "vis_types": json_info['response'][0]['vis_types']
                                              }]
                            pcp_json = json.dumps(
                                {"request": json_info['request'], "response": response_json, "position": json_info['position']})
                            infile.close()
                            wfile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "pcp.json"), "w")
                            wfile.write(pcp_json)
                    elif i.vis_types == "Scatterplot Matrix":
                        if os.path.exists(os.path.join(dst_path, i.block_iden, str(i.block_ver), "scm.json")) is True:
                            infile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "scm.json"), "r")
                            content = infile.readlines()
                            json_info = json.loads(content[0])
                            scm_path = os.path.join(file_path, "scm.json")
                            annotation_path = os.path.join(anno_path, "annotation.json")
                            response_json = [{"scm_path": scm_path,
                                              "brushed_axis": json_info['response'][0]['brushed_axis'],
                                              "brushed_range": json_info['response'][0]['brushed_range'],
                                              "annotation_path": annotation_path,
                                              "block_ver": json_info['response'][0]["block_ver"],
                                              "data": json_info['response'][0]["data"],
                                              "selected_index": "",
                                              "vis_types": json_info['response'][0]['vis_types']
                                              }]
                            scm_json = json.dumps(
                                {"request": json_info['request'], "response": response_json, "position": json_info['position']})
                            infile.close()
                            wfile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "scm.json"), "w")
                            wfile.write(scm_json)
                    elif i.vis_types == "Scatter Plot":
                        if os.path.exists(
                                os.path.join(dst_path, i.block_iden, str(i.block_ver), "sp.json")) is True:
                            infile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "sp.json"),
                                            "r")
                            content = infile.readlines()
                            json_info = json.loads(content[0])
                            sp_path = os.path.join(file_path, "sp.json")
                            annotation_path = os.path.join(anno_path, "annotation.json")
                            response_json = [{"sp_path": sp_path,
                                                  "brushed_range": json_info['response'][0]['brushed_range'],
                                                  "annotation_path": annotation_path,
                                                  "block_ver": json_info['response'][0]["block_ver"],
                                                  "data": json_info['response'][0]["data"],
                                                  "selected_index": json_info['response'][0]['selected_index'],
                                                  "vis_types": json_info['response'][0]['vis_types'],
                                                  "x_axis": json_info['response'][0]['x_axis'],
                                                  "y_axis": json_info['response'][0]['y_axis']
                                                  }]
                            sp_json = json.dumps(
                                    {"request": json_info['request'], "response": response_json,
                                    "position": json_info['position']})
                            infile.close()
                            wfile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "sp.json"),
                                                 "w")
                            wfile.write(sp_json)

                #renew the last_date of project and session
                proj_rn = project.objects.filter(user_id = username, project_name = project_name)
                proj_rn.update(last_date = datetime.datetime.now())
                ses_rn = session.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
                ses_rn.update(last_date = datetime.datetime.now())
                return HttpResponse(json.dumps({'success' : True, 'detail' : "Saved a session.", 'output' : ses_info}) ,content_type="application/json")
            else:
                ses = session_history.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
                prev_bls = eval(json.loads(json.dumps(ses[0].prev_block_list)))
                total_bls = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
                added_list = []
                for i in total_bls:
                    is_same = False
                    for j in prev_bls:
                        if j['block_iden'] == i.block_iden and j['block_ver'] == i.block_ver:
                            is_same = True
                    if is_same == False:
                        total_elem = {}
                        total_elem['block_iden'] = i.block_iden
                        total_elem['block_ver'] = int(i.block_ver)
                        added_list.append(total_elem)
                for i in added_list:
                    added_bl = block.objects.filter(user_id = username, project_name = project_name,
                                         session_name = session_name, session_ver = int(session_ver),
                                         block_iden = i['block_iden'], block_ver = int(i['block_ver']), is_closed=False)
                    added_bl.delete()
                    added_log = log_history.objects.filter(user_id = username, project_name = project_name,
                                         session_name = session_name, session_ver = int(session_ver),
                                         block_iden = i['block_iden'], block_ver = int(i['block_ver']), is_closed=False)
                    added_log.delete()
                    if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name,
                                                     str(session_ver), str(i['block_iden']), str(i['block_ver']))) is True:
                        shutil.rmtree(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name,
                                                     str(session_ver), str(i['block_iden']), str(i['block_ver'])))
                return HttpResponse(json.dumps({'success': True, 'detail': "Deleted a units.", 'output': None}),
                                    content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

@ensure_csrf_cookie
def branch_session(request):
    """
    branch session (save as)
    """
    errors = []
    username = ""
    project_name = ""
    session_name = ""
    session_ver = 0
    if request.method == 'POST':
        param_list = ['username', 'project_name', 'session_name', 'parent_session_name', 'parent_session_ver']
        errors = param_checker(request, errors, param_list)
        if not errors:
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            parent_session_name = '%r' % request.POST['parent_session_name']
            parent_session_name = parent_session_name.replace('\'', '')
            parent_session_ver = '%r' % request.POST['parent_session_ver']
            parent_session_ver = parent_session_ver.replace('\'', '')
            now = datetime.datetime.now()
            try:
                du_ses = session.objects.get(user_id=username, project_name=project_name,
                                             session_name=session_name, session_ver=0)
                ses_info = []
                ses_info_elem = {}
                ses_info_elem['username'] = username
                ses_info_elem['project_name'] = project_name
                ses_info_elem['session_name'] = session_name
                ses_info_elem['session_ver'] = session_ver
                ses_info.append(ses_info_elem)
                return HttpResponse(
                    json.dumps({'success': False, 'detail': "Duplicated a session.", 'output': ses_info}),
                    content_type="application/json")
            except session.DoesNotExist:
                du_ses = None
            if int(parent_session_ver) == 0:
                ses = session(user_id=username, project_name=project_name, last_date=now, session_name=session_name,
                              parent_session_name=parent_session_name, parent_session_ver=parent_session_ver,
                              branched_date=now, is_first = True)
            else:
                parent_session_ver = int(parent_session_ver) - 1
                ses = session(user_id=username, project_name=project_name, last_date=now, session_name=session_name,
                              parent_session_name=parent_session_name, parent_session_ver=parent_session_ver,
                              branched_date=now)

            ses.save()
            get_ses = session_history.objects.filter(user_id = username, project_name = project_name, session_name = parent_session_name, session_ver = int(parent_session_ver)).values('project_name', 'session_name', 'session_ver', 'block_list').annotate(last_date = Max('last_date')).distinct().order_by('last_date')

            if 'block_list' in get_ses[0]:
                ses_his = session_history(user_id=username, project_name=project_name, session_name=session_name,
                                          session_ver=0, block_list=get_ses[0]['block_list'])
            else:
                ses_his = session_history(user_id=username, project_name=project_name, session_name=session_name,
                                          session_ver=0)
            ses_his.save()

            # get blocks
            bl = block.objects.filter(user_id=username, project_name=project_name,
                                          session_name=parent_session_name, session_ver=int(parent_session_ver)).order_by('last_date')

            # update blocks
            for i in bl:
                new_obj = i
                new_obj.block_id = None
                new_obj.save()
                new_obj = block.objects.filter(block_id=new_obj.block_id).order_by('-last_date')
                # update several vis information according to vis_types
                if new_obj[0].vis_types == "Parallel Coordinate Plot":
                    pcp_obj = pcp.objects.get(pcp_id = new_obj[0].pcp_id)
                    new_pcp_obj = pcp_obj
                    new_pcp_obj.pcp_id = None
                    new_pcp_obj.save()
                    new_obj.update(pcp_id=new_pcp_obj.pcp_id)
                elif new_obj[0].vis_types == "Scatterplot Matrix":
                    scm_obj = scm.objects.get(scm_id = new_obj[0].scm_id)
                    new_scm_obj = scm_obj
                    new_scm_obj.scm_id = None
                    new_scm_obj.save()
                    new_obj.update(scm_id=new_scm_obj.scm_id)
                elif new_obj[0].vis_types == "Scatter Plot":
                    sp_obj = sp.objects.get(sp_id = new_obj[0].sp_id)
                    new_sp_obj = sp_obj
                    new_sp_obj.sp_id = None
                    new_sp_obj.save()
                    new_obj.update(sp_id=new_sp_obj.sp_id)
                new_obj.update(session_name = session_name, session_ver = 0, last_date = datetime.datetime.now())

            bl_anno = block_annotation_history.objects.filter(user_id = username, project_name = project_name, session_name = parent_session_name, session_ver = int(parent_session_ver))
            for i in bl_anno:
                new_bl_anno = block_annotation_history(user_id = i.user_id, project_name = i.project_name, session_name = session_name, session_ver = 0, block_iden = i.block_iden, block_ver = 0, author = i.author, data_annotation = i.data_annotation, research_annotation = i.research_annotation, annotation_num = i.annotation_num, experiment_type = i.experiment_type, platform_name = i.platform_name, organism = i.organism)
                new_bl_anno.save()

            # store log history
            bl_log = log_history.objects.filter(scope='unit', user_id=username, project_name=project_name,
                                                    session_name=parent_session_name,
                                                    session_ver=int(parent_session_ver)).order_by(
                    'creatation_date')

            for i in bl_log:
                new_bl_log = i
                new_bl_log.action_id = None
                new_bl_log.save()
                new_bl_log = log_history.objects.filter(action_id=new_bl_log.action_id)
                new_bl_log.update(session_name=session_name, session_ver=0, creatation_date=datetime.datetime.now())
                if i.block_iden is not None and i.block_ver is not None:
                    # get block in order to know pcp_id or scm_id
                    get_bl_vis_id = block.objects.filter(user_id=username, project_name=project_name,
                                                          session_name=session_name, session_ver=int(0),
                                                          block_iden=i.block_iden, block_ver=int(i.block_ver))
                    if len(get_bl_vis_id) > 0:
                        # update several vis information according to vis_types
                        if new_bl_log[0].vis_types == "Parallel Coordinate Plot":
                            pcp_obj = pcp.objects.get(pcp_id=get_bl_vis_id[0].pcp_id)
                            new_bl_log.update(pcp_id=pcp_obj.pcp_id)
                        elif new_bl_log[0].vis_types == "Scatterplot Matrix":
                            scm_obj = scm.objects.get(scm_id=get_bl_vis_id[0].scm_id)
                            new_bl_log.update(scm_id=scm_obj.scm_id)
                        elif new_bl_log[0].vis_types == "Scatter Plot":
                            sp_obj = sp.objects.get(sp_id=get_bl_vis_id[0].sp_id)
                            new_bl_log.update(sp_id=sp_obj.sp_id)
                        new_bl_log.update(session_ver=int(0), creatation_date = datetime.datetime.now())
                    else:
                        new_bl_log.delete()

            # modify parent position
            if parent_session_name is not None:
                p_ses = session.objects.filter(user_id=username, project_name=project_name,
                                            session_name=parent_session_name, session_ver=int(parent_session_ver))
                if len(p_ses) > 0:
                    if p_ses[0].parent_session_name is not None:
                        is_first_child = False
                        ses.__dict__.update(parent_session_name=p_ses[0].parent_session_name,
                                            parent_session_ver=int(p_ses[0].parent_session_ver),
                                            is_first=is_first_child)
                        ses.save()

            bls = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(0))

            ses_info = []
            ses_info_elem = {}
            ses_info_elem['username'] = username
            ses_info_elem['project_name'] = project_name
            ses_info_elem['session_name'] = session_name
            ses_info_elem['session_ver'] = 0
            ses_info_elem['date'] = now.strftime("%Y-%m-%d %H:%M:%S")
            ses_info_elem['block_list'] = get_ses[0]['block_list']
            ses_info.append(ses_info_elem)
            src_path = os.path.join(BASE_DIR, "member", str(username), str(project_name), str(parent_session_name), str(parent_session_ver))
            dst_path = os.path.join(BASE_DIR, "member", str(username), str(project_name), str(session_name), str(int(0)))
            shutil.copytree(src_path, dst_path)
            for i in bl:
                file_path = os.path.join("static", "member", str(username), str(project_name),
                                         str(session_name), str(0),
                                         i.block_iden, str(i.block_ver))
                anno_path = os.path.join("static", "member", str(username), str(project_name),
                                         str(session_name), str(0),
                                         i.block_iden, str(0))
                if i.vis_types == "Heatmap":
                    if os.path.exists(os.path.join(dst_path, i.block_iden, str(i.block_ver), "clusters.json")) is True:
                        infile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "clusters.json"), "r")
                        content = infile.readlines()
                        json_info = json.loads(content[0])
                        if not i.clusterType == "Hierarchy":
                            heatmap_path = os.path.join(file_path, "clusters.json")
                            annotation_path = os.path.join(anno_path, "annotation.json")
                            response_json = [{"cluster_data":json_info['response'][0]['cluster_data'], "label":json_info['response'][0]['label'],
                                              "min":json_info['response'][0]['min'], "max":json_info['response'][0]["max"],
                                              "name_data":json_info['response'][0]["name_data"], "heatmap_path":heatmap_path ,
                                              "annotation_path":annotation_path , "block_ver" : json_info['response'][0]['block_ver'],
                                              "vis_types": json_info['response'][0]['vis_types']}]
                        else:
                            heatmap_path = os.path.join(file_path, "clusters.json")
                            annotation_path = os.path.join(anno_path, "annotation.json")
                            dendro_path = os.path.join(file_path, i.clusterType + ".csv")
                            dendro_col_path = os.path.join(file_path, i.clusterType + "Col.csv")
                            response_json = [{"cluster_data":json_info['response'][0]['cluster_data'], "label":json_info['response'][0]['label'],
                                              "min":json_info['response'][0]['min'], "max":json_info['response'][0]["max"],
                                              "name_data":json_info['response'][0]["name_data"], "heatmap_path":heatmap_path ,
                                              "dendro_data":json_info['response'][0]["dendro_data"], "dendro_path":dendro_path, "dendro_col_path":dendro_col_path,
                                              "annotation_path":annotation_path , "block_ver" : json_info['response'][0]['block_ver'],
                                              "vis_types": json_info['response'][0]['vis_types']}]
                            heatmap_json = json.dumps({"request" : json_info['request'], "response" : response_json, "position" : json_info['position'],})
                            infile.close()
                            wfile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "clusters.json"), "w")
                            wfile.write(heatmap_json)
                elif i.vis_types == "Parallel Coordinate Plot":
                    if os.path.exists(os.path.join(dst_path, i.block_iden, str(i.block_ver), "pcp.json")) is True:
                        infile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "pcp.json"), "r")
                        content = infile.readlines()
                        json_info = json.loads(content[0])
                        pcp_path = os.path.join(file_path, "pcp.json")
                        annotation_path = os.path.join(anno_path, "annotation.json")
                        response_json = [{"pcp_path": pcp_path,
                                          "column_order": json_info['response'][0]['column_order'],
                                          "brushed_axis": json_info['response'][0]['brushed_axis'],
                                          "brushed_range": json_info['response'][0]['brushed_range'],
                                          "annotation_path": annotation_path,
                                          "block_ver": json_info['response'][0]["block_ver"],
                                          "data": json_info['response'][0]["data"],
                                          "selected_index": "",
                                          "vis_types": json_info['response'][0]['vis_types']
                                          }]
                        pcp_json = json.dumps(
                            {"request": json_info['request'], "response": response_json, "position": json_info['position']})
                        infile.close()
                        wfile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "pcp.json"), "w")
                        wfile.write(pcp_json)
                elif i.vis_types == "Scatterplot Matrix":
                    if os.path.exists(os.path.join(dst_path, i.block_iden, str(i.block_ver), "scm.json")) is True:
                        infile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "scm.json"), "r")
                        content = infile.readlines()
                        json_info = json.loads(content[0])
                        scm_path = os.path.join(file_path, "scm.json")
                        annotation_path = os.path.join(anno_path, "annotation.json")
                        response_json = [{"scm_path": scm_path,
                                          "annotation_path": annotation_path,
                                          "brushed_axis": json_info['response'][0]['brushed_axis'],
                                          "brushed_range": json_info['response'][0]['brushed_range'],
                                          "block_ver": json_info['response'][0]["block_ver"],
                                          "data": json_info['response'][0]["data"],
                                          "selected_index": "",
                                          "vis_types": json_info['response'][0]['vis_types']
                                          }]
                        scm_json = json.dumps(
                            {"request": json_info['request'], "response": response_json, "position": json_info['position']})
                        infile.close()
                        wfile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "scm.json"), "w")
                        wfile.write(scm_json)
                elif i.vis_types == "Scatter Plot":
                    if os.path.exists(
                            os.path.join(dst_path, i.block_iden, str(i.block_ver), "sp.json")) is True:
                        infile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "sp.json"),
                                        "r")
                        content = infile.readlines()
                        json_info = json.loads(content[0])
                        sp_path = os.path.join(file_path, "sp.json")
                        annotation_path = os.path.join(anno_path, "annotation.json")
                        response_json = [{"sp_path": sp_path,
                                          "brushed_range": json_info['response'][0]['brushed_range'],
                                          "annotation_path": annotation_path,
                                          "block_ver": json_info['response'][0]["block_ver"],
                                          "data": json_info['response'][0]["data"],
                                          "vis_types": json_info['response'][0]['vis_types'],
                                          "x_axis": json_info['response'][0]['x_axis'],
                                          "y_axis": json_info['response'][0]['y_axis']
                                          }]
                        sp_json = json.dumps(
                            {"request": json_info['request'], "response": response_json,
                            "position": json_info['position']})
                        infile.close()
                        wfile = open(os.path.join(dst_path, i.block_iden, str(i.block_ver), "sp.json"),
                                        "w")
                        wfile.write(sp_json)

            #renew the last_date of project and session
            proj_rn = project.objects.filter(user_id = username, project_name = project_name)
            proj_rn.update(last_date = datetime.datetime.now())
            ses_rn = session.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(0))
            ses_rn.update(last_date = datetime.datetime.now())
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Branched a session.", 'output' : ses_info}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")


def update_session_annotation(request):
    """
    Update Session Annotation
    """
    errors = []
    username = ""
    project_name = ""
    session_name = ""
    if request.method == 'POST':
        # check information
        param_list = ['username', 'project_name', 'session_name']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get parameter
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            # check existence
            try:
                user = member.objects.get(user_id = username)
            except member.DoesNotExist:
                user = None

            if not user:
                return HttpResponse(json.dumps({'success' : False, 'detail' : "No user.", 'output' : None}) ,content_type="application/json")
            # check existence
            try:
                proj = project.objects.get(user_id=username, project_name = project_name)
            except project.DoesNotExist:
                proj = None

            if not proj:
                return HttpResponse(json.dumps({'success' : False, 'detail' : "No project.", 'output' : None}) ,content_type="application/json")
            else:
                # check existence
                # save information in the db
                try:
                    ses = session.objects.get(session_name = session_name, user_id = username, project_name = project_name, session_ver = int(session_ver))
                    if not request.POST.get('session_annotation', ''):
                        session_annotation = None
                        up_ses = session.objects.filter(session_name = session_name, user_id = username, project_name = project_name, session_ver = int(session_ver))
                        up_ses.update(session_annotation = None, last_date = datetime.datetime.now())
                        ses_his = session_history(user_id = user.user_id, project_name = project_name, session_name = session_name, session_ver = int(session_ver), session_annotation = None, last_date = datetime.datetime.now())
                        ses_his.save()
                    else:
                        session_annotation = '%r' % request.POST['session_annotation']
                        session_annotation = session_annotation.replace('\'', '')
                        up_ses = session.objects.filter(session_name = session_name, user_id = username, project_name = project_name, session_ver = int(session_ver))
                        up_ses.update(session_annotation = session_annotation, last_date = datetime.datetime.now())
                        ses_his = session_history(user_id = user.user_id, project_name = project_name, session_name = session_name, session_ver = int(session_ver), session_annotation = session_annotation, last_date = datetime.datetime.now())
                        ses_his.save()
                    ses_info = []
                    ses_info_elem = {}
                    ses_info_elem['username'] = username
                    ses_info_elem['project_name'] = project_name
                    ses_info_elem['session_name'] = session_name
                    ses_info_elem['session_ver'] = session_ver
                    ses_info_elem['session_annotation'] = session_annotation
                    ses_info.append(ses_info_elem)
                    #renew the last_date of project and session
                    proj_rn = project.objects.filter(user_id = username, project_name = project_name)
                    proj_rn.update(last_date = datetime.datetime.now())
                    ses_rn = session.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
                    ses_rn.update(last_date = datetime.datetime.now())
                    return HttpResponse(json.dumps({'success' : True, 'detail' : "Updated session annotation.", 'output' : ses_info}) ,content_type="application/json")
                except session.DoesNotExist:
                    ses_info = []
                    ses_info_elem = {}
                    ses_info_elem['username'] = username
                    ses_info_elem['project_name'] = project_name
                    ses_info_elem['session_name'] = session_name
                    ses_info_elem['session_ver'] = session_ver
                    ses_info.append(ses_info_elem)
                    return HttpResponse(json.dumps({'success' : False, 'detail' : "No the session.", 'output' : ses_info}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : "No user or No session name.", 'output' : errors}) ,content_type="application/json")

def check_preview_session(request):
    """
    check preview session
    """
    errors = []
    username = ""
    project_name = ""
    session_name = ""
    session_ver = 0
    if request.method == 'POST':
        # check information
        param_list = ['username', 'project_name', 'session_name', 'session_ver']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get parameter
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            bls = block.objects.filter(user_id = username, session_name = session_name, session_ver = int(session_ver))
            total_list = []
            saved_list = []
            for i in bls:
                if i.block_iden not in total_list:
                    total_list.append(i.block_iden)
                if i.is_save == True:
                    if i.block_iden not in saved_list:
                        saved_list.append(i.block_iden)
            for i in saved_list:
                if i in total_list:
                    total_list.remove(i)
            json_bl_list = []
            for i in total_list:
                json_bl_elem = {}
                json_bl_elem['block_iden'] = i
                json_bl_list.append(json_bl_elem)
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Enumerated unsaved unitis.", 'output' : json_bl_list}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")
