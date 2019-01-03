from heatmap import *

@ensure_csrf_cookie
def get_answer(request):
    errors = []
    if request.method == 'POST':
        """
        if not request.POST.get('username', ''):
            errors.append("Enter a username.")
        if not request.POST.get('start_num', ''):
            errors.append("Enter a start_num")
        if not request.POST.get('last_num', ''):
            errors.append("Enter a last_num")
            """
        if not errors:
            #username = '%r' % request.POST['username']
            #username = username.replace('\'', '')
            #start_num = '%r' % request.POST['start_num']
            #start_num = start_num.replace('\'', '')
            #last_num = '%r' % request.POST['last_num']
            #last_num = last_num.replace('\'', '')
            username = "S"
            start_num = 38
            last_num = 55
          # a_test_ans_list = ['78', '46.6', '46~230', 'Buick Estate Wagon (Wagon)', 'Buick Regal Sport Coupe (Turbo)', 'Mercedes-Benz 280S', '(1)', '2']
        # a_exp_ans_list = ['Buick Estate Wagon (Wagon)', 'Buick Regal Sport Coupe (Turbo)', 'Mercedes-Benz 280S', '(1)', '2']
            ans_list = ['buickestatewagon(wagon)', 'buickregalsportcoupe(turbo)', 'mercedes-benz280s', '(3)', '7']
            f = open(os.path.join(os.getcwd(), 'static', 'file', 'groupa_score.txt'), 'w')
            answer_sheet = []

            for i in range(int(start_num), int(last_num)+1):
                user_id = username+str(i)
                user_stat = {}

                try:

                    user = member.objects.get(user_id = user_id)
                    proj = project.objects.filter(user_id = user_id)

                    logs = log_history.objects.filter(user_id=user_id, action="Show-Session")
                    user_stat["user"] = user_id

                    proj_num = 0


                    ses = session.objects.filter(user_id=user_id, project_name="experiment")
                    project_name = "experiment"
                    if not ses:
                        ses = session.objects.filter(user_id=user_id, project_name="Experiment")
                        project_name = "Experiment"

                    u_ans_list = [None] * 5
                    for m in range(5):
                        u_ans_list[m] = ""
                    answer_list = [None] * 5
                    score_list = [None] * 5
                    conf_list = [None] * 5


                    for k in ses:


                        get_ses = session.objects.filter(user_id=user_id, project_name=project_name,
                                                         session_name=k.session_name).aggregate(Max('session_ver'))
                        max_ses_ver = get_ses['session_ver__max']
                        anno = block_annotation_history.objects.filter(user_id=user_id, project_name=project_name, session_name=k.session_name, session_ver=int(max_ses_ver))
                        ex_num = 0

                        for n in anno:
                            if len(re.findall('\d+', n.data_annotation)) > 0:
                                is_ans = False
                                if "ans" in n.data_annotation:
                                    is_ans = True

                                if is_ans is True:
                                    data_no_space = n.data_annotation.replace(' ', '')
                                    data_ans = data_no_space.replace(' ', '')

                                    for m in range(5):

                                        if "ans"+str(m+1) in data_ans:

                                            if u_ans_list[m] != ans_list[m]:
                                                answer_list[m] = n.data_annotation
                                                ans = data_ans.replace('ans'+str(m+1)+':','')
                                                conf_list[m] = n.research_annotation
                                                if m == 3:
                                                    if "1980" in ans:
                                                        ans = "(3)"
                                                if ans.lower() in ans_list[m]:
                                                    score_list[m] = "1"
                                                    u_ans_list[m] = n.data_annotation
                                                else:
                                                    score_list[m] = "0"

                    user_stat["score"] = score_list
                    user_stat["answer"] = answer_list
                    user_stat["conf"] = conf_list

                    answer_sheet.append(user_stat)


                except member.DoesNotExist:
                    continue
                except project.DoesNotExist:
                    continue

            f.write(json.dumps(answer_sheet))
            f.close()
        return HttpResponse(json.dumps({'success' : True, 'detail' : "Answer", 'output': None}) ,content_type="application/json")

    else:
        return HttpResponse(json.dumps({'success' : False, 'detail' : "Duplicated username", 'output': None}) ,content_type="application/json")

