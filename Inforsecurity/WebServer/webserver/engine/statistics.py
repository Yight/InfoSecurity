#!/usr/bin/python
#-*-coding:utf-8-*-

from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from models import ResEmail,Userinfo,ResUrl,BlackEmail,BlackIp,BlackUrl,ResIp
from django.template.loader import render_to_string
from models import ALARM_CHOICES,RESTYPE_CHOICES,TYPE_CHOICES,IPPROTOCOL_CHOICES,FLOW_CHOICES
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from django.template import RequestContext
from engine.utils import get_datatables_records
from django.db.models import Q
from forms import ResEmail_Search,BlackEmail_Search,BlackEmail_Add,BlackEmail_Edit,BlackIp_Add,BlackIp_Edit,BlackUrl_Add,BlackUrl_Edit,ResUrl_Search,ResIp_Search
import traceback
import datetime
import time

##########################################statistic_email################################################### 

@login_required
def statistic_email(request):
    title = u'邮件记录统计'
    emailtypes = [('resemailtype'+k,k,y) for k,y in RESTYPE_CHOICES]
    return render_to_response('statistic/email.html',locals(), context_instance = RequestContext(request))

@login_required
def get_resemails_list(request):

    filterdict = dict()

    if request.GET.get('emailtypes',False) > '':
        for i in request.GET.get('emailtypes').split(','):
            if i in dict(RESTYPE_CHOICES).keys():
                filterdict["emailtype"] = i

    riskdict=dict()
    riskdict["$gt"] = -1
    filterdict["riskvalue"] = riskdict

    if request.GET.get('riskvalue',False):
        try:
            filterdict["riskvalue"] = int(request.GET.get('riskvalue',False))
        except Exception,e:
            riskdict["$ne"] = -1
            filterdict["riskvalue"] = riskdict

    timedict = dict()
    if request.GET.get('begintime',False):
        try:
            timedict["$gt"]=datetime.datetime.strptime(request.GET.get('begintime'),'%Y-%m-%d')
        except Exception,e:
            traceback.print_exc() 
    if request.GET.get('endtime',False):
        
        try:
            timedict["$lt"] = datetime.datetime.strptime(request.GET.get('endtime'),'%Y-%m-%d')
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()
    if timedict:filterdict["datetime"] = timedict

    columnIndexNameMap = { 
        0: 'id',
        1: 'autoid',
        2: 'user_id',
        3: 'datetime',
        4: 'sendfrom', 
        5: 'sendto', 
        6: 'sip', 
        7: 'dip',
        8: 'riskvalue',
        9: 'emailtype',
        10: 'sendcc',
        11: 'sendbcc',
        12: 'subject',
        13: 'sport',
        14: 'dport',
        15: 'processname',
        16: 'processmd5',
    }

    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, 
                                                                                        ResEmail, 
                                                                                        columnIndexNameMap,
                                                                                        None,
                                                                                        filterdict,
                                                                                        True,
                                                                                        'datetime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0))+1
    for i in aaData:     
        try:    
            i.insert(1,index)
            index = index +1
            i[columnNameIndexMap['emailtype']] = dict(RESTYPE_CHOICES)[i[columnNameIndexMap['emailtype']]]
            i[columnNameIndexMap['user_id']] = Userinfo.objects.get(id=i[columnNameIndexMap['user_id']]).realname
        except Exception,e:
            continue
    response_dict = {}
    response_dict.update({'aaData':aaData})
    
    response_dict.update({'sEcho': sEcho, 'iTotalRecords': iTotalRecords, 'iTotalDisplayRecords':iTotalDisplayRecords, 'sColumns':sColumns})
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')

    #阻止缓存
    add_never_cache_headers(response)
    return response



