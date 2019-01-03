from heatmap import *

@ensure_csrf_cookie
def network(request):
    errors = []
    if request.method == 'POST':
        # check information
        param_list = ['gene_list', 'species', 'width', 'height', 'username', 'project_name', 'session_name', 'session_ver', 'block_iden', 'parent_block_iden']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get parameter
            ori_path = os.getcwd()
            gene_list = request.POST['gene_list']
            species = '%r' % request.POST['species']
            species = species.replace('\'', '')
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
            parent_block_iden = '%r' % request.POST['parent_block_iden']
            parent_block_iden = parent_block_iden.replace('\'', '')
            width = '%r' % request.POST['width']
            width = width.replace('\'', '')
            height = '%r' % request.POST['height']
            height = height.replace('\'', '')
            os.chdir('..')
            if os.path.exists(os.path.join(os.getcwd(), 'geonome-vis', 'static', 'member', username, project_name, session_name, session_ver, block_iden)) is False:
                os.mkdir(os.path.join(os.getcwd(), 'geonome-vis', 'static', 'member', username, project_name, session_name, session_ver, block_iden))
            input_path = os.path.join(os.getcwd(), 'geonome-vis', 'static', 'member', username, project_name, session_name, session_ver, block_iden, 'input.txt')
            input = open(input_path, 'w')
            input.write(gene_list)
            input.close()
            #subprocess.call(['cd', '..'], shell=True)
            #subprocess.call(['cd', os.path.join('static','file')], shell=True)
            os.chdir(os.path.join(os.getcwd(), 'geonome-vis', 'static', 'file'))
            if species == "human":
                subprocess.call(['python3 network_process.py ../member/' +username + '/' + project_name + '/' + session_name + '/' + session_ver + '/' + block_iden + '/input.txt 9606_human/9606.protein.links.v10.txt.to_gene_symbol ' + width + ' ' +  height + ' ' + username + ' ' + project_name + ' ' + session_name + ' ' + session_ver + ' ' + block_iden], shell=True)
            elif species == "rat":
                subprocess.call(['python3 network_process.py ../member/' +username + '/' + project_name + '/' + session_name + '/' + session_ver + '/' + block_iden + '/input.txt 10116_rat/10116.protein.links.v10.txt.to_gene_symbol ' + width + ' ' +  height + ' ' + username + ' ' + project_name + ' ' + session_name + ' ' + session_ver + ' ' + block_iden], shell=True)
            elif species == "mouse":
                subprocess.call(['python3 network_process.py ../member/' +username + '/' + project_name + '/' + session_name + '/' + session_ver + '/' + block_iden +  '/input.txt 10090_mouse/10090.protein.links.v10.txt.to_gene_symbol ' + width + ' ' +  height + ' ' + username + ' ' + project_name + ' ' + session_name + ' ' + session_ver + ' ' + block_iden], shell=True)

            node_path = os.path.join('static', 'member', username, project_name, session_name, session_ver, block_iden, 'result_node.txt')
            edge_path = os.path.join('static', 'member', username, project_name, session_name, session_ver, block_iden, 'result_edge.txt')
            os.chdir(ori_path)
            graph_path = os.path.join(os.getcwd(), 'static', 'member', username, project_name, session_name, session_ver, block_iden, 'graph.json')

            ['gene_list', 'species', 'width', 'height']
            request_json = []
            rj_elem = {}
            rj_elem['gene_list'] = gene_list
            rj_elem['species'] = species
            rj_elem['username'] = username
            rj_elem['project_name'] = project_name
            rj_elem['session_name'] = session_name
            rj_elem['session_ver'] = int(session_ver)
            rj_elem['block_iden'] = block_iden
            rj_elem['parent_block_iden'] = parent_block_iden
            rj_elem['width'] = width
            rj_elem['height'] = height
            rj_elem['graph_path'] = graph_path
            request_json.append(rj_elem)
            position = {}
            position['width'] = 800
            position['height'] = 600
            position['top'] = 0
            position['left'] = 0
            position_json = []
            position_json.append(position)

            response_json = [{"node_path": node_path, 'edge_path': edge_path, 'gene_list': gene_list,
                              'species': species, "username": username,
                              "project_name": project_name, "session_name": session_name,
                              "session_ver": int(session_ver), "block_iden": block_iden,
                              "parent_block_iden" : parent_block_iden, 'width' : width, 'height' : height, 'graph_path' : graph_path}]
            heatmap_json = json.dumps(
                {"request": request_json, "response": response_json, "position": position_json})

            infile = open(rj_elem['graph_path'], 'w')
            infile.write(heatmap_json)
            infile.close()

            get_p_bl_ver = block.objects.filter(user_id=username, project_name=project_name, session_name=session_name, session_ver = int(session_ver), block_iden = parent_block_iden, is_save = True).aggregate(Max('block_ver'))
            max_p_bl_ver = get_p_bl_ver['block_ver__max']
            if max_p_bl_ver is not None: #null
                max_p_bl_ver = int(max_p_bl_ver)
            else:
                max_p_bl_ver = None
            if max_p_bl_ver is None:
                #p_bl = block.objects.filter(user_id=username, project_name=project_name, session_name=session_name, session_ver = int(session_ver), block_iden = parent_block_iden, block_ver = int(max_p_bl_ver))
                bl = block(user_id=username, project_name=project_name, session_name=session_name, session_ver = int(session_ver), block_iden = block_iden, block_ver = 0,
                           ori_p_block_iden = parent_block_iden, ori_p_block_ver = int(0), is_graph = True, is_save = False, parent_block_iden = parent_block_iden, save_ver = 0)
                bl.save()
            else:
                p_bl = block.objects.filter(user_id=username, project_name=project_name, session_name=session_name,
                                            session_ver=int(session_ver), block_iden=parent_block_iden,
                                            block_ver=int(max_p_bl_ver))
                bl = block(user_id=username, project_name=project_name, session_name=session_name,
                           session_ver=int(session_ver), block_iden=block_iden, block_ver = 0,
                           ori_p_block_iden=parent_block_iden, ori_p_block_ver=int(max_p_bl_ver), is_graph=True,
                           is_save=True, parent_block_iden = parent_block_iden,  parent_block_ver = int(max_p_bl_ver), save_ver = 0)
                bl.save()


            if p_bl[0].parent_block_iden is not None:
                update_bl = block.objects.filter(block_id=bl.block_id)
                update_bl.update(parent_block_iden = p_bl[0].parent_block_iden, parent_block_ver = int(p_bl[0].parent_block_ver))
            else:
                update_bl = block.objects.filter(block_id=bl.block_id)
                update_bl.update(is_first = True)

            # Create Annotation File
            get_bl = block.objects.filter(user_id=username, project_name=project_name, session_name=session_name,
                                            session_ver=int(session_ver), block_iden=block_iden)
            annotation_path = os.path.join(os.getcwd(), 'static', 'member', username, project_name, session_name,
                                      session_ver, block_iden, 'annotation.json')
            infile = open(annotation_path, 'w')
            json_str = "{'annotation_list':[]}"
            json_str = json_str.replace("'", '"')
            infile.write(json_str)
            infile.close()

            return HttpResponse(json.dumps({'success' : True, 'detail' : "Get network.", 'output' : {'node_path' : node_path, 'edge_path' : edge_path}}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : True, 'detail' : "No network.", 'output' : None}) ,content_type="application/json")
