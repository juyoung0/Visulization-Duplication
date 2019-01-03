from heatmap import *

def cluster_indices_numpy(clustNum, labels_array): #numpy
    """
    find cluster id
    """
    return numpy.where(labels_array == clustNum)[0]

def make_hier(data, length, type_rc, p_id, g_p_id):
    """
    This function puts root and makes hierarchy tree
    """
# put very first data (root)
    hier_data = str(int(data[len(data)-1])) + "."
# data : whole data, len(hier_matrix)-1 : data's length,
# hier_data : current stored data array
    get_elem(data, len(data)-1, hier_data,
		length, type_rc, p_id, g_p_id)

def get_elem(data, p_num, hier,
		length, type_rc, p_id, g_p_id):
    """
    This function puts other data excluding root
    data : total hiermatrix,
    p_num : cluster number,
    hier : total string which separate ".",
    length : each total length of col or row matrix,
    p_id : parent Id (it differs parent number)
    """
# Check whether it is
    if p_num-4 >= 0:
    #isChecked = 0
    # Put current data
        if p_num != len(data)-1:
      #leafData.append(str(int(hier_matrix[-1])) + ".")
            hier += str(int(data[p_num])) + "."
            if type_rc == "row":
                dot_leaf_data.append(hier)
            else:
                dot_col_leaf_data.append(hier)
        if data[p_num-3] > length and data[p_num-4] > length:
            get_elem(data, search_num(data,
                        numpy.where(data == data[p_num-4]), p_num-4),
			hier, length, type_rc, int(data[p_num]-4), int(data[p_num]))
            get_elem(data, search_num(data,
                        numpy.where(data == data[p_num-3]), p_num-3),
			hier, length, type_rc, int(data[p_num]-3), int(data[p_num]))
        elif data[p_num-3] <= length and data[p_num-4] > length:
            hier += str(int(data[p_num-3])) + "."
            if type_rc == "row":
                dot_leaf_data.append(hier)
            else:
                dot_col_leaf_data.append(hier)
            remove_num = len(str(int(data[p_num-3]))) + 1
            hier = hier[:-remove_num]
            get_elem(data, search_num(data,
                        numpy.where(data == data[p_num-4]), p_num-4),
			hier, length, type_rc, int(data[p_num]-4), int(data[p_num]))
        elif data[p_num-3] > length and data[p_num-4] <= length:
            hier += str(int(data[p_num-4])) + "."
            if type_rc == "row":
                dot_leaf_data.append(hier)
            else:
                dot_col_leaf_data.append(hier)
            remove_num = len(str(int(data[p_num-4]))) + 1
            hier = hier[:-remove_num]
            get_elem(data, search_num(data,
                numpy.where(data == data[p_num-3]), p_num-3),
		hier, length, type_rc, int(data[p_num]-3), int(data[p_num]))
        elif data[p_num-3] <= length and data[p_num-4] <= length:
            hier += str(int(data[p_num-4])) + "."
            if type_rc == "row":
                dot_leaf_data.append(hier)
            else:
                dot_col_leaf_data.append(hier)
            remove_num = len(str(int(data[p_num-4]))) + 1
            hier = hier[:-remove_num]
            hier += str(int(data[p_num-3])) + "."
            if type_rc == "row":
                dot_leaf_data.append(hier)
            else:
                dot_col_leaf_data.append(hier)

def search_num(data, index, p_id):
    """
    search_num fuction
    """
    if index[0][0] < p_id and ((index[0][0] % 5 == 0) or (index[0][0] % 5 == 1) or (index[0][0] % 5 == 4)):
        return index[0][0]
    else:
        return -1

def run_vis(vis_info):
    if vis_info['vis_types'] == "Heatmap":
        return run_clusters(vis_info)
    elif vis_info['vis_types'] == "Parallel Coordinate Plot":
        return run_pcp(vis_info)
    elif vis_info['vis_types'] == "Scatterplot Matrix":
        return run_scm(vis_info)
    elif vis_info['vis_types'] == "Scatter Plot":
        return run_sp(vis_info)