@ensure_csrf_cookie
def get_second_answer(request):
    errors = []
    if request.method == 'POST':
        """
        if not request.POST.get('username', ''):
            errors.append("Enter a username.")
        if not request.POST.get('start_num', ''):
            errors.append("Enter a start_num")
        if not request.POST.get('last_num', ''):
            errors.append("Enter a last_num")
            """
        if not errors:
            #username = '%r' % request.POST['username']
            #username = username.replace('\'', '')
            #start_num = '%r' % request.POST['start_num']
            #start_num = start_num.replace('\'', '')
            #last_num = '%r' % request.POST['last_num']
            #last_num = last_num.replace('\'', '')
            username = "S"
            start_num = 1
            last_num = 37
          # a_test_ans_list = ['78', '46.6', '46~230', 'Buick Estate Wagon (Wagon)', 'Buick Regal Sport Coupe (Turbo)', 'Mercedes-Benz 280S', '(1)', '2']
        # a_exp_ans_list = ['Buick Estate Wagon (Wagon)', 'Buick Regal Sport Coupe (Turbo)', 'Mercedes-Benz 280S', '(1)', '2']
            ans_list = ['bmw2002', '(2)', '3']
            f = open(os.path.join(os.getcwd(), 'static', 'file', 'user_study_score.txt'), 'w')
            answer_sheet = []

            for i in range(int(start_num), int(last_num)+1):
                user_id = username+str(i)
                user_stat = {}

                try:

                    user = member.objects.get(user_id = user_id)
                    proj = project.objects.filter(user_id = user_id)

                    logs = log_history.objects.filter(user_id=user_id, action="Show-Session")
                    user_stat["user"] = user_id

                    proj_num = 0


                    ses = session.objects.filter(user_id=user_id, project_name="experiment2")
                    project_name = "experiment2"
                    if not ses:
                        ses = session.objects.filter(user_id=user_id, project_name="Experiment2")
                        project_name = "Experiment2"

                    u_ans_list = [None] * 3
                    for m in range(3):
                        u_ans_list[m] = ""
                    answer_list = [None] * 3
                    score_list = [None] * 3
                    conf_list = [None] * 3


                    for k in ses:


                        get_ses = session.objects.filter(user_id=user_id, project_name=project_name,
                                                         session_name=k.session_name).aggregate(Max('session_ver'))
                        max_ses_ver = get_ses['session_ver__max']
                        anno = block_annotation_history.objects.filter(user_id=user_id, project_name=project_name, session_name=k.session_name, session_ver=int(max_ses_ver))
                        ex_num = 0

                        for n in anno:
                            if len(re.findall('\d+', n.data_annotation)) > 0:
                                is_ans = False
                                if "ans" in n.data_annotation:
                                    is_ans = True

                                if is_ans is True:
                                    data_no_space = n.data_annotation.replace(' ', '')
                                    data_ans = data_no_space.replace(' ', '')

                                    for m in range(3):

                                        if "ans"+str(m+1) in data_ans:

                                            if u_ans_list[m] != ans_list[m]:
                                                answer_list[m] = n.data_annotation
                                                ans = data_ans.replace('ans'+str(m+1)+':','')
                                                conf_list[m] = n.research_annotation
                                                if m == 3:
                                                    if "1981" in ans:
                                                        ans = "(2)"
                                                if ans.lower() in ans_list[m]:
                                                    score_list[m] = "1"
                                                    u_ans_list[m] = n.data_annotation
                                                else:
                                                    score_list[m] = "0"

                    user_stat["score"] = score_list
                    user_stat["answer"] = answer_list
                    user_stat["conf"] = conf_list

                    answer_sheet.append(user_stat)


                except member.DoesNotExist:
                    continue
                except project.DoesNotExist:
                    continue

            f.write(json.dumps(answer_sheet))
            f.close()
        return HttpResponse(json.dumps({'success' : True, 'detail' : "Answer", 'output': None}) ,content_type="application/json")

    else:
        return HttpResponse(json.dumps({'success' : False, 'detail' : "Duplicated username", 'output': None}) ,content_type="application/json")

