#!/usr/bin/python
#-*- coding:utf-8 -*-

from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
import time,string,random
import traceback

def gen_random_pwd(pwdlenght):
    passwd = ""
    seed = string.letters + string.digits
    for i in xrange(pwdlenght):
        passwd += seed[random.randrange(1,len(seed))]
    return passwd

'''
* datestr转换成secs
* 将时间字符串转化为秒("2012-07-20 00:00:00"->1342713600.0)
* @param datestr;
* @return secs;
*
'''

def datestrtsecs(datestr):
    tmlist = []
    array = datestr.split(' ')
    array1 = array[0].split('-')
    array2 = array[1].split(':')
    for v in array1:
        tmlist.append(int(v))
    for v in array2:
        tmlist.append(int(v))
    tmlist.append(0)
    tmlist.append(0)
    tmlist.append(0)
    if len(tmlist) != 9:
        return 0
    return int(time.mktime(tmlist)) #+8*60*60
    
def get_highcharts_records(DBMODEL,columnIndexNameMap,filterdict={},dt=""):
    #Pass sColumns
    
    keys = columnIndexNameMap.keys()
    keys.sort()
    colitems = [columnIndexNameMap[key] for key in keys]
    sColumns = ",".join(map(str,colitems))
    querySet = DBMODEL.objects.raw_query(filterdict)
    querySet = querySet.order_by(dt)
    aaData = []
    a = querySet.values() 
    
    begin = time.time()
    for row in a:
        rowkeys = row.keys()
        # print "row.keys()",row.keys()
        rowvalues = row.values()
        # print "row.values()",row.values()
        rowlist = []
        for col in range(0,len(colitems)):
            for idx, val in enumerate(rowkeys):
                if val == colitems[col]:
                    if isinstance(rowvalues[idx],datetime):
                        rowvalues[idx] = datestrtsecs(rowvalues[idx].strftime('%Y-%m-%d %H:%M')+':00')*1000
                    rowlist.append(unicode(rowvalues[idx]))
        aaData.append(rowlist)
    end = time.time()
    print "000000000000000",end-begin
    return aaData

def get_highcharts_detail_records(DBMODEL,columnIndexNameMap,filterdict={},dt=""):
    #Pass sColumns
    keys = columnIndexNameMap.keys()
    keys.sort()
    colitems = [columnIndexNameMap[key] for key in keys]
    sColumns = ",".join(map(str,colitems))
    querySet = DBMODEL.objects.raw_query(filterdict)
    querySet = querySet.order_by(dt)
    aaData = []
    a = querySet.values() 

    try:
        for row in a:
            rowkeys = row.keys()
            rowvalues = row.values()
            rowlist = []
            for col in range(0,len(colitems)):
                for idx, val in enumerate(rowkeys):
                    if val == colitems[col]:
                        if isinstance(rowvalues[idx],datetime):
                            rowvalues[idx] = datestrtsecs(rowvalues[idx].strftime('%Y-%m-%d %H')+':00:00')*1000
                        rowlist.append(unicode(rowvalues[idx]))
            aaData.append(rowlist)
    except Exception,e:
        traceback.print_exc() 
    return aaData

