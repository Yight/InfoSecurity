#!/usr/bin/python
#-*-coding:utf-8-*-

from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from models import Userinfo,Job,User,WhiteProcesss
from django.template.loader import render_to_string
from models import ALARM_CHOICES,RESTYPE_CHOICES,TYPE_CHOICES
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from django.template import RequestContext
from engine.utils import get_datatables_records

from engine.tasks import generate_ca,sendsms,sendemail

from forms import WhiteProcess_Add,WhiteProcess_Edit,WhiteProcess_Search

from bson.objectid import ObjectId
import urllib
import traceback
import datetime

##########################################get_register################################
@login_required
def get_register(request):
    title = u'注册管理'
    return render_to_response('sysmanage/register.html',locals(), context_instance = RequestContext(request))
    
##########################################get_register_list################################
@login_required
def get_register_list(request):

    filterdict = dict()
    verifydict = dict()
    verifydict["$ne"] = True
    filterdict["ifverify"] = verifydict
    columnIndexNameMap = {
        0: 'id',
        1: 'id',
        2: 'user_id',
        3: 'realname', 
        4: 'regtime',
        5: 'ifverify', 
        6: 'address', 
        7: 'mobile',
        8: 'email',
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, 
                                                                                    Userinfo, 
                                                                                    columnIndexNameMap,
                                                                                    None,
                                                                                    filterdict,
                                                                                    True,
                                                                                    'regtime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()

    for i in aaData:
        i[columnNameIndexMap['ifverify']] = "未通过" if i[columnNameIndexMap['ifverify']] == "False" else "未审核"
        i[columnNameIndexMap['address']] = "无" if  not i[columnNameIndexMap['address']] else i[columnNameIndexMap['address']]
        i[columnNameIndexMap['user_id']] = User.objects.get(id=i[columnNameIndexMap['user_id']]).username

    for i in aaData:
        i[0] = "<input type=\"checkbox\">"
    response_dict = {}
    response_dict.update({'aaData':aaData})
    
    response_dict.update({'sEcho': sEcho, 
                        'iTotalRecords': iTotalRecords,
                        'iTotalDisplayRecords':iTotalDisplayRecords, 
                        'sColumns':sColumns})
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')

    #阻止缓存
    add_never_cache_headers(response)
    return response
######################risk_manage##########################################

##########################################get_user################################
@login_required
def get_user(request):
    title = u'用户管理'
    return render_to_response('sysmanage/user.html',locals(), context_instance = RequestContext(request))

##########################################get_user_list################################
@login_required
def get_user_list(request):
    filterdict = dict()
    filterdict["ifverify"] = True
    columnIndexNameMap = { 
        0: 'autoid',
        1: 'user_id',
        2: 'id',
        3: 'realname', 
        4: 'regtime', 
        5: 'address', 
        6: 'mobile', 
        7: 'email',
        8: 'dlcertificate',
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, 
                                                                                    Userinfo, 
                                                                                    columnIndexNameMap,
                                                                                    None,
                                                                                    filterdict,
                                                                                    True,
                                                                                    'regtime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0)) + 1
    for i in aaData:
        i.insert(0,index)
        index = index + 1
        i[columnNameIndexMap['address']] = "无" if  not i[columnNameIndexMap['address']] else i[columnNameIndexMap['address']]
        i[columnNameIndexMap['user_id']] = User.objects.get(id=i[columnNameIndexMap['user_id']]).username
        i.append("")
    response_dict = {}
    response_dict.update({'aaData':aaData})
    
    response_dict.update({'sEcho': sEcho, 
                        'iTotalRecords': iTotalRecords,
                        'iTotalDisplayRecords':iTotalDisplayRecords, 
                        'sColumns':sColumns})
    response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')

    #阻止缓存
    add_never_cache_headers(response)
    return response

@login_required
def prove_user(request):

    ifverify = False
    # if request.is_ajax():
    try:
        result = True
        if request.GET.get('type') == 'true':
            ifverify = True
        else:
            ifverify = False
        for i in request.GET.get('id').split(','):
            userinfo = Userinfo.objects.raw_query({"_id":ObjectId(i)})
            if ifverify:
                generate_ca.delay(i)
                sendsms(userinfo[0].mobile,"您在失窃秘系统注册用户已经认证，请及时登录，下载证书~")
                sendemail("失窃秘系统注册用户审核信息","您在失窃秘系统注册用户已经审核通过，请及时登录，下载证书~",userinfo[0].email)

            if len(userinfo):
                userinfo = userinfo[0]
                userinfo.ifverify = ifverify
                userinfo.save()
        return HttpResponse("ok")
    except ObjectDoesNotExist,e:
        result = False
        traceback.print_exc()
        return HttpResponse(simplejson.dumps([result]), mimetype='application/json')
    # raise Http404
#    job管理中如果大类的小类已经被使用那么该大类和该小类是不能删除的，当大类可删除时在删除大类时要先循环其小类逐个删除后再删除大类
@login_required
def job_manage(request):
    jobinfo = "出错了"
    error = False
    success = False
    if request.POST:
        try:
            jobid = request.GET["id"]
            if jobid == "1":
                add_top_category = urllib.unquote(request.POST["add_top_category"])
                if add_top_category:
                    ifexist=Job.objects.raw_query({"name":add_top_category})
                    if ifexist:
                        jobinfo = "您已经添加过此大类了"
                        error = True
                    else:
                        p = Job(pid = None,name = add_top_category)
                        p.save()
                        jobinfo = "恭喜您添加大类成功"
                        success = True
                else:
                    jobinfo = "添加类别不可为空"
                    error = True
            if jobid == "2":
                add_sub_category_top = request.POST["add_sub_category_top"]
                add_sub_category = urllib.unquote(request.POST["add_sub_category"])
                if add_sub_category_top and add_sub_category:
                    parentjob=Job.objects.get(id__exact = add_sub_category_top)
                    ifexist = Job.objects.raw_query({"pid_id":ObjectId(add_sub_category_top),"name":add_sub_category})
                    if ifexist:
                        jobinfo = "您已经添加过此小类了"
                        error = True
                    else:
                        p = Job(pid = parentjob,name = add_sub_category)
                        p.save()
                        jobinfo = "恭喜您添加小类成功"
                        success = True
                else:
                    jobinfo = "添加类别不可为空 "
                    error = True
            if jobid == "3":
                delete_top_category = request.POST["delete_top_category"]
                if delete_top_category:
                    selected = False
                    sub_category = Job.objects.raw_query({"pid_id": ObjectId(delete_top_category)})
                    for single_category in sub_category:
                        jobselecteduser = Userinfo.objects.raw_query({"job_id":ObjectId(single_category.id)})
                        if jobselecteduser:
                            selected = True
                            break
                    if selected:
                        error = True
                        jobinfo = "不可删除已被使用的大类"
                    else:
                        for single_category in sub_category:
                            single_category.delete()
                        Job.objects.raw_query({"_id": ObjectId(delete_top_category)}).delete()
                        jobinfo = "恭喜您删除大类成功"
                        success = True
                else:
                    jobinfo = "请选择要删除的类别"
                    error = True
            if jobid == "4":
                delete_sub_category_top = str(request.POST["delete_sub_category_top"])
                delete_sub_category = str(request.POST["delete_sub_category"])
                if delete_sub_category:
                    jobselecteduser = Userinfo.objects.raw_query({"job_id":ObjectId(delete_sub_category)})
                    if jobselecteduser:
                        error = True
                        jobinfo = "不可删除已被使用的小类"
                    else:
                        Job.objects.raw_query({"_id": ObjectId(delete_sub_category)}).delete()
                        jobinfo = "恭喜您删除小类成功"
                        success = True
                else:
                    jobinfo = "请选择要删除的类别"
                    error = True
            return render_to_response('usermanage/jobmanage.html',{"title":'职业管理',"jobinfo":jobinfo,"error":error,"success":success},context_instance = RequestContext(request))
        except:
            error = True
            jobinfo = "请选择要删除的类别"
            return render_to_response('usermanage/jobmanage.html',{"title":'职业管理',"jobinfo":jobinfo,"error":error,"success":success},context_instance = RequestContext(request))
    return render_to_response('usermanage/jobmanage.html',{"title":'职业管理',"jobinfo":jobinfo,"error":error,"success":success},context_instance = RequestContext(request))

#######################################################process_manage##########################################################
@login_required
def process_manage(request):
    title = u'进程白名单管理'
    if request.method == "POST":
        form = WhiteProcess_Add(data=request.POST)
        if form.is_valid():
            add_success = True
            if not WhiteProcesss.objects.filter(processname=form.cleaned_data['processname']):
                newwhiteprocess = WhiteProcesss(user=request.user.userinfo,
                                processname=form.cleaned_data['processname'],
                                addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                md5=form.cleaned_data['md5'],
                                description=form.cleaned_data['description'],
                                version=form.cleaned_data['version'],)
                newwhiteprocess.save()
                add = True
            return render_to_response('sysmanage/whiteprocess.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return render_to_response('sysmanage/whiteprocess.html',locals(), context_instance = RequestContext(request))
#--------------------------------------------------------------get_blackemails_list-------------------------------------------------------#
@login_required
def get_whiteprocess_list(request):

    filterdict = dict()
        
    # riskdict=dict()
    # riskdict["$ne"] = -1
    # filterdict["riskvalue"] = riskdict

    # if request.GET.get('riskvalue',False):
    #     try:
    #         filterdict["riskvalue"] = int(request.GET.get('riskvalue',False))
    #     except Exception,e:
    #         riskdict["$ne"] = -1
    #         filterdict["riskvalue"] = riskdict
            
    # if request.GET.get('blackemailtype',False) > '':
    #     for i in request.GET.get('blackemailtype').split(','):
    #         if i in dict(TYPE_CHOICES).keys():
    #             filterdict["emailtype"] = i
                
    # riskdict=dict()
    # riskdict["$ne"] = -1
    # filterdict["riskvalue"] = riskdict

    # if request.GET.get('riskvalue',False):
    #     try:
    #         filterdict["riskvalue"] = int(request.GET.get('riskvalue',False))
    #     except Exception,e:
    #         riskdict["$ne"] = -1
    #         filterdict["riskvalue"] = riskdict
            
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
    print "filterdict",filterdict
    print "test1"
    columnIndexNameMap = {
        0: 'id', 
        1: 'autoid',
        2: 'user_id',
        3: 'processname',
        4: 'md5',
        5: 'description',
        6: 'version',
        7 : 'addtime',
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    print "test2"
    try:
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = get_datatables_records(request, WhiteProcesss, columnIndexNameMap,None,filterdict,True,'addtime') 
    except Exception,e:
        traceback.print_exc()
        aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns = [],1,0,0,columnIndexNameMap.values()
    index = int(request.GET.get('iDisplayStart',0))+1
    print "test3"
    for i in aaData:#将emailtype和user_id字段在数据库中的存储和界面显示对应
        i.insert(1,index)
        index = index +1
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

#-------------------------------------------------------------delete_whiteprocess------------------------------------------------------#
@login_required
def delete_whiteprocess(request):
        
    if request.is_ajax():
        try:
            result = 'true'
            id = request.GET.get('id')
        except Exception,e:
            traceback.print_stack()
        try:
            whiteprocess = WhiteProcesss.objects.get(id=id)
            whiteprocess.delete()
        except ObjectDoesNotExist,e:
            traceback.print_stack()
            result = 'false'
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

        return HttpResponse(simplejson.dumps([result]), mimetype='application/json')
    raise Http404 

#---------------------------------------------------------whiteprocess---------------------------------------------------------
@login_required
def edit_whiteprocess(request):
    if request.is_ajax():
        form = WhiteProcess_Edit(data=request.GET)
        if form.is_valid():
            try:
                result = 'true'
                id = request.GET.get('id')
            except Exception,e:
                traceback.print_stack()
                return render_to_response('error.html',locals(), context_instance = RequestContext(request))
            print "test"
            try:
                print id 
                whiteprocess = WhiteProcesss.objects.get(id=id)
                whiteprocess.processname = form.cleaned_data['processname']
                whiteprocess.md5 = form.cleaned_data['md5']
                whiteprocess.addtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                whiteprocess.description = form.cleaned_data['description']
                whiteprocess.user = request.user.userinfo
                whiteprocess.save()
            except ObjectDoesNotExist,e:
                traceback.print_stack()
                result = 'false'
                return render_to_response('error.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

        return HttpResponse(simplejson.dumps([result]), mimetype='application/json')
    raise Http404

#------------------------------------------------------------------whiteprocess_search--------------------------------------------------------
@login_required
def whiteprocess_search(request):
    title = u'收件人黑名单管理查找'
    if request.method == "POST":
        form = WhiteProcess_Search(request=request,data=request.POST)
        if form.is_valid():
            form = form.cleaned_data
            return render_to_response('sysmanage/whiteprocess_search.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    return HttpResponseRedirect('/sysmanage/whiteprocess/')

#------------------------------------------------------------------whiteprocess_search--------------------------------------------------------
@login_required
def client_download(request):
    title = u'客户端下载'
    # if request.method == "POST":
    #     form = WhiteProcess_Search(request=request,data=request.POST)
    #     if form.is_valid():
    #         form = form.cleaned_data
    #         return render_to_response('sysmanage/whiteprocess_search.html',locals(), context_instance = RequestContext(request))
    #     else:
    #         return render_to_response('error.html',locals(), context_instance = RequestContext(request))

    # return HttpResponseRedirect('/sysmanage/whiteprocess/')
    return render_to_response('sysmanage/client_download.html',locals(), context_instance = RequestContext(request))
