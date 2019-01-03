from heatmap import *

# Processing function for recommendation after reading json file
def processing(name_list, data_list):
    data = []
    for i in range(0, len(data_list)):
        temp = []
        for j in range(0, len(data_list[i])):
            temp.append(data_list[i][j][0])
        data.append(temp)

    result = []
    for k in range(0, len(name_list)):
        result.append([name_list[k]]+data[k])

    return result

# Recommendation Algorithm for several clustered data
def algorithm(type1, type2):
    m = len(type1)
    n = len(type2)

    counter = [[0]*(n+1) for x in range(m+1)]

    # common sequence set
    cs_set = []

    for i in range(m):
        for j in range(n):
            if type1[i] == type2[j]:
                c = counter[i][j] + 1
                counter[i+1][j+1] = c

    for i in range(m+1):
        for j in range(n+1):
            if counter[i][j] > 1:
                if i+1 >= m+1 or j+1 >= n+1:
                    c = counter[i][j]
                    cs_set.append(type1[i-c:i])
                elif counter[i+1][j+1] == 0:
                    c = counter[i][j]
                    cs_set.append(type1[i-c:i])

    return cs_set

# When checking the three more cluster types, it needs middle processing
def mid_process(mid):
    temp = []

    for i in range(len(mid)):
        for j in range(len(mid[i])):
            temp.append(mid[i][j])
        temp.append([0])    # Trash value for separating each pair

    return temp

def recommendation_system(clusters):
    temp = clusters[0]["gene"]

    for i in range(1, len(clusters)):
        temp = algorithm(temp, clusters[i]["gene"])
        result = temp
        temp = mid_process(temp)

    return result

@ensure_csrf_cookie
def recommendation(request):

    errors = []
    if request.method == 'POST':
        # check necessary information
        param_list = ['username','project_name', 'session_name', 'session_ver', 'block_list']
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

            block_list = request.POST.get('block_list')
            block_list = eval(json.loads(json.dumps(block_list)))

            block_iden = block_list[0]['block_iden']
            block_ver = block_list[0]['block_ver']

            path = open(os.path.join("static", "member", str(username), str(project_name), str(session_name), str(session_ver), str(block_iden), str(block_ver), "clusters.json"), "r")

            json_string = path.readline()

            json_string = json.loads(json_string)

            temp = json_string["request"][0]["data_name"]

            json_dic = {}
            clusters = []     # path list for clusters.json
            cluster_types = []

            for bl in block_list:

                block_iden = bl['block_iden']
                block_ver = bl['block_ver']

                path = open(os.path.join("static", "member", str(username), str(project_name), str(session_name), str(session_ver), str(block_iden), str(block_ver), "clusters.json"), "r")

                json_string = path.readline()

                json_string = json.loads(json_string)

                data_name = json_string["request"][0]["data_name"]

                if temp != data_name:
                    return HttpResponse(json.dumps({'success': False, 'detail': "Data name must be same", 'output': data_name}),content_type="application/json")

                name_data = json_string["response"][0]["name_data"]
                cluster_data = json_string["response"][0]["cluster_data"]

                processed_data = processing(name_data, cluster_data)

                dic = {}
                dic["cluster_type"] = json_string["request"][0]["cluster_type"]
                dic["cluster_param"] = json_string["request"][0]["cluster_param"]
                dic["gene"] = processed_data

                cluster_types.append(dic["cluster_type"]+"-"+dic["cluster_param"])
                clusters.append(dic)

            result = recommendation_system(clusters)

            json_dic["data_name"] = data_name
            json_dic["Cluster_types"] = cluster_types
            json_dic["Recommendation_pairs"] = result

            json_rs = json.loads(json.dumps(json_dic))

        return HttpResponse(json.dumps({'success': True, 'detail': "Success recommendation", 'output': json_rs}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': False, 'detail': "Fail recommendation", 'output': errors}), content_type="application/json")