# import database
from heatmap.models import *
# import libraries
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models import Max, Count, Q
import sys, numpy, scipy
import scipy.cluster.hierarchy as hier
import scipy.spatial.distance as dist
import csv
import scipy.stats as stats
import json
from django.template import loader, Context, RequestContext
import os
import pandas
from sendfile import sendfile
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.views.decorators.csrf import ensure_csrf_cookie
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
import datetime
import shutil
import re
from functools import reduce
import operator
from django.views.decorators.gzip import gzip_page
import scipy.stats as stats
from django.utils import timezone
from random import randint
import networkx as nx
import matplotlib
import subprocess

BASE_DIR = 'static'

# list of action in order to check action from client
action_check_list = ['Create-Unit', 'Delete-Unit', 'Save-Unit',
                     'Select-Unit', 'Change-Data', 'Change-Cluster-Type',
                     'Change-Cluster-Parameter', 'Locate-Unit', 'Show-Session',
                     'Create-Session', 'Branch-Session', 'Delete-Session', #11
                     'Create-Project', 'Delete-Project', 'Change-Data-Annotation',
                     'Change-Unit-Annotation' ,'Change-Session-Annotation', 'Change-Unit-Name',
                     'Save-Session', 'Branch-Unit', 'Apply-Unit', #20
                     'Change-Color', 'Create-Unit-Annotation', 'Delete-Unit-Annotation',
                     'Update-Unit-Annotation', 'Copy-Unit', 'Move-Unit',
                     'Change-PCP-Column', 'Brush-PCP-Axis', 'Brush-SCM-Axis',
                     'Brush-SP-Axis', 'Search-Table', 'Search-Table-Row', #32
                     'Restore-Unit', 'Unit-Workflow', 'Session-Workflow',
                     'Create-Unit-Graph', 'Click-Sankey-Tab', 'Click-Table-Tab',
                     'Click-Menu-Tab', 'Pin-Unit', 'Unpin-Unit', #41
                     'Change_Table_Order', 'Change_Table_Page']

depen_list = ['Create-Unit', 'Select-Unit', 'Locate-Unit',
                          'Apply-Unit', 'Save-Unit', 'Create-Unit-Annotation',
                          'Delete-Unit-Annotation', 'Update-Unit-Annotation', 'Delete-Unit',
                          'Change-Data', 'Change-Unit-Name', 'Change-Color',
                          'Change-Cluster-Type', 'Change-Cluster-Parameter', 'Copy-Unit',
                          'Move-Unit', 'Branch-Unit', 'Change-PCP-Column',
                          'Brush-PCP-Axis', 'Brush-SCM-Axis', 'Brush-SP-Axis',
                          'Restore-Unit', 'Create-Unit-Graph']

def param_checker(request, error, param_list):
    """
    parameter check function when get request
    :param request:
    :param error:
    :param param_list:
    :return: error
    """
    for param in param_list:
        if not request.POST.get(param):
            error.append("Enter " + param)
    return error

def get_params(request, param_list):
    """
    get parameters when got request
    :param request:
    :param param_list:
    :return: req
    """
    req = {}
    for i in param_list:
        req[i] = '%r' % request.POST[i]
        req[i] = req[i].replace('\'', '')
    return req

def list_checker(param, check_list, num_list):
    """
    list check function whether an elem is in the list
    :param param:
    :param check_list:
    :param num_list:
    :return: Boolean value
    """
    for i in num_list:
        if param == check_list[i]:
            return True
    return False

def insert_depen_bl(range1, range2, bl_list, block_iden):
    """
    make a list which consists of block iden and block ver
    :param range1:
    :param range2:
    :param bl_list:
    :param block_iden:
    :return: bl_list
    """
    for j in range(range1, range2):
        depen_bl_elem = {}
        depen_bl_elem['block_iden'] = block_iden
        depen_bl_elem['block_ver'] = j
        is_dup = False
        for i in bl_list:
            if block_iden in dict.values(i) and j in dict.values(i):
                is_dup = True
                break
        if is_dup == False:
            bl_list.append(depen_bl_elem)
    return bl_list

