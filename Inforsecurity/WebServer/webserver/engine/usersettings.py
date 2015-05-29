#!/usr/bin/python
#-*-coding:utf-8-*-

from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Userinfo,WhiteEmail,WhiteIp,WhiteUrl,AlarmList,User,ResUrl,ResEmail,ResIp
import traceback
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from engine.utils import get_datatables_records
from forms import WhiteList_Add
import datetime
from django.contrib import admin
from bson.objectid import ObjectId
import time 

#######################################################risk_manage####################################################################
@login_required
def risk_manage(request):

    userinfo = Userinfo.objects.get(user=request.user)
    
    infodict = dict()
    infodict["title"] = u'风险值管理'
    infodict["userid"] = request.user
    try:
        if request.GET["success"]:
            infodict["success"]=True
    except:
        infodict["success"]=False
    infodict["emailsms"] = True if userinfo.emailalarmtype[0] == "1" else False
    infodict["emailemail"] = True if userinfo.emailalarmtype[1] == "1" else False
    
    infodict["urlsms"] = True if userinfo.urlalarmtype[0] == "1" else False
    infodict["urlemail"] = True if userinfo.urlalarmtype[1] == "1" else False
    infodict["ipsms"] = True if userinfo.ipalarmtype[0] == "1" else False
    infodict["ipemail"] = True if userinfo.ipalarmtype[1] == "1" else False
    infodict["userinfo"] = userinfo
    return render_to_response('usersettings/risk_manage.html',infodict,context_instance = RequestContext(request))

@login_required
def risk_manage_post(request):
    userinfo = Userinfo.objects.get(user=request.user)
    try:
        userinfo.emailalarmvalue = int(request.POST["email_risk"])
    except:
        userinfo.emailalarmvalue = 0
    try:
        userinfo.urlalarmvalue = int(request.POST["url_risk"])
    except:
        userinfo.urlalarmvalue = 0
    try:
        userinfo.ipalarmvalue =  int(request.POST["ip_risk"])
    except:
        userinfo.ipalarmvalue = 0
    
    emailalarmtype = list("00")
    urlalarmtype = list("00")
    ipalarmtype = list("00")
    emailalarmtype[0] = "1" if request.POST.get("email_type_sms",None) else "0"
    emailalarmtype[1] = "1" if request.POST.get("email_type_email",None) else "0"
    urlalarmtype[0] = "1" if request.POST.get("url_type_sms",None) else "0"
    urlalarmtype[1] = "1" if request.POST.get("url_type_email",None) else "0"
    ipalarmtype[0] = "1" if request.POST.get("ip_type_sms",None) else "0"
    ipalarmtype[1] = "1" if request.POST.get("ip_type_email",None) else "0"
    userinfo.emailalarmtype = emailalarmtype[0]+emailalarmtype[1]
    userinfo.urlalarmtype = urlalarmtype[0]+urlalarmtype[1]
    userinfo.ipalarmtype = ipalarmtype[0]+ipalarmtype[1]
    userinfo.save()
    
    return HttpResponseRedirect("/usersettings/risk_manage/?success=True")

