#!/usr/bin/python
#-*-coding:utf-8-*-

from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from models import ResEmail,Userinfo,ResUrl,BlackEmail,BlackIp,BlackUrl,ResIp,\
                    WhiteEmail,ResEmail,ResIp,ResUrl,WhiteIp,WhiteUrl,NetBehaviour,\
                    DriverBehaviour
from django.template.loader import render_to_string
from models import ALARM_CHOICES,RESTYPE_CHOICES,TYPE_CHOICES,IPPROTOCOL_CHOICES,FLOW_CHOICES
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from django.template import RequestContext
from engine.utils import get_datatables_records,get_highcharts_records
from django.db.models import Q
from forms import ResEmail_Search,BlackEmail_Search,BlackEmail_Add,\
                BlackEmail_Edit,BlackIp_Add,BlackIp_Edit,\
                BlackUrl_Add,BlackUrl_Edit,ResUrl_Search,ResIp_Search,WhiteList_Add,\
                NetBehaviour_Search
from utils import datestrtsecs 
import traceback
import datetime
from datetime import timedelta
from bson.objectid import ObjectId

##########################################user_statistic_email################################################### 

@login_required
def user_statistic_email(request):
    title = u'邮件记录统计'
    emailtypes = [('resemailtype'+k,k,y) for k,y in RESTYPE_CHOICES]
    return render_to_response('userstatistic/email.html',locals(), context_instance = RequestContext(request))

@login_required
def get_user_resemails_list(request):

    filterdict = dict()

    if request.GET.get('emailtypes',False) > '':
        for i in request.GET.get('emailtypes').split(','):
            if i in dict(RESTYPE_CHOICES).keys():
                filterdict["emailtype"] = i
    filterdict["iswhite"] = {"$ne":True}
    
    userinfo = Userinfo.objects.get(user = request.user)
    filterdict["user_id"] = ObjectId(userinfo.id)

    riskdict=dict()
    riskdict["$ne"] = '-1'
    filterdict["riskvalue"] = riskdict

    if request.GET.get('riskvalue',False):
        try:
            filterdict["riskvalue"] = int(request.GET.get('riskvalue',False))
        except Exception,e:
            riskdict["$ne"] = '-1'
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
        2: 'datetime', 
        3: 'sendfrom', 
        4: 'sendto', 
        5: 'sip', 
        6: 'dip',
        7: 'riskvalue', 
        8: 'emailtype',
        9: 'sendcc',
        10: 'sendbcc',
        11: 'subject',
        12: 'sport',
        13: 'dport',
        14: 'addtowhite',
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
        i.insert(1,index)
        index = index+1
        i[columnNameIndexMap['emailtype']] = dict(RESTYPE_CHOICES)[i[columnNameIndexMap['emailtype']]]
        i.append("")
#        i[columnNameIndexMap['user_id']] = Userinfo.objects.get(id=i[columnNameIndexMap['user_id']]).realname

    response_dict = {}
    response_dict.update({'aaData':aaData})
    
    response_dict.update({'sEcho': sEcho, 'iTotalRecords': iTotalRecords, 'iTotalDisplayRecords':iTotalDisplayRecords, 'sColumns':sColumns})
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')

    #阻止缓存
    add_never_cache_headers(response)
    return response



