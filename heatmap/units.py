from heatmap import *

@ensure_csrf_cookie
def clusters(request):
    """
    Receive cluster block information and Send clustering expression value and others.
    New added username, session_num or session_name
    """
    errors = []
    cluster_type = ""
    cluster_param = 0
    if request.method == 'POST':
        # Determine whether parameter collectly received
        param_list = [ 'username', 'project_name', 'session_name', "session_ver", 'block_iden', 'block_name', 'data', "vis_types"]
        errors = param_checker(request, errors, param_list)
        if not errors:
            vis_types = '%r' % request.POST['vis_types']
            vis_types = vis_types.replace('\'', '')
            if vis_types == "Heatmap":
                param_list = ['cluster_type', 'cluster_param', 'color_type']
                errors = param_checker(request, errors, param_list)
            elif vis_types == "Parallel Coordinate Plot":
                param_list = ['selected_index', 'column_order', 'brushed_axis', 'brushed_range']
                errors = param_checker(request, errors, param_list)
            elif vis_types == "Scatterplot Matrix":
                param_list = ['selected_index', 'brushed_axis', 'brushed_range']
                errors = param_checker(request, errors, param_list)
            elif vis_types == "Scatter Plot":
                param_list = ['brushed_range', 'x_axis', 'y_axis']
                errors = param_checker(request, errors, param_list)
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")
        if not errors:
            # get unit information
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            is_save = False if request.POST.get('is_save') == 'false' else True
            block_id = '%r' % request.POST['block_iden']
            block_id = block_id.replace('\'', '')
            block_name = '%r' % request.POST['block_name']
            block_name = block_name.replace('\'', '')
            data = request.POST['data']
            data_name = request.POST.get('data_name', '')

            data_type = data_name[data_name.find(".")+1:data_name.find(" (")]
            if data_type != "tsv" and data_type != "csv" and data_type != "txt":
                errors.append("Unsupported data type")
                return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

            position = json.loads(request.POST.get('position'))
            vis_types = '%r' % request.POST['vis_types']
            vis_types = vis_types.replace('\'', '')
            if not request.POST.get('data_annotation', ''):
                data_annotation = None
            else:
                data_annotation = '%r' % request.POST['data_annotation']
                data_annotation = data_annotation.replace('\'', '')
            if not request.POST.get('parent_block_iden', ''):
                parent_block_iden = None
            else:
                parent_block_iden = '%r' % request.POST['parent_block_iden']
                parent_block_iden = parent_block_iden.replace('\'', '')
            if parent_block_iden is not None:
                is_save = True
            if not request.POST.get('parent_block_ver', ''):
                parent_block_ver = 0
            else:
                parent_block_ver = '%r' % request.POST['parent_block_ver']
                parent_block_ver = parent_block_ver.replace('\'', '')
            """
            is_first_child = False
            if parent_block_iden is not None:
                if int(parent_block_ver) - 1 > -1:
                    parent_block_ver = int(parent_block_ver) - 1
                else:
                    is_first_child = True
            """

            get_block_ver = block.objects.all().filter(user_id = username, project_name = project_name,
                                                       session_name = session_name, session_ver = int(session_ver),
                                                       block_iden = block_id).aggregate(Max('block_ver'))
            max_block_ver = get_block_ver['block_ver__max']
            block_ver = 0

            if max_block_ver is not None: #null

                if not request.POST.get('block_ver', ''):
                    block_ver = 0
                else:
                    block_ver = '%r' % request.POST['block_ver']
                    block_ver = block_ver.replace('\'', '')

                errors = []
                if int(block_ver) > max_block_ver:
                    errors.append("This is not last version of unit")
                    return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

                block_ver = max_block_ver + 1
                """
                get_parent_block = block.objects.all().filter(user_id = username, project_name = project_name,
                                                              session_name = session_name, session_ver = int(session_ver),
                                                              block_iden = block_id, block_ver = max_block_ver).values('parent_block_iden', 'parent_block_ver').order_by('block_ver')
                if not get_parent_block[0]['parent_block_iden']:
                    parent_block_iden = None
                else:
                    parent_block_iden = get_parent_block[0]['parent_block_iden']
                    parent_block_ver = get_parent_block[0]['parent_block_ver']
                """
            else:
                block_ver = 0
            if parent_block_iden is None and is_save == True: # save
                get_save_ver = block.objects.all().filter(user_id = username, project_name = project_name,
                                                          session_name = session_name, session_ver = int(session_ver),
                                                          block_iden = block_id, is_save = True).aggregate(Max('save_ver'))
                max_save_ver = get_save_ver['save_ver__max']
                if max_save_ver is not None: # not first save
                    save_ver = max_save_ver + 1
                else: # first save
                    save_ver = 0
                block_insert = block(user_id = username, project_name = project_name,
                                     session_name = session_name, session_ver = int(session_ver),
                                     block_iden = block_id, block_name = block_name, block_ver = block_ver,
                                     parent_block_iden = parent_block_iden, parent_block_ver = parent_block_ver,
                                     data = data, data_annotation = data_annotation, data_name = data_name,
                                     position_top = position['top'], position_left = position['left'],
                                     position_height = position['height'], position_width = position['width'],
                                     is_save = True, save_ver = save_ver,
                                     vis_types = vis_types)
            elif parent_block_iden is not None and is_save == True: # branch unit before already saved unit
                get_save_ver = block.objects.all().filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_id, is_save = True).aggregate(Max('save_ver'))
                max_save_ver = get_save_ver['save_ver__max']
                if max_save_ver is not None: # not first save
                    save_ver = max_save_ver + 1
                else: # first save
                    save_ver = 0
                block_insert = block(user_id = username, project_name = project_name,
                                     session_name = session_name, session_ver = int(session_ver),
                                     block_iden = block_id, block_name = block_name, block_ver = block_ver,
                                     parent_block_iden = parent_block_iden, parent_block_ver = parent_block_ver,
                                     data = data, data_annotation = data_annotation, data_name = data_name,
                                     position_top = position['top'], position_left = position['left'],
                                     position_height = position['height'], position_width = position['width'],
                                     is_save = True, save_ver = save_ver,
                                     vis_types = vis_types)
                pre_bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = parent_block_iden, block_ver__lte = int(parent_block_ver), is_save = True)
                if len(pre_bl) == 0:
                    brch_bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = parent_block_iden, block_ver = parent_block_ver).update(is_save = True, save_ver = 0)
            else:
                block_insert = block(user_id = username, project_name = project_name,
                                     session_name = session_name, session_ver = int(session_ver),
                                     block_iden = block_id, block_name = block_name, block_ver = block_ver,
                                     parent_block_iden = parent_block_iden, parent_block_ver = parent_block_ver,
                                     data = data, data_annotation = data_annotation, data_name = data_name,
                                     position_top = position['top'], position_left = position['left'],
                                     position_height = position['height'], position_width = position['width'],
                                     vis_types = vis_types)
            block_insert.save()

            if parent_block_iden is not None:
                brch_logs = log_history.objects.filter(user_id=username, project_name=project_name,
                                                       session_name=session_name, session_ver=int(session_ver),
                                                       block_iden=parent_block_iden, block_ver=int(parent_block_ver))
                for i in brch_logs:
                    if i.action != action_check_list[3]:
                        new_log_obj = i
                        new_log_obj.action_id = None
                        new_log_obj.save()
                        new_add_log = log_history.objects.filter(action_id=new_log_obj.action_id)
                        new_add_log.update(block_iden=block_id, block_ver=int(block_ver))

            """
            if is_first_child == True:
                brch_logs = log_history.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = parent_block_iden, block_ver = int(0))
                for i in brch_logs:
                    if i.action != action_check_list[3]:
                        new_log_obj = i
                        new_log_obj.action_id = None
                        new_log_obj.save()
                        new_add_log = log_history.objects.filter(action_id = new_log_obj.action_id)
                        new_add_log.update(block_iden = block_id, block_ver = int(block_ver))
                fir_bl = block.objects.filter(block_id = block_insert.block_id)
                fir_bl.update(is_first = True)
            elif is_first_child == False and parent_block_iden is not None and int(block_ver) is 0:
                brch_logs = log_history.objects.filter(user_id=username, project_name=project_name,
                                                       session_name=session_name, session_ver=int(session_ver),
                                                       block_iden=parent_block_iden, block_ver=int(parent_block_ver)+1)
                for i in brch_logs:
                    if i.action != action_check_list[3]:
                        new_log_obj = i
                        new_log_obj.action_id = None
                        new_log_obj.save()
                        new_add_log = log_history.objects.filter(action_id=new_log_obj.action_id)
                        new_add_log.update(block_iden=block_id, block_ver=int(block_ver))

            # modify parent position

            if parent_block_iden is not None and int(block_ver) is 0:
                p_bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = parent_block_iden, block_ver = int(parent_block_ver))
                if len(p_bl) > 0:
                    if p_bl[0].parent_block_iden is not None:
                        is_first_child = False
                        block_insert.__dict__.update(parent_block_iden = p_bl[0].parent_block_iden, parent_block_ver = int(p_bl[0].parent_block_ver), is_first = is_first_child)
                        block_insert.save()
            """
            saved_bls = block.objects.all().filter(user_id=username, project_name=project_name,
                                                      session_name=session_name, session_ver=int(session_ver),
                                                      block_iden=block_id, is_save=True)
            # default
            if parent_block_iden is not None:
                ori_p_block_iden = parent_block_iden
                orI_p_block_ver = int(parent_block_ver)
                is_first = False
                block_insert.__dict__.update(is_first=is_first, ori_p_block_iden = ori_p_block_iden, orI_p_block_ver = orI_p_block_ver)
                block_insert.save()
            elif is_save == True and parent_block_iden is None:
                is_first = True
                block_insert.__dict__.update(is_first = is_first)
                block_insert.save()
            if len(saved_bls) > 1:
                is_first = False
                block_insert.__dict__.update(is_first=is_first)
                block_insert.save()
            if parent_block_iden is not None:
                if orI_p_block_ver > 0:
                    is_first = False
                parent_bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = ori_p_block_iden, block_ver = int(orI_p_block_ver))
                is_first=parent_bl[0].is_first
                block_insert.__dict__.update(is_first=is_first)
                block_insert.save()
                fir_bl_list = {}
                info = {}
                info['username'] = username
                info['project_name'] = project_name
                info['session_name'] = session_name
                info['session_ver'] = int(session_ver)
                info['block_iden'] = parent_block_iden
                info['block_ver'] = int(parent_block_ver)
                p_bl_info = find_ori_bl(fir_bl_list, info)
                """
                if p_bl_info == {}:
                    parent_block_iden = parent_block_iden
                    parent_block_ver = int(parent_block_ver) - 1
                else:
                """
                find_block_iden = p_bl_info['block_iden']
                find_block_ver = int(int(p_bl_info['block_ver']))
                ori_bl = block.objects.filter(user_id=username, project_name=project_name,
                                                    session_name=session_name, session_ver=int(session_ver),
                                                    block_iden=find_block_iden, block_ver=int(find_block_ver))
                ori_bl = block.objects.filter(user_id=username, project_name=project_name,
                                              session_name=session_name, session_ver=int(session_ver),
                                              block_iden=find_block_iden, block_ver=int(find_block_ver))
                p_ori_bl = block.objects.filter(user_id=username, project_name=project_name,
                                              session_name=session_name, session_ver=int(session_ver),
                                              block_iden=ori_bl[0].parent_block_iden, block_ver=int(ori_bl[0].parent_block_ver))
                if ori_bl[0].save_ver > 0:
                    last_ori_bl = block.objects.filter(user_id=username, project_name=project_name,
                                                  session_name=session_name, session_ver=int(session_ver),
                                                  block_iden=find_block_iden, save_ver = int(ori_bl[0].save_ver) - 1, is_save=True).order_by("-last_date")
                    parent_block_iden = ori_bl[0].block_iden
                    parent_block_ver = int(last_ori_bl[0].block_ver)
                else:
                    parent_block_iden = ori_bl[0].parent_block_iden
                    parent_block_ver = int(ori_bl[0].parent_block_ver)
                block_insert.__dict__.update(parent_block_iden=parent_block_iden,
                                             parent_block_ver=int(parent_block_ver))
                block_insert.save()

            if vis_types == "Heatmap":
                hm_bl = block.objects.filter(block_id = block_insert.block_id)
                cluster_type = '%r' % request.POST['cluster_type']
                cluster_type = cluster_type.replace('\\xa0', '')
                cluster_type = cluster_type.replace('\'', '')
                cluster_param = '%r' % request.POST['cluster_param']
                cluster_param = cluster_param.replace('\'', '')
                color_type = request.POST.getlist('color_type')[0]
                hm_bl.update(clusterType = cluster_type, clusterParam = cluster_param, colors = color_type)
            elif vis_types == "Parallel Coordinate Plot":
                pcp_bl = block.objects.filter(block_id = block_insert.block_id)
                column_order = '%r' % request.POST['column_order']
                column_order = column_order.replace('\'', '')
                selected_index = '%r' % request.POST['selected_index']
                selected_index = selected_index.replace('\'', '')
                brushed_axis = '%r' % request.POST['brushed_axis']
                brushed_axis = brushed_axis.replace('\'', '')
                brushed_range = '%r' % request.POST['brushed_range']
                brushed_range = brushed_range.replace('\'', '')
                elem_bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_id, block_ver = int(block_ver)-1).order_by('-last_date')
                if len(elem_bl) > 0:
                    if elem_bl[0].pcp_id is not None:
                        get_pcp = pcp.objects.filter(pcp_id = elem_bl[0].pcp_id)
                        if len(get_pcp) > 0:
                            column_order = get_pcp[0].column_order
                            selected_index = get_pcp[0].selected_index
                            brushed_axis = get_pcp[0].brushed_axis
                            brushed_range = get_pcp[0].brushed_range

                pcp_obj = pcp(column_order = column_order, selected_index = selected_index, brushed_axis = brushed_axis, brushed_range = brushed_range)
                pcp_obj.save()
                pcp_bl.update(pcp_id = pcp_obj.pcp_id)
            elif vis_types == "Scatterplot Matrix":
                scm_bl = block.objects.filter(block_id=block_insert.block_id)
                selected_index = '%r' % request.POST['selected_index']
                selected_index = selected_index.replace('\'', '')
                brushed_axis = '%r' % request.POST['brushed_axis']
                brushed_axis = brushed_axis.replace('\'', '')
                brushed_range = '%r' % request.POST['brushed_range']
                brushed_range = brushed_range.replace('\'', '')
                elem_bl = block.objects.filter(user_id=username, project_name=project_name, session_name=session_name,
                                               session_ver=int(session_ver), block_iden=block_id,
                                               block_ver=int(block_ver)-1).order_by('-last_date')
                if len(elem_bl) > 0:
                    if elem_bl[0].scm_id is not None:
                        get_scm = scm.objects.filter(scm_id=elem_bl[0].scm_id)
                        if len(get_scm) > 0:
                            selected_index = get_scm[0].selected_index
                            brushed_axis = get_scm[0].brushed_axis
                            brushed_range = get_scm[0].brushed_range
                scm_obj = scm(selected_index=selected_index, brushed_axis = brushed_axis, brushed_range = brushed_range)
                scm_obj.save()
                scm_bl.update(scm_id=scm_obj.scm_id)
            elif vis_types == "Scatter Plot":
                sp_bl = block.objects.filter(block_id=block_insert.block_id)
                brushed_range = '%r' % request.POST['brushed_range']
                brushed_range = brushed_range.replace('\'', '')
                x_axis = '%r' % request.POST['x_axis']
                x_axis = x_axis.replace('\'', '')
                x_axis = x_axis.replace('\"', '')
                y_axis = '%r' % request.POST['y_axis']
                y_axis = y_axis.replace('\'', '')
                y_axis = y_axis.replace('\"', '')
                elem_bl = block.objects.filter(user_id=username, project_name=project_name, session_name=session_name,
                                               session_ver=int(session_ver), block_iden=block_id,
                                               block_ver=int(block_ver)-1).order_by('-last_date')
                if len(elem_bl) > 0:
                    if elem_bl[0].sp_id is not None:
                        get_sp = sp.objects.filter(sp_id=elem_bl[0].sp_id)
                        if len(get_sp) > 0:
                            brushed_range = get_sp[0].brushed_range
                            x_axis = get_sp[0].x_axis
                            y_axis = get_sp[0].y_axis
                sp_obj = sp(brushed_range=brushed_range, x_axis = x_axis, y_axis = y_axis)
                sp_obj.save()
                sp_bl.update(sp_id=sp_obj.sp_id)
            request_json = []
            rj_elem = {}
            rj_elem['username'] = username
            rj_elem['project_name'] = project_name
            rj_elem['session_ver'] = int(session_ver)
            rj_elem['block_iden'] = block_id
            rj_elem['block_name'] = block_name
            rj_elem['block_ver'] = block_ver
            rj_elem['parent_block_iden'] = parent_block_iden
            rj_elem['parent_block_ver'] = parent_block_ver
            rj_elem['session_name'] = session_name
            rj_elem['data'] = data
            rj_elem['data_annotation'] = data_annotation
            rj_elem['data_name'] = data_name
            rj_elem['vis_types'] = vis_types
            if vis_types == "Heatmap":
                rj_elem['cluster_type'] = cluster_type
                rj_elem['cluster_param'] = cluster_param
                rj_elem['color_type'] = color_type
            elif vis_types == "Parallel Coordinate Plot":
                rj_elem['column_order'] = column_order
                rj_elem['selected_index'] = selected_index
                rj_elem['brushed_axis'] = brushed_axis
                rj_elem['brushed_range'] = brushed_range
            elif vis_types == "Scatterplot Matrix":
                rj_elem['selected_index'] = selected_index
                rj_elem['brushed_axis'] = brushed_axis
                rj_elem['brushed_range'] = brushed_range
            elif vis_types == "Scatter Plot":
                rj_elem['x_axis'] = x_axis
                rj_elem['y_axis'] = y_axis
                rj_elem['brushed_range'] = brushed_range
            request_json.append(rj_elem)
            position_json = []
            position_json.append(position)

            try:
                if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name,
                                               str(session_ver), str(block_id))) is False:
                    os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name, str(session_ver), str(block_id)))
                if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name,
                                               str(session_ver), str(block_id), str(block_ver))) is False:
                    os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name, str(
                                          session_ver), str(block_id), str(block_ver)))
            except OSError as e:
                if e.errno == 17:
                    pass
                if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member')) is False:
                    os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member'))
                if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username)) is False:
                    os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username))
                if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name)) is False:
                    os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name))
                if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name)) is False:
                    os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name,
                                          str(session_name)))
                if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name, session_name, str(session_ver))) is False:
                    os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name,
                                          str(session_name), str(session_ver)))
                    os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name,
                                          str(session_name), str(session_ver), str(block_id)))
                    os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name,
                                          str(session_name), str(session_ver), str(block_id), str(block_ver)))

            #renew the last_date of project and session
            proj_rn = project.objects.filter(user_id = username, project_name = project_name)
            proj_rn.update(last_date = datetime.datetime.now())
            ses_rn = session.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
            ses_rn.update(last_date = datetime.datetime.now())

            #save the column/row headers (conditions/genes) into an array
            bl_info = {}
            bl_info['username'] = username
            bl_info['project_name'] = project_name
            bl_info['session_name'] = session_name
            bl_info['session_ver'] = session_ver
            bl_info['block_iden'] = block_id
            bl_info['block_ver'] = block_ver
            bl_info['data'] = data
            bl_info['request_json'] = request_json
            bl_info['position_json'] = position
            bl_info['is_cluster'] = True
            bl_info['data_type'] = data_type
            bl_info['vis_types'] = vis_types
            bl_info['parent_block_iden'] = parent_block_iden
            if vis_types == "Heatmap":
                bl_info['cluster_type'] = cluster_type
                bl_info['cluster_param'] = cluster_param
                bl_info['color_type'] = color_type
            elif vis_types == "Parallel Coordinate Plot":
                bl_info['column_order'] = column_order
                bl_info['selected_index'] = selected_index
                bl_info['brushed_axis'] = brushed_axis
                bl_info['brushed_range'] = brushed_range
            elif vis_types == "Scatterplot Matrix":
                bl_info['selected_index'] = selected_index
                bl_info['brushed_axis'] = brushed_axis
                bl_info['brushed_range'] = brushed_range
            elif vis_types == "Scatter Plot":
                bl_info['x_axis'] = x_axis
                bl_info['y_axis'] = y_axis
                bl_info['brushed_range'] = brushed_range

            # run clusters (this function is in the clustering.py)\
            return HttpResponse(run_vis(bl_info), content_type="application/json")

        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