@login_required
def get_detail_resemails_list(request):
    
    try:
        if request.GET.get('id'):
            emailid = request.GET.get('id')
            receiver = ResEmail.objects.get(id=emailid).sendto
            resemails = ResEmail.objects.filter(sendto=receiver)
            iTotalDisplayRecords = resemails.count()
            resemails = resemails.values('sendfrom','dport','sip','datetime')
            for i in resemails:
                i['datetime'] = i['datetime'].strftime('%Y-%m-%d')
            from collections import defaultdict

            resemails_detail = defaultdict(list)
            for i in resemails:
                resemails_detail[i['datetime']].append(i)
            iTotalRecords = iTotalDisplayRecords = len(resemails_detail)
            aaData = []
            for k,v in resemails_detail.items():
                aaData.append([receiver,
                    str(v[0]['dport']),
                    v[0]['sendfrom'],
                    v[0]['sip'],
                    k.split(',')[0],
                    str(len(v)),
                    '']
                )

            #Ordering data
            iSortingCols =  int(request.GET.get('iSortingCols',0))#根据几columns进行排序
            asortingCols = []


            if iSortingCols:
                sortedColID = int(request.GET.get('iSortCol_0',0))
                if request.GET.get('bSortable_{0}'.format(sortedColID), 'false')  == 'true':  #判断是否可以sort
                    reverse = request.GET.get('sSortDir_0') == 'desc'
                    aaData.sort(cmp=lambda x,y: cmp(x[sortedColID].lower(), y[sortedColID].lower()),reverse=reverse)

            aaData = aaData[int(request.GET.get('iDisplayStart')):int(request.GET.get('iDisplayStart'))+int(request.GET.get('iDisplayLength'))]
            
      #      jsonTemplatePath = 'json_detail.txt'
      #      jstonString = render_to_string(jsonTemplatePath,locals())
      #      response = HttpResponse(jstonString,mimetype="application/javascript")
        else:
            aaData,iTotalDisplayRecords,iTotalRecords = [],0,0

    except Exception,e:
        aaData,iTotalDisplayRecords,iTotalRecords = [],0,0
        traceback.print_exc()

    response_dict = {}
    response_dict.update({'aaData':aaData})
    response_dict.update({
        'iTotalDisplayRecords':iTotalDisplayRecords,
        'iTotalRecords':iTotalRecords
    })#实际上起作用的数据
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')

    #阻止缓存
    add_never_cache_headers(response)

    return response

@login_required
def statistic_email_search(request):
    title = u'邮件查找统计'
    
    if request.method == "POST":
        form = ResEmail_Search(request=request,data=request.POST)
        if form.is_valid():
            form = form.cleaned_data
            return render_to_response('statistic/email_search_result.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return HttpResponseRedirect('/statistic/email/')

##########################################statistic_url################################################### 

@login_required
def statistic_url(request):
    title = u'URL记录统计'
    urltypes = [('resurltype'+k,k,y) for k,y in RESTYPE_CHOICES]

    return render_to_response('statistic/url.html',locals(), context_instance = RequestContext(request))
    
@login_required    
def get_resurls_list(request):
    filterdict = dict()

    if request.GET.get('urltypes',False) > '':
        for i in request.GET.get('urltypes').split(','):
            if i in dict(RESTYPE_CHOICES).keys():
                filterdict["urltype"] = i
                
    riskdict=dict()
    riskdict["$ne"] = -1
    filterdict["riskvalue"] = riskdict

    if request.GET.get('riskvalue',False):
        try:
            filterdict["riskvalue"] = int(request.GET.get('riskvalue',False))
        except Exception,e:
            riskdict["$ne"] = -1
            filterdict["riskvalue"] = riskdict

    timedict = dict()
    if request.GET.get('begintime',False):
        try:
            timedict["$gt"]=datetime.datetime.strptime(request.GET.get('begintime'),'%Y-%m-%d')
        except Exception,e:
            traceback.print_exc() 
    if request.GET.get('endtime',False):
        
        try:
            timedict["$lt"] = datetime.datetime.strptime(request.GET.get('endtime'),'%Y-%m-%d')
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()
            
    if timedict:filterdict["datetime"] = timedict
    
    columnIndexNameMap = { 
        0: 'id', 
        1: 'autoid',
        2: 'user_id',
        3: 'datetime', 
        4: 'url', 
        5: 'urltype', 
        6: 'riskvalue',
        7: 'sip',
        8: 'dip',
        9: 'sport',
        10: 'dport',
        11: 'processname',
        12: 'processmd5'

    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])
    #jsonTemplatePath = 'json_resurls.txt'
    extrafilters = {'urltype':RESTYPE_CHOICES}

    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, 
                                                                                    ResUrl, 
                                                                                    columnIndexNameMap,
                                                                                    None,
                                                                                    filterdict,
                                                                                    True,
                                                                                    'datetime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0))+1
    for i in aaData:
        try:
            i.insert(1,index)
            index = index +1
            i[columnNameIndexMap['urltype']] = dict(RESTYPE_CHOICES)[i[columnNameIndexMap['urltype']]]
            i[columnNameIndexMap['user_id']] = Userinfo.objects.get(id=i[columnNameIndexMap['user_id']]).realname
        except Exception,e:
            continue
    response_dict = {}
    response_dict.update({'aaData':aaData})
    
    response_dict.update({'sEcho': sEcho, 'iTotalRecords': iTotalRecords, 'iTotalDisplayRecords':iTotalDisplayRecords, 'sColumns':sColumns})
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

    #阻止缓存
    add_never_cache_headers(response)
    return response