def insert_depen_ses(range1, range2, ses_list, ses_name):
    """
    make a list which consists of block iden and block ver
    :param range1:
    :param range2:
    :param ses_list:
    :param ses_name:
    :return: ses_list
    """
    for j in range(range1, range2):
        depen_bl_elem = {}
        depen_bl_elem['session_name'] = ses_name
        depen_bl_elem['session_ver'] = j
        is_dup = False
        for i in ses_list:
            if ses_name in dict.values(i) and j in dict.values(i):
                is_dup = True
                break
        if is_dup == False:
            ses_list.append(depen_bl_elem)
    return ses_list

def find_descen(bl_list, info):
    """
    Find all descendants
    :param bl_list:
    :param info:
    :return: bl_list
    """
    # get original block's logs information (block_ver__gt)
    origin_log = log_history.objects.filter(action = info['action'],
                         user_id = info['username'], project_name = info['project_name'],
                         session_name = info['session_name'], session_ver = int(info['session_ver']),
                         block_iden = info['block_iden'], block_ver__gt = int(info['block_ver']),
                         is_used = True, is_undo = False).order_by("creatation_date")
    # There are other logs information
    if len(origin_log) > 0:
        # put from block_ver of current log to block_ver of next in the log block list 
        bl_list = insert_depen_bl(info['block_ver'], origin_log[0].block_ver, bl_list, info['block_iden'])
        # find all blocks with parent_block_iden is current block_iden and parent_block_ver is between current block_ver and next block_ver
        btw_bl = block.objects.filter(user_id = info['username'], project_name = info['project_name'],
                                      session_name = info['session_name'], session_ver = int(info['session_ver']),
                                      parent_block_iden = info['block_iden'], parent_block_ver__range = (int(info['block_ver']), int(origin_log[0].block_ver)-1))
        # find all logs with parent_block_iden is current block_iden and parent_block_ver is between current block_ver and next block_ver
        btw_brch = log_history.objects.filter(action = info['action'],
                                              user_id = info['username'], project_name = info['project_name'],
                                              session_name = info['session_name'], session_ver = int(info['session_ver']),
                                              parent_block_iden = info['block_iden'], parent_block_ver__range = (int(info['block_ver']), int(origin_log[0].block_ver)-1), is_used = True, is_undo = False)

    else:
        # get max block_ver
        get_block_ver = block.objects.all().filter(user_id = info['username'], project_name = info['project_name'],
                                                   session_name = info['session_name'], session_ver = int(info['session_ver']),
                                                   block_iden = info['block_iden']).aggregate(Max('block_ver'))
        max_block_ver = get_block_ver['block_ver__max']
        # put from block_ver of current log to block_ver of max in the log block list

        bl_list = insert_depen_bl(info['block_ver'], max_block_ver+1, bl_list, info['block_iden'])
        # find all  blocks with parent_block_iden is current block_iden and parent_block_ver is between current block_ver and max block_ver
        btw_bl = block.objects.filter(user_id = info['username'], project_name = info['project_name'],
                                      session_name = info['session_name'], session_ver = int(info['session_ver']),
                                      parent_block_iden = info['block_iden'], parent_block_ver__range = (int(info['block_ver']), int(max_block_ver)))

        # find all  blocks with parent_block_iden is current block_iden and parent_block_ver is between current block_ver and max block_ver
        btw_brch = log_history.objects.filter(action = info['action'],
                                              user_id = info['username'], project_name = info['project_name'],
                                              session_name = info['session_name'], session_ver = int(info['session_ver']),
                                              parent_block_iden = info['block_iden'], parent_block_ver__range = (int(info['block_ver']), int(max_block_ver)), is_used = True, is_undo = False)
    # check duplicated blocks and update max block_ver
    max_list = []
    iden_list = []
    for i in btw_bl:
        if i.block_iden not in iden_list:
            iden_list.append(i.block_iden)
            max_list.append(int(i.block_ver))
        else:
            if int(i.block_ver) > int(max_list[iden_list.index(i.block_iden)]):
                max_list[iden_list.index(i.block_iden)] = i.block_ver

    # check blocks which didn't have any logs
    checked_list = []
    for i in btw_brch:
        checked_list.append(i.block_iden)
        bl_list = insert_depen_bl(0, i.block_ver+1, bl_list, i.block_iden)
    non_list = list(set(iden_list) - set(checked_list))

    # put from 0 to block_ver of max in the log block list
    for i in non_list:
        bl_list = insert_depen_bl(0, max_list[iden_list.index(i)]+1, bl_list, i)

    # put all information of block
    brch_info = {}
    brch_info['action'] = info['action']
    brch_info['username'] = info['username']
    brch_info['project_name'] = info['project_name']
    brch_info['session_name'] = info['session_name']
    brch_info['session_ver'] = info['session_ver']
    # find children blocks recursively
    for i in iden_list:
        brch_info['block_iden'] = i
        brch_info['block_ver'] = 0
        bl_list = find_descen(bl_list, brch_info)
    return bl_list