#######################################################white_email####################################################################
@login_required
def white_email(request):
    title = u'Email白名单管理'
    
    if request.method == "POST":
        form = WhiteList_Add(data=request.POST)
        if form.is_valid():
            add_success = True
            user = Userinfo.objects.get(user=request.user)
            email=form.cleaned_data['white_email']
            if not WhiteEmail.objects.filter(user=user,email=email):
                newwhiteemail = WhiteEmail(   user = Userinfo.objects.get(user=request.user),
                                    email=form.cleaned_data['white_email'],
                                    addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                newwhiteemail.save()
                try:
                    whitemails = ResEmail.objects.filter(user=user,sendto=email)
                    for i in whitemails:
                        i.iswhite = True
                        i.save()
                    add = True
                except:
                    add = True
            return render_to_response('usersettings/white_email.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return render_to_response('usersettings/white_email.html',locals(), context_instance = RequestContext(request))

#--------------------------------------------------------------get_blackemails_list-------------------------------------------------------#
@login_required
def get_white_email_list(request):

    filterdict = dict()
    if User.objects.get(username = request.user).is_superuser == False:
        userinfo = Userinfo.objects.get(user=request.user)
        filterdict["user_id"] =ObjectId(userinfo.id)
    columnIndexNameMap = {
        0: 'id', 
        1: 'autoid',
        2: 'email',
        3: 'addtime',
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, WhiteEmail,columnIndexNameMap,None,filterdict,True,'addtime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0)) + 1
    for i in aaData:
        i.insert(1,index)
        index = index + 1
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
    
#------------------------------------------------------------del_white_email_list-------------------------------------------------------#
@login_required
def delete_white_email(request):
        
    if request.is_ajax():
        try:
            result = 'true'
            id = request.GET.get('id')
            email = request.GET.get('email')
        except Exception,e:
            traceback.print_stack()
        try:
            newwhiteemail = WhiteEmail.objects.get(id=id)
            newwhiteemail.delete()
            resemail = ResEmail.objects.filter(sendfrom=email)
            for i in resemail:
                i.iswhite = False
                i.save()
        except ObjectDoesNotExist,e:
            traceback.print_stack()
            result = 'false'
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

        return HttpResponse(simplejson.dumps([result]), mimetype='application/json')
    raise Http404
#######################################################white_ip####################################################################
@login_required
def white_ip(request):
    title = u'IP白名单管理'

    if request.method == "POST":
        form = WhiteList_Add(data=request.POST)
        if form.is_valid():
            add_success = True
            if not WhiteIp.objects.filter(user=Userinfo.objects.get(user=request.user),ip=form.cleaned_data['white_ip']):
                newwhiteip = WhiteIp(   user = Userinfo.objects.get(user=request.user),
                                    ip=form.cleaned_data['white_ip'],
                                    addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                newwhiteip.save()
                try:
                    whiteips = ResIp.objects.filter(user=Userinfo.objects.get(user=request.user),suspiciousip=form.cleaned_data['white_ip'])
                    for i in whiteips:
                        i.iswhite = True
                        i.save()
                    add = True
                except:
                    add = True
            return render_to_response('usersettings/white_ip.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return render_to_response('usersettings/white_ip.html',locals(), context_instance = RequestContext(request))

#--------------------------------------------------------------get_white_ip_list-------------------------------------------------------#
@login_required
def get_white_ip_list(request):

    filterdict = dict()
    if User.objects.get(username = request.user).is_superuser == False:
        userinfo = Userinfo.objects.get(user=request.user)
        filterdict["user_id"] =ObjectId(userinfo.id)
    columnIndexNameMap = {
        0: 'id', 
        1: 'autoid',
        2: 'ip',
        3: 'addtime',
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, WhiteIp,columnIndexNameMap,None,filterdict,True,'addtime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0)) + 1
    for i in aaData:
        i.insert(1,index)
        index = index + 1
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
    
#------------------------------------------------------------del_white_ip_list-------------------------------------------------------#
@login_required
def delete_white_ip(request):
        
    if request.is_ajax():
        try:
            result = 'true'
            id = request.GET.get('id')
            suspiciousip = request.GET.get('ip')
        except Exception,e:
            traceback.print_stack()
        try:
            blackip = WhiteIp.objects.get(id=id)
            blackip.delete()
            # resip = ResIp.objects.filter(suspiciousip=suspiciousip)
            # for i in resip:
            #     i.iswhite = False
            #     i.save()
        except ObjectDoesNotExist,e:
            traceback.print_stack()
            result = 'false'
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

        return HttpResponse(simplejson.dumps([result]), mimetype='application/json')
    raise Http404
#######################################################white_url####################################################################
@login_required
def white_url(request):
    title = u'URL白名单管理'

    if request.method == "POST":
        form = WhiteList_Add(data=request.POST)
        if form.is_valid():
            add_success = True
            if not WhiteUrl.objects.filter(user=Userinfo.objects.get(user=request.user),url=form.cleaned_data['white_url']):
                newwhiteurl = WhiteUrl(   user = Userinfo.objects.get(user=request.user),
                                    url=form.cleaned_data['white_url'],
                                    addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                newwhiteurl.save()
                try:
                    whiteurls = ResUrl.objects.filter(user=Userinfo.objects.get(user=request.user),url=form.cleaned_data['white_url'])
                    for i in whiteurls:
                        i.iswhite = True
                        i.save()
                    add = True
                except:
                    add = True
            return render_to_response('usersettings/white_url.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return render_to_response('usersettings/white_url.html',locals(), context_instance = RequestContext(request))

#--------------------------------------------------------------get_blackemails_list-------------------------------------------------------#
@login_required
def get_white_url_list(request):

    filterdict = dict()

    if User.objects.get(username = request.user).is_superuser == False:
        userinfo = Userinfo.objects.get(user=request.user)
        filterdict["user_id"] =ObjectId(userinfo.id)

    columnIndexNameMap = {
        0: 'id',
        1: 'autoid', 
        2: 'url',
        3: 'addtime',
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, WhiteUrl,columnIndexNameMap,None,filterdict,True,'addtime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0)) + 1
    for i in aaData:
        i.insert(1,index)
        index = index + 1
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
    
#------------------------------------------------------------del_white_url_list-------------------------------------------------------#
@login_required
def delete_white_url(request):
        
    if request.is_ajax():
        try:
            result = 'true'
            id = request.GET.get('id')
            url = request.GET.get('url')
        except Exception,e:
            traceback.print_stack()
        try:
            blackemail = WhiteUrl.objects.get(id=id)
            blackemail.delete()
            resurl = ResUrl.objects.filter(url=url)
            for i in resurl:
                i.iswhite = False
                i.save()
        except ObjectDoesNotExist,e:
            traceback.print_stack()
            result = 'false'
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

        return HttpResponse(simplejson.dumps([result]), mimetype='application/json')
    raise Http404

@login_required
def alarm_list(request):
    title = u'报警列表'
    return render_to_response('usersettings/alarm_list.html',locals(), context_instance = RequestContext(request))

@login_required
def get_alarm_list(request): 
    starttime = time.time()
    columnIndexNameMap = { 
        0: 'id',
        1:'autoid',
        2: 'user_id', 
        3: 'riskvalue', 
        4: 'blackdata', 
        5: 'isfigured', 
        6: 'insert_time',
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])
    filterdict = dict()
    if User.objects.get(username = request.user).is_superuser == False:
        userinfo = Userinfo.objects.get(user=request.user)
        filterdict["user_id"] =ObjectId(userinfo.id)
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, 
                                                                                    AlarmList, 
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
        i[columnNameIndexMap['user_id']] = Userinfo.objects.get(id=i[columnNameIndexMap['user_id']]).realname
        if i[columnNameIndexMap['isfigured']] == 'false':
             i[columnNameIndexMap['isfigured']] = '是'
        else:
            i[columnNameIndexMap['isfigured']] = '否'

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

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
