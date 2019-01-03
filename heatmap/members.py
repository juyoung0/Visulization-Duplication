from heatmap import *

@gzip_page
@ensure_csrf_cookie
def login(request):
    """
    check whether valid username or not
    """
    errors = []
    username = ""
    password = ""
    if request.method == 'POST':
        if not request.POST.get('username', ''):
            errors.append("Enter a username.")
        if not request.POST.get('password', ''):
            errors.append("Enter a password")
        if not errors:
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            password = '%r' % request.POST['password']
            password = password.replace('\'', '')
        try:
            user = member.objects.get(user_id=username)
        except member.DoesNotExist:
            user = None
        if not user:
            return HttpResponse(json.dumps({'success' : False, 'detail' : "Your username and password didn't match.", 'output' : None}) ,content_type="application/json")
        if user.user_pw == password:
            request.session['user_id'] = user.user_id
            ses = session.objects.filter(user_id=username).values('project_name', 'session_name', 'session_ver').annotate(last_date = Max('last_date')).distinct().order_by('-last_date')
            user_info = []
            user_info_elem = {}
            user_info_elem['username'] = username
            if ses.exists():
                user_info_elem['project_name'] = ses[0]['project_name']
                user_info_elem['lastEdited'] = ses[0]['last_date'].strftime("%Y-%m-%d %H:%M:%S")
                user_info_elem['session_name'] = ses[0]['session_name']
                user_info_elem['session_ver'] = ses[0]['session_ver']
            else:
                user_info_elem['project_name'] = None
                user_info_elem['lastEdtied'] = None
                user_info_elem['session_name'] = None
                user_info_elem['session_ver'] = None
            if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username)) is False:
                os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username))
            user_info.append(user_info_elem)
            return HttpResponse(json.dumps({'success' : True, 'detail' : 'Logged in', 'output' : user_info}) ,content_type="application/json")
        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : "Your username and password didn't match.", 'output': None}) ,content_type="application/json")
    errors_str = ""
    for i in errors:
        errors_str += i + " "
    return HttpResponse(json.dumps({'success' : False, 'detail' : errors_str, 'output': None}) ,content_type="application/json")


@ensure_csrf_cookie
def logout(request):
    """
    logout
    """
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponse(json.dumps({'success' : True, 'detail' : "Logged out.", 'output': None}) ,content_type="application/json")

@ensure_csrf_cookie
def register(request):
    """
    sign up a user
    """
    errors = []
    username = ""
    password = ""
    email = ""
    if request.method == 'POST':
        if not request.POST.get('username', ''):
            errors.append("Enter a username.")
        if not request.POST.get('password', ''):
            errors.append("Enter a password")
        if not request.POST.get('email', ''):
            errors.append("Enter a email")
        if not errors:
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            password = '%r' % request.POST['password']
            password = password.replace('\'', '')
            email = '%r' % request.POST['email']
            email = email.replace('\'', '')
            try:
                user = member.objects.get(user_id = username)
            except member.DoesNotExist:
                user = None
            if not user:
                reg = member(user_id = username, user_pw = password, email = email)
                reg.save()
                try:
                    os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username))
                except OSError as e:
                    if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', username)) is False:
                        os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member'))
                        os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', username))
                    if e.errno == 17:
                        pass
                return HttpResponse(json.dumps({'success' : True, 'detail' : "Congratulations to Register", 'output': username}) ,content_type="application/json")

            else:
                return HttpResponse(json.dumps({'success' : False, 'detail' : "Duplicated username", 'output': username}) ,content_type="application/json")

@ensure_csrf_cookie
def registerTest(request):
    return render(request, 'registerTest.html')

@ensure_csrf_cookie
def get_members(request):
    """
    get members
    """
    mems = member.objects.all()
    mem_list = []
    for i in mems:
        mem_elem = {}
        mem_elem['user_id'] = i.user_id
        mem_list.append(mem_elem)
    return HttpResponse(json.dumps({'success' : True, 'detail' : "Get members", 'output': mem_list}) ,content_type="application/json")

@ensure_csrf_cookie
def make_members(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('username', ''):
            errors.append("Enter a username.")
        if not request.POST.get('start_num', ''):
            errors.append("Enter a start_num")
        if not request.POST.get('last_num', ''):
            errors.append("Enter a last_num")
        if not errors:
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            start_num = '%r' % request.POST['start_num']
            start_num = start_num.replace('\'', '')
            last_num = '%r' % request.POST['last_num']
            last_num = last_num.replace('\'', '')
            for i in range(int(start_num), int(last_num)+1):
                user_id = username+str(i)
                try:
                    user = member.objects.get(user_id = user_id)
                except member.DoesNotExist:
                    user = None
                    if not user:
                        reg = member(user_id = user_id, user_pw = user_id, email = "a@a.a")
                        reg.save()
                        try:
                            os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', user_id))
                        except OSError as e:
                            if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', user_id)) is False:
                                os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member'))
                                os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member', user_id))
                            if e.errno == 17:
                                pass
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Congratulations to Register", 'output': ""}) ,content_type="application/json")

        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : "Duplicated username", 'output': ""}) ,content_type="application/json")

@ensure_csrf_cookie
def del_members(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('username', ''):
            errors.append("Enter a username.")
        if not request.POST.get('start_num', ''):
            errors.append("Enter a start_num")
        if not request.POST.get('last_num', ''):
            errors.append("Enter a last_num")
        if not errors:
            username = '%r' % request.POST['username']
            username = username.replace('\'', '')
            start_num = '%r' % request.POST['start_num']
            start_num = start_num.replace('\'', '')
            last_num = '%r' % request.POST['last_num']
            last_num = last_num.replace('\'', '')
            for i in range(int(start_num), int(last_num)+1):
                user_id = username+str(i)
                mem = member.objects.filter(user_id=user_id)
                if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member', user_id)) is True:
                    os.rmdir(os.path.join(os.getcwd(), BASE_DIR, 'member', user_id))
            return HttpResponse(json.dumps({'success' : True, 'detail' : "Deleted to Register", 'output': user_id}) ,content_type="application/json")

        else:
            return HttpResponse(json.dumps({'success' : False, 'detail' : "Duplicated username", 'output': user_id}) ,content_type="application/json")