@login_required
def get_detail_resurls_list(request):
    try:
        if request.GET.get('id'):
            urlid = request.GET.get('id')
            url = ResUrl.objects.get(id=urlid).url

            resurls = ResUrl.objects.filter(url=url,riskvalue__gt=-1)
            iTotalDisplayRecords = resurls.count()
            resurls = resurls.values('dport','sip','datetime','urltype','url')
            for i in resurls:
                i['datetime'] = i['datetime'].strftime('%Y-%m-%d')
            from collections import defaultdict

            resurls_detail = defaultdict(list)
            for i in resurls:
                resurls_detail[i['datetime'] + ',' + i['urltype']].append(i)
            iTotalRecords = iTotalDisplayRecords = len(resurls_detail)
            
            aaData = []
            for k,v in resurls_detail.items():
                aaData.append([v[0]['url'],
                    str(v[0]['dport']),
                    v[0]['sip'],
                    k.split(',')[0],
                    str(len(v)),
                    k.split(',')[1],
                    '']
                )

            #Ordering data
            iSortingCols =  int(request.GET.get('iSortingCols',0))#根据几columns进行排序
            asortingCols = []

            if iSortingCols:
                sortedColID = int(request.GET.get('iSortCol_0',0))
                if request.GET.get('bSortable_{0}'.format(sortedColID), 'false')  == 'true':  #判断是否可以sort
                    reverse = request.GET.get('sSortDir_0') == 'desc'
                    aaData.sort(cmp=lambda x,y: cmp(x[sortedColID].lower(), y[sortedColID].lower()),reverse=reverse)

            aaData = aaData[int(request.GET.get('iDisplayStart')):int(request.GET.get('iDisplayStart'))+int(request.GET.get('iDisplayLength'))]
            for i in aaData:
                i[5] = dict(RESTYPE_CHOICES)[i[5]]
            
      #      jsonTemplatePath = 'json_detail.txt'
      #      jstonString = render_to_string(jsonTemplatePath,locals())
      #      response = HttpResponse(jstonString,mimetype="application/javascript")
        else:
            aaData,iTotalDisplayRecords,iTotalRecords = [],0,0
    except Exception,e:
        aaData,iTotalDisplayRecords,iTotalRecords = [],0,0
        traceback.print_exc()

    response_dict = {}
    response_dict.update({'aaData':aaData})
    response_dict.update({
        'iTotalDisplayRecords':iTotalDisplayRecords,
        'iTotalRecords':iTotalRecords
    })#实际上起作用的数据
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')

    #阻止缓存
    add_never_cache_headers(response)

    return response

@login_required
def statistic_url_search(request):
    title = u'URL查找统计'
    if request.method == "POST":
        form = ResUrl_Search(request=request,data=request.POST)
        if form.is_valid():
            form = form.cleaned_data
            return render_to_response('statistic/url_search_result.html',
                                                    locals(), 
                                                    context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return HttpResponseRedirect('/statistic/url/')


##########################################statistic_ip################################################### 

@login_required
def statistic_ip(request):
    title = u'IP记录统计'
    iptypes = [('resiptype'+k,k,y) for k,y in RESTYPE_CHOICES]

    return render_to_response('statistic/ip.html',locals(), context_instance = RequestContext(request))
    
@login_required
def get_resips_list(request):
    print "test"
    filterdict = dict()
    if request.GET.get('iptypes',False) > '':
        for i in request.GET.get('iptypes').split(','):
            if i in dict(RESTYPE_CHOICES).keys():
                filterdict["iptype"] = i

    riskdict=dict()
    riskdict["$gt"] = -1
    filterdict["riskvalue"] = riskdict

    if request.GET.get('riskvalue',False):
        try:
            filterdict["riskvalue"] = int(request.GET.get('riskvalue',False))
        except Exception,e:
            riskdict["$gt"] = -1
            filterdict["riskvalue"] = riskdict

    timedict = dict()
    if request.GET.get('begintime',False):
        try:
            timedict["$gt"]=datetime.datetime.strptime(request.GET.get('begintime'),'%Y-%m-%d')
        except Exception,e:
            traceback.print_exc() 
    if request.GET.get('endtime',False):       
        try:
            timedict["$lt"] = datetime.datetime.strptime(request.GET.get('endtime'),'%Y-%m-%d')
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()
    if timedict:filterdict["datetime"] = timedict  
    print "test"

    columnIndexNameMap = { 
        0: 'id', 
        1: 'autoid',
        2: 'user_id',
        3: 'datetime', 
        4: 'iptype', 
        5: 'protocol',
        6: 'riskvalue',
        7: 'sip',
        8: 'dip',
        9: 'sport',
        10: 'dport',
        11: 'flow',  
        12: 'processmd5',
        13: 'length',
        14: 'processname'
    }

    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])
    extrafilters = {'iptype':RESTYPE_CHOICES,'alarm':ALARM_CHOICES}
    print "test"
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, 
                                                                                    ResIp, 
                                                                                    columnIndexNameMap,
                                                                                    None,
                                                                                    filterdict,
                                                                                    True,
                                                                                    'datetime')
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0))+1
    print "test"
    for i in aaData:
        try:
            i.insert(1,index)
            index = index +1
            i[columnNameIndexMap['protocol']] = dict(IPPROTOCOL_CHOICES)[i[columnNameIndexMap['protocol']]]
            i[columnNameIndexMap['iptype']] = dict(RESTYPE_CHOICES)[i[columnNameIndexMap['iptype']]]
            i[columnNameIndexMap['flow']] = dict(FLOW_CHOICES)[i[columnNameIndexMap['flow']]]
            print "i[columnNameIndexMap['user_id']]",i[columnNameIndexMap['user_id']]
            i[columnNameIndexMap['user_id']] = Userinfo.objects.get(id=i[columnNameIndexMap['user_id']]).realname
        except Exception,e:
            continue
    response_dict = {}
    response_dict.update({'aaData':aaData})
    
    response_dict.update({'sEcho': sEcho, 'iTotalRecords': iTotalRecords, 'iTotalDisplayRecords':iTotalDisplayRecords, 'sColumns':sColumns})
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

    print "test"
    #阻止缓存
    add_never_cache_headers(response)
    return response