def run_pcp(info):
    # Create Annotation File
    get_bl = block.objects.filter(user_id=info['username'], project_name=info['project_name'],
                                  session_name=info['session_name'], session_ver=int(info['session_ver']),
                                  block_iden=info['block_iden'])
    annotation_path = os.path.join('static', 'member', str(info['username']), str(info['project_name']),
                                   str(info['session_name']), str(info['session_ver']), str(info['block_iden']),
                                   'annotation.json')
    if info['is_cluster'] != False and len(get_bl) == 1:
        infile = open(annotation_path, 'w')
        json_str = "{'annotation_list':[]}"
        json_str = json_str.replace("'", '"')
        infile.write(json_str)
        infile.close()

    file_name = os.path.join(str(BASE_DIR), 'member', str(info['username']), str(info['project_name']),
                             str(info['session_name']), str(info['session_ver']), str(info['block_iden']),
                             str(info['block_ver']), 'pcp.json')

    pcp_info = {}
    pcp_info['file_name'] = file_name
    pcp_info['annotation_path'] = annotation_path
    pcp_info['username'] = info['username']
    pcp_info['project_name'] = info['project_name']
    pcp_info['session_name'] = info['session_name']
    pcp_info['session_ver'] = info['session_ver']
    pcp_info['block_iden'] = info['block_iden']
    pcp_info['block_ver'] = info['block_ver']
    pcp_info['data'] = info['data']
    pcp_info['column_order'] = info['column_order']
    pcp_info['selected_index'] = info['selected_index']
    pcp_info['brushed_axis'] = info['brushed_axis']
    pcp_info['brushed_range'] = info['brushed_range']
    pcp_info['request_json'] = info['request_json']
    pcp_info['position_json'] = info['position_json']
    pcp_info['vis_types'] = info['vis_types']

    response_json = [{"pcp_path": pcp_info['file_name'],
                      "annotation_path": pcp_info['annotation_path'],
                      "block_ver": pcp_info['block_ver'],
                      "data":pcp_info['data'],
                      "column_order":pcp_info['column_order'],
                      "selected_index":pcp_info['selected_index'],
                      "vis_types":pcp_info['vis_types'],
                      "brushed_axis":pcp_info['brushed_axis'],
                      "brushed_range":pcp_info['brushed_range']}]
    heatmap_json = json.dumps(
        {"request": pcp_info['request_json'], "response": response_json, "position": pcp_info['position_json']})
    infile = open(pcp_info['file_name'], 'w')
    infile.write(heatmap_json)
    infile.close()
    return json.dumps({'success' : True, 'detail' : 'pcp', 'output':response_json[0]})


def run_sp(info):
    # Create Annotation File
    get_bl = block.objects.filter(user_id=info['username'], project_name=info['project_name'],
                                  session_name=info['session_name'], session_ver=int(info['session_ver']),
                                  block_iden=info['block_iden'])
    annotation_path = os.path.join('static', 'member', str(info['username']), str(info['project_name']),
                                   str(info['session_name']), str(info['session_ver']), str(info['block_iden']),
                                   'annotation.json')
    if info['is_cluster'] != False and len(get_bl) == 1:
        infile = open(annotation_path, 'w')
        json_str = "{'annotation_list':[]}"
        json_str = json_str.replace("'", '"')
        infile.write(json_str)
        infile.close()

    file_name = os.path.join(str(BASE_DIR), 'member', str(info['username']), str(info['project_name']),
                             str(info['session_name']), str(info['session_ver']), str(info['block_iden']),
                             str(info['block_ver']), 'sp.json')

    sp_info = {}
    sp_info['file_name'] = file_name
    sp_info['annotation_path'] = annotation_path
    sp_info['username'] = info['username']
    sp_info['project_name'] = info['project_name']
    sp_info['session_name'] = info['session_name']
    sp_info['session_ver'] = info['session_ver']
    sp_info['block_iden'] = info['block_iden']
    sp_info['block_ver'] = info['block_ver']
    sp_info['data'] = info['data']
    sp_info['x_axis'] = info['x_axis']
    sp_info['y_axis'] = info['y_axis']
    sp_info['brushed_range'] = info['brushed_range']
    sp_info['request_json'] = info['request_json']
    sp_info['position_json'] = info['position_json']
    sp_info['vis_types'] = info['vis_types']

    response_json = [{"sp_path": sp_info['file_name'],
                      "annotation_path": sp_info['annotation_path'],
                      "block_ver": sp_info['block_ver'],
                      "data":sp_info['data'],
                      "vis_types":sp_info['vis_types'],
                      "x_axis": sp_info['x_axis'],
                      "y_axis": sp_info['y_axis'],
                      "brushed_range": sp_info['brushed_range']
                      }]
    sp_json = json.dumps(
        {"request": sp_info['request_json'], "response": response_json, "position": sp_info['position_json']})
    infile = open(sp_info['file_name'], 'w')
    infile.write(sp_json)
    infile.close()
    return json.dumps({'success' : True, 'detail' : 'sp', 'output':response_json[0]})