def get_datatables_records(request, DBMODEL, columnIndexNameMap, jsonTemplatePath = None,filterdict={},handle_user=False,dt="", *args):
    # starttime = time.time()
    ######################################参数解析过程################################################
    cols = int(request.GET.get('iColumns',0)) #获取有多少列数据
    iDisplayLength = min(int(request.GET.get('iDisplayLength',10)),100)     #每页获取rows个数
    startRecord = int(request.GET.get('iDisplayStart',0)) #本页第一条数据，是所有数据的第几个,从0开始
    endRecord = startRecord + iDisplayLength  

    #Pass sColumns
    keys = columnIndexNameMap.keys()
    keys.sort()
    colitems = [columnIndexNameMap[key] for key in keys]
    sColumns = ",".join(map(str,colitems))#
    #看哪些column可以search
    searchableColumns = []
    for col in range(0,cols):
        if request.GET.get('bSearchable_{0}'.format(col), False) == 'true': searchableColumns.append(columnIndexNameMap[col])
    #or search
    customSearch = request.GET.get('sSearch', '').rstrip().encode('utf-8');
    if customSearch != '':
        outputQ = None
        first = True
        tmporfilters = list()
        for searchableColumn in searchableColumns:
            if searchableColumn=="id": searchableColumn="_id"
            tmporfilters.append({searchableColumn:{'$regex':"%s"%customSearch}})
        if handle_user:
            tmporfilters.append({searchableColumn:{'$regex':"%s"%customSearch}})
        filterdict["$or"] = tmporfilters


    # #and search 
    outputQ = None
    for col in range(0,cols):
        if request.GET.get('sSearch_{0}'.format(col), False) > '':
            filterdict[columnIndexNameMap[col]] = request.GET['sSearch_{0}'.format(col)]


    ######################################参数解析过程################################################
    querySet = DBMODEL.objects.raw_query(filterdict)#本页内容切片
    # #Ordering data
    iSortingCols =  int(request.GET.get('iSortingCols',0))#根据几columns进行排序
    asortingCols = []

    if iSortingCols:
        for sortedColIndex in range(0, iSortingCols):
            sortedColID = int(request.GET.get('iSortCol_'+str(sortedColIndex),0))
            if request.GET.get('bSortable_{0}'.format(sortedColID), 'false')  == 'true':  #判断是否可以sort
                sortedColName = columnIndexNameMap[sortedColID]
                if handle_user:######根据用户realname进行排序#######
                    if sortedColName == 'user_id':
                        sortedColName = 'user'
                sortingDirection = request.GET.get('sSortDir_'+str(sortedColIndex), 'asc')
                if sortingDirection == 'desc':
                    sortedColName = '-'+sortedColName
                if sortedColName == "id":
                    asortingCols.append('-'+dt)
                else:
                    asortingCols.append(sortedColName)
        querySet = querySet.order_by(*asortingCols)
    iTotalRecords = iTotalDisplayRecords = querySet.count() #总共的rows数
    querySet = querySet[startRecord:endRecord] #本页内容切片
    sEcho = int(request.GET.get('sEcho',0)) #页数

    # querySet = querySet.order_by('-'+dt)

    if jsonTemplatePath:
        jstonString = render_to_string(jsonTemplatePath, locals()) 
        response = HttpResponse(jstonString, mimetype="application/javascript")
    else:
        aaData = []
        a = querySet.values() 
        for row in a:
            rowkeys = row.keys()
            rowvalues = row.values()
            rowlist = []
            for col in range(0,len(colitems)):
                for idx, val in enumerate(rowkeys):
                    if val == colitems[col]:
                        if isinstance(rowvalues[idx],datetime):
                            rowvalues[idx] = rowvalues[idx].strftime('%Y-%m-%d %H:%M:%S') 
                        #使用unicode原因是为了处理int,long,和unicode类型的中文问题,此处使用str，若遇到unicode中文会出错
                        rowlist.append(unicode(rowvalues[idx]))
            aaData.append(rowlist)
    # endtime = time.time()
    ######################################提取json中的数据集################################################
    # endtime = time.time()
    return (aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns)