@ensure_csrf_cookie
def get_blocks(request):
    """
    Get session blocks
    """
    errors = []
    username = ""
    project_name = ""
    session_name = ""
    session_ver = 0
    if request.method == 'POST':
        param_list = ['username', 'project_name', 'session_name', "session_ver"]
        errors = param_checker(request, errors, param_list)
        if not errors:
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            session_name = '%r' % request.POST['session_name']
            session_name = session_name.replace('\'', '')
            session_ver = '%r' % request.POST['session_ver']
            session_ver = session_ver.replace('\'', '')
            project_name = '%r' % request.POST['project_name']
            project_name = project_name.replace('\'', '')
            bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), is_closed = False, is_save = True).values_list('block_iden', 'block_ver', 'clusterType', 'vis_types').annotate(last_date = Max('last_date')).order_by('-block_ver').distinct()

            bl_list = []
            for i in bl:
                bl_list.append(i)
            du_list = []
            result_list = []
            for i in bl_list:
                if du_list.count(i[0]) == 0:
                    result_list.append(i)
                    du_list.append(i[0])
                else:
                    pass

            #BASE_DIR = "static/member/"
            path = os.path.join("static", "member", str(username), str(project_name), str(session_name), str(session_ver))
            path_list = []
            for i in result_list:
                path_str = os.path.join(path, str(i[0]), str(i[1]))
                anno_str = os.path.join(path, str(i[0]))
                graph_path = os.path.join(path, str(i[0]))
                path_elem = {}
                graph_bl = block.objects.filter(user_id=username, project_name=project_name, session_name=session_name,
                                                session_ver=int(session_ver), block_iden=i[0])
                if 'Parallel Coordinate Plot' in i:
                    path_elem['pcp_path'] = os.path.join(path_str, "pcp.json")
                    path_elem['annotation_path'] = os.path.join(anno_str, "annotation.json")
                    if os.path.exists(path_elem['pcp_path']) is True:
                        path_list.append(path_elem)
                elif 'Scatterplot Matrix' in i:
                    path_elem['scm_path'] = os.path.join(path_str, "scm.json")
                    path_elem['annotation_path'] = os.path.join(anno_str, "annotation.json")
                    if os.path.exists(path_elem['scm_path']) is True:
                        path_list.append(path_elem)
                elif 'Scatter Plot' in i:
                    path_elem['sp_path'] = os.path.join(path_str, "sp.json")
                    path_elem['annotation_path'] = os.path.join(anno_str, "annotation.json")
                    if os.path.exists(path_elem['sp_path']) is True:
                        path_list.append(path_elem)
                elif graph_bl[0].is_graph == True:
                    if os.path.exists(os.path.join(graph_path, 'result_node.txt')) is True and os.path.exists(os.path.join(graph_path, 'result_edge.txt')) is True and os.path.exists(os.path.join(graph_path, 'graph.json')):
                        path_elem['graph_path'] = os.path.join(graph_path, 'graph.json')
                        path_elem['node_path'] = os.path.join(graph_path, 'result_node.txt')
                        path_elem['edge_path'] = os.path.join(graph_path, 'result_edge.txt')
                        path_list.append(path_elem)
                else:
                    path_elem['heatmap_path'] = os.path.join(path_str, "clusters.json")
                    path_elem['annotation_path'] = os.path.join(anno_str, "annotation.json")
                    if i[2] == "Hierarchy":
                        path_elem['dendro_path'] = os.path.join(path_str, str(i[2]) + ".csv")
                        path_elem['dendro_col_path'] = os.path.join(path_str, str(i[2]) + "Col.csv")
                    else:
                        path_elem['dendro_path'] = None
                        path_elem['dendro_col_path'] = None
                    if os.path.exists(path_elem['heatmap_path']) is True:
                        path_list.append(path_elem)
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Got Blocks.", 'output' : path_list}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