def run_scm(info):
    # Create Annotation File
    get_bl = block.objects.filter(user_id=info['username'], project_name=info['project_name'],
                                  session_name=info['session_name'], session_ver=int(info['session_ver']),
                                  block_iden=info['block_iden'])
    annotation_path = os.path.join('static', 'member', str(info['username']), str(info['project_name']),
                                   str(info['session_name']), str(info['session_ver']), str(info['block_iden']),
                                   'annotation.json')
    if info['is_cluster'] != False and len(get_bl) == 1:
        infile = open(annotation_path, 'w')
        json_str = "{'annotation_list':[]}"
        json_str = json_str.replace("'", '"')
        infile.write(json_str)
        infile.close()

    file_name = os.path.join(str(BASE_DIR), 'member', str(info['username']), str(info['project_name']),
                             str(info['session_name']), str(info['session_ver']), str(info['block_iden']),
                             str(info['block_ver']), 'scm.json')

    scm_info = {}
    scm_info['file_name'] = file_name
    scm_info['annotation_path'] = annotation_path
    scm_info['username'] = info['username']
    scm_info['project_name'] = info['project_name']
    scm_info['session_name'] = info['session_name']
    scm_info['session_ver'] = info['session_ver']
    scm_info['block_iden'] = info['block_iden']
    scm_info['block_ver'] = info['block_ver']
    scm_info['data'] = info['data']
    scm_info['selected_index'] = info['selected_index']
    scm_info['brushed_axis'] = info['brushed_axis']
    scm_info['brushed_range'] = info['brushed_range']
    scm_info['request_json'] = info['request_json']
    scm_info['position_json'] = info['position_json']
    scm_info['vis_types'] = info['vis_types']

    response_json = [{"scm_path": scm_info['file_name'],
                      "annotation_path": scm_info['annotation_path'],
                      "block_ver": scm_info['block_ver'],
                      "data":scm_info['data'],
                      "selected_index":scm_info['selected_index'],
                      "vis_types":scm_info['vis_types'],
                      "brushed_axis":scm_info['brushed_axis'],
                      "brushed_range":scm_info['brushed_range']}]
    heatmap_json = json.dumps(
        {"request": scm_info['request_json'], "response": response_json, "position": scm_info['position_json']})
    infile = open(scm_info['file_name'], 'w')
    infile.write(heatmap_json)
    infile.close()
    return json.dumps({'success' : True, 'detail' : 'scm', 'output':response_json[0]})