@login_required
def get_detail_resips_list(request):
    try:
        if request.GET.get('ip'):
            ip = request.GET.get('ip')
            resips = ResIp.objects.filter(Q(riskvalue__gt=-1),Q(sip=ip)|Q(dip=ip))
            
            iTotalDisplayRecords = resips.count()
            
            resips = resips.values('dip','sip','datetime','iptype','sport','dport') 

            starttime = time.time()
            for i in resips:
                i['datetime'] = i['datetime'].strftime('%Y-%m-%d')
            endtime = time.time()
            print "-------------------get_detail_resips_list-----------------------",(endtime-starttime)
      
            from collections import defaultdict
    
            resips_detail = defaultdict(list)
            for i in resips:
                resips_detail[i['datetime'] + ',' + str(i['iptype'])].append(i)
            iTotalRecords = iTotalDisplayRecords = len(resips_detail)

            aaData = []
            for k,v in resips_detail.items():
                aaData.append([ip,
                    v[0]['dip'],
                    v[0]['sip'],
                    str(v[0]['sport']),
                    str(v[0]['dport']),
                    k.split(',')[0],
                    str(len(v)),
                    k.split(',')[1],
                    '']
                )

            #Ordering data
            iSortingCols =  int(request.GET.get('iSortingCols',0))#根据几columns进行排序
            asortingCols = []


            if iSortingCols:
                sortedColID = int(request.GET.get('iSortCol_0',0))
                if request.GET.get('bSortable_{0}'.format(sortedColID), 'false')  == 'true':  #判断是否可以sort
                    reverse = request.GET.get('sSortDir_0') == 'desc'
                    aaData.sort(cmp=lambda x,y: cmp(x[sortedColID].lower(), y[sortedColID].lower()),reverse=reverse)

            aaData = aaData[int(request.GET.get('iDisplayStart')):int(request.GET.get('iDisplayStart'))+int(request.GET.get('iDisplayLength'))]
            for i in aaData:
                i[7] = dict(RESTYPE_CHOICES)[i[7]]
            
        else:
            aaData,iTotalDisplayRecords,iTotalRecords = [],0,0
    except Exception,e:
        aaData,iTotalDisplayRecords,iTotalRecords = [],0,0
        traceback.print_exc()

    response_dict = {}
    response_dict.update({'aaData':aaData})
    response_dict.update({
        'iTotalDisplayRecords':iTotalDisplayRecords,
        'iTotalRecords':iTotalRecords
    })#实际上起作用的数据
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')

    #阻止缓存
    add_never_cache_headers(response)


    return response

@login_required
def statistic_ip_search(request):
    title = u'IP查找统计'
    if request.method == "POST":
        form = ResIp_Search(request=request,data=request.POST)
        if form.is_valid():
            form = form.cleaned_data
            return render_to_response('statistic/ip_search_result.html',
                                                    locals(), 
                                                    context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return HttpResponseRedirect('/statistic/ip/')