def get_datatables_records_mysql(request, querySet, columnIndexNameMap, jsonTemplatePath = None,extrafilters={},handle_user=False, *args):

    ######################################参数解析过程################################################
    cols = int(request.GET.get('iColumns',0)) #获取有多少列数据
    iDisplayLength = min(int(request.GET.get('iDisplayLength',10)),100)     #每页获取rows个数
    startRecord = int(request.GET.get('iDisplayStart',0)) #本页第一条数据，是所有数据的第几个,从0开始
    endRecord = startRecord + iDisplayLength  
    
    #Pass sColumns
    keys = columnIndexNameMap.keys()
    keys.sort()
    colitems = [columnIndexNameMap[key] for key in keys]
    sColumns = ",".join(map(str,colitems))#
    
    #Ordering data
    iSortingCols =  int(request.GET.get('iSortingCols',0))#根据几columns进行排序
    asortingCols = []

    if iSortingCols:
        for sortedColIndex in range(0, iSortingCols):
            sortedColID = int(request.GET.get('iSortCol_'+str(sortedColIndex),0))
            if request.GET.get('bSortable_{0}'.format(sortedColID), 'false')  == 'true':  #判断是否可以sort
                sortedColName = columnIndexNameMap[sortedColID]
                if handle_user:######根据用户realname进行排序#######
                    if sortedColName == 'user_id':
                        sortedColName = 'user'
                sortingDirection = request.GET.get('sSortDir_'+str(sortedColIndex), 'asc')
                if sortingDirection == 'desc':
                    sortedColName = '-'+sortedColName
                asortingCols.append(sortedColName) 
        querySet = querySet.order_by(*asortingCols)

    #看哪些column可以search
    searchableColumns = []
    for col in range(0,cols):
        if request.GET.get('bSearchable_{0}'.format(col), False) == 'true': searchableColumns.append(columnIndexNameMap[col])

    #or search
    customSearch = request.GET.get('sSearch', '').rstrip().encode('utf-8');

    if customSearch != '':
        outputQ = None
        first = True
        if settings.DATABASES["default"]['ENGINE'] == "django_mongodb_engine":
            print "django_mongodb_engine"
        else:
            for searchableColumn in searchableColumns:
                kwargz = {searchableColumn+"__icontains" : customSearch}
                outputQ = outputQ | Q(**kwargz) if outputQ else Q(**kwargz)
            if extrafilters:
                for k,v in extrafilters.items():
                    for i in [real for real,mapping in v if customSearch in mapping]:
                        kwargz = {k+'__iexact':i}
                        outputQ = outputQ | Q(**kwargz) if outputQ else Q(**kwargz)
                        
            #####################handle user or filter####################
            if handle_user:
                kwargz = {'user__realname__icontains':customSearch}
                outputQ = outputQ | Q(**kwargz)
            querySet = querySet.filter(outputQ)
    
    #and search 
    outputQ = None
    for col in range(0,cols):
        if request.GET.get('sSearch_{0}'.format(col), False) > '':
            kwargz = {columnIndexNameMap[col]+"__iexact" : request.GET['sSearch_{0}'.format(col)]}
            outputQ = outputQ & Q(**kwargz) if outputQ else Q(**kwargz)
    if outputQ: 
        querySet = querySet.filter(outputQ)

    ######################################参数解析过程################################################
        
    ######################################提取json中的数据集################################################

    iTotalRecords = iTotalDisplayRecords = querySet.count() #总共的rows数
    querySet = querySet[startRecord:endRecord] #本页内容切片
    sEcho = int(request.GET.get('sEcho',0)) #页数
    
    if jsonTemplatePath:
        jstonString = render_to_string(jsonTemplatePath, locals()) 
        response = HttpResponse(jstonString, mimetype="application/javascript")
    else:
        aaData = []
        a = querySet.values() 
        for row in a:
            rowkeys = row.keys()
            rowvalues = row.values()
            rowlist = []
            for col in range(0,len(colitems)):
                #print "col",col
                for idx, val in enumerate(rowkeys):
                    #print "idx,val",idx,val
                    if val == colitems[col]:
                        #print "val,collections",val,colitems[col]
                        if isinstance(rowvalues[idx],datetime):
                            #print "rowvalues[idx]",rowvalues[idx]
                            rowvalues[idx] = rowvalues[idx].strftime('%Y-%m-%d %H:%M:%S')
                            #print "rowvalues[idx]1111",rowvalues[idx]
                        #使用unicode原因是为了处理int,long,和unicode类型的中文问题,此处使用str，若遇到unicode中文会出错
                        rowlist.append(unicode(rowvalues[idx]))
            aaData.append(rowlist)

    ######################################提取json中的数据集################################################

    return (aaData,sEcho,iTotalRecords,iTotalDisplayRecords,sColumns)