def run_pcp(info):
    # Create Annotation File
    get_bl = block.objects.filter(user_id=info['username'], project_name=info['project_name'],
                                  session_name=info['session_name'], session_ver=int(info['session_ver']),
                                  block_iden=info['block_iden'])
    annotation_path = os.path.join('static', 'member', str(info['username']), str(info['project_name']),
                                   str(info['session_name']), str(info['session_ver']), str(info['block_iden']),
                                   'annotation.json')
    if info['is_cluster'] != False and len(get_bl) == 1:
        infile = open(annotation_path, 'w')
        json_str = "{'annotation_list':[]}"
        json_str = json_str.replace("'", '"')
        infile.write(json_str)
        infile.close()

    file_name = os.path.join(str(BASE_DIR), 'member', str(info['username']), str(info['project_name']),
                             str(info['session_name']), str(info['session_ver']), str(info['block_iden']),
                             str(info['block_ver']), 'pcp.json')

    pcp_info = {}
    pcp_info['file_name'] = file_name
    pcp_info['annotation_path'] = annotation_path
    pcp_info['username'] = info['username']
    pcp_info['project_name'] = info['project_name']
    pcp_info['session_name'] = info['session_name']
    pcp_info['session_ver'] = info['session_ver']
    pcp_info['block_iden'] = info['block_iden']
    pcp_info['block_ver'] = info['block_ver']
    pcp_info['data'] = info['data']
    pcp_info['column_order'] = info['column_order']
    pcp_info['selected_index'] = info['selected_index']
    pcp_info['brushed_axis'] = info['brushed_axis']
    pcp_info['brushed_range'] = info['brushed_range']
    pcp_info['request_json'] = info['request_json']
    pcp_info['position_json'] = info['position_json']
    pcp_info['vis_types'] = info['vis_types']
    response_json = [{"pcp_path": pcp_info['file_name'],
                      "annotation_path": pcp_info['annotation_path'],
                      "block_ver": pcp_info['block_ver'],
                      "data":pcp_info['data'],
                      "column_order":pcp_info['column_order'],
                      "selected_index":pcp_info['selected_index'],
                      "vis_types":pcp_info['vis_types'],
                      "brushed_axis":pcp_info['brushed_axis'],
                      "brushed_range":pcp_info['brushed_range']}]
    heatmap_json = json.dumps(
        {"request": pcp_info['request_json'], "response": response_json, "position": pcp_info['position_json']})
    infile = open(pcp_info['file_name'], 'w')
    infile.write(heatmap_json)
    infile.close()
    return json.dumps({'success' : True, 'detail' : 'pcp', 'output':response_json[0]})

def run_clusters(info):
    row_headers = []
    data_matrix = []

    #Extract row data
    #if info['is_cluster'] == True:
        #data = info['data'].split('\n')#.splitlines()
    #else:
    data = info['data'].split('\n')
    label = data[0]
    data = data[1:len(data)-1]
    label_matrix = []
    label_line = []
    #label_line = label.split('\t')

    if info['data_type'] == "tsv" or info['data_type'] == 'txt':
        label_line = label.split('\t')
    elif info['data_type'] == "csv":
        label_line = label.split(',')

    for line in label_line:
        if line != "":
            label_matrix.append(line)

    for line in data:
        if info['data_type'] == "tsv"or info['data_type'] == 'txt':
            strline = line.split('\t')
        elif info['data_type'] == "csv":
            strline = line.split(',')
        #strline = line.split('\t')
        row_headers.append([str(strline[0])])
        data_matrix.append([float(x) for x in strline[1:]])

    #Extract col data
    col_data_matrix = []
    for i in range(0, len(label_matrix)):
        col_data_matrix.append([row[i] for row in data_matrix])

    data_matrix = numpy.array(data_matrix)
    col_data_matrix = numpy.array(col_data_matrix) 

    #detect whether log2 transform
    express_value = pandas.DataFrame(numpy.log2(data_matrix))
    qunant_val = express_value.quantile([0., 0.25, 0.5, 0.75, 0.99, 1.0])
    aver_quant_val = (qunant_val[0] + qunant_val[1] + qunant_val[2] + qunant_val[3]) / 4
    if (aver_quant_val[.99] > 100) or (aver_quant_val[1.0] - aver_quant_val[0.0] > 50 and aver_quant_val[0.25] > 0) or (aver_quant_val[0.25] > 0 and aver_quant_val[0.25] < 1 and aver_quant_val[0.75] > 1 and aver_quant_val[0.75] < 2):
        #log2 transform
        data_matrix = numpy.log2(data_matrix)
        #convert native data array into a numpy array
        col_data_matrix = numpy.log2(col_data_matrix)

    #zscore transform
    data_matrix = stats.zscore(data_matrix, 1, 1)
    col_data_matrix = stats.zscore(col_data_matrix, 1, 1)

    #max, min data
    max_value = numpy.amax(data_matrix)
    min_value = numpy.amin(data_matrix)

    name_data = []

    #Create Annotation File
    get_bl = block.objects.filter(user_id = info['username'], project_name = info['project_name'], session_name = info['session_name'], session_ver = int(info['session_ver']), block_iden = info['block_iden'])
    annotation_path = os.path.join('static', 'member', str(info['username']), str(info['project_name']), str(info['session_name']), str(info['session_ver']), str(info['block_iden']),'annotation.json')
    if info['is_cluster'] != False and len(get_bl) == 1:
        infile = open(annotation_path, 'w')
        json_str = "{'annotation_list':[]}"
        json_str = json_str.replace("'", '"')
        infile.write(json_str)
        infile.close()
    """
    if info['block_ver'] != 0 and info['parent_block_iden'] is None:
        prev_anno_path = os.path.join('static', 'member', str(info['username']), str(info['project_name']),
                                       str(info['session_name']), str(info['session_ver']), str(info['block_iden']),
                                       'annotation.json')
        os.remove(os.path.join(os.getcwd(), annotation_path))
        src_path = os.path.join(os.getcwd(), prev_anno_path)
        dst_path = os.path.join(os.getcwd(), annotation_path)
        shutil.copyfile(src_path, dst_path)
        anno_file = open(annotation_path, 'r')
        anno_data = json.loads(anno_file.read())
        for elem in anno_data['annotation_list']:
            elem['block_ver'] = int(info['block_ver'])
    """

    heatmap_path = os.path.join('static', 'member', str(info['username']), str(info['project_name']), str(info['session_name']), str(info['session_ver']), str(info['block_iden']), str(info['block_ver']), 'clusters.json')
    file_name = os.path.join(str(BASE_DIR), 'member', str(info['username']), str(info['project_name']), str(info['session_name']), str(info['session_ver']), str(info['block_iden']), str(info['block_ver']), 'clusters.json')

    clu_info = {}
    clu_info['data_matrix'] = data_matrix
    clu_info['file_name'] = file_name
    clu_info['row_headers'] = row_headers
    clu_info['min_value'] = min_value
    clu_info['max_value'] = max_value
    clu_info['label_matrix'] = label_matrix
    clu_info['heatmap_path'] = heatmap_path
    clu_info['annotation_path'] = annotation_path
    clu_info['username'] = info['username']
    clu_info['project_name'] = info['project_name']
    clu_info['session_name'] = info['session_name']
    clu_info['session_ver'] = info['session_ver']
    clu_info['block_iden'] = info['block_iden']
    clu_info['block_ver'] = info['block_ver']
    clu_info['cluster_type'] = info['cluster_type']
    clu_info['cluster_param'] = info['cluster_param']
    clu_info['cluster_param'] = info['cluster_param']
    clu_info['color_type'] = info['color_type']
    clu_info['data'] = info['data']
    clu_info['request_json'] = info['request_json']
    clu_info['position_json'] = info['position_json']
    clu_info['vis_types'] = info['vis_types']

    if info['cluster_type'] == "KMeans":
       return run_KMeans(clu_info)
    elif info['cluster_type'] == "Spectral":
       return run_Spectral(clu_info)
    elif info['cluster_type'] == "Hierarchy":
       clu_info['col_data_matrix'] = col_data_matrix
       return run_Hierarchy(clu_info)