@login_required
def get_user_detail_resemails_list(request):
    
    try:
        if request.GET.get('id'):
            receiver = ResEmail.objects.get(id=request.GET.get('id'),user = Userinfo.objects.get(user=request.user)).sendto
            resemails = ResEmail.objects.filter(sendto=receiver,user = Userinfo.objects.get(user=request.user))
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
def user_statistic_email_search(request):
    title = u'邮件查找统计'
    if request.method == "POST":
        form = ResEmail_Search(request=request,data=request.POST)
        if form.is_valid():
            form = form.cleaned_data
            return render_to_response('userstatistic/email_search_result.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return HttpResponseRedirect('/user_statistic/email/')


@login_required
def add_white_email(request):
    form = WhiteList_Add(data=request.GET)
    if form.is_valid():
        user = Userinfo.objects.get(user=request.user)
        email = form.cleaned_data['white_email']

        newwhiteemail = WhiteEmail(   user = user,
                                email=email,
                                addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        newwhiteemail.save()
        id = request.GET.get('id')
        editresemail = ResEmail.objects.get(id=id)
        editresemail.iswhite = True
        editresemail.save()
        add_success = True
        return HttpResponseRedirect('/user_statistic/email/')
#        return render_to_response('error.html',locals(), context_instance = RequestContext(request))
    else:
        return render_to_response('error.html',locals(), context_instance = RequestContext(request))
    
##########################################user_statistic_url################################################### 

@login_required
def user_statistic_url(request):
    title = u'URL记录统计'
    urltypes = [('resurltype'+k,k,y) for k,y in RESTYPE_CHOICES]

    return render_to_response('userstatistic/url.html',locals(), context_instance = RequestContext(request))
    
@login_required    
def get_user_resurls_list(request):
 
    filterdict = dict()
    if request.GET.get('urltypes',False) > '':
        for i in request.GET.get('urltypes').split(','):
            if i in dict(RESTYPE_CHOICES).keys():
                filterdict["urltype"] = i
    filterdict["iswhite"] = {"$ne":True}
    riskdict=dict()
    riskdict["$ne"] = -1
    filterdict["riskvalue"] = riskdict

    if request.GET.get('riskvalue',False):
        try:
            filterdict["riskvalue"] = int(request.GET.get('riskvalue',False))
        except Exception,e:
            riskdict["$ne"] = -1
            filterdict["riskvalue"] = riskdict
    userinfo = Userinfo.objects.get(user = request.user)
    filterdict["user_id"] = ObjectId(userinfo.id)
    
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
        2: 'datetime', 
        3: 'url', 
        4: 'urltype', 
        5: 'riskvalue',
        6: 'sip',
        7: 'dip',
        8: 'sport',
        9: 'dport',
        10: 'processname',
        11: 'processmd5',
        12: 'addtowhite'
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
        i.insert(1,index)
        index = index + 1
        i[columnNameIndexMap['urltype']] = dict(RESTYPE_CHOICES)[i[columnNameIndexMap['urltype']]]
        i.append("")

    response_dict = {}
    response_dict.update({'aaData':aaData})
    
    response_dict.update({'sEcho': sEcho, 'iTotalRecords': iTotalRecords, 'iTotalDisplayRecords':iTotalDisplayRecords, 'sColumns':sColumns})
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

    #阻止缓存
    add_never_cache_headers(response)
    return response
    
    



@login_required
def get_user_detail_resurls_list(request):
    try:
        if request.GET.get('id'):
            url = str(ResUrl.objects.get(id=request.GET.get('id')))
            resurls = ResUrl.objects.filter(url=url,user = Userinfo.objects.get(user=request.user))
            iTotalDisplayRecords = resurls.count()
            resurls = resurls.values('dport','sip','datetime','urltype')
            for i in resurls:
                i['datetime'] = i['datetime'].strftime('%Y-%m-%d')
            from collections import defaultdict
            resurls_detail = defaultdict(list)
            for i in resurls:
                resurls_detail[i['datetime'] + ',' + i['urltype']].append(i)
            iTotalRecords = iTotalDisplayRecords = len(resurls_detail)
            aaData = []
            for k,v in resurls_detail.items():
                aaData.append([url,
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
def user_statistic_url_search(request):
    title = u'URL查找统计'
    if request.method == "POST":
        form = ResUrl_Search(request=request,data=request.POST)
        if form.is_valid():
            form = form.cleaned_data
            return render_to_response('userstatistic/url_search_result.html',
                                                    locals(), 
                                                    context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return HttpResponseRedirect('/user_statistic/url/')

@login_required
def add_white_url(request):
    form = WhiteList_Add(data=request.GET)
    if form.is_valid():
        newwhiteurl = WhiteUrl(   user = Userinfo.objects.get(user=request.user),
                                url=form.cleaned_data['white_url'],
                                addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        newwhiteurl.save()
        add_success = True
        id = request.GET.get('id')
        editresurl = ResUrl.objects.get(id=id)
        editresurl.iswhite = True
        editresurl.save()
        add_success = True
        return HttpResponseRedirect('/user_statistic/url/')
    else:
        return render_to_response('error.html',locals(), context_instance = RequestContext(request))
        
##########################################user_statistic_ip################################################### 

@login_required
def user_statistic_ip(request):
    title = u'IP记录统计'
    iptypes = [('resiptype'+k,k,y) for k,y in RESTYPE_CHOICES]

    return render_to_response('userstatistic/ip.html',locals(), context_instance = RequestContext(request))
    
@login_required
def get_user_resips_list(request):

    filterdict = dict()

    riskdict=dict()
    riskdict["$ne"] = -1
    filterdict["riskvalue"] = riskdict

    if request.GET.get('riskvalue',False):
        try:
            filterdict["riskvalue"] = int(request.GET.get('riskvalue',False))
        except Exception,e:
            riskdict["$ne"] = -1
            filterdict["riskvalue"] = riskdict

    userinfo = Userinfo.objects.get(user = request.user)
    filterdict["user_id"] = ObjectId(userinfo.id)

    filterdict["iswhite"] = {"$ne":True}

    if request.GET.get('iptypes',False) > '':
        for i in request.GET.get('iptypes').split(','):
            if i in dict(RESTYPE_CHOICES).keys():
                filterdict["iptype"] = i
                
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
        2: 'datetime', 
        3: 'protocol',
        4: 'riskvalue',
        5: 'iptype', 
        6: 'length',
        7: 'sip',
        8: 'dip',
        9: 'sport',
        10: 'dport',
        11: 'flow',  
        12: 'processname',
        13: 'processmd5',
        14: 'addtowhite'
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])
    #jsonTemplatePath = 'json_resips.txt'
    extrafilters = {'iptype':RESTYPE_CHOICES}

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
    for i in aaData:
        i.insert(1,index)
        index = index +1
        i[columnNameIndexMap['protocol']] = dict(IPPROTOCOL_CHOICES)[i[columnNameIndexMap['protocol']]]
        i[columnNameIndexMap['iptype']] = dict(RESTYPE_CHOICES)[i[columnNameIndexMap['iptype']]]
        i[columnNameIndexMap['flow']] = dict(FLOW_CHOICES)[i[columnNameIndexMap['flow']]]

        i.append("")

    response_dict = {}
    response_dict.update({'aaData':aaData})
    
    response_dict.update({'sEcho': sEcho, 'iTotalRecords': iTotalRecords, 'iTotalDisplayRecords':iTotalDisplayRecords, 'sColumns':sColumns})
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')

    #阻止缓存
    add_never_cache_headers(response)
    return response

@login_required
def get_user_detail_resips_list(request):
    try:
        if request.GET.get('ip'):
            ip = request.GET.get('ip')
            userinfo = Userinfo.objects.get(user = request.user)
            resips = ResIp.objects.filter(Q(user=userinfo),Q(sip=ip)|Q(dip=ip))
            iTotalDisplayRecords = resips.count()
            resips = resips.values('dip','sip','datetime','iptype','sport','dport')
            for i in resips:
                i['datetime'] = i['datetime'].strftime('%Y-%m-%d')
            from collections import defaultdict
            resips_detail = defaultdict(list)
            for i in resips:
                resips_detail[i['datetime'] + ',' + str(i['iptype'])].append(i)
            iTotalRecords = iTotalDisplayRecords = len(resips_detail)
            aaData = []
            for k,v in resips_detail.items():
                aaData.append([ip,
                    v[0]['sip'],
                    v[0]['dip'],
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
def user_statistic_ip_search(request):
    title = u'IP查找统计'
    if request.method == "POST":
        form = ResIp_Search(request=request,data=request.POST)
        if form.is_valid():
            form = form.cleaned_data
            return render_to_response('userstatistic/ip_search_result.html',
                                                    locals(), 
                                                    context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return HttpResponseRedirect('/user_statistic/ip/')

@login_required
def add_white_ip(request):
    form = WhiteList_Add(data=request.GET)
    if form.is_valid():
        newwhiteip = WhiteIp(   user = Userinfo.objects.get(user=request.user),
                                ip=form.cleaned_data['white_ip'],
                                addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        newwhiteip.save()
        add_success = True
        whiteip = request.GET.get('white_ip')
        ipflow = request.GET.get('flow')
        if ipflow == "上行":
            ipflow = "0"
        else:
            ipflow = "1"
        print "ipflow",ipflow,"whiteip",whiteip

        resips = ResIp.objects.filter(Q(sip=whiteip,flow="0")|Q(dip=whiteip,flow="1"))
        print "resips",resips
        for i in resips:
            i.iswhite = True
            i.save()
        add_success = True
        return HttpResponseRedirect('/user_statistic/ip/')
    else:
        return render_to_response('error.html',locals(), context_instance = RequestContext(request))


@login_required
def user_statistic_net(request):
    title = u'网络事件统计'
    return render_to_response('userstatistic/net_behaviour.html',locals(), context_instance = RequestContext(request))

@login_required
def get_net_behaviour_list(request):
    filterdict = dict()
    if User.objects.get(username = request.user).is_superuser == False:
        userinfo = Userinfo.objects.get(user = request.user)
        filterdict["user_id"] = ObjectId(userinfo.id)
    # riskdict=dict()
    # riskdict["$ne"] = -1
    # filterdict["riskvalue"] = riskdict

    # if request.GET.get('riskvalue',False):
    #     try:
    #         filterdict["riskvalue"] = int(request.GET.get('riskvalue',False))
    #     except Exception,e:
    #         riskdict["$ne"] = -1
    #         filterdict["riskvalue"] = riskdict
    # if request.GET.get('blackiptype',False) > '':
    #     for i in request.GET.get('blackiptype').split(','):
    #         if i in dict(TYPE_CHOICES).keys():
    #             filterdict["iptype"] = i
    
    # timeQ = None
    # timedict = dict()
    # if request.GET.get('begintime',False):
    #     try:
    #         timedict["$gt"]=datetime.datetime.strptime(request.GET.get('begintime'),'%Y-%m-%d')
    #     except Exception,e:
    #         traceback.print_exc() 
    # if request.GET.get('endtime',False):
    #     try:
    #         timedict["$lt"] = datetime.datetime.strptime(request.GET.get('endtime'),'%Y-%m-%d')
    #     except Exception,e:
    #         timedict["$lt"] = datetime.datetime.now()
    # if timedict:filterdict["addtime"] = timedict
    
    columnIndexNameMap = { 
        0: 'id', 
        1: 'autoid',
        2: 'user_id', 
        3: 'content', 
        4: 'level', 
        5: 'tick',
        6: 'sip',
        7: 'dip',   
        8: 'version',
        9: 'transfprotc', 
        10: 'appprotc',
        11: 'nettype', 
        12: 'datetime',
        13: 'riskvalue',
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, NetBehaviour, columnIndexNameMap,None,filterdict,True,'datetime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0))+1
    for i in aaData:#将iptype和user_id字段在数据库中的存储和界面显示对应
        i.insert(1,index)
        index = index+1
        i[columnNameIndexMap['user_id']] = Userinfo.objects.get(id=i[columnNameIndexMap['user_id']]).realname
    response_dict = {}
    response_dict.update({'aaData':aaData})
    response_dict.update({
        'sEcho': sEcho, 
        'iTotalRecords': iTotalRecords, 
        'iTotalDisplayRecords':iTotalDisplayRecords, 
        'sColumns':sColumns
    })
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')
    #阻止缓存
    add_never_cache_headers(response)
    return response
#------------------------------------------------------------------blackip_search--------------------------------------------------------
@login_required
def net_behaviour_search(request):
    title = u'网络事件统计查找'
    if request.method == "POST":
        form = NetBehaviour_Search(request=request,data=request.POST)
        print "11111111"
        if form.is_valid():
            print "22222222222"
            form = form.cleaned_data
            return render_to_response('userstatistic/net_behaviour_search_result.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return HttpResponseRedirect('/userstatistic/user_statistic_net/')

@login_required
def user_statistic_driver(request):
    title = u'驱动事件统计'
    return render_to_response('userstatistic/driver_behaviour.html',locals(), context_instance = RequestContext(request))

'''
author : myc
edit : myc
creat_time : 2013.04.16 
last_edit : 2013.04.17
function : return the driver name that DriverBehaviour different
'''

@login_required
def user_statistic_driver_compare(request):

    print 'in user_statistic_driver_compare'
    title = u'驱动事件统计比对'
    drivers = DriverBehaviour.objects.distinct('driver')
    drivernames = []
    for driver in drivers:
        filterdict = {'driver':driver}
        print driver
        drivernames.append(driver)

    #print drivernames
    names = ",".join(drivernames)
    return render_to_response('userstatistic/driver_compare_behaviour.html',locals(),context_instance = RequestContext(request))


'''
author : myc
edit : myc
creat_time : 2013.04.17 
last_edit : 2013.04.18
dunction : 给事件统计比对数据 json style
'''

@login_required
def get_driver_compare_data_list(request):

    print 'in get_driver_compare_data_list'
    driver = request.GET["driver"]
    datas =[]
    columnIndexNameMap = {0: 'datetime'}
    print "test"
    print DriverBehaviour.objects.order_by("datetime")
    earliest_time = DriverBehaviour.objects.order_by("datetime")[0].datetime
    print "earliest_time",earliest_time
    latest_time = DriverBehaviour.objects.order_by("-datetime")[0].datetime
    end_days = (latest_time-earliest_time).days

    #check the days between make sure it is 30 days 
    if end_days < 30:
        earliest_time = earliest_time + datetime.timedelta(hours=-1)
        print earliest_time,'earliest_time if  '
        end_days = 30
    else:
        earliest_time = latest_time + datetime.timedelta(hours=-30*24)
        print earliest_time,'earliest_time else '
    filterdict = dict()
    #find the filter driver to get the datetime 

    filterdict["driver"] = driver

    if User.objects.get(username = request.user).is_superuser == False:
        userinfo = Userinfo.objects.get(user=request.user)
        filterdict["user_id"] =ObjectId(userinfo.id)
    db_datetime = get_highcharts_records(DriverBehaviour,columnIndexNameMap,filterdict,"datetime")

    print (latest_time - earliest_time).days*24

    driverdict = {}

    #fill the time with 0 and add num to the one that exist
    for i in range((latest_time - earliest_time).seconds/3600 + 1 + end_days*24):
        currtime = earliest_time + datetime.timedelta(hours=i)
        totime = earliest_time + datetime.timedelta(hours=i+1)
        secstimestr  = datestrtsecs(currtime.strftime("%Y-%m-%d %H:00:00"))*1000
        #print secstimestr
        totimestr = datestrtsecs(totime.strftime("%Y-%m-%d %H:00:00"))*1000
        driverdict[secstimestr]  = 0

        for cmp_time in db_datetime:
            icmp_time = int(cmp_time[0])
            #print icmp_time,'icmp_time'
            if  icmp_time >= secstimestr and icmp_time <= totimestr:
                driverdict[secstimestr]  += 1
    # change tha data to style what we want
    strlist = list()
    for i in sorted(driverdict):
        tmpstr = "[%s,%d]"%(i,driverdict[i])
        strlist.append(tmpstr)
    driverdata = ",".join(strlist)
    datas.append(driverdata)
    response =  HttpResponse(simplejson.dumps(datas), mimetype='application/json')
    #阻止缓存
    add_never_cache_headers(response)
    #print response
    return response

'''
author : myc
edit : myc
creat_time : 2013.04.17 
last_edit : 2013.04.18
function : return the driver name that DriverBehaviour different
'''

@login_required
def user_statistic_net_compare(request):

    title = u'网络事件统计比对'
    print 'in user_statistic_net_compare '
    appprotcs = NetBehaviour.objects.distinct('appprotc')
    appprotcnames = []
    for appprotc in appprotcs:
        filterdict = {'appprotc':appprotc}
        print appprotc
        appprotcnames.append(appprotc)

    print appprotcnames
    names = ",".join(appprotcnames)
    return render_to_response('userstatistic/net_compare_behaviour.html',locals(),context_instance = RequestContext(request))




'''
author : myc
edit : myc
creat_time : 2013.04.17
last_edit : 2013.04.18
function : 给事件统计比对数据 json style
'''

@login_required
def get_net_compare_data_list(request):

    print 'in get_net_compare_data_list'
    datas =[]
    columnIndexNameMap = {0: 'datetime'}

    appprotc = request.GET["appprotc"]
    print appprotc

    earliest_time = NetBehaviour.objects.order_by("datetime")[0].datetime
    latest_time = NetBehaviour.objects.order_by("-datetime")[0].datetime
    end_days = (latest_time-earliest_time).days

    #check the days between make sure it is 30 days 
    if end_days < 30:
        earliest_time = earliest_time 
        print earliest_time,'get_net_compare_data_list 30 '
        end_days = 30
    else:
        earliest_time = latest_time + datetime.timedelta(hours=-30*24)
        print earliest_time,'get_net_compare_data_list 60'

    #fill the time with 0 and add num to the one that exist
    filterdict = dict()
    filterdict["appprotc"] = appprotc

    if User.objects.get(username = request.user).is_superuser == False:
        userinfo = Userinfo.objects.get(user=request.user)
        filterdict["user_id"] =ObjectId(userinfo.id)

    db_datetime = get_highcharts_records(NetBehaviour,columnIndexNameMap,filterdict,"datetime")
    appprotcdict = {}

    for i in range((latest_time - earliest_time).seconds/3600 + 1 + end_days*24):
        currtime = earliest_time + datetime.timedelta(hours=i)
        totime = earliest_time + datetime.timedelta(hours=i+1)
        secstimestr  = datestrtsecs(currtime.strftime("%Y-%m-%d %H:00:00"))*1000
        #print secstimestr
        totimestr = datestrtsecs(totime.strftime("%Y-%m-%d %H:00:00"))*1000
        appprotcdict[secstimestr]  = 0
        for cmp_time in db_datetime:
            icmp_time = int(cmp_time[0])
            #print icmp_time,'icmp_time'
            if icmp_time >= secstimestr and icmp_time <= totimestr:
                appprotcdict[secstimestr]  += 1

    # change tha data to style what we want
    strlist = list()
    for i in sorted(appprotcdict):
        tmpstr = "[%s,%d]"%(i,appprotcdict[i])
        strlist.append(tmpstr)
    appprotcdata = ",".join(strlist)
    #print driverdata
    datas.append(appprotcdata)
    response =  HttpResponse(simplejson.dumps(datas), mimetype='application/json')
    #阻止缓存
    add_never_cache_headers(response)
    #print response
    return response


@login_required
def get_driver_behaviour_list(request):
    filterdict = dict()
    if User.objects.get(username = request.user).is_superuser == False:
        userinfo = Userinfo.objects.get(user = request.user)
        filterdict["user_id"] = ObjectId(userinfo.id)


    # riskdict=dict()
    # riskdict["$ne"] = -1
    # filterdict["riskvalue"] = riskdict

    # if request.GET.get('riskvalue',False):
    #     try:
    #         filterdict["riskvalue"] = int(request.GET.get('riskvalue',False))
    #     except Exception,e:
    #         riskdict["$ne"] = -1
    #         filterdict["riskvalue"] = riskdict
    # if request.GET.get('blackiptype',False) > '':
    #     for i in request.GET.get('blackiptype').split(','):
    #         if i in dict(TYPE_CHOICES).keys():
    #             filterdict["iptype"] = i
    
    # timeQ = None
    # timedict = dict()
    # if request.GET.get('begintime',False):
    #     try:
    #         timedict["$gt"]=datetime.datetime.strptime(request.GET.get('begintime'),'%Y-%m-%d')
    #     except Exception,e:
    #         traceback.print_exc() 
    # if request.GET.get('endtime',False):
    #     try:
    #         timedict["$lt"] = datetime.datetime.strptime(request.GET.get('endtime'),'%Y-%m-%d')
    #     except Exception,e:
    #         timedict["$lt"] = datetime.datetime.now()
    # if timedict:filterdict["addtime"] = timedict

    columnIndexNameMap = { 
        0: 'id', 
        1: 'autoid',
        2: 'user_id', 
        3: 'driver', 
        4: 'dritype', 
        5: 'program',     
        6: 'flow',
        7: 'commnum', 
        8: 'smscontent',
        9: 'datetime', 
        10: 'riskvalue',

    }

    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, DriverBehaviour, columnIndexNameMap,None,filterdict,True,'datetime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0))+1
    for i in aaData:#将iptype和user_id字段在数据库中的存储和界面显示对应
        i.insert(1,index)
        index = index+1
        i[columnNameIndexMap['user_id']] = Userinfo.objects.get(id=i[columnNameIndexMap['user_id']]).realname
    response_dict = {}
    response_dict.update({'aaData':aaData})
    response_dict.update({
        'sEcho': sEcho, 
        'iTotalRecords': iTotalRecords, 
        'iTotalDisplayRecords':iTotalDisplayRecords, 
        'sColumns':sColumns
    })
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')
    #阻止缓存
    add_never_cache_headers(response)
    return response