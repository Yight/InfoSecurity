#!/usr/bin/python
#-*-coding:utf-8-*-

from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from models import ResEmail,Userinfo,ResUrl,BlackEmail,BlackIp,BlackUrl
from django.template.loader import render_to_string
from models import ALARM_CHOICES,RESTYPE_CHOICES,TYPE_CHOICES
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from django.template import RequestContext
from engine.utils import get_datatables_records
from django.db.models import Q
from forms import ResEmail_Search,BlackEmail_Search,BlackEmail_Add,BlackEmail_Edit,BlackIp_Add,BlackIp_Edit
from forms import BlackUrl_Add,BlackUrl_Edit,BlackUrl_Search,Blackip_Search
import traceback
import datetime
from bson.objectid import ObjectId

#####################################################################black_email############################################################
@login_required
def black_email(request):
    title = u'收件人黑名单管理'
    emailtypes = [('blackemailtype'+k,k,y) for k,y in TYPE_CHOICES]

    if request.method == "POST":
        form = BlackEmail_Add(data=request.POST)
        if form.is_valid():
            add_success = True
            if not BlackEmail.objects.filter(blackemail=form.cleaned_data['blackemail']):
                newblackemail = BlackEmail(user=request.user.userinfo,blackemail=form.cleaned_data['blackemail'],emailtype=form.cleaned_data['blackemailtype'],riskvalue=form.cleaned_data['riskvalue'],description=form.cleaned_data['description'])
                newblackemail.save()
                add = True
            return render_to_response('management/email.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return render_to_response('management/email.html',locals(), context_instance = RequestContext(request))

#--------------------------------------------------------------get_blackemails_list-------------------------------------------------------#
@login_required
def get_blackemails_list(request):

    filterdict = dict()
        
    #blackemails = BlackEmail.objects.all().reverse()

    riskdict=dict()
    riskdict["$ne"] = -1
    filterdict["riskvalue"] = riskdict

    if request.GET.get('riskvalue',False):
        try:
            filterdict["riskvalue"] = int(request.GET.get('riskvalue',False))
        except Exception,e:
            riskdict["$ne"] = -1
            filterdict["riskvalue"] = riskdict
            
    emailtypeQ = None
    if request.GET.get('blackemailtype',False) > '':
        for i in request.GET.get('blackemailtype').split(','):
            if i in dict(TYPE_CHOICES).keys():
                filterdict["emailtype"] = i
                
    riskdict=dict()
    riskdict["$ne"] = -1
    filterdict["riskvalue"] = riskdict

    if request.GET.get('riskvalue',False):
        try:
            filterdict["riskvalue"] = int(request.GET.get('riskvalue',False))
        except Exception,e:
            riskdict["$ne"] = -1
            filterdict["riskvalue"] = riskdict
            
    timeQ = None
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
    if timedict:filterdict["addtime"] = timedict
    columnIndexNameMap = {
        0: 'id', 
        1: 'autoid',
        2: 'blackemail',
        3: 'emailtype',
        4: 'riskvalue',
        5: 'description',
        6: 'user_id',
        7 : 'addtime',
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    
    extrafilters = {'emailtype':TYPE_CHOICES}#方便使用filter查询邮件类型
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, BlackEmail, columnIndexNameMap,None,filterdict,True,'addtime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0))+1
    for i in aaData:#将emailtype和user_id字段在数据库中的存储和界面显示对应
        i.insert(1,index)
        index = index +1
        i[columnNameIndexMap['emailtype']] = dict(TYPE_CHOICES)[i[columnNameIndexMap['emailtype']]]
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
#-------------------------------------------------------------blackemail_search-------------------------------------------------------#
@login_required
def blackemail_search(request):
    title = u'收件人黑名单管理查找'
    
    if request.method == "POST":
        form = BlackEmail_Search(request=request,data=request.POST)
        if form.is_valid():
            form = form.cleaned_data
            return render_to_response('management/email_search.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return HttpResponseRedirect('/management/blackemail/')
    
#-------------------------------------------------------------delete_blackemail------------------------------------------------------#
@login_required
def delete_blackemail(request):
        
    if request.is_ajax():
        try:
            result = 'true'
            id = request.GET.get('id')
        except Exception,e:
            traceback.print_stack()
        try:
            blackemail = BlackEmail.objects.get(id=id)
            blackemail.delete()
        except ObjectDoesNotExist,e:
            traceback.print_stack()
            result = 'false'
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

        return HttpResponse(simplejson.dumps([result]), mimetype='application/json')
    raise Http404 
    
#-------------------------------------------------------------edit_blackemail-----------------------------------------------------#
@login_required
def edit_blackemail(request):
        
    if request.is_ajax():
        form = BlackEmail_Edit(data=request.GET)
        if form.is_valid():
            try:
                result = 'true'
                id = request.GET.get('id')
            except Exception,e:
                traceback.print_stack()
                return render_to_response('error.html',locals(), context_instance = RequestContext(request))
            try:
                blackemail = BlackEmail.objects.get(id=id)
                blackemail.blackemail = form.cleaned_data['blackemail']
                blackemail.emailtype = form.cleaned_data['blackemailtype']
                blackemail.riskvalue = form.cleaned_data['riskvalue']
                blackemail.description = form.cleaned_data['description']
                blackemail.save()
            except ObjectDoesNotExist,e:
                traceback.print_stack()
                result = 'false'
                return render_to_response('error.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

        return HttpResponse(simplejson.dumps([result]), mimetype='application/json')
    raise Http404 

#####################################################################black_url############################################################
@login_required
def black_url(request):
    title = u'Url黑名单管理'
    urltypes = [('blackurltype'+k,k,y) for k,y in TYPE_CHOICES]
    if request.method == "POST":
        form = BlackUrl_Add(data=request.POST)
        if form.is_valid():
            add_success = True
            if not BlackUrl.objects.filter(blackurl=form.cleaned_data['blackurl']):
                newblackurl = BlackUrl(user=request.user.userinfo,blackurl=form.cleaned_data['blackurl'],urltype=form.cleaned_data['blackurltype'],riskvalue=form.cleaned_data['riskvalue'],description=form.cleaned_data['description'])
                newblackurl.save()
                add = True
            return render_to_response('management/url.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return render_to_response('management/url.html',locals(), context_instance = RequestContext(request))


#----------------------------------------------------get_blackUrl_list-------------------------------------------------------------------#
@login_required
def get_blackurl_list(request):
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
    urltypeQ = None
    if request.GET.get('blackurltype',False) > '':
        for i in request.GET.get('blackurltype').split(','):
            if i in dict(TYPE_CHOICES).keys():
                filterdict["urltype"] = i
    
    timeQ = None
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
    if timedict:filterdict["addtime"] = timedict

    columnIndexNameMap = { 
        0: 'id', 
        1: 'autoid',
        2: 'blackurl', 
        3: 'urltype', 
        4: 'riskvalue', 
        5: 'description',     
        6: 'user_id',
        7: 'addtime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    extrafilters = {'urltype':TYPE_CHOICES}#方便使用filter查询邮件类型
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, BlackUrl, columnIndexNameMap,None,filterdict,True,'addtime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0))+1
    for i in aaData:#将Urltype和user_id字段在数据库中的存储和界面显示对应
        i.insert(1,index)
        index = index +1
        i[columnNameIndexMap['urltype']] = dict(TYPE_CHOICES)[i[columnNameIndexMap['urltype']]]
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
#------------------------------------------------------delete_blackUrl------------------------------------------------------------------#
@login_required
def delete_blackurl(request):
    if request.is_ajax():
        try:
            result = 'true'
            id = request.GET.get('id')
        except Exception,e:
            traceback.print_stack()
        try:
            blackurl = BlackUrl.objects.get(id=id)
            blackurl.delete()
        except ObjectDoesNotExist,e:
            traceback.print_stack()
            result = 'false'
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

        return HttpResponse(simplejson.dumps([result]), mimetype='application/json')
    raise Http404 
    
#------------------------------------------------------------edit_blackUrl------------------------------------------------------------#
@login_required
def edit_blackurl(request):
    if request.is_ajax():
        form = BlackUrl_Edit(data=request.GET)
        if form.is_valid():
            try:
                result = 'true'
                id = request.GET.get('id')
            except Exception,e:
                traceback.print_stack()
                return render_to_response('error.html',locals(), context_instance = RequestContext(request))
            try:
                blackurl = BlackUrl.objects.get(id=id)
                blackurl.blackurl = form.cleaned_data['blackurl']
                blackurl.urltype = form.cleaned_data['blackurltype']
                blackurl.riskvalue = form.cleaned_data['riskvalue']
                blackurl.description = form.cleaned_data['description']
                blackurl.save()
            except ObjectDoesNotExist,e:
                traceback.print_stack()
                result = 'false'
                return render_to_response('error.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

        return HttpResponse(simplejson.dumps([result]), mimetype='application/json')
    raise Http404 
    
@login_required
def blackurl_search(request):
    title = u'收件人黑名单管理查找'
    if request.method == "POST":
        form = BlackUrl_Search(request=request,data=request.POST)
        if form.is_valid():
            form = form.cleaned_data
            return render_to_response('management/url_search.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return HttpResponseRedirect('/management/blackURL/')
    
#######################################################black_IP##########################################################
@login_required
def black_ip(request):
    title = u'IP黑名单管理'
    iptypes = [('blackiptype'+k,k,y) for k,y in TYPE_CHOICES]
    if request.method == "POST":
        form = BlackIp_Add(data=request.POST)
        if form.is_valid():
            add_success = True
            if not BlackIp.objects.filter(blackip=form.cleaned_data['blackip']):
                newblackip = BlackIp(user=request.user.userinfo,
                                blackip=form.cleaned_data['blackip'],
                                iptype=form.cleaned_data['blackiptype'],
                                riskvalue=form.cleaned_data['riskvalue'],
                                description=form.cleaned_data['description'])
                newblackip.save()
                add = True
            return render_to_response('management/ip.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return render_to_response('management/ip.html',locals(), context_instance = RequestContext(request))


#---------------------------------------------------------get_blackip_list---------------------------------------------------------
@login_required
def get_blackip_list(request):
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
    if request.GET.get('blackiptype',False) > '':
        for i in request.GET.get('blackiptype').split(','):
            if i in dict(TYPE_CHOICES).keys():
                filterdict["iptype"] = i
    
    timeQ = None
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
    if timedict:filterdict["addtime"] = timedict
    
    columnIndexNameMap = { 
        0: 'id', 
        1: 'autoid',
        2: 'blackip', 
        3: 'iptype', 
        4: 'riskvalue', 
        5: 'description',     
        6: 'user_id',
        7 : 'addtime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    extrafilters = {'iptype':TYPE_CHOICES}#方便使用filter查询邮件类型
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, BlackIp, columnIndexNameMap,None,filterdict,True,'addtime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0))+1
    for i in aaData:#将iptype和user_id字段在数据库中的存储和界面显示对应
        i.insert(1,index)
        index = index+1
        i[columnNameIndexMap['iptype']] = dict(TYPE_CHOICES)[i[columnNameIndexMap['iptype']]]
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
#---------------------------------------------------------delete_blackip---------------------------------------------------------
@login_required
def delete_blackip(request):
    if request.is_ajax():
        try:
            result = 'true'
            id = request.GET.get('id')
        except Exception,e:
            traceback.print_stack()
        try:
            blackip = BlackIp.objects.get(id=id)
            blackip.delete()
        except ObjectDoesNotExist,e:
            traceback.print_stack()
            result = 'false'
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

        return HttpResponse(simplejson.dumps([result]), mimetype='application/json')
    raise Http404 
    
#---------------------------------------------------------edit_blackip---------------------------------------------------------
@login_required
def edit_blackip(request):
    if request.is_ajax():
        form = BlackIp_Edit(data=request.GET)
        if form.is_valid():
            try:
                result = 'true'
                id = request.GET.get('id')
            except Exception,e:
                traceback.print_stack()
                return render_to_response('error.html',locals(), context_instance = RequestContext(request))
            try:
                blackip = BlackIp.objects.get(id=id)
                blackip.blackip = form.cleaned_data['blackip']
                blackip.iptype = form.cleaned_data['blackiptype']
                blackip.riskvalue = form.cleaned_data['riskvalue']
                blackip.description = form.cleaned_data['description']
                blackip.save()
            except ObjectDoesNotExist,e:
                traceback.print_stack()
                result = 'false'
                return render_to_response('error.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

        return HttpResponse(simplejson.dumps([result]), mimetype='application/json')
    raise Http404
#------------------------------------------------------------------blackip_search--------------------------------------------------------
@login_required
def blackip_search(request):
    title = u'收件人黑名单管理查找'
    if request.method == "POST":
        form = Blackip_Search(request=request,data=request.POST)
        if form.is_valid():
            form = form.cleaned_data
            return render_to_response('management/ip_search.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return HttpResponseRedirect('/management/blackip/')
    