def run_KMeans(KM_info):
    name_data = []
    km_data = []
    row = 0
    kmeans = KMeans(n_clusters=int(KM_info['cluster_param']), random_state=0).fit(KM_info['data_matrix'])
    for i in range(0, kmeans.n_clusters):
        km_list = cluster_indices_numpy(i, kmeans.labels_)
        for j in km_list:
            col = 0
            name_data.extend(KM_info['row_headers'][int(j)])
            record_list = []
            for label in KM_info['label_matrix']:
                record = [float(list(KM_info['data_matrix'][j])[col]), int(row), int(col)]
                record_list.append(record)
                col += 1
            row += 1
            km_data.append(record_list)
    response_json = [{"cluster_data" : km_data, 'label' : KM_info['label_matrix'], 'min' : KM_info['min_value'], 'max' : KM_info['max_value'], "name_data" : name_data, "heatmap_path" : KM_info['heatmap_path'], "annotation_path" : KM_info['annotation_path'], "block_ver" : KM_info['block_ver'], "vis_types":KM_info['vis_types']}]
    heatmap_json = json.dumps({"request" : KM_info['request_json'], "response" : response_json, "position" : KM_info['position_json'], "vis_types":KM_info['vis_types']})
    infile = open(KM_info['file_name'], 'w')
    infile.write(heatmap_json)
    infile.close()
    return json.dumps({'success' : True, 'detail' : 'KMeans', 'output':response_json[0]})