def find_unit(bl_list, info):
    """
    Find all units after made info unit
    :param bl_list:
    :param info:
    :return: bl_list
    """
    # get max block_ver
    get_block_ver = block.objects.all().filter(user_id = info['username'], project_name = info['project_name'],
                                               session_name = info['session_name'], session_ver = int(info['session_ver']),
                                               block_iden = info['block_iden']).aggregate(Max('block_ver'))
    max_block_ver = get_block_ver['block_ver__max']

    bl_list = insert_depen_bl(int(info['block_ver']), int(max_block_ver )+ 1, bl_list, info['block_iden'])
    bls = block.objects.filter(user_id = info['username'], project_name = info['project_name'],
                              session_name = info['session_name'], session_ver = int(info['session_ver']),
                              parent_block_iden = info['block_iden'], parent_block_ver__range = (int(info['block_ver']), int(max_block_ver)), is_first = False).order_by('last_date')

    # check duplicated blocks and update max block_ver
    max_list = []
    iden_list = []
    for i in bls:
        if i.block_iden not in iden_list:
            iden_list.append(i.block_iden)
            max_list.append(int(i.block_ver))
        else:
            if int(i.block_ver) > int(max_list[iden_list.index(i.block_iden)]):
                max_list[iden_list.index(i.block_iden)] = i.block_ver
    # call recursive function
    recur_info = {}
    recur_info['username'] = info['username']
    recur_info['project_name'] = info['project_name']
    recur_info['session_name'] = info['session_name']
    recur_info['session_ver'] = info['session_ver']
    bl_list = insert_depen_bl(int(info['block_ver']), max_block_ver, bl_list, info['block_iden'])
    for i in iden_list:
        recur_info['block_iden'] = i
        recur_info['block_ver'] = 0
        bl_list = find_unit(bl_list, recur_info)
    return bl_list

def find_ance(bl_list, info):
    """
    Find all units before made info unit
    :param bl_list:
    :param info:
    :return: bl_list
    """

    # first input
    if len(bl_list) == 0:
        bl_list = insert_depen_bl(0, int(info['block_ver']), bl_list, info['block_iden'])

    if info['parent_block_iden'] is not None:
        bls = block.objects.filter(user_id = info['username'], project_name = info['project_name'],
                                  session_name = info['session_name'], session_ver = int(info['session_ver']),
                                  block_iden = info['parent_block_iden'], block_ver = 0).order_by('last_date')

        bl_list = insert_depen_bl(0, int(info['parent_block_ver'])+1, bl_list, info['parent_block_iden'])
        # call recursive function
        recur_info = {}
        recur_info['username'] = info['username']
        recur_info['project_name'] = info['project_name']
        recur_info['session_name'] = info['session_name']
        recur_info['session_ver'] = info['session_ver']

        if bls[0].parent_block_iden is not None:
            recur_info['parent_block_iden'] = bls[0].parent_block_iden
            recur_info['parent_block_ver'] = bls[0].parent_block_ver
            bl_list = find_ance(bl_list, recur_info)
    return bl_list