@ensure_csrf_cookie
def close_block(request):
    errors = []
    username = ""
    session_name = ""
    session_ver = 0
    if request.method == 'POST':
        param_list = ['username', 'project_name', 'session_name', "session_ver", "block_iden"]
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
            block_iden = '%r' % request.POST['block_iden']
            block_iden = block_iden.replace('\'', '')
            bl = closed_block(user_id = username, project_name = project_name, session_name = session_name, session_ver = session_ver, block_iden = block_iden)
            bl.save()
            bls = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = session_ver, block_iden = block_iden).update(is_closed = True)

            #renew the last_date of project and session
            proj_rn = project.objects.filter(user_id = username, project_name = project_name)
            proj_rn.update(last_date = datetime.datetime.now())
            ses_rn = session.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
            ses_rn.update(last_date = datetime.datetime.now())

            return HttpResponse(json.dumps({'success' : True, 'detail' : "Closed a block.", 'output' : block_iden}) ,content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")


@ensure_csrf_cookie
def create_block_annotation(request):
    """
    add block annotation in the each blocks annotation.json
    """
    errors = []
    username = ""
    session_name = ""
    session_ver = 0
    block_iden = ""
    block_ver = 0
    if request.method == 'POST':
        # check necessary information
        param_list = ['username', 'project_name', 'session_name', "session_ver", "block_iden", "block_ver", "block_annotation"]
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
            block_annotation = '%r' % request.POST['block_annotation']
            block_annotation = block_annotation.replace('\'', '')
            # get max annotation number
            annotation_num = 0
            get_anno_num = block_annotation_history.objects.all().filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_iden, block_ver = 0, is_removed = False).aggregate(Max('annotation_num'))
            max_anno_num = get_anno_num['annotation_num__max']
            get_bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_iden, block_ver = int(0))
            if max_anno_num is not None: #null
                annotation_num = max_anno_num + 1
            else:
                annotation_num = 0
            block_anno_json = json.loads(block_annotation)
            # insert block_annotation table
            bl_anno = block_annotation_history(user_id = username, project_name = project_name,
                                               session_name = session_name, session_ver = int(session_ver),
                                               block_iden = block_iden, block_ver = 0,
                                               author = block_anno_json['author'], data_annotation = block_anno_json['data_annotation'],
                                               research_annotation = block_anno_json['research_annotation'], annotation_num = annotation_num,
                                               experiment_type = block_anno_json['experiment_type'], platform_name = block_anno_json['platform_name'],
                                               organism = block_anno_json['organism'])
            bl_anno.save()

            # open annotation.json file
            annotation_path = os.path.join(str(BASE_DIR),'member', str(username), str(project_name), str(session_name), str(session_ver), str(block_iden), 'annotation.json')
            rfile = open(annotation_path, 'r')
            # get annotations
            existing_json = rfile.readline()
            if existing_json:
                line = json.loads(existing_json)
            rfile.close()
            # add new annotation
            wfile = open(annotation_path, 'w')
            json_str = "{'annotation_list':["
            if existing_json:
                for i in line["annotation_list"]:
                    json_str += str(i) + ","
            annotation = {}
            annotation['username'] = block_anno_json['username']
            annotation['project_name'] = block_anno_json['project_name']
            annotation['session_name'] = block_anno_json['session_name']
            annotation['session_ver'] = block_anno_json['session_ver']
            annotation['block_iden'] = block_anno_json['block_iden']
            annotation['block_ver'] = 0
            annotation['author'] = block_anno_json['author']
            annotation['data_annotation'] = block_anno_json['data_annotation']
            annotation['research_annotation'] = block_anno_json['research_annotation']
            now = datetime.datetime.now()
            annotation['date'] = now.strftime("%Y-%m-%d %H:%M:%S")
            annotation['experiment_type'] = block_anno_json['experiment_type']
            annotation['platform_name'] = block_anno_json['platform_name']
            annotation['organism'] = block_anno_json['organism']
            if get_bl[0].clusterType is not None or get_bl[0].clusterParam is not None:
                annotation['cluster_annotation'] = get_bl[0].clusterType + "-" + get_bl[0].clusterParam
            else:
                annotation['cluster_annotation'] = ""
            json_str += str(json.dumps({"annotation":annotation}))
            json_str += "]}"
            json_str = json_str.replace("'", '"')
            wfile.write(json_str)
            wfile.close()

            #renew the last_date of project and session
            proj_rn = project.objects.filter(user_id = username, project_name = project_name)
            proj_rn.update(last_date = datetime.datetime.now())
            ses_rn = session.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
            ses_rn.update(last_date = datetime.datetime.now())

            return HttpResponse(json.dumps({'success' : True, 'detail' : "Created Block Annotation.", 'output' : block_annotation}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

@ensure_csrf_cookie
def delete_block_annotation(request):
    """
    delete block annotation in each block annotation.json file
    """
    errors = []
    username = ""
    session_name = ""
    session_ver = 0
    block_iden = ""
    block_ver = 0
    block_annotation = ""
    if request.method == 'POST':
        # check necessary information
        param_list = ['username', 'project_name', 'session_name', "session_ver", "block_iden", "block_ver", 'annotation_num']
        errors = param_checker(request, errors, param_list)
        #if not request.POST.get('block_annotation', ''):
            #errors.append("Enter a block_annotation.")
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
            annotation_num = '%r' % request.POST['annotation_num']
            annotation_num = annotation_num.replace('\'', '')
            """
            block_annotation = '%r' % request.POST['block_annotation']
            block_annotation = block_annotation.replace('\'', '')
            block_anno_json = json.loads(block_annotation)
            # set is_removed value true
            get_bl_anno = block_annotation_history.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_iden, block_ver = int(block_ver), author = block_anno_json['author'], data_annotation = block_anno_json['data_annotation'], research_annotation = block_anno_json['research_annotation'],is_removed = False)
            if not get_bl_anno:
                return HttpResponse(json.dumps({'success' : False, 'detail' : "No Block Annotation.", 'output' : block_annotation}) ,content_type="application/json")
            else:
                annotation_num = get_bl_anno[0].annotation_num
            """
            get_ses = session.objects.filter(user_id=username, project_name=project_name,
                                             session_name=session_name).aggregate(Max('session_ver'))
            max_ses_ver = get_ses['session_ver__max']
            for j in range(int(session_ver), int(max_ses_ver)+1):
                bl_anno = block_annotation_history.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(j), block_iden = block_iden, block_ver = 0, annotation_num = annotation_num).update(is_removed = True)
                af_del_anno = block_annotation_history.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(j), block_iden = block_iden, block_ver = 0, annotation_num__gt = int(annotation_num), is_removed = False)
                for i in af_del_anno:
                    i.annotation_num = i.annotation_num -1
                    i.save()
                # erase annotation
                annotation_path = os.path.join(str(BASE_DIR), 'member', str(username), str(project_name), str(session_name), str(j), str(block_iden), 'annotation.json')
                rfile = open(annotation_path, 'r')
                line = json.loads(rfile.readline())
                rfile.close()
                wfile = open(annotation_path, 'w')
                json_str = "{'annotation_list':["
                num = 0
                for i in line["annotation_list"]:
                    #if not i['annotation']['username'] == block_anno_json['username'] or not i['annotation']['project_name'] == block_anno_json['project_name'] or not i['annotation']['session_name'] == block_anno_json['session_name'] or not i['annotation']['session_ver'] == block_anno_json['session_ver'] or not i['annotation']['block_iden'] == block_anno_json['block_iden'] or not i['annotation']['block_ver'] == block_anno_json['block_ver'] or not i['annotation']['author'] == block_anno_json['author'] or not i['annotation']['data_annotation'] == block_anno_json['data_annotation'] or not i['annotation']['research_annotation'] == block_anno_json['research_annotation']:
                    if not num == int(annotation_num):
                        json_str += str(i)
                        json_str += ","
                    num += 1
                if json_str != "{'annotation_list':[":
                    json_str = json_str[:-1]
                json_str += "]}"
                json_str = json_str.replace("'", '"')
                wfile.write(json_str)
                wfile.close()

            #renew the last_date of project and session
            proj_rn = project.objects.filter(user_id = username, project_name = project_name)
            proj_rn.update(last_date = datetime.datetime.now())
            ses_rn = session.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
            ses_rn.update(last_date = datetime.datetime.now())

            return HttpResponse(json.dumps({'success' : True, 'detail' : "Deleted Block Annotation.", 'output' : block_annotation}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

def update_block_annotation(request):
    errors = []
    username = ""
    session_name = ""
    session_ver = 0
    block_iden = ""
    block_ver = 0
    if request.method == 'POST':
        # check necessary information
        param_list = ['username', 'project_name', 'session_name', "session_ver", "block_iden", "block_ver", "block_annotation"]
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
            block_annotation = '%r' % request.POST['block_annotation']
            block_annotation = block_annotation.replace('\'', '')
            annotation_num = '%r' % request.POST['annotation_num']
            annotation_num = annotation_num.replace('\'', '')
            block_anno_json = json.loads(block_annotation)
            # insert block_annotation table
            get_bl_anno = block_annotation_history.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_iden, block_ver = 0, annotation_num = annotation_num, is_removed = False)
            if not get_bl_anno:
                return HttpResponse(json.dumps({'success' : False, 'detail' : "No Block Annotation.", 'output' : block_annotation}) ,content_type="application/json")
            else:
                prev_author = get_bl_anno[0].author
                prev_data_annotation = get_bl_anno[0].data_annotation
                prev_research_annotation = get_bl_anno[0].research_annotation
            """
            """
            now = datetime.datetime.now()
            bl_anno = block_annotation_history.objects.filter(user_id = username, project_name = project_name,
                                                              session_name = session_name, session_ver = int(session_ver),
                                                              block_iden = block_iden, block_ver = 0,
                                                              annotation_num = annotation_num, is_removed = False).update(author = block_anno_json['author'], data_annotation = block_anno_json['data_annotation'],
                                                                                                                          research_annotation = block_anno_json['research_annotation'], last_date = now,
                                                                                                                          experiment_type = block_anno_json['experiment_type'], platform_name = block_anno_json['platform_name'],
                                                                                                                          organism = block_anno_json['organism'])
            # open annotation.json file
            annotation_path = os.path.join(str(BASE_DIR), 'member', str(username), str(project_name), str(session_name), str(session_ver), str(block_iden) + ',annotation.json')
            rfile = open(annotation_path, 'r')
            # get annotations
            existing_json = rfile.readline()
            if existing_json:
                line = json.loads(existing_json)
            rfile.close()
            # add new annotation
            json_str = ""
            wfile = open(annotation_path, 'w')
            json_str = "{'annotation_list':["
            if existing_json:
                for i in line["annotation_list"]:
                    if i['annotation']['author'] == prev_author or i['annotation']['data_annotation'] == prev_data_annotation or i['annotation']['research_annotation'] == prev_research_annotation:
                        i['annotation']['author'] = block_anno_json['author']
                        i['annotation']['data_annotation'] = block_anno_json['data_annotation']
                        i['annotation']['research_annotation'] = block_anno_json['research_annotation']
                        i['annotation']['date'] = now.strftime("%Y-%m-%d %H:%M:%S")
                        i['annotation']['experiment_type'] = block_anno_json['experiment_type']
                        i['annotation']['platform_name'] = block_anno_json['platform_name']
                        i['annotation']['organism'] = block_anno_json['organism']
                        if block_anno_json['cluster_type'] is not None or block_anno_json['cluster_param'] is not None:
                            i['annotation']['cluster_annotation'] = block_anno_json['cluster_type'] + "-" + block_anno_json['cluster_param']
                        else:
                            i['annotation']['cluster_annotation'] = ""
                        json_str += str(i)
                        json_str += ","
                    else:
                        json_str += str(i)
                        json_str += ","
            json_str = json_str[:-1]
            json_str += "]}"
            json_str = json_str.replace("'", '"')
            wfile.write(json_str)
            wfile.close()

            #renew the last_date of project and session
            proj_rn = project.objects.filter(user_id = username, project_name = project_name)
            proj_rn.update(last_date = datetime.datetime.now())
            ses_rn = session.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver))
            ses_rn.update(last_date = datetime.datetime.now())

            return HttpResponse(json.dumps({'success' : True, 'detail' : "Updated Block Annotation.", 'output' : block_annotation}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")

def restoration(request):
    errors = []
    username = ""
    session_name = ""
    session_ver = 0
    block_iden = ""
    block_ver = 0
    if request.method == 'POST':
        # check necessary information
        param_list = ['username', 'project_name', 'session_name', "session_ver", "block_iden", "save_ver"]
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
            save_ver = '%r' % request.POST['save_ver']
            save_ver = save_ver.replace('\'', '')
            bl = block.objects.filter(user_id = username, project_name = project_name, session_name = session_name, session_ver = int(session_ver), block_iden = block_iden, save_ver = int(save_ver))
            if bl[0].is_closed == True:
                return HttpResponse(json.dumps({'success': False, 'detail': "This is deleted unit.", 'output': errors}),
                                    content_type="application/json")
            if bl[0].is_broken == True:
                return HttpResponse(json.dumps(
                    {'success': False, 'detail': "This is broken unit. Please redo action.", 'output': errors}),
                                    content_type="application/json")
            path = os.path.join("static", "member", str(username), str(project_name), str(session_name), str(session_ver), str(block_iden) , str(bl[0].block_ver))
            anno_path = os.path.join("static", "member", str(username), str(project_name), str(session_name),
                                str(session_ver), str(block_iden))

            path_list = []
            path_elem = {}
            if bl[0].vis_types == 'Parallel Coordinate Plot':
                path_elem = {}
                path_elem['pcp_path'] = os.path.join(path, "pcp.json")
                path_elem['annotation_path'] = os.path.join(anno_path, "annotation.json")
            elif bl[0].vis_types == 'Scatterplot Matrix':
                path_elem = {}
                path_elem['scm_path'] = os.path.join(path, "scm.json")
                path_elem['annotation_path'] = os.path.join(anno_path, "annotation.json")
            elif bl[0].vis_types == 'Scatter Plot':
                path_elem = {}
                path_elem['sp_path'] = os.path.join(path, "sp.json")
                path_elem['annotation_path'] = os.path.join(anno_path, "annotation.json")
            else:
                path_elem['heatmap_path'] = os.path.join(path, "clusters.json")
                path_elem['annotation_path'] = os.path.join(anno_path, "annotation.json")
                if bl[0].clusterType == "Hierarchy":
                    path_elem['dendro_path'] = os.path.join(path, str(bl[0].clusterType) + ".csv")
                    path_elem['dendro_col_path'] = os.path.join(path, str(bl[0].clusterType) + "Col.csv")
                else:
                    path_elem['dendro_path'] = None
                    path_elem['dendro_col_path'] = None
            path_list.append(path_elem)
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Get Unit information.", 'output' : path_list}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : "lack information.", 'output' : errors}) ,content_type="application/json")

def depen_check(request):
    errors = []
    if request.method == 'POST':
        # check necessary information
        param_list = ['action_list']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get necessary information
            action_list = request.POST.get('action_list')
            action_list = eval(json.loads(json.dumps(action_list)))
            # Unavailable undo - 0, 1, 2, 3, 4, 5, 6, 7
            # Available undo -
            hier_param_list = ["single", "complete", "average",
                               "weighted", "centroid", "median",
                               "ward"]
            block_list = []
            for i in action_list:
                action_elem = {}
                action_elem['action_id'] = i['action_id']
                try:
                    action = log_history.objects.get(action_id = int(i['action_id']))
                    action_elem['username'] = action.user_id
                    action_elem['project_name'] = action.project_name
                    action_elem['session_name'] = action.session_name
                    action_elem['session_ver'] = int(action.session_ver)
                    action_elem['block_iden'] = action.block_iden
                    action_elem['block_ver'] = int(action.block_ver)
                    action_elem['action'] = action.action
                except log_history.DoesNotExist:
                    action_elem['output'] = "Unavailable"
                block_list.append(action_elem)
            # 0, 1, 2, 3, 4, 5, 6, 7 - Unavailable
            # (8), (9, 10, 11), (12, 13), (14, 15), (16) - Available
            # sorting creatation date ascending order
            for i in block_list:
                # get action information
                try:
                    lho = log_history.objects.get(action_id=int(i['action_id']))
                except log_history.DoesNotExist:
                    i['output'] = "Unavailable"
                    continue
                try:
                    bl = block.objects.filter(user_id=i['username'], project_name=i['project_name'],
                                           session_name=i['session_name'], session_ver=int(i['session_ver']),
                                           block_iden=i['block_iden'], block_ver=int(i['block_ver']))
                except block.DoesNotExist:
                    i['output'] = "Unavailable"
                    continue

                # initial insert check (block_ver = -1)
                if int(i['block_ver']) == 0:
                    i['output'] = "Unavailable"

                if lho.is_used == False and list_checker(i['action'], depen_list, [9, 10, 11, 12, 13]):
                    i['output'] = "Available"
                    continue
                if lho.is_undo == True:
                    i['output'] = "Unavailable"
                    continue
                """
                query_list = []
                if list_checker(i['action'], depen_list, [6,7,8]):
                    for j in depen_list[6:9]:
                        query_list.append(Q(action = j,
                                             user_id = i['username'], project_name = i['project_name'],
                                             session_name = i['session_name'], session_ver = int(i['session_ver']),
                                             block_iden = i['block_iden'], block_ver__lt = i['block_ver'],
                                             is_used = True, is_undo = False))
                    saved_lh = log_history.objects.filter(reduce(operator.or_, query_list)).order_by("-creatation_date")
                else:
                """
                bl_info = {}
                bl_info['username'] = i['username']
                bl_info['project_name'] = i['project_name']
                bl_info['session_name'] = i['session_name']
                bl_info['session_ver'] = int(i['session_ver'])
                bl_info['block_iden'] = i['block_iden']
                bl_info['block_ver'] = int(i['block_ver'])
                if bl[0].parent_block_iden is not None and bl[0].is_first == False:
                    bl_info['parent_block_iden'] = bl[0].parent_block_iden
                    bl_info['parent_block_ver'] = bl[0].parent_block_ver
                else:
                    bl_info['parent_block_iden'] = None
                    bl_info['parent_block_ver'] = None
                bl_list = []
                bl_list = find_ance(bl_list, bl_info)

                logs = []
                for j in bl_list:
                    saved_lh = log_history.objects.filter(action = i['action'],
                                                       user_id = i['username'], project_name = i['project_name'],
                                                       session_name = i['session_name'], session_ver = int(i['session_ver']),
                                                       block_iden = j['block_iden'], block_ver__lte = int(j['block_ver']),
                                                       is_used = True, is_undo = False).order_by("-creatation_date")
                    for k in saved_lh:
                        logs.append(k)
                    if len(logs) > 0:
                        break

                saved_lh = logs

                get_block_ver = block.objects.all().filter(user_id = i['username'], project_name = i['project_name'],
                                                            session_name = i['session_name'], session_ver = int(i['session_ver']),
                                                            block_iden = i['block_iden']).aggregate(Max('block_ver'))
                max_block_ver = get_block_ver['block_ver__max']
                bl_info = {}
                bl_info['action_id'] = i['action_id']
                bl_info['action'] = i['action']
                bl_info['username'] = i['username']
                bl_info['project_name'] = i['project_name']
                bl_info['session_name'] = i['session_name']
                bl_info['session_ver'] = int(i['session_ver'])
                bl_info['block_iden'] = i['block_iden']
                bl_info['block_ver'] = int(i['block_ver'])
                depen_bl_list = []
                # Not cluster type or param part
                if list_checker(i['action'], depen_list, [0, 1, 2, 3, 4, 5, 6, 7]):
                    i['output'] = "Unavailable"
                elif list_checker(i['action'], depen_list, [8]):
                    i['output'] = "Available"
                elif list_checker(i['action'], depen_list, [9, 10, 11]):
                    depen_bl_list = []
                    if len(saved_lh) > 0:
                        i['output'] = "Available"
                        child_bl = block.objects.filter(user_id = i['username'], project_name = i['project_name'],
                                                   session_name = i['session_name'], session_ver = int(i['session_ver']),
                                                   parent_block_iden = i['block_iden'], parent_block_ver = i['block_ver'])
                        if int(max_block_ver) != int(lho.block_ver) or len(child_bl) > 0:
                            i['output'] = "Need to select"
                            depen_bl_list = find_descen(depen_bl_list, bl_info)
                            i['depend'] = depen_bl_list
                            for j in i['depend']:
                                j['detail'] = "Can run"
                    else:
                        i['output'] = "Unavailable"
                    """
                    if lho.parent_block_iden is not None : # branched case
                        brch_lh = log_history.objects.filter(action = i['action'],
                                                              user_id = i['username'], project_name = i['project_name'],
                                                              session_name = i['session_name'], session_ver = int(i['session_ver']),
                                                              block_iden = lho.parent_block_iden, block_ver__lte = int(lho.parent_block_ver),
                                                              is_used = True, is_undo = False).order_by("-creatation_date")
                        if len(brch_lh) > 0:
                            i['output'] = "Need to select"
                            # branched part
                            depen_bl_list = find_descen(depen_bl_list, bl_info)
                            i['depend'] = depen_bl_list
                            for j in i['depend']:
                                j['detail'] = "Can run"
                    """
                elif list_checker(i['action'], depen_list, [12, 13]): # 'Change-Cluster-Type', 'Change-Cluster-Parameter'
                    # change cluster type case
                    if len(saved_lh) > 0 and i['action'] == "Change-Cluster-Type":
                        if (saved_lh[0].clusterType == "Hierarchy" and list_checker(bl[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])) or \
                            ((saved_lh[0].clusterType == "KMeans" or saved_lh[0].clusterType == "Spectral") and not list_checker(bl[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])):
                            i['output'] = "Available"
                        if (int(saved_lh[0].block_ver) != 0 and int(lho.block_ver) != int(saved_lh[0].block_ver)) or \
                            (int(lho.block_ver) - int(saved_lh[0].block_ver) == int(lho.block_ver)):
                            i['output'] = "Need to select"
                            depen_bl_list = find_descen(depen_bl_list, bl_info)
                            i['depend'] = depen_bl_list
                            for j in i['depend']:
                                chk_depen_bl = block.objects.filter(user_id=i['username'], project_name=i['project_name'],
                                           session_name=i['session_name'], session_ver=int(i['session_ver']),
                                           block_iden=j['block_iden'], block_ver=int(j['block_ver']))
                                if (saved_lh[0].clusterType == "Hierarchy" and list_checker(chk_depen_bl[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])) or \
                            ((saved_lh[0].clusterType == "KMeans" or saved_lh[0].clusterType == "Spectral") and not list_checker(chk_depen_bl[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])):
                                    j['detail'] = "Can run"
                                else:
                                    j['detail'] = "Cannot run"
                    # change cluster param case
                    elif len(saved_lh) > 0 and i['action'] == "Change-Cluster-Parameter":
                        if (bl[0].clusterType == "Hierarchy" and list_checker(saved_lh[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])) or \
                            ((bl[0].clusterType == "KMeans" or bl[0].clusterType == "Spectral") and not list_checker(saved_lh[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])):
                            i['output'] = "Available"
                        if (int(saved_lh[0].block_ver) != 0 and int(lho.block_ver) != int(saved_lh[0].block_ver)) or \
                            (int(lho.block_ver) - int(saved_lh[0].block_ver) == int(lho.block_ver)):
                            i['output'] = "Need to select"
                            depen_bl_list = find_descen(depen_bl_list, bl_info)
                            i['depend'] = depen_bl_list
                            for j in i['depend']:
                                chk_depen_bl = block.objects.filter(user_id=i['username'],
                                                                    project_name=i['project_name'],
                                                                    session_name=i['session_name'],
                                                                    session_ver=int(i['session_ver']),
                                                                    block_iden=j['block_iden'],
                                                                    block_ver=int(j['block_ver']))
                                if (chk_depen_bl[0].clusterType == "Hierarchy" and list_checker(saved_lh[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])) or \
                                        ((chk_depen_bl[0].clusterType == "KMeans" or chk_depen_bl[0].clusterType == "Spectral") and not list_checker(saved_lh[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])):
                                    j['detail'] = "Can run"
                                else:
                                    j['detail'] = "Cannot run"
                    else:
                        i['output'] = "Unavailable"

                    # branched
                    if lho.parent_block_iden is not None and lho.is_first == False:
                        brch_lh = log_history.objects.filter(action = i['action'],
                                                              user_id = i['username'], project_name = i['project_name'],
                                                              session_name = i['session_name'], session_ver = int(i['session_ver']),
                                                              block_iden = lho.parent_block_iden, block_ver__lte = int(lho.parent_block_ver),
                                                              is_used = True, is_undo = False).order_by("-creatation_date")
                        # change cluster type case
                        if len(brch_lh) > 0 and i['action'] == "Change-Cluster-Type":
                            if (brch_lh[0].clusterType == "Hierarchy" and list_checker(bl[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])) or \
                                ((brch_lh[0].clusterType == "KMeans" or brch_lh[0].clusterType == "Spectral") and not list_checker(bl[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])) and len(brch_lh) > 0:
                                i['output'] = "Need to select"
                                depen_bl_list = find_descen(depen_bl_list, bl_info)
                                i['depend'] = depen_bl_list
                                for j in i['depend']:
                                    chk_depen_bl = block.objects.filter(user_id=i['username'],
                                                                        project_name=i['project_name'],
                                                                        session_name=i['session_name'],
                                                                        session_ver=int(i['session_ver']),
                                                                        block_iden=j['block_iden'],
                                                                        block_ver=int(j['block_ver']))
                                    if (brch_lh[0].clusterType == "Hierarchy" and list_checker(chk_depen_bl[0].clusterParam, hier_param_list,[ 0, 1, 2, 3, 4, 5,6])) or \
                                                    ((brch_lh[0].clusterType == "KMeans" or brch_lh[0].clusterType == "Spectral") and not list_checker(chk_depen_bl[0].clusterParam, hier_param_list,[0, 1, 2, 3, 4, 5, 6])) and len(brch_lh) > 0:
                                        j['detail'] = "Can run"
                                    else:
                                        j['detail'] = "Cannot run"
                        elif len(brch_lh) > 0 and i['action'] == "Change-Cluster-Parameter":
                            if (bl[0].clusterType == "Hierarchy" and list_checker(brch_lh[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])) or \
                                ((bl[0].clusterType == "KMeans" or bl[0].clusterType == "Spectral") and not list_checker(brch_lh[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])) and len(brch_lh) > 0:
                                i['output'] = "Need to select"
                                depen_bl_list = find_descen(depen_bl_list, bl_info)
                                i['depend'] = depen_bl_list
                                for j in i['depend']:
                                    chk_depen_bl = block.objects.filter(user_id=i['username'],
                                                                        project_name=i['project_name'],
                                                                        session_name=i['session_name'],
                                                                        session_ver=int(i['session_ver']),
                                                                        block_iden=j['block_iden'],
                                                                        block_ver=int(j['block_ver']))
                                    if (chk_depen_bl[0].clusterType == "Hierarchy" and list_checker(brch_lh[0].clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])) or \
                                                    ((chk_depen_bl[0].clusterType == "KMeans" or chk_depen_bl[0].clusterType == "Spectral") and not list_checker(brch_lh[0].clusterParam, hier_param_list,[0, 1, 2, 3, 4, 5, 6])) and len(brch_lh) > 0:
                                        j['detail'] = "Can run"
                                    else:
                                        j['detail'] = "Cannot run"
                        else:
                            i['output'] = "Unavailable"
                elif list_checker(i['action'], depen_list, [14, 15]):
                    i['output'] = "Unavailable"
                elif list_checker(i['action'], depen_list, [16]):
                    brch_bls = block.objects.filter(user_id=i['username'], project_name=i['project_name'],
                                                   session_name=i['session_name'], session_ver=int(i['session_ver']),
                                                   parent_block_iden=i['block_iden'], parent_block_ver__gte=0)
                    ori_bls = block.objects.filter(user_id = i['username'], project_name=i['project_name'],
                                                   session_name=i['session_name'], session_ver=int(i['session_ver']),
                                                   block_iden=i['block_iden'], block_ver__gte=0)
                    if len(brch_bls) is not 0 or len(ori_bls) is not 0:
                        i['output'] = "Available"
                    else:
                        i['output'] = "Unavailable"
                elif list_checker(i['action'], depen_list, [17]):
                    # check pcp column order
                    pcp_lho = log_history.objects.filter(action=i['action'],
                                                          user_id=i['username'], project_name=i['project_name'],
                                                          session_name=i['session_name'],
                                                          session_ver=int(i['session_ver']),
                                                          block_iden=i['block_iden'], block_ver__lt=int(i['block_ver']),
                                                        is_undo=False).order_by("-creatation_date")
                    if len(pcp_lho) > 0:
                        i['output'] = "Available"
                    else:
                        i['output'] = "Unavailable"
                elif list_checker(i['action'], depen_list, [18]):
                    # check pcp slected index
                    pcp_lho = log_history.objects.filter(action=i['action'],
                                                         user_id=i['username'], project_name=i['project_name'],
                                                         session_name=i['session_name'],
                                                         session_ver=int(i['session_ver']),
                                                         block_iden=i['block_iden'], block_ver__lt=int(i['block_ver']),
                                                         is_undo=False).order_by("-creatation_date")
                    if len(pcp_lho) > 0:
                        i['output'] = "Available"
                    else:
                        i['output'] = "Unavailable"
                elif list_checker(i['action'], depen_list, [19]):
                    scm_lho = log_history.objects.filter(action=i['action'],
                                                         user_id=i['username'], project_name=i['project_name'],
                                                         session_name=i['session_name'],
                                                         session_ver=int(i['session_ver']),
                                                         block_iden=i['block_iden'], block_ver__lt=int(i['block_ver']),
                                                         is_undo=False).order_by("-creatation_date")
                    if len(scm_lho) > 0:
                        i['output'] = "Available"
                    else:
                        i['output'] = "Unavailable"
                else:
                    i['output'] = "Unavailable"
            """
            for i in block_list:
                if i['output'] == "Unavailable":
                    continue
                if (i['action'] == "Change-Cluster-Parameter" or i['action'] == "Change-Cluster-Type") and \
                     i['output'] == "Need to select":
                    saved_lh = log_history.objects.filter(action = i['action'],
                                                          user_id = i['username'], project_name = i['project_name'],
                                                          session_name = i['session_name'], session_ver = int(i['session_ver']),
                                                          block_iden = i['block_iden'], block_ver__lte = i['block_ver'],
                                                          is_used = True, is_undo = False).order_by("-creatation_date")
                    brch_lh = log_history.objects.filter(action = i['action'],
                                                         user_id = i['username'], project_name = i['project_name'],
                                                         session_name = i['session_name'], session_ver = int(i['session_ver']),
                                                         block_iden = lho.parent_block_iden, block_ver__lte = int(lho.parent_block_ver),
                                                         is_used = True, is_undo = False).order_by("-creatation_date")
                    if len(saved_lh) > 0:
                        prev_lh = saved_lh[0]
                    else:
                        prev_lh = brch_lh[0]
                    for j in i['depend']:
                        prev_bl = block.objects.get(user_id = i['username'], project_name = i['project_name'], session_name = i['session_name'], session_ver = int(i['session_ver']), block_iden = j['block_iden'], block_ver = int(j['block_ver']))
                        if i['action'] == "Change-Cluster-Type" and \
                           ((prev_lh.clusterType == "Hierarchy" and list_checker(prev_bl.clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])) or \
                           ((prev_lh.clusterType == "KMeans" or prev_lh.clusterType == "Spectral") and not list_checker(prev_bl.clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6]))):
                            j['detail'] = "Can run"
                        elif i['action'] == "Change-Cluster-Parameter" and \
                             ((prev_bl.clusterType == "Hierarchy" and list_checker(prev_lh.clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6])) or \
                             ((prev_bl.clusterType == "KMeans" or prev_bl.clusterType == "Spectral") and not list_checker(prev_lh.clusterParam, hier_param_list, [0, 1, 2, 3, 4, 5, 6]))):
                            j['detail'] = "Can run"
                        else:
                            j['detail'] = "Cannot run"
            """
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Dependency Checked.", 'output' : block_list}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : "No block list.", 'output' : errors}) ,content_type="application/json")

def undo_action(request):
    errors = []
    if request.method == 'POST':
        # check necessary information
        param_list = ['action_list']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get necessary information
            action_list = request.POST.get('action_list')
            action_list = eval(json.loads(json.dumps(action_list)))
            for i in action_list:
                bl = block.objects.filter(user_id = i['username'], project_name = i['project_name'],
                                       session_name = i['session_name'], session_ver = int(i['session_ver']),
                                       block_iden = i['block_iden'], block_ver = int(i['block_ver']))
                lho = log_history.objects.get(action_id=int(i['action_id']))
                undo_bl = undo_block(action = i['action'],
                                     user_id = i['username'], project_name = i['project_name'],
                                     session_name = i['session_name'], session_ver = int(i['session_ver']),
                                     block_iden = i['block_iden'], block_ver = int(i['block_ver']))
                undo_bl.save()
                if lho.is_used == False:
                    lho.__dict__.update(is_undo = True)
                    lho.save()
                else:
                    lho.__dict__.update(is_undo = True)
                    lho.save()

                undo_blo = undo_block.objects.filter(action = i['action'],
                                                     user_id = i['username'], project_name = i['project_name'],
                                                     session_name = i['session_name'], session_ver = int(i['session_ver']),
                                                     block_iden = i['block_iden'], block_ver = int(i['block_ver']))

                bl_info = {}
                bl_info['username'] = i['username']
                bl_info['project_name'] = i['project_name']
                bl_info['session_name'] = i['session_name']
                bl_info['session_ver'] = int(i['session_ver'])
                bl_info['block_iden'] = i['block_iden']
                bl_info['block_ver'] = int(i['block_ver'])
                if bl[0].parent_block_iden is not None and bl[0].is_first == False:
                    bl_info['parent_block_iden'] = bl[0].parent_block_iden
                    bl_info['parent_block_ver'] = bl[0].parent_block_ver
                else:
                    bl_info['parent_block_iden'] = None
                    bl_info['parent_block_ver'] = None
                bl_list = []
                bl_list = find_ance(bl_list, bl_info)

                logs = []
                for j in bl_list:
                    saved_lh = log_history.objects.filter(action=i['action'],
                                                          user_id=i['username'], project_name=i['project_name'],
                                                          session_name=i['session_name'],
                                                          session_ver=int(i['session_ver']),
                                                          block_iden=j['block_iden'],
                                                          block_ver__lte=int(j['block_ver']),
                                                          is_used=True, is_undo=False).order_by("-creatation_date")
                    for k in saved_lh:
                        logs.append(k)
                    if len(logs) > 0:
                        break

                saved_lh = logs
                if i['action'] != depen_list[16] and i['action'] != depen_list[8]:
                    prev_lh = block.objects.filter(user_id = saved_lh[0].user_id, project_name = saved_lh[0].project_name, session_name = saved_lh[0].session_name, session_ver = int(saved_lh[0].session_ver), block_iden = saved_lh[0].block_iden, block_ver = int(saved_lh[0].block_ver))
                # 0, 1, 2, 3, 4, 5, 6, 7 - Unavailable
                # (8), (9, 10, 11), (12, 13), (14, 15), (16) - Available
                #undo_blo.update(vis_types = bl[0].vis_types)
                if list_checker(i['action'], depen_list, [8]):
                    del_bls = block.objects.filter(user_id=i['username'], project_name=i['project_name'],
                                                   session_name=i['session_name'], session_ver=int(i['session_ver']),
                                                   block_iden=i['block_iden'], block_ver__gte=0, is_closed=True)
                    del_bls.update(is_closed=False)
                elif list_checker(i['action'], depen_list, [9]):
                    undo_blo.update(data = bl[0].data)
                    undo_blo.update(data_name = bl[0].data_name)
                elif list_checker(i['action'], depen_list, [10]):
                    undo_blo.update(block_name = bl[0].block_name)
                elif list_checker(i['action'], depen_list, [11]):
                    undo_blo.update(colors = bl[0].colors)
                elif list_checker(i['action'], depen_list, [12]):
                    undo_blo.update(clusterType = bl[0].clusterType)
                elif list_checker(i['action'], depen_list, [13]):
                    undo_blo.update(clusterParam = bl[0].clusterParam)
                elif list_checker(i['action'], depen_list, [16]):
                    act_brch_bls = []
                    act_brch_info = {}
                    act_brch_info['username'] = i['username']
                    act_brch_info['project_name'] = i['project_name']
                    act_brch_info['session_name'] = i['session_name']
                    act_brch_info['session_ver'] = i['session_ver']
                    act_brch_info['block_iden'] = i['block_iden']
                    act_brch_info['block_ver'] = int(i['block_ver'])
                    act_brch_bls = find_unit(act_brch_bls, act_brch_info)
                    for brch_bl in act_brch_bls:
                        get_brch_bl = block.objects.filter(user_id=i['username'], project_name=i['project_name'],
                                                   session_name=i['session_name'], session_ver=int(i['session_ver']),
                                                   block_iden=brch_bl['block_iden'], block_ver = brch_bl['block_ver'])
                        get_brch_bl.update(is_closed = True)
                elif list_checker(i['action'], depen_list, [17]):
                    undo_blo.update(pcp_id=bl[0].pcp_id)
                elif list_checker(i['action'], depen_list, [18]):
                    undo_blo.update(pcp_id=bl[0].pcp_id)
                elif list_checker(i['action'], depen_list, [19]):
                    undo_blo.update(scm_id=bl[0].scm_id)

                if ('depend' in i) == False:
                    i['depend'] = None
                undo_blo.update(block_list = i['depend'])

                depen_bls = []
                if i['depend'] is not None:
                    depen_bls = i['depend']
                else:
                    depen_elem = {}
                    depen_elem['block_iden'] = i['block_iden']
                    depen_elem['block_ver'] = int(i['block_ver'])
                    depen_elem['detail'] = "Can run"
                    depen_bls.append(depen_elem)
                for j in depen_bls:
                    if j['detail'] == "Can run":
                        depen_bl = block.objects.filter(user_id = i['username'], project_name = i['project_name'],
                                                        session_name = i['session_name'], session_ver = int(i['session_ver']),
                                                        block_iden = j['block_iden'], block_ver = int(j['block_ver']))
                        if i['action'] != depen_list[16] or i['action'] != depen_list[8]:
                            if list_checker(i['action'], depen_list, [9]):
                                depen_bl.update(data=prev_lh[0].data)
                                depen_bl.update(data_name=prev_lh[0].data_name)
                            elif list_checker(i['action'], depen_list, [10]):
                                depen_bl.update(block_name = prev_lh[0].block_name)
                            elif list_checker(i['action'], depen_list, [11]):
                                depen_bl.update(colors = prev_lh[0].colors)
                            elif list_checker(i['action'], depen_list, [12]):
                                depen_bl.update(clusterType = prev_lh[0].clusterType)
                            elif list_checker(i['action'], depen_list, [13]):
                                depen_bl.update(clusterParam = prev_lh[0].clusterParam)
                            elif list_checker(i['action'], depen_list, [17]):
                                depen_bl.update(pcp_id=prev_lh[0].pcp_id)
                            elif list_checker(i['action'], depen_list, [18]):
                                depen_bl.update(pcp_id=prev_lh[0].pcp_id)
                            elif list_checker(i['action'], depen_list, [19]):
                                depen_bl.update(scm_id=prev_lh[0].scm_id)

                            depen_bl.update(data = depen_bl[0].data)
                            request_json = []
                            rj_elem = {}
                            bl_info = {}
                            rj_elem['username'] = bl_info['username'] = depen_bl[0].user_id
                            rj_elem['project_name'] = bl_info['project_name'] = depen_bl[0].project_name
                            rj_elem['session_name'] = bl_info['session_name'] = depen_bl[0].session_name
                            rj_elem['session_ver'] = bl_info['session_ver'] = int(depen_bl[0].session_ver)
                            rj_elem['block_iden'] = bl_info['block_iden'] = depen_bl[0].block_iden
                            rj_elem['block_name'] = depen_bl[0].block_name
                            rj_elem['block_ver'] = bl_info['block_ver'] = int(depen_bl[0].block_ver)
                            rj_elem['parent_block_iden'] = depen_bl[0].parent_block_iden
                            rj_elem['parent_block_ver'] = int(depen_bl[0].parent_block_ver)
                            rj_elem['data'] = bl_info['data'] = depen_bl[0].data
                            rj_elem['data_annotation'] = depen_bl[0].data_annotation
                            rj_elem['data_name'] = depen_bl[0].data_name
                            rj_elem['color_type'] = depen_bl[0].colors
                            rj_elem['vis_types'] = depen_bl[0].vis_types
                            if depen_bl[0].vis_types == "Heatmap":
                                rj_elem['cluster_type'] = depen_bl[0].clusterType
                                rj_elem['cluster_param'] = depen_bl[0].clusterParam
                                rj_elem['color_type'] = depen_bl[0].colors
                            elif depen_bl[0].vis_types == "Parallel Coordinate Plot":
                                pcp_obj = pcp.objects.filter(pcp_id = depen_bl[0].pcp_id)
                                if list_checker(i['action'], depen_list, [17]):
                                    rj_elem['column_order'] = pcp_obj[0].column_order
                                    rj_elem['selected_index'] = pcp_obj[0].selected_index
                                    rj_elem['brushed_axis'] = pcp_obj[0].brushed_axis
                                    rj_elem['brushed_range'] = pcp_obj[0].brushed_range
                                elif list_checker(i['action'], depen_list, [18]):
                                    rj_elem['selected_index'] = pcp_obj[0].selected_index
                                    rj_elem['column_order'] = pcp_obj[0].column_order
                                    rj_elem['brushed_axis'] = pcp_obj[0].brushed_axis
                                    rj_elem['brushed_range'] = pcp_obj[0].brushed_range
                            elif depen_bl[0].vis_types == "Scatterplot Matrix":
                                scm_obj = scm.objects.filter(scm_id=depen_bl[0].scm_id)
                                rj_elem['selected_index'] = scm_obj[0].selected_index
                                rj_elem['brushed_axis'] = scm_obj[0].brushed_axis
                                rj_elem['brushed_range'] = scm_obj[0].brushed_range
                            elif depen_bl[0].vis_types == "Scatter Plot":
                                sp_obj = sp.objects.filter(sp_id=depen_bl[0].sp_id)
                                rj_elem['x_axis'] = sp_obj[0].x_axis
                                rj_elem['y_axis'] = sp_obj[0].y_axis
                                rj_elem['brushed_range'] = sp_obj[0].brushed_range
                            request_json.append(rj_elem)
                            position_json = []
                            position = {}
                            position['top'] = depen_bl[0].position_top
                            position['left'] = depen_bl[0].position_left
                            position['height'] = depen_bl[0].position_height
                            position['width'] = depen_bl[0].position_width
                            position_json.append(position)

                            bl_info['request_json'] = request_json
                            bl_info['position_json'] = position
                            bl_info['is_cluster'] = False
                            data_type = rj_elem['data_name'][rj_elem['data_name'].find(".") + 1:rj_elem['data_name'].find(" (")]
                            bl_info['data_type'] = data_type
                            bl_info['vis_types'] = depen_bl[0].vis_types
                            if bl_info['vis_types'] == "Heatmap":
                                bl_info['cluster_type'] = depen_bl[0].clusterType
                                bl_info['cluster_param'] = depen_bl[0].clusterParam
                                bl_info['color_type'] = depen_bl[0].colors
                            elif bl_info['vis_types'] == "Parallel Coordinate Plot":
                                pcp_obj = pcp.objects.filter(pcp_id = depen_bl[0].pcp_id)
                                if list_checker(i['action'], depen_list, [17]):
                                    bl_info['column_order'] = pcp_obj[0].column_order
                                    bl_info['selected_index'] = pcp_obj[0].selected_index
                                    bl_info['brushed_axis'] = pcp_obj[0].brushed_axis
                                    bl_info['brushed_range'] = pcp_obj[0].brushed_range
                                elif list_checker(i['action'], depen_list, [18]):
                                    bl_info['selected_index'] = pcp_obj[0].selected_index
                                    bl_info['column_order'] = pcp_obj[0].column_order
                                    bl_info['brushed_axis'] = pcp_obj[0].brushed_axis
                                    bl_info['brushed_range'] = pcp_obj[0].brushed_range
                            elif bl_info['vis_types'] == "Scatterplot Matrix":
                                scm_obj = scm.objects.filter(scm_id=depen_bl[0].scm_id)
                                bl_info['selected_index'] = scm_obj[0].selected_index
                                bl_info['brushed_axis'] = scm_obj[0].brushed_axis
                                bl_info['brushed_range'] = scm_obj[0].brushed_range
                            elif bl_info['vis_types'] == "Scatter Plot":
                                sp_obj = sp.objects.filter(sp_id=depen_bl[0].sp_id)
                                bl_info['x_axis'] = sp_obj[0].x_axis
                                bl_info['y_axis'] = sp_obj[0].y_axis
                                bl_info['brushed_range'] = sp_obj[0].brushed_range

                            run_vis(bl_info)

                    else:
                        depen_bl = block.objects.filter(user_id=i['username'], project_name=i['project_name'],
                                                        session_name=i['session_name'],
                                                        session_ver=int(i['session_ver']),
                                                        block_iden=j['block_iden'], block_ver=int(j['block_ver']))
                        depen_bl.update(is_broken = True)
            """
            #renew the last_date of project and session
            if len(block_list) != 0:
                proj_rn = project.objects.filter(user_id = block_list[0]['username'], project_name = block_list[0]['project_name'])
                proj_rn.update(last_date = datetime.datetime.now())
                ses_rn = session.objects.filter(user_id =  block_list[0]['username'], project_name =  block_list[0]['project_name'], session_name =  block_list[0]['session_name'], session_ver = int( block_list[0]['session_ver']))
                ses_rn.update(last_date = datetime.datetime.now())
            """
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Get Unit information.", 'output' : None}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : "lack information.", 'output' : errors}) ,content_type="application/json")


def redo_action(request):
    errors = []
    if request.method == 'POST':
        # check necessary information
        param_list = ['action_list']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get necessary information
            action_list = request.POST.get('action_list')
            action_list = eval(json.loads(json.dumps(action_list)))
            block_list = []
            for i in action_list:
                action = log_history.objects.get(action_id=int(i['action_id']))
                action_elem = {}
                action_elem['action_id'] = action.action_id
                action_elem['username'] = action.user_id
                action_elem['project_name'] = action.project_name
                action_elem['session_name'] = action.session_name
                action_elem['session_ver'] = action.session_ver
                action_elem['block_iden'] = action.block_iden
                action_elem['block_ver'] = action.block_ver
                action_elem['action'] = action.action
                if action.is_undo == True:
                    block_list.append(action_elem)
            result_list = []
            for i in block_list:
                result_elem = {}
                lho = log_history.objects.get(action_id = int(i['action_id']))
                if lho.is_undo == False:
                    result_elem['result'] = "It didn't undo action"
                    result_list.append(result_elem)
                    continue
                lho.__dict__.update(is_undo = False)
                lho.save()
                undo_blo = undo_block.objects.filter(action = i['action'],
                                                     user_id = i['username'], project_name = i['project_name'],
                                                     session_name = i['session_name'], session_ver = int(i['session_ver']),
                                                     block_iden = i['block_iden'], block_ver = int(i['block_ver']))
                if undo_blo[0].block_list is not None:
                    undo_list = eval(json.loads(json.dumps(undo_blo[0].block_list)))
                else:
                    undo_list = []
                depen_bls = []
                if len(undo_list) != 0:
                    depen_bls = undo_list
                else:
                    depen_elem = {}
                    depen_elem['block_iden'] = i['block_iden']
                    depen_elem['block_ver'] = int(i['block_ver'])
                    depen_elem['detail'] = "Can run"
                    depen_bls.append(depen_elem)
                for j in depen_bls:
                    if i['action'] != action_check_list[12] and i['action'] != action_check_list[13]:
                        if j['detail'] == "Can run":
                            depen_bl = block.objects.filter(user_id = i['username'], project_name = i['project_name'],
                                                            session_name = i['session_name'], session_ver = int(i['session_ver']),
                                                            block_iden = j['block_iden'], block_ver = int(j['block_ver']))
                            # 0, 1, 2, 3, 4, 5, 6, 7 - Unavailable
                            # (8), (9, 10, 11), (12, 13), (14, 15), (16) - Available
                            if list_checker(i['action'], depen_list, [8]):
                                del_bls = block.objects.filter(user_id=i['username'], project_name=i['project_name'],
                                                               session_name=i['session_name'],
                                                               session_ver=int(i['session_ver']),
                                                               block_iden=i['block_iden'], block_ver__gte=0, is_closed=False)
                                del_bls.update(is_closed=False)
                            elif list_checker(i['action'], depen_list, [9]):
                                depen_bl.update(data=undo_blo[0].data)
                                depen_bl.update(data_name=undo_blo[0].data_name)
                            elif list_checker(i['action'], depen_list, [10]):
                                depen_bl.update(block_name=undo_blo[0].block_name)
                            elif list_checker(i['action'], depen_list, [11]):
                                depen_bl.update(colors=undo_blo[0].colors)
                            elif list_checker(i['action'], depen_list, [12]):
                                depen_bl.update(clusterType=undo_blo[0].clusterType)
                            elif list_checker(i['action'], depen_list, [13]):
                                depen_bl.update(clusterParam=undo_blo[0].clusterParam)
                            elif list_checker(i['action'], depen_list, [16]):
                                act_brch_bls = []
                                act_brch_info = {}
                                act_brch_info['username'] = i['username']
                                act_brch_info['project_name'] = i['project_name']
                                act_brch_info['session_name'] = i['session_name']
                                act_brch_info['session_ver'] = i['session_ver']
                                act_brch_info['block_iden'] = i['block_iden']
                                act_brch_info['block_ver'] = int(i['block_ver'])
                                act_brch_bls = find_unit(act_brch_bls, act_brch_info)
                                for brch_bl in act_brch_bls:
                                    get_brch_bl = block.objects.filter(user_id=i['username'], project_name=i['project_name'],
                                                                       session_name=i['session_name'],
                                                                       session_ver=int(i['session_ver']),
                                                                       block_iden=brch_bl['block_iden'],
                                                                       block_ver=brch_bl['block_ver'])
                                    get_brch_bl.update(is_closed=False)
                            elif list_checker(i['action'], depen_list, [17]):
                                depen_bl.update(pcp_id=undo_blo[0].pcp_id)
                            elif list_checker(i['action'], depen_list, [18]):
                                depen_bl.update(pcp_id=undo_blo[0].pcp_id)
                            elif list_checker(i['action'], depen_list, [19]):
                                depen_bl.update(scm_id=undo_blo[0].scm_id)

                            request_json = []
                            rj_elem = {}
                            bl_info = {}
                            rj_elem['username'] = bl_info['username'] = depen_bl[0].user_id
                            rj_elem['project_name'] = bl_info['project_name'] = depen_bl[0].project_name
                            rj_elem['session_name'] = bl_info['session_name'] = depen_bl[0].session_name
                            rj_elem['session_ver'] = bl_info['session_ver'] = int(depen_bl[0].session_ver)
                            rj_elem['block_iden'] = bl_info['block_iden'] = depen_bl[0].block_iden
                            rj_elem['block_name'] = depen_bl[0].block_name
                            rj_elem['block_ver'] = bl_info['block_ver'] = int(depen_bl[0].block_ver)
                            rj_elem['parent_block_iden'] = depen_bl[0].parent_block_iden
                            rj_elem['parent_block_ver'] = int(depen_bl[0].parent_block_ver)
                            rj_elem['data'] = bl_info['data'] = depen_bl[0].data
                            rj_elem['data_annotation'] = depen_bl[0].data_annotation
                            rj_elem['data_name'] = depen_bl[0].data_name
                            rj_elem['color_type'] = depen_bl[0].colors
                            rj_elem['vis_types'] = depen_bl[0].vis_types
                            if depen_bl[0].vis_types == "Heatmap":
                                rj_elem['cluster_type'] = depen_bl[0].clusterType
                                rj_elem['cluster_param'] = depen_bl[0].clusterParam
                                rj_elem['color_type'] = depen_bl[0].colors
                            elif depen_bl[0].vis_types == "Parallel Coordinate Plot":
                                pcp_obj = pcp.objects.filter(pcp_id = depen_bl[0].pcp_id)
                                if list_checker(i['action'], depen_list, [17]):
                                    rj_elem['column_order'] = pcp_obj[0].column_order
                                    rj_elem['selected_index'] = pcp_obj[0].selected_index
                                    rj_elem['brushed_axis'] = pcp_obj[0].brushed_axis
                                    rj_elem['brushed_range'] = pcp_obj[0].brushed_range
                                elif list_checker(i['action'], depen_list, [18]):
                                    rj_elem['selected_index'] = pcp_obj[0].selected_index
                                    rj_elem['column_order'] = pcp_obj[0].column_order
                                    rj_elem['brushed_axis'] = pcp_obj[0].brushed_axis
                                    rj_elem['brushed_range'] = pcp_obj[0].brushed_range
                            elif depen_bl[0].vis_types == "Scatterplot Matrix":
                                scm_obj = scm.objects.filter(scm_id=depen_bl[0].scm_id)
                                rj_elem['selected_index'] = scm_obj[0].selected_index
                                rj_elem['brushed_axis'] = scm_obj[0].brushed_axis
                                rj_elem['brushed_range'] = scm_obj[0].brushed_range
                            elif depen_bl[0].vis_types == "Scatter Plot":
                                sp_obj = sp.objects.filter(sp_id=depen_bl[0].sp_id)
                                rj_elem['x_axis'] = sp_obj[0].x_axis
                                rj_elem['y_axis'] = sp_obj[0].y_axis
                                rj_elem['brushed_range'] = sp_obj[0].brushed_range
                            request_json.append(rj_elem)
                            position_json = []
                            position = {}
                            position['top'] = depen_bl[0].position_top
                            position['left'] = depen_bl[0].position_left
                            position['height'] = depen_bl[0].position_height
                            position['width'] = depen_bl[0].position_width
                            position_json.append(position)

                            bl_info['request_json'] = request_json
                            bl_info['position_json'] = position
                            bl_info['is_cluster'] = False
                            data_type = rj_elem['data_name'][rj_elem['data_name'].find(".") + 1:rj_elem['data_name'].find(" (")]
                            bl_info['data_type'] = data_type
                            bl_info['vis_types'] = depen_bl[0].vis_types
                            if bl_info['vis_types'] == "Heatmap":
                                bl_info['cluster_type'] = depen_bl[0].clusterType
                                bl_info['cluster_param'] = depen_bl[0].clusterParam
                                bl_info['color_type'] = depen_bl[0].colors
                            elif bl_info['vis_types'] == "Parallel Coordinate Plot":
                                pcp_obj = pcp.objects.filter(pcp_id = depen_bl[0].pcp_id)
                                if list_checker(i['action'], depen_list, [17]):
                                    bl_info['column_order'] = pcp_obj[0].column_order
                                    bl_info['selected_index'] = pcp_obj[0].selected_index
                                    bl_info['brushed_axis'] = pcp_obj[0].brushed_axis
                                    bl_info['brushed_range'] = pcp_obj[0].brushed_range
                                elif list_checker(i['action'], depen_list, [18]):
                                    bl_info['selected_index'] = pcp_obj[0].selected_index
                                    bl_info['column_order'] = pcp_obj[0].column_order
                                    bl_info['brushed_axis'] = pcp_obj[0].brushed_axis
                                    bl_info['brushed_range'] = pcp_obj[0].brushed_range
                            elif bl_info['vis_types'] == "Scatterplot Matrix":
                                scm_obj = scm.objects.filter(scm_id=depen_bl[0].scm_id)
                                bl_info['selected_index'] = scm_obj[0].selected_index
                                bl_info['brushed_axis'] = scm_obj[0].brushed_axis
                                bl_info['brushed_range'] = scm_obj[0].brushed_range
                            elif bl_info['vis_types'] == "Scatter Plot":
                                sp_obj = sp.objects.filter(sp_id=depen_bl[0].sp_id)
                                bl_info['x_axis'] = sp_obj[0].x_axis
                                bl_info['y_axis'] = sp_obj[0].y_axis
                                bl_info['brushed_range'] = sp_obj[0].brushed_range


                            run_vis(bl_info)
                        else:
                            depen_bl = block.objects.filter(user_id=i['username'], project_name=i['project_name'],
                                                            session_name=i['session_name'],
                                                            session_ver=int(i['session_ver']),
                                                            block_iden=j['block_iden'], block_ver=int(j['block_ver']))
                            depen_bl.update(is_broken = True)
                    else:
                        if j['detail'] == "Cannot run":
                            depen_bl = block.objects.filter(user_id=i['username'], project_name=i['project_name'],
                                                            session_name=i['session_name'],
                                                            session_ver=int(i['session_ver']),
                                                            block_iden=j['block_iden'], block_ver=int(j['block_ver']))
                            # 0, 1, 2, 3, 4, 5, 6, 7 - Unavailable
                            # (8), (9, 10, 11), (12, 13), (14, 15), (16) - Available
                            if list_checker(i['action'], depen_list, [8]):
                                del_bls = block.objects.filter(user_id=i['username'], project_name=i['project_name'],
                                                               session_name=i['session_name'],
                                                               session_ver=int(i['session_ver']),
                                                               block_iden=i['block_iden'], block_ver__gte=0,
                                                               is_closed=False)
                                del_bls.update(is_closed=False)
                            elif list_checker(i['action'], depen_list, [9]):
                                depen_bl.update(data=undo_blo[0].data)
                                depen_bl.update(data_name=undo_blo[0].data_name)
                            elif list_checker(i['action'], depen_list, [10]):
                                depen_bl.update(block_name=undo_blo[0].block_name)
                            elif list_checker(i['action'], depen_list, [11]):
                                depen_bl.update(colors=undo_blo[0].colors)
                            elif list_checker(i['action'], depen_list, [12]):
                                depen_bl.update(clusterType=undo_blo[0].clusterType)
                            elif list_checker(i['action'], depen_list, [13]):
                                depen_bl.update(clusterParam=undo_blo[0].clusterParam)
                            elif list_checker(i['action'], depen_list, [16]):
                                act_brch_bls = []
                                act_brch_info = {}
                                act_brch_info['username'] = i['username']
                                act_brch_info['project_name'] = i['project_name']
                                act_brch_info['session_name'] = i['session_name']
                                act_brch_info['session_ver'] = i['session_ver']
                                act_brch_info['block_iden'] = i['block_iden']
                                act_brch_info['block_ver'] = int(i['block_ver'])
                                act_brch_bls = find_unit(act_brch_bls, act_brch_info)
                                for brch_bl in act_brch_bls:
                                    get_brch_bl = block.objects.filter(user_id=i['username'],
                                                                       project_name=i['project_name'],
                                                                       session_name=i['session_name'],
                                                                       session_ver=int(i['session_ver']),
                                                                       block_iden=brch_bl['block_iden'],
                                                                       block_ver=brch_bl['block_ver'])
                                    get_brch_bl.update(is_closed=False)
                            elif list_checker(i['action'], depen_list, [17]):
                                depen_bl.update(pcp_id=undo_blo[0].pcp_id)
                            elif list_checker(i['action'], depen_list, [18]):
                                depen_bl.update(pcp_id=undo_blo[0].pcp_id)
                            elif list_checker(i['action'], depen_list, [19]):
                                depen_bl.update(scm_id=undo_blo[0].scm_id)

                            request_json = []
                            rj_elem = {}
                            bl_info = {}
                            rj_elem['username'] = bl_info['username'] = depen_bl[0].user_id
                            rj_elem['project_name'] = bl_info['project_name'] = depen_bl[0].project_name
                            rj_elem['session_name'] = bl_info['session_name'] = depen_bl[0].session_name
                            rj_elem['session_ver'] = bl_info['session_ver'] = int(depen_bl[0].session_ver)
                            rj_elem['block_iden'] = bl_info['block_iden'] = depen_bl[0].block_iden
                            rj_elem['block_name'] = depen_bl[0].block_name
                            rj_elem['block_ver'] = bl_info['block_ver'] = int(depen_bl[0].block_ver)
                            rj_elem['parent_block_iden'] = depen_bl[0].parent_block_iden
                            rj_elem['parent_block_ver'] = int(depen_bl[0].parent_block_ver)
                            rj_elem['data'] = bl_info['data'] = depen_bl[0].data
                            rj_elem['data_annotation'] = depen_bl[0].data_annotation
                            rj_elem['data_name'] = depen_bl[0].data_name
                            rj_elem['color_type'] = depen_bl[0].colors
                            rj_elem['vis_types'] = depen_bl[0].vis_types
                            if depen_bl[0].vis_types == "Heatmap":
                                rj_elem['cluster_type'] = depen_bl[0].clusterType
                                rj_elem['cluster_param'] = depen_bl[0].clusterParam
                                rj_elem['color_type'] = depen_bl[0].colors
                            elif depen_bl[0].vis_types == "Parallel Coordinate Plot":
                                pcp_obj = pcp.objects.filter(pcp_id=depen_bl[0].pcp_id)
                                if list_checker(i['action'], depen_list, [17]):
                                    rj_elem['column_order'] = pcp_obj[0].column_order
                                    rj_elem['selected_index'] = pcp_obj[0].selected_index
                                    rj_elem['brushed_axis'] = pcp_obj[0].brushed_axis
                                    rj_elem['brushed_range'] = pcp_obj[0].brushed_range
                                elif list_checker(i['action'], depen_list, [18]):
                                    rj_elem['selected_index'] = pcp_obj[0].selected_index
                                    rj_elem['column_order'] = pcp_obj[0].column_order
                                    rj_elem['brushed_axis'] = pcp_obj[0].brushed_axis
                                    rj_elem['brushed_range'] = pcp_obj[0].brushed_range
                            elif depen_bl[0].vis_types == "Scatterplot Matrix":
                                scm_obj = scm.objects.filter(scm_id=depen_bl[0].scm_id)
                                rj_elem['selected_index'] = scm_obj[0].selected_index
                                rj_elem['brushed_axis'] = scm_obj[0].brushed_axis
                                rj_elem['brushed_range'] = scm_obj[0].brushed_range
                            elif depen_bl[0].vis_types == "Scatter Plot":
                                sp_obj = sp.objects.filter(sp_id=depen_bl[0].sp_id)
                                rj_elem['x_axis'] = sp_obj[0].x_axis
                                rj_elem['y_axis'] = sp_obj[0].y_axis
                                rj_elem['brushed_range'] = sp_obj[0].brushed_range
                            request_json.append(rj_elem)
                            position_json = []
                            position = {}
                            position['top'] = depen_bl[0].position_top
                            position['left'] = depen_bl[0].position_left
                            position['height'] = depen_bl[0].position_height
                            position['width'] = depen_bl[0].position_width
                            position_json.append(position)

                            bl_info['request_json'] = request_json
                            bl_info['position_json'] = position
                            bl_info['is_cluster'] = False
                            data_type = rj_elem['data_name'][
                                        rj_elem['data_name'].find(".") + 1:rj_elem['data_name'].find(" (")]
                            bl_info['data_type'] = data_type
                            bl_info['vis_types'] = depen_bl[0].vis_types
                            if bl_info['vis_types'] == "Heatmap":
                                bl_info['cluster_type'] = depen_bl[0].clusterType
                                bl_info['cluster_param'] = depen_bl[0].clusterParam
                                bl_info['color_type'] = depen_bl[0].colors
                            elif bl_info['vis_types'] == "Parallel Coordinate Plot":
                                pcp_obj = pcp.objects.filter(pcp_id=depen_bl[0].pcp_id)
                                if list_checker(i['action'], depen_list, [17]):
                                    bl_info['column_order'] = pcp_obj[0].column_order
                                    bl_info['selected_index'] = pcp_obj[0].selected_index
                                    bl_info['brushed_axis'] = pcp_obj[0].brushed_axis
                                    bl_info['brushed_range'] = pcp_obj[0].brushed_range
                                elif list_checker(i['action'], depen_list, [18]):
                                    bl_info['selected_index'] = pcp_obj[0].selected_index
                                    bl_info['column_order'] = pcp_obj[0].column_order
                                    bl_info['brushed_axis'] = pcp_obj[0].brushed_axis
                                    bl_info['brushed_range'] = pcp_obj[0].brushed_range
                            elif bl_info['vis_types'] == "Scatterplot Matrix":
                                scm_obj = scm.objects.filter(scm_id=depen_bl[0].scm_id)
                                bl_info['selected_index'] = scm_obj[0].selected_index
                                bl_info['brushed_axis'] = scm_obj[0].brushed_axis
                                bl_info['brushed_range'] = scm_obj[0].brushed_range
                            elif bl_info['vis_types'] == "Scatter Plot":
                                sp_obj = sp.objects.filter(sp_id=depen_bl[0].sp_id)
                                bl_info['x_axis'] = sp_obj[0].x_axis
                                bl_info['y_axis'] = sp_obj[0].y_axis
                                bl_info['brushed_range'] = sp_obj[0].brushed_range

                            run_vis(bl_info)
                        else:
                            depen_bl = block.objects.filter(user_id=i['username'], project_name=i['project_name'],
                                                            session_name=i['session_name'],
                                                            session_ver=int(i['session_ver']),
                                                            block_iden=j['block_iden'], block_ver=int(j['block_ver']))
                            depen_bl.update(is_broken=True)

                result_elem['result'] = "Success"
                result_list.append(result_elem)
            """
            #renew the last_date of project and session
            if len(block_list) != 0:
                proj_rn = project.objects.filter(user_id = block_list[0]['username'], project_name = block_list[0]['project_name'])
                proj_rn.update(last_date = datetime.datetime.now())
                ses_rn = session.objects.filter(user_id =  block_list[0]['username'], project_name =  block_list[0]['project_name'], session_name =  block_list[0]['session_name'], session_ver = int( block_list[0]['session_ver']))
                ses_rn.update(last_date = datetime.datetime.now())
            """
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Success Redo Action.", 'output' : result_list}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : "lack information.", 'output' : errors}) ,content_type="application/json")