def run_Spectral(SP_info):
    sp_data = []
    name_data = []
    row = 0
    speclu = SpectralClustering(n_clusters=int(SP_info['cluster_param'])).fit(SP_info['data_matrix'])
    for i in range(0, speclu.n_clusters):
        sp_list = cluster_indices_numpy(i, speclu.labels_)
        for j in sp_list:
            col = 0
            name_data.extend(SP_info['row_headers'][int(j)])
            record_list = []
            for label in SP_info['label_matrix']:
                record = [float(list(SP_info['data_matrix'][j])[col]), int(row), int(col)]
                record_list.append(record)
                col += 1
            row += 1
            sp_data.append(record_list)
    response_json = [{"cluster_data" : sp_data, 'label' : SP_info['label_matrix'], 'min' : SP_info['min_value'], 'max' : SP_info['max_value'], "name_data" : name_data, "heatmap_path" : SP_info['heatmap_path'], "annotation_path" : SP_info['annotation_path'], "block_ver" : SP_info['block_ver'], "vis_types":SP_info['vis_types']}]
    heatmap_json = json.dumps({"request" : SP_info['request_json'], "response" : response_json, "position" : SP_info['position_json'], "vis_types":SP_info['vis_types']})
    infile = open(SP_info['file_name'], 'w')
    infile.write(heatmap_json)
    infile.close()
    return json.dumps({'success' : True, 'detail' : 'Spectral', 'output':response_json[0]})

def run_Hierarchy(HI_info):
    distance_matrix = dist.pdist(HI_info['data_matrix'])
    col_distance_matrix = dist.pdist(HI_info['col_data_matrix'])
    distance_square_matrix = dist.squareform(distance_matrix)
    col_distance_square_matrix = dist.squareform(col_distance_matrix)
    linkage_matrix = hier.linkage(distance_square_matrix, HI_info['cluster_param'])
    col_linkage_matrix = hier.linkage(col_distance_square_matrix, HI_info['cluster_param'])
    heatmap_order = hier.leaves_list(linkage_matrix)
    # fix y - axis
    #heatmap_order = numpy.arange(11)

    hier_matrix = [[]]
    col_hier_matrix = [[]]
    new_num = len(linkage_matrix)
    col_new_num = len(col_linkage_matrix)
    for i in range(0, len(linkage_matrix)):
        new_num += 1
        hier_matrix = numpy.array(numpy.append(hier_matrix, numpy.append(linkage_matrix[i], [new_num])))

    for i in range(0, len(col_linkage_matrix)):
        col_new_num += 1
        col_hier_matrix = numpy.array(numpy.append(col_hier_matrix, numpy.append(col_linkage_matrix[i], [col_new_num])))

    global dot_leaf_data
    dot_leaf_data = []
    dot_leaf_data.append(str(int(hier_matrix[-1]))+".")

    global dot_col_leaf_data
    dot_col_leaf_data = []
    dot_col_leaf_data.append(str(int(col_hier_matrix[-1]))+".")

    make_hier(hier_matrix, len(linkage_matrix), "row", int(hier_matrix[-1]), len(linkage_matrix))
    make_hier(col_hier_matrix, len(col_linkage_matrix), "col", int(col_hier_matrix[-1]), len(col_linkage_matrix))

    for i in range(len(dot_leaf_data)):
        dot_leaf_data[i] = dot_leaf_data[i][:-1]

    for i in range(len(dot_col_leaf_data)):
        dot_col_leaf_data[i] = dot_col_leaf_data[i][:-1]
    ordered_data_matrix = HI_info['data_matrix'][heatmap_order, :]

    row_headers = numpy.array(HI_info['row_headers'])
    ordered_row_headers = row_headers[heatmap_order, :]


    col_cluster_output = []
    leaf_mat = []

    for i in range(0, len(dot_col_leaf_data)):
        re_str = dot_col_leaf_data[i][::-1]
        dot_find = re_str.find('.')
        if dot_find != -1:
            leaf = dot_col_leaf_data[i][len(dot_col_leaf_data[i])-int(dot_find):len(dot_col_leaf_data[i])]
            if int(leaf) < len(col_linkage_matrix)+1:
                leaf_mat.append(leaf)

    chan_col_head = []
    # fix x-axis
    for j in range(0, len(leaf_mat)):
        chan_col_head.append(HI_info['label_matrix'][int(leaf_mat[j])])

    matrix_output = []
    row = 0
    for row_data in ordered_data_matrix:
        col = 0
        row_output = []
        #for i in leaf_mat:
        for col_data in row_data:
            # fix x-axis
            row_output.append([col_data, row, chan_col_head.index(HI_info['label_matrix'][col])])
            col += 1
        matrix_output.append(row_output)
        row += 1

    one_di_ord_row_head = []
    for i in range(len(ordered_row_headers)):
        one_di_ord_row_head.append(ordered_row_headers[i][0])

    cluster_data = []
    name_data = []
    for i in range(0, len(matrix_output)):
        add_name_data = []
        row_mat = []
        col_cluster_output = []
        col_cluster_output.extend(matrix_output[i])
        name_data.extend([one_di_ord_row_head[i]])
        cluster_data.append(col_cluster_output)

    dendro_data = []
    path = os.path.join(str(BASE_DIR), 'member', str(HI_info['username']), str(HI_info['project_name']), str(HI_info['session_name']), str(HI_info['session_ver']), str(HI_info['block_iden']), str(HI_info['block_ver']))
    csv_file = open(os.path.join(path, 'Hierarchy.csv'), 'w', newline='')
    copy_write = csv.writer(csv_file, delimiter=',', quotechar='|')
    copy_write.writerow(("id", "value"))
    for i in range(len(dot_leaf_data)):
        if int(dot_leaf_data[i][-1]) <= len(linkage_matrix):
            num = ""
            for j in range(len(dot_leaf_data[i])):
                k = 1 + j
                if dot_leaf_data[i][-k] == ".":
                    break
                else:
                    num += dot_leaf_data[i][-k]
            copy_write.writerow((str(dot_leaf_data[i]), ""))
        else:
            copy_write.writerow((str(dot_leaf_data[i]), ""))
    csv_file.close()

    csv_file = open(os.path.join(path, "HierarchyCol.csv"), "w", newline='')
    copy_write = csv.writer(csv_file, delimiter=',', quotechar='|')
    copy_write.writerow(("id", "value"))

    col_leaf_list = []
    for i in range(len(dot_col_leaf_data)):
        if int(dot_col_leaf_data[i][-1]) <= len(col_linkage_matrix):
            num = ""
            for j in range(len(dot_col_leaf_data[i])):
                k = 1 + j
                if dot_col_leaf_data[i][-k] == ".":
                    break
                else:
