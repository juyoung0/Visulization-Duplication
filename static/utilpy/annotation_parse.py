from heatmap.models import *

for i in range(1, 41):
    user_name = "S" + str(i)
    logs = log_history.objects.filter(user_id=user_name, action="Create-Unit-Annotation")
    bl_anno = block_annotation_history.objects.filter(user_id=user_name)
    block_anno_info = []
    for j in bl_anno:
        block_anno_elem = {}
        block_anno_elem['user_id'] = j.user_id
        block_anno_elem['project_name'] = j.project_name
        block_anno_elem['session_name'] = j.session_name
        block_anno_elem['session_ver'] = j.session_ver
        block_anno_elem['block_iden'] = j.block_iden
        block_anno_elem['block_ver'] = j.block_ver
        block_anno_elem['data_annotation'] = j.data_annotation
        block_anno_elem['last_date'] = j.last_date
        block_anno_elem['annotation_id'] = j.annotation_id
        block_anno_info.append(block_anno_elem)
        #print(j.user_id, j.project_name, j.session_name, j.session_ver, j.block_iden, j.block_ver, j.data_annotation)
    for j in logs:
        min_id = 0
        min_time = 99999999999
        for k in block_anno_info:
            if k['user_id'] == j.user_id and k['project_name'] == j.project_name and k['session_name'] == j.session_name and k['session_ver'] == j.session_ver and k['block_iden'] == j.block_iden and  k['block_ver'] == j.block_ver:#and k['last_date']
                if min_time > (j.creatation_date - k['last_date']).total_seconds():
                    print(j.creatation_date, k['last_date'])
                    min_id = k['annotation_id']
        if min_id != 0:
            print(j.user_id)
            j.__dict__.update(anno_id = min_id)
            j.save()
        print(min_id)
                #print(k['last_date'])
        #print(j.user_id, j.project_name, j.session_name, j.session_ver, j.block_iden, j.block_ver)