def find_session(ses_list, info):
    """
    Find all sessions after made info session
    :param ses_list:
    :param info:
    :return: ses_list
    """
    # get max session_ver
    get_session_ver = session.objects.all().filter(user_id = info['username'], project_name = info['project_name'],
                                               session_name = info['session_name']).aggregate(Max('session_ver'))
    max_session_ver = get_session_ver['session_ver__max']
    ses_list = insert_depen_ses(int(info['session_name']), int(max_session_ver )+ 1, ses_list, info['session_name'])
    ses = session.objects.filter(user_id = info['username'], project_name = info['project_name'],
                              session_name = info['session_name'], session_ver = int(info['session_ver']),
                              parent_session_name = info['session_name'], parent_session_ver__range = (int(info['session_ver']), int(max_session_ver))).order_by('last_date')

    # check duplicated blocks and update max block_ver
    max_list = []
    iden_list = []
    for i in ses:
        if i.session_name not in iden_list:
            iden_list.append(i.session_name)
            max_list.append(int(i.session_ver))
        else:
            if int(i.session_ver) > int(max_list[iden_list.index(i.session_name)]):
                max_list[iden_list.index(i.session_name)] = i.session_ver
    # call recursive function
    recur_info = {}
    recur_info['username'] = info['username']
    recur_info['project_name'] = info['project_name']
    ses_list = insert_depen_bl(int(info['session_ver']), max_session_ver, ses_list, info['session_name'])
    for i in iden_list:
        recur_info['session_name'] = i
        recur_info['session_ver'] = 0
        ses_list = find_session(ses_list, recur_info)
    return ses_list

def random_with_N_digits(n):
    """
    Make random n digits
    :param n:
    :return: int (n digits)
    """
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def find_ori_bl(bl_list, info):
    """
    Find all firsted unit
    :param bl_list:
    :param info:
    :return: bl_list
    """
    bl = block.objects.filter(user_id = info['username'], project_name=info['project_name'], session_name=info['session_name'], session_ver=int(info['session_ver']), block_iden=info['block_iden'], block_ver=int(info['block_ver']))
    if len(bl) > 0:
        fir_info = {}
        fir_info['username'] = info['username']
        fir_info['project_name'] = info['project_name']
        fir_info['session_name'] = info['session_name']
        fir_info['session_ver'] = int(info['session_ver'])
        fir_info['block_iden'] = bl[0].ori_p_block_iden
        fir_info['block_ver'] = int(bl[0].ori_p_block_ver)

        if bl[0].ori_p_block_iden is not None:
            bl_list = find_ori_bl(bl_list, fir_info)
        else:
            bl_list = {}
            bl_list['block_iden'] = bl[0].block_iden
            bl_list['block_ver'] = int(bl[0].block_ver)
        #print(bl[0].block_iden)
        #print(bl[0].parent_block_iden)
        #if bl[0].parent_block_iden is None:
            #bl_list = {}

    return bl_list

# for local environment, make new folder in the local
if os.path.exists(os.path.join(os.getcwd(), BASE_DIR, 'member')) is False:
    os.mkdir(os.path.join(os.getcwd(), BASE_DIR, 'member'))

# import other source files
from heatmap.clustering import *
from heatmap.projects import *
from heatmap.sessions import *
from heatmap.units import *
from heatmap.sankey import *
from heatmap.members import *
from heatmap.recAlgo import *
from heatmap.graph import *
from heatmap.gsea import *
from heatmap.answer import *
from heatmap.analysis import *