#                    global dot_col_leaf_data
                    num += dot_col_leaf_data[i][-k]
                if str(dot_col_leaf_data[i]) not in col_leaf_list:
                    col_leaf_list.append(str(dot_col_leaf_data[i]))
                    copy_write.writerow((str(dot_col_leaf_data[i]), ""))
        else:
            if str(dot_col_leaf_data[i]) not in col_leaf_list:
                col_leaf_list.append(str(dot_col_leaf_data[i]))
                copy_write.writerow((str(dot_col_leaf_data[i]), ""))
    csv_file.close()

    dendro_path = os.path.join(str(BASE_DIR), 'member', str(HI_info['username']), str(HI_info['project_name']), str(HI_info['session_name']), str(HI_info['session_ver']), str(HI_info['block_iden']), str(HI_info['block_ver']), 'Hierarchy.csv')
    dendro_col_path = os.path.join(str(BASE_DIR), 'member', str(HI_info['username']), str(HI_info['project_name']), str(HI_info['session_name']), str(HI_info['session_ver']), str(HI_info['block_iden']), str(HI_info['block_ver']), 'HierarchyCol.csv')
    response_json = [{"cluster_data" : cluster_data, 'label' : chan_col_head,
                      'min' : HI_info['min_value'], 'max' : HI_info['max_value'],
                      "name_data" : name_data, 'dendro_data' : dendro_data,
                      "heatmap_path" : HI_info['heatmap_path'], "dendro_path" : dendro_path,
                      "dendro_col_path" : dendro_col_path, "annotation_path" : HI_info['annotation_path'],
                      "block_ver" : HI_info['block_ver'], "vis_types":HI_info['vis_types']}]
    heatmap_json = json.dumps({"request" : HI_info['request_json'], "response" : response_json, "position" : HI_info['position_json']})
    infile = open(HI_info['file_name'], 'w')
    infile.write(heatmap_json)
    infile.close()
    return json.dumps({'success' : True, 'detail' : 'Hierarchy', 'output':response_json[0]})
