#!/usr/bin/python
#-*-coding:utf-8-*-

from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Userinfo,WhiteEmail,WhiteIp,WhiteUrl,AlarmList,User,ResUrl,ResEmail,ResIp,AlarmPre
from models import DATATYPE_CHOICES
import traceback
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from engine.utils import get_datatables_records
from forms import WhiteList_Add
import datetime
from django.contrib import admin
from bson.objectid import ObjectId
import time 

@login_required
def get_user_alarmpre(request):
	return render_to_response('useralarmlist/useralarmprelist.html',{"title":'预警名单查询'},context_instance = RequestContext(request))

@login_required
def get_user_alarmpre_list(request):
	starttime = time.time()
	columnIndexNameMap = { 
        0: 'id',
        1: 'autoid',
        2: 'datacontent', 
        3: 'datatype',
        4: 'isalarmed',
        5: 'insert_time'
    }
	columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])
	filterdict = dict()
	if User.objects.get(username = request.user).is_superuser == False:
		userinfo = Userinfo.objects.get(user=request.user)
		filterdict["user_id"] =ObjectId(userinfo.id)
	try:
		aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, 
                                                                                    AlarmPre, 
                                                                                    columnIndexNameMap,
                                                                                    None,
                                                                                    filterdict,
                                                                                    True,
                                                                                    'insert_time') 
	except Exception,e:
		traceback.print_exc()
		aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
	midtime = time.time()
	print "----------------------------",(midtime-starttime) 

	index = int(request.GET.get('iDisplayStart',0))+1
	for i in aaData:
		i.insert(1,index)
		index = index + 1
		if i[columnNameIndexMap['isalarmed']] == 'false':
			i[columnNameIndexMap['isalarmed']] = '是'
		else:
			i[columnNameIndexMap['isalarmed']] = '否'
		i[columnNameIndexMap['datacontent']] = "您所在组内有人访问黑名单中的"+i[columnNameIndexMap['datacontent']]
		i[columnNameIndexMap['datatype']] = dict(DATATYPE_CHOICES)[i[columnNameIndexMap['datatype']]]
		

	response_dict = {}
	response_dict.update({'aaData':aaData})
    
	response_dict.update({'sEcho': sEcho, 
                        'iTotalRecords': iTotalRecords,
                        'iTotalDisplayRecords':iTotalDisplayRecords, 
                        'sColumns':sColumns})
	response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')
    #阻止缓存
	add_never_cache_headers(response)
	endtime = time.time()
	print "----------------------------",(endtime-midtime) 
	return response
