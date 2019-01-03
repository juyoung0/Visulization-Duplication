from heatmap import *

@ensure_csrf_cookie
def get_analysis(request):
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
            # username = '%r' % request.POST['username']
            # username = username.replace('\'', '')
            # start_num = '%r' % request.POST['start_num']
            # start_num = start_num.replace('\'', '')
            # last_num = '%r' % request.POST['last_num']
            # last_num = last_num.replace('\'', '')
            username = "S"
            start_num = 1
            last_num = 10

            wfile = os.path.join(os.getcwd(), 'static', 'file', 'user_study_result.txt')

            with open(wfile, 'w') as wf:
                fieldnames = ['user', 'session', 'restore-unit', 'unit-workflow', 'branch-unit', 'save-unit', 'save-session', 'branch-session']
                csvw = csv.DictWriter(wf, fieldnames = fieldnames)
                csvw.writeheader()

                for i in range(int(start_num), int(last_num) + 1):
                    user_id = username + str(i)
                    user_logs = {}
                    try:

                        user = member.objects.get(user_id=user_id)
                        proj = project.objects.filter(user_id=user_id)

                        logs = log_history.objects.filter(user_id=user_id, action="Show-Session")
                        user_logs["user"]= user_id

                        proj_num = 0
                        u_ans_list = []

                        ses = session.objects.filter(user_id=user_id, project_name="experiment")
                        project_name = "experiment"
                        if not ses:
                            ses = session.objects.filter(user_id=user_id, project_name="Experiment")
                            project_name = "Experiment"


                        for k in ses:
                            re_unit = log_history.objects.filter(user_id=user_id, project_name=project_name,
                                                                 session_name=k.session_name, action="Restore-Unit")
                            work_unit = log_history.objects.filter(user_id=user_id, project_name=project_name,
                                                                   session_name=k.session_name, action="Unit-Workflow")
                            brch_unit = log_history.objects.filter(user_id=user_id, project_name=project_name,
                                                                   session_name=k.session_name, action="Branch-Unit")
                            save_unit = log_history.objects.filter(user_id=user_id, project_name=project_name,
                                                                   session_name=k.session_name, action="Save-Unit")
                            save_ses = log_history.objects.filter(user_id=user_id, project_name=project_name,
                                                                  session_name=k.session_name, action="Save-Session")
                            brch_ses = log_history.objects.filter(user_id=user_id, project_name=project_name,
                                                                  session_name=k.session_name, action="Branch-Session")

                            #print("proj : " + project_name + " ses : " + k.session_name + " ver : " + str(k.session_ver) + " restoration : " + str(len(re_unit)) + " work-unit : " + str(len(work_unit)))
                            user_logs["session"] = k.session_name
                            user_logs["restore-unit"] = len(re_unit)
                            user_logs["unit-workflow"] = len(work_unit)
                            user_logs["branch-unit"] = len(brch_unit)
                            user_logs["save-unit"] = len(save_unit)
                            user_logs["save-session"] = len(save_ses)
                            user_logs["branch-session"] = len(brch_ses)

                            csvw.writerow(user_logs)


                    except member.DoesNotExist:
                        continue
                    except project.DoesNotExist:
                        continue

        return HttpResponse(json.dumps({'success': True, 'detail': "Answer", 'output': None}),
                            content_type="application/json")

    else:
        return HttpResponse(json.dumps({'success': False, 'detail': "Duplicated username", 'output': None}),
                            content_type="application/json")


def find(user_id, project_name, session_name, max_session_ver):
    #prob_num = str(prob_num)
    #session_name = "problem "+prob_num

    #ses = session.objects.filter(user_id = user_id, session_name = session_name, session_ver = 0)

    start_block = block.objects.filter(user_id = user_id, project_name = project_name, session_name = session_name, session_ver = 0).order_by("last_date")
    start_time = start_block[0].last_date

    #print(len(ses))
    #print(start_time)

    anno_list = block_annotation_history.objects.filter(user_id = user_id, project_name = project_name, session_name = session_name, session_ver = max_session_ver, is_removed = False).order_by("last_date")

    print(len(anno_list))
    #print(anno_list[0].last_date, " DSFD ", anno_list[1].last_date)

    print(start_time, " start time ")

    anno_num = 0
    for anno in anno_list:
        print(anno.user_id, anno.project_name, anno.session_name, anno.session_ver, anno.last_date)
        if len(re.findall('\d+', anno.data_annotation)) > 0:
            is_ans = False
            if "ans" in anno.data_annotation:
                num = int(re.findall('\d+', anno.data_annotation)[0])
                is_ans = True
            if "ans" in anno.research_annotation:
                num = int(re.findall('\d+', anno.research_annotation)[0])
                is_ans = True
            if is_ans:
                finish_time = anno.last_date
                anno_num = anno_num+1
                break
        if anno.last_date > start_time:
            anno_num = anno_num+1

#    answer = ""
#    minF = ans_list[0].last_date

#    for f in ans_list:
#        temp = f.last_date
#        if minF > temp:
#            minF = temp

    #print(finish_time)
    solving_time = finish_time - start_time
    print(solving_time)
    print(anno_num)

    #get_anno_num = block_annotation_history.objects.filter(user_id = user_id, project_name = project_name, session_name = session_name, session_ver = max_session_ver, is_removed = False)

    anno_num = 0
    for unit in anno_list:
        #print(unit.data_annotation)
        anno_num = anno_num + (unit.annotation_num+1)
        #print(unit.annotation_num)

    #print(anno_num)

