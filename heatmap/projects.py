from heatmap import *

@ensure_csrf_cookie
def create_project(request):
    """
    create a project
    """
    errors = []
    username = ""
    project_name = ""
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
            # check duplicated project
            try:
                pro_obj = project.objects.get(user_id = username, project_name = project_name)
                return HttpResponse(json.dumps({'success' : False, 'detail' : "Duplicated a project", 'output': project_name}) ,content_type="application/json")
            except project.DoesNotExist:
                pro_obj = None
            if not pro_obj:
                # check existence of project_annotation
                # save project information in the db
                if not request.POST.get('project_annotation', ''):
                    pro_reg = project(user_id = username, project_name = project_name)
                else:
                    project_annotation = '%r' % request.POST['project_annotation']
                    project_annotation = project_annotation.replace('\'', '')
                    pro_reg = project(user_id = username, project_name = project_name, project_annotation = project_annotation)
                pro_reg.save()
                # make project directory

                try:
                    os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name))
                except OSError as e:
                    if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member')) is False:
                        os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member'))
                    if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username)) is False:
                        os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username))
                        os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name))
                    if e.errno == 17:
                        pass
                return HttpResponse(json.dumps({'success' : True, 'detail' : "Created a project", 'output': project_name}) ,content_type="application/json")
            else:
                return HttpResponse(json.dumps({'success' : False, 'detail' : errors, 'output': None}) ,content_type="application/json")


@ensure_csrf_cookie
def delete_project(request):
    """
    Delete a project
    """
    errors = []
    username = ""
    project_name = ""
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
            try:
                # delete project, session, and block
                proj = project.objects.get(user_id = str(username), project_name = str(project_name))
                ses = session.objects.filter(user_id = username, project_name = project_name)
                ses_his = session_history.objects.filter(user_id = username, project_name = project_name)
                blocks = block.objects.all().filter(user_id = username, project_name = project_name)
                log_history.objects.filter(user_id = username, project_name = project_name, is_closed = False).update(is_closed = True)
                bl_anno = block_annotation_history.objects.filter(user_id = username, project_name = project_name).update(is_removed = True)
                blocks.delete()
                ses.delete()
                ses_his.delete()
                proj.delete()
                # delete directory
                shutil.rmtree(os.path.join(os.getcwd(), BASE_DIR, 'member', username, project_name))
                return HttpResponse(json.dumps({'success' : True, 'detail' : "Deleted project.", 'output' : str(project_name)}) ,content_type="application/json")
            except project.DoesNotExist:
                proj = None
                return HttpResponse(json.dumps({'success' : False, 'detail' : "No project.", 'output' : None}) ,content_type="application/json")

@ensure_csrf_cookie
def get_projects(request):
    errors = []
    username = ""
    if request.method == 'POST':
        # check information
        param_list = ['username']
        errors = param_checker(request, errors, param_list)
        if not errors:
            # get parameter
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            # get projects and save projects
            proj = project.objects.filter(user_id=username).values('user_id', 'project_name', 'project_annotation').annotate(last_date = Max('last_date')).distinct().order_by('-last_date')
            if proj.exists():
                projects = []
                for i in proj:
                    proj_elem = {}
                    proj_date = i['last_date'].strftime("%Y-%m-%d %H:%M:%S")
                    proj_elem['username'] = username
                    proj_elem['project_name'] = i['project_name']
                    proj_elem['lastEdited'] = proj_date
                    proj_elem['project_annotation'] = i['project_annotation']
                    projects.append(proj_elem)
                return HttpResponse(json.dumps({'success' : True, 'detail' : "Get session.", 'output' : projects}) ,content_type="application/json")
            #except session.DoesNotExist:
            else:
                ses = None
                return HttpResponse(json.dumps({'success' : True, 'detail' : "No session.", 'output' : None}) ,content_type="application/json")

