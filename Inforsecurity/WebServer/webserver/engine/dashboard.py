#!/usr/bin/python
#-*-coding:utf-8-*-

from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from models import ResEmail,PcAssess,UserPC,Userinfo,ResUrl,ResIp
from models import ALARM_CHOICES,RESTYPE_CHOICES
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from django.template import RequestContext
from engine.utils import get_datatables_records, get_highcharts_records,get_highcharts_detail_records
from utils import datestrtsecs 
import random
import datetime,time
from datetime import timedelta
import traceback
from bson.objectid import ObjectId

@login_required
def general(request):
    return render_to_response('dashboard/general.html',{"title":'风险值查看'},context_instance = RequestContext(request))

@login_required
def ajaxgeneral(request):

    print "i am in"

    #查询条件
    filterdict = dict()
    
    #设定一个月的开始结束时间
    begin = datetime.datetime.now()-timedelta(days=30)
    end = datetime.datetime.now()
    
    #查询条件-开始结束时间
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()
    if timedict: filterdict["datetime"] = timedict
    userinfo = Userinfo.objects.get(user = request.user)
    filterdict["user_id"] = ObjectId(userinfo.id)
    print "i am going to search"
    #约定在数据库返回的值
    columnIndexNameMap = {
        0: 'datetime', 
        1: 'riskvalue',
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    #得到根据前面定义的条件所返回的数据
    aaData = get_highcharts_records(PcAssess,columnIndexNameMap,filterdict,'datetime')

    #将emailtype和user_id字段在数据库中的存储和界面显示对应
    for i in aaData:
        i[columnNameIndexMap['datetime']] = int(i[columnNameIndexMap['datetime']])
        i[columnNameIndexMap['riskvalue']] = int(i[columnNameIndexMap['riskvalue']])

    #定义要返回的变量名
    redata = []
    riskdict = dict()
    #定义开始时间，单位以分钟计算，并且转换成highcharts所需的时间类型
    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d %H:%M"+':00'))*1000
    #把每分钟为单位的一个月时间中，riskdict复位0.为了比较相同时间的风险值，显示比较大的风险值。
    for i in range(30*24*60):
        riskdict[str(tempbegin)]=0
        tempbegin = tempbegin+60*1000
    for i in aaData:
        temptime = i[0]
        riskdict[str(temptime)] = 0
#    #取到得到数据的所有时间，并且对这些时间的riskvalue进行比较，只取最大值，并存在riskdict里面。
    for i in aaData:
        temptime = i[0]
        if i[1]>riskdict[str(temptime)]:
            riskdict[str(temptime)] = i[1]

    # 把riskdict存至我们要返回的数组redata
    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d %H:%M"+':00'))*1000 
    tempend = datestrtsecs(end.strftime("%Y-%m-%d %H:%M"+':00'))*1000    
    for i in range(30*24*60):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=riskdict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*1000
    json = simplejson.dumps(redata)

    return HttpResponse(json, 'application/javascript')
    
#跟用户相关的具体到每台机器的图表显示
@login_required
def general_detail(request):
    
    userinfo = Userinfo.objects.get(user = request.user)
    success = False
    #机器的列表
    pclist = list()
    pcs = UserPC.objects.filter(user=userinfo)
    index = 0
    if len(pcs) != 0: 
        for i in pcs:
            risk =  PcAssess.objects.filter(pc=i).order_by("-datetime")
            if len(risk) != 0:
                #定义pclist的格式
                pclist.append((index,i.id,risk[0].riskvalue))
                index+=1
        if len(pclist) == 0: 
            success = True
    else:
        success = True

    return render_to_response('dashboard/general_detail.html', {'data': pclist,'success':success,'title':"详细信息"},context_instance = RequestContext(request))
    
@login_required
def get_angular_data(request):
    data ={}
    data["pcid"] = []
    data["pcrisk"] = []
    userinfo = Userinfo.objects.get(user = request.user)
    pcs = UserPC.objects.filter(user=userinfo)
    if len(pcs) != 0:
        for i in pcs:
            data["pcid"].append(i.id)
            risk =  PcAssess.objects.filter(pc=i).order_by("-datetime")
            if len(risk) != 0:
                data["pcrisk"].append(risk[0].riskvalue)
    json = simplejson.dumps(data)
    return HttpResponse(json, 'application/javascript')



def get_chart_data(request):
    data ={}
    data["pcid"] = []
    data["pcchart"] = []
    data["index"] = [request.GET["pcnum"]]
    
    filterdict = dict()
    userinfo = Userinfo.objects.get(user = request.user)
    filterdict["user_id"] = ObjectId(userinfo.id)
    pcinfo = UserPC.objects.get(id = ObjectId(request.GET["pc"]))

    filterdict["pc_id"] = ObjectId(pcinfo.id)
    data["pcid"].append(request.GET["pc"])
    begin = datetime.datetime.now()-timedelta(days=30)
    end = datetime.datetime.now()
    
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()
    if timedict: filterdict["datetime"] = timedict
    
    columnIndexNameMap = {
        0: 'datetime', 
        1: 'riskvalue',
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    
    aaData = get_highcharts_records(PcAssess,columnIndexNameMap,filterdict,"datetime")

    # print "aaData",aaData
    for i in aaData:#将emailtype和user_id字段在数据库中的存储和界面显示对应
        i[columnNameIndexMap['datetime']] = int(i[columnNameIndexMap['datetime']])
        i[columnNameIndexMap['riskvalue']] = int(i[columnNameIndexMap['riskvalue']])
    data["pcchart"].append(aaData)

    return HttpResponse(simplejson.dumps(data), 'application/javascript')
    
    
@login_required
def get_chartdt_data(request):

    data ={}
    data["pcid"] = []
    data["pcemailchart"] = []
    data["pcurlchart"] = []
    data["pcipchart"] = []
    data["index"] = [request.GET["pcnum"]]
    
    filterdict = dict()
    userinfo = Userinfo.objects.get(user = request.user)
    filterdict["user_id"] = ObjectId(userinfo.id)
    
    pcinfo = UserPC.objects.get(id = ObjectId(request.GET["pc"]))
    filterdict["pc_id"] = ObjectId(pcinfo.id)
    data["pcid"].append(request.GET["pc"])
    
    begin = datetime.datetime.now()-timedelta(days=1)
    end = datetime.datetime.now()
    
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()
    if timedict: filterdict["datetime"] = timedict
    
    columnIndexNameMap = {0: 'datetime',}
    
    urlData = get_highcharts_records(ResUrl,columnIndexNameMap,filterdict,"datetime")
    emailData = get_highcharts_records(ResEmail,columnIndexNameMap,filterdict,"datetime")
    
    del filterdict['datetime']
    columnIndexNameMap = {0: 'begintime',}
    #ip搜索
    filterdict["begintime"] = timedict
    ipData = get_highcharts_records(ResIp,columnIndexNameMap,filterdict,"begintime")
    
    
    emaildict = dict()
    urldict = dict()
    ipdict = dict()
    timeyestoday = datestrtsecs((datetime.datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d %H:%M:")+'00')*1000;
    temptime = timeyestoday
    for i in range(24*60):
        emaildict[str(timeyestoday)]=0
        urldict[str(timeyestoday)]=0
        ipdict[str(timeyestoday)]=0
        timeyestoday = timeyestoday+60*1000

    for i in emailData:
        minite = i[0]
        emaildict[str(minite)] +=1
    for i in urlData:
        minite = i[0]
        urldict[str(minite)] +=1
    for i in ipData:
        minite = i[0]
        ipdict[str(minite)] +=1
        
    timeyestoday = temptime
    for i in range(24*60):
        tempdata = [0,0]
        tempdata[0]=timeyestoday
        tempdata[1]=emaildict[str(timeyestoday)]
        data["pcemailchart"].append(tempdata)
        timeyestoday = timeyestoday+60*1000
        
    timeyestoday = temptime
    for i in range(24*60):
        tempdata = [0,0]
        tempdata[0]=timeyestoday
        tempdata[1]=urldict[str(timeyestoday)]
        data["pcurlchart"].append(tempdata)
        timeyestoday = timeyestoday+60*1000
        
    timeyestoday = temptime
    for i in range(24*60):
        tempdata = [0,0]
        tempdata[0]=timeyestoday
        tempdata[1]=ipdict[str(timeyestoday)]
        data["pcipchart"].append(tempdata)
        timeyestoday = timeyestoday+60*1000

    return HttpResponse(simplejson.dumps(data), 'application/javascript')


@login_required
def statistic_ip(request):
    ip = request.GET.get('statisticip')

    begin =  datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")
    end = datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")+timedelta(days=1)
    filterdict = dict()
    print "I am here 11"
    filterdict["$or"]=({"sip":ip},{"dip":ip})
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()

    if timedict: filterdict["datetime"] = timedict

    riskdict=dict()
    riskdict["$ne"] = -1
    filterdict["riskvalue"] = riskdict
    
    print "I am here 22"
    columnIndexNameMap = {
        0: 'datetime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    print "I am here 33"
    aaData = get_highcharts_detail_records(ResIp,columnIndexNameMap,filterdict,'datetime')
    print "I am here"
    tempbegin = datestrtsecs(request.GET.get('datetime')+' 00:00:00')*1000

    redata = []
    ipdict = dict()
    for i in range(24):
        ipdict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000

    for i in aaData:
        hours = i[0]
        ipdict[str(hours)] += 1

    tempbegin = datestrtsecs(request.GET.get('datetime')+' 00:00:00')*1000
    for i in range(24):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=ipdict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')

@login_required
def statistic_weekip(request):
    ip = request.GET.get('statisticip')

    end =  datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d") + timedelta(days=1)
    begin = datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")-timedelta(days=6)

    filterdict = dict()
    
    filterdict["$or"]=({"sip":ip},{"dip":ip})
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()

    if timedict: filterdict["datetime"] = timedict
    
    columnIndexNameMap = {
        0: 'datetime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    aaData = get_highcharts_detail_records(ResIp,columnIndexNameMap,filterdict,'datetime')

    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d %H:%M:%S"))*1000

    redata = []
    ipdict = dict()
    for i in range(24*7):
        ipdict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000

    for i in aaData:
        hours = i[0]
        ipdict[str(hours)] += 1

    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d ")+'00:00:00')*1000
    for i in range(24*7):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=ipdict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')
    
#------------------------------nan-----------------------------------------
@login_required
def statistic_url(request):
    url_id = request.GET.get('statisticurl_id')
    url = ResUrl.objects.get(id=url_id).url
    begin =  datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")
    end = datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")+timedelta(days=1)

    filterdict = dict()
    filterdict['url'] = url
    
    riskdict=dict()
    riskdict["$ne"] = -1
    filterdict["riskvalue"] = riskdict

    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()

    if timedict: filterdict["datetime"] = timedict
    
    columnIndexNameMap = {
        0: 'datetime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    aaData = get_highcharts_detail_records(ResUrl,columnIndexNameMap,filterdict,'datetime')
    tempbegin = datestrtsecs(request.GET.get('datetime')+' 00:00:00')*1000

    redata = []
    urldict = dict()
    for i in range(24):
        urldict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000

    for i in aaData:
        hours = i[0]
        urldict[str(hours)] += 1

    tempbegin = datestrtsecs(request.GET.get('datetime')+' 00:00:00')*1000
    for i in range(24):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=urldict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')

@login_required
def statistic_weekurl(request):
    url_id = request.GET.get('statisticurl_id')
    url=ResUrl.objects.get(id=url_id).url
    end =  datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d") + timedelta(days=1)

    begin = datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")-timedelta(days=6)

    filterdict = dict()
    
    filterdict['url'] = url
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()

    if timedict: filterdict["datetime"] = timedict
    
    columnIndexNameMap = {
        0: 'datetime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    aaData = get_highcharts_detail_records(ResUrl,columnIndexNameMap,filterdict,'datetime')

    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d %H:%M:%S"))*1000

    redata = []
    ipdict = dict()
    for i in range(24*7):
        ipdict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000

    for i in aaData:
        hours = i[0]
        ipdict[str(hours)] += 1

    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d ")+'00:00:00')*1000
    for i in range(24*7):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=ipdict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')
#--------------------------------------end---------------------------------
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')
    
@login_required
def statistic_email(request):

    emailid = request.GET.get('emailid')
    sendto = ResEmail.objects.get(id=emailid).sendto

    begin =  datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")
    end = datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")+timedelta(days=1)

    filterdict = dict()
    
    filterdict["sendto"] =  sendto
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()

    if timedict: filterdict["datetime"] = timedict
    
    columnIndexNameMap = {
        0: 'datetime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    aaData = get_highcharts_detail_records(ResEmail,columnIndexNameMap,filterdict,'datetime')

    tempbegin = datestrtsecs(request.GET.get('datetime')+' 00:00:00')*1000

    redata = []
    emaildict = dict()
    for i in range(24):
        emaildict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000

    for i in aaData:
        hours = i[0]
        emaildict[str(hours)] += 1

    tempbegin = datestrtsecs(request.GET.get('datetime')+' 00:00:00')*1000
    for i in range(24):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=emaildict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')

@login_required
def statistic_weekemail(request):

    emailid = request.GET.get('emailid')
    sendto = ResEmail.objects.get(id=emailid).sendto

    end =  datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d") + timedelta(days=1)
    begin = datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")-timedelta(days=6)

    filterdict = dict()
    
    filterdict["sendto"] = sendto
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()

    if timedict: filterdict["datetime"] = timedict
    
    columnIndexNameMap = {
        0: 'datetime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    aaData = get_highcharts_detail_records(ResEmail,columnIndexNameMap,filterdict,'datetime')

    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d %H:%M:%S"))*1000

    redata = []
    emaildict = dict()
    for i in range(24*7):
        emaildict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000

    for i in aaData:
        hours = i[0]
        emaildict[str(hours)] += 1

    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d ")+'00:00:00')*1000
    for i in range(24*7):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=emaildict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')

#----------------------------------------user_highcharts-------------------------------------
@login_required
def user_statistic_ip(request):
    ip = request.GET.get('userstatisticip')
    print ip
    begin =  datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")
    end = datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")+timedelta(days=1)
    userinfo = Userinfo.objects.get(user = request.user)
    filterdict = dict()
    filterdict["user_id"] = ObjectId(userinfo.id)
    filterdict["$or"]=({"sip":ip},{"dip":ip})
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()

    if timedict: filterdict["datetime"] = timedict

    columnIndexNameMap = {
        0: 'datetime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    aaData = get_highcharts_detail_records(ResIp,columnIndexNameMap,filterdict,'datetime')

    tempbegin = datestrtsecs(request.GET.get('datetime')+' 00:00:00')*1000

    redata = []
    ipdict = dict()
    for i in range(24):
        ipdict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000

    for i in aaData:
        hours = i[0]
        ipdict[str(hours)] += 1

    tempbegin = datestrtsecs(request.GET.get('datetime')+' 00:00:00')*1000
    for i in range(24):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=ipdict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')

@login_required
def user_statistic_weekip(request):
    ip = request.GET.get('userstatisticip')
    end =  datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d") + timedelta(days=1)
    begin = datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")-timedelta(days=6)
    userinfo = Userinfo.objects.get(user=request.user)
    filterdict = dict()
    filterdict["user_id"] = ObjectId(userinfo.id)
    filterdict["$or"]=({"sip":ip},{"dip":ip})
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()

    if timedict: filterdict["datetime"] = timedict
    
    columnIndexNameMap = {
        0: 'datetime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    aaData = get_highcharts_detail_records(ResIp,columnIndexNameMap,filterdict,'datetime')

    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d %H:%M:%S"))*1000

    redata = []
    ipdict = dict()
    for i in range(24*7):
        ipdict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000

    for i in aaData:
        hours = i[0]
        ipdict[str(hours)] += 1

    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d ")+'00:00:00')*1000
    for i in range(24*7):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=ipdict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')
    
@login_required
def user_statistic_email(request):
    emailid = request.GET.get('emailid')
    sendto = ResEmail.objects.get(id=emailid).sendto
    begin =  datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")
    end = datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")+timedelta(days=1)
    userinfo = Userinfo.objects.get(user = request.user)
    filterdict = dict()
    filterdict["user_id"] = ObjectId(userinfo.id)
    filterdict["sendto"] = sendto
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()

    if timedict: filterdict["datetime"] = timedict
    
    columnIndexNameMap = {
        0: 'datetime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    aaData = get_highcharts_detail_records(ResEmail,columnIndexNameMap,filterdict,'datetime')

    tempbegin = datestrtsecs(request.GET.get('datetime')+' 00:00:00')*1000

    redata = []
    ipdict = dict()
    for i in range(24):
        ipdict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000

    for i in aaData:
        hours = i[0]
        ipdict[str(hours)] += 1

    tempbegin = datestrtsecs(request.GET.get('datetime')+' 00:00:00')*1000
    for i in range(24):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=ipdict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')

@login_required
def user_statistic_weekemail(request):
    emailid = request.GET.get('emailid')
    sendto = ResEmail.objects.get(id=emailid).sendto
    end =  datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d") + timedelta(days=1)
    begin = datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")-timedelta(days=6)
    userinfo = Userinfo.objects.get(user=request.user)
    filterdict = dict()
    filterdict["user_id"] = ObjectId(userinfo.id)
    filterdict["sendto"] = sendto
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()

    if timedict: filterdict["datetime"] = timedict
    
    columnIndexNameMap = {
        0: 'datetime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    aaData = get_highcharts_detail_records(ResEmail,columnIndexNameMap,filterdict,'datetime')

    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d %H:%M:%S"))*1000


    redata = []
    ipdict = dict()
    for i in range(24*7):
        ipdict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000

    for i in aaData:
        hours = i[0]
        ipdict[str(hours)] += 1

    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d ")+'00:00:00')*1000
    for i in range(24*7):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=ipdict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')
    
@login_required
def userstatistic_url(request):

    urlid = request.GET.get('urlid')
    url = ResUrl.objects.get(id=urlid).url
    userinfo = Userinfo.objects.get(user = request.user)
    begin =  datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")
    end = datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")+timedelta(days=1)

    filterdict = dict()

    filterdict["user_id"] = ObjectId(userinfo.id)
    filterdict["url"] =  url
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()

    if timedict: filterdict["datetime"] = timedict
    
    columnIndexNameMap = {
        0: 'datetime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    aaData = get_highcharts_detail_records(ResUrl,columnIndexNameMap,filterdict,'datetime')

    tempbegin = datestrtsecs(request.GET.get('datetime')+' 00:00:00')*1000

    redata = []
    urldict = dict()
    for i in range(24):
        urldict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000

    for i in aaData:
        hours = i[0]
        urldict[str(hours)] += 1

    tempbegin = datestrtsecs(request.GET.get('datetime')+' 00:00:00')*1000
    for i in range(24):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=urldict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')
    
@login_required
def userstatistic_weekurl(request):

    urlid = request.GET.get('urlid')
    url = ResUrl.objects.get(id=urlid).url
    userinfo = Userinfo.objects.get(user = request.user)
    end =  datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d") + timedelta(days=1)
    begin = datetime.datetime.strptime(request.GET.get('datetime'),"%Y-%m-%d")-timedelta(days=6)

    filterdict = dict()
    
    filterdict["url"] = url
    filterdict["user_id"] = ObjectId(userinfo.id)
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()

    if timedict: filterdict["datetime"] = timedict
    
    columnIndexNameMap = {
        0: 'datetime', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    aaData = get_highcharts_detail_records(ResUrl,columnIndexNameMap,filterdict,'datetime')

    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d %H:%M:%S"))*1000

    redata = []
    urldict = dict()
    for i in range(24*7):
        urldict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000

    for i in aaData:
        hours = i[0]
        urldict[str(hours)] += 1

    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d ")+'00:00:00')*1000
    for i in range(24*7):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=urldict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')

@login_required
def get_user_riskvalue(request):
    data ={}
    data["pcid"] = []
    data["pcchart"] = []
    data["index"] = [request.GET["pcnum"]]
    
    filterdict = dict()
    userinfo = Userinfo.objects.get(user = request.user)
    filterdict["user_id"] = ObjectId(userinfo.id)
    # pcinfo = UserPC.objects.get(id = ObjectId(request.GET["pc"]))
    # print "pcinfo",pcinfo

    filterdict["pc_id"] = ObjectId(pcinfo.id)
    # data["pcid"].append(request.GET["pc"])
    begin = datetime.datetime.now()-timedelta(days=14)
    end = datetime.datetime.now()
    
    timedict = dict()
    if begin:
        try:
            timedict["$gt"]= begin
        except Exception,e:
            traceback.print_exc()
    if end:
        try:
            timedict["$lt"] = end
        except Exception,e:
            timedict["$lt"] = datetime.datetime.now()
    if timedict: filterdict["datetime"] = timedict

    pcinfo = UserPC.objects.filter(user = userinfo)

    pcdict = {}
    for onepc in pcinfo:
        filterdict["pc_id"] = ObjectId(onepc.id)
        pcdict[onepc.id] = get_highcharts_records(PcAssess,columnIndexNameMap,filterdict,"datetime")


    
    columnIndexNameMap = {
        0: 'datetime', 
        1: 'riskvalue',
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    
    aaData = get_highcharts_records(PcAssess,columnIndexNameMap,filterdict,"datetime")
    
    for i in aaData:#将emailtype和user_id字段在数据库中的存储和界面显示对应
        i[columnNameIndexMap['datetime']] = int(i[columnNameIndexMap['datetime']])
        i[columnNameIndexMap['riskvalue']] = int(i[columnNameIndexMap['riskvalue']])
    data["pcchart"].append(aaData)

    return HttpResponse(simplejson.dumps(data), 'application/javascript')