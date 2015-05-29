#!/usr/bin/python
#-*- coding:utf-8 -*-

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils import simplejson

from engine.forms import ResetPwdForm,RegisterForm,UpdateUserinfoForm
from engine.models import Login,Userinfo,Userloginvalid,Job,AlarmList,ResEmail,ResUrl,ResIp
from engine.utils import get_datatables_records, get_highcharts_records,get_highcharts_detail_records
from utils import datestrtsecs

from random import randint
import datetime
import traceback
from bson.objectid import ObjectId
import string
import random
import time
from django.core.mail import send_mail
from datetime import timedelta

from django.conf import settings
from engine.tasks import sendsms


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def user_login_post(request):
    error = False
    print "--------------------++++--------------------"
    loginfo = "请输入有效信息"
    username = request.POST['username']
    password = request.POST['password']
    validvalue = request.POST['validvalue']
    if User.objects.filter(username=username):
        if validvalue: 
            user = authenticate(username=username, password=password)
            if user is not None:
                userinfo = Userinfo.objects.get(user = user)
                if userinfo.ifverify:
                    validvaluedb = Userloginvalid.objects.get(user=userinfo).validvalue
                    try:
                        if validvaluedb==int(validvalue):
                            login(request, user)
                            userinfo = Userinfo.objects.get(user=user)
                            loginobj = Login(user=userinfo,userip=get_client_ip(request))
                            loginobj.save()
                            return HttpResponseRedirect('/')
                        else:
                            error = True
                            loginfo = "验证码错误"
                            return render_to_response('accounts/login.html',{"loginfo":loginfo,"error":error},context_instance = RequestContext(request))
                    except:
                        error = True
                        loginfo = "验证码错误"
                        return render_to_response('accounts/login.html',{"loginfo":loginfo,"error":error},context_instance = RequestContext(request))
                else:
                    error = True
                    loginfo = "抱歉，用户还没激活"
                    return render_to_response('accounts/login.html',{"loginfo":loginfo,"error":error},context_instance = RequestContext(request))
            else:
                error = True
                loginfo = "用户名或密码错误"
                return render_to_response('accounts/login.html',{"loginfo":loginfo,"error":error},context_instance = RequestContext(request))
        else:
            error = True
            loginfo = "请输入验证码"
            render_to_response('accounts/login.html',{"loginfo":loginfo,"error":error},context_instance = RequestContext(request))
    else:
        error = True
        loginfo = "用户名不存在!"
        render_to_response('accounts/login.html',{"loginfo":loginfo,"error":error},context_instance = RequestContext(request))
    return render_to_response('accounts/login.html',{"loginfo":loginfo,"error":error},context_instance = RequestContext(request))

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    return render_to_response('accounts/login.html',None,context_instance = RequestContext(request))

@login_required
def reset_password(request):
    if request.method == "GET":
        return render_to_response('accounts/resetpwd.html',{"title":"密码修改"},context_instance = RequestContext(request))
    elif request.method == "POST":
        form = ResetPwdForm(request=request,data=request.POST)
        if form.is_valid():
            form = form.cleaned_data
            infodict = {} 
            if not request.user.check_password(form["oripwd"]):
                infodict["messagetype"] = "error"
                infodict["message"] = "please input the right pass!"
                infodict["title"] = "密码修改"
                return render_to_response('accounts/resetpwd.html',infodict,context_instance = RequestContext(request))        
            else:
                request.user.set_password(form["newpwd1"])
                request.user.save()
                infodict["messagetype"] = "success"
                infodict["message"] = "ok!"
                infodict["title"] = "密码修改"
                return render_to_response('accounts/resetpwd.html',infodict,context_instance = RequestContext(request))        
        else:
            infodict = {}
            infodict["messagetype"] = "error"
            infodict["message"] = "please input the right parms!"
            infodict["title"] = "密码修改"
            return render_to_response('accounts/resetpwd.html',infodict,context_instance = RequestContext(request))
            

def fogetpwd(request):
    try:
        temp = dict()
        username = request.GET["username"]
        user = User.objects.get(username = username)
        question = Userinfo.objects.get(user=user).question
        temp["username"] = username
        temp["question"] = question
        return render_to_response('accounts/refindpwd.html',{"temp":temp},context_instance = RequestContext(request))
    except:
        return HttpResponseRedirect('/accounts/login/')

def refindpwd(request):
    temp = dict()
    temp["username"] = request.POST["username"]
    temp["email"] = request.POST["email"]
    temp["mobile"] = request.POST["mobile"]
    temp["answer"] = request.POST["answer"]
    temp["question"] = request.POST["question"]
    temp["status"] = False
    user = User.objects.get(username = temp["username"])
    if user is not None:
        
#        mail = "hyqdream336@163.com"
#        mailto_list=["414793925@qq.com"]
#        #####################
#        #设置服务器，用户名、口令以及邮箱的后缀
#        mail_host="smtp.163.com"
#        mail_user="hyqdream336"
#        mail_pass="hyq0820^(!$"
#        mail_postfix="163.com"
#        content = "content"
#        sub = "sub"
#        
#        to_list = mailto_list
#        
#        me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
#        msg = MIMEText(content)
#        msg['Subject'] = sub
#        msg['From'] = me
#        msg['To'] = ";".join(to_list)
#        try:
#            s = smtplib.SMTP()
#            s.connect(mail_host)
#            s.login(mail_user,mail_pass)
#            s.sendmail(me, to_list, msg.as_string())
#            s.close()
#        except Exception, e:
            
        
        try:
            userinfo = Userinfo.objects.get(user=user)
            #生成随机验证码
            allw = string.letters+string.digits
            code = random.sample(allw, 10)
            code = ''.join( [ str(x) for x in code])
            
            user.set_password(code)
            user.save()
            return HttpResponseRedirect('/accounts/login/')
        except:
            temp["status"] = True
            return render_to_response('accounts/refindpwd.html',{"temp":temp},context_instance = RequestContext(request))
#        ,mobile=temp["mobile"],email=temp["email"],answer=temp["answer"]

    return HttpResponseRedirect('/accounts/fogetpwd/?username='+temp["username"])



def sendverifycode(request):
    try: 
        
        username = request.GET["username"]
        code = randint(100000,999999)
        user = User.objects.filter(username = username)
        if len(user)==0:
            return  HttpResponse(simplejson.dumps("该用户不存在"), mimetype='application/json')
        user = User.objects.get(username = username)
        print "00000000000",user
        mobile = Userinfo.objects.raw_query({"user_id":ObjectId(user.id)})[0].mobile
        print mobile
        user = Userinfo.objects.get(user = user)
        newuserloginvalid = Userloginvalid.objects.filter(user = user)
        if newuserloginvalid:
            last_sendtime = Userloginvalid.objects.get(user=user).sendtime
            timepass = (datetime.datetime.now()-last_sendtime).seconds
            if timepass > 10:
                newuserloginvalid = Userloginvalid.objects.get(user = user)
                newuserloginvalid.validvalue = code
                newuserloginvalid.sendtime = datetime.datetime.now()
                newuserloginvalid.save()
            else:
                code="短信发送不可太频繁，请过"+str(10-timepass)+"秒后再发"
                code = simplejson.dumps(code)
                return HttpResponse({code}, mimetype='application/json')
        else:
            newuserloginvalid = Userloginvalid(user=user,sendtime=datetime.datetime.now(),validvalue=code)
            newuserloginvalid.save()

        if settings.IFEMSMODEL:
            sendstr="验证码已以短信发送至您的手机%s,请查收"%(mobile)
            notify = "您的登录验证码是%s"%(code)
            sendsms.delay(mobile,notify)
            sendstr = simplejson.dumps(sendstr)
            return HttpResponse({sendstr}, mimetype='application/json')
        else:
            code = '暂无短信包，验证码为:'+str(code)
            code = simplejson.dumps(code)
            return HttpResponse(code, mimetype='application/json')
    except:
        return HttpResponse({}, mimetype='application/json')
    

def register(request):
    if request.POST:
        success = False
        birthday = False
        pet = False
        fathername = False
        teachername = False
        school = False
        yourself =False
        myquestion = ""
        username = request.POST["username"]
        realname = request.POST["realname"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        telephone = request.POST["telephone"]
        workspace = request.POST["workspace"]
        address = request.POST["address"]
        answer = request.POST["answer"]
        question = request.POST["select_question"]
        custom_question = request.POST["custom_question"]
        if custom_question:
            question = request.POST["custom_question"]
        if question ==u"您的生日是几月几号": birthday = True
        elif question ==u"您最喜欢的宠物的名字": pet = True
        elif question ==u"您父亲的名字": fathername = True
        elif question ==u"您高中老师的名字": teachername = True
        elif question ==u"您的小学是在哪里上的": school = True
        else:
            yourself = True
            myquestion = question
#        以上是用户输入的数据，用以当注册失败时返回到界面显示的数据
        form = RegisterForm(request.POST)
        captcha = form['captcha']
        userexit = False
        if form.is_valid():
            try:
                user_exit = User.objects.get(username = request.POST['username'])
                if user_exit:
                    userexit = True
                    userexitmessage = "用户名已经被使用了"
                    return render_to_response('accounts/register.html',locals(),context_instance = RequestContext(request))
            except:
                form.save()
                success = True
                return render_to_response('accounts/login.html',{"success":success}, context_instance = RequestContext(request))
        else:
            return render_to_response('accounts/register.html',locals(),context_instance = RequestContext(request))
            #return render_to_response('error.html',locals(), context_instance = RequestContext(request))
    else:
        form = RegisterForm()
        captcha = form['captcha']
    return render_to_response('accounts/register.html',locals(),context_instance = RequestContext(request))
    
def changeinfo(request):
    if request.POST:
        birthday = False
        pet = False
        fathername = False
        teachername = False
        school = False
        yourself =False
        myquestion = ""
        username = request.POST["username"]
        realname = request.POST["realname"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        telephone = request.POST["telephone"]
        workspace = request.POST["workspace"]
        address = request.POST["address"]
        top_job = request.POST["top_job"]
        sub_job = request.POST["sub_job"]
        answer = request.POST["answer"]
        question = request.POST["select_question"]
        custom_question = request.POST["custom_question"]
        if custom_question:
            question = request.POST["custom_question"]
        if question ==u"您的生日是几月几号": birthday = True
        elif question ==u"您最喜欢的宠物的名字": pet = True
        elif question ==u"您父亲的名字": fathername = True
        elif question ==u"您高中老师的名字": teachername = True
        elif question ==u"您的小学是在哪里上的": school = True
        else:
            yourself = True
            myquestion = question
#        以上为用户输入的数据，用以在修改失败后返回到界面时显示的数据
        success = False
        fail = False
        form = UpdateUserinfoForm(request.POST)
        if form.is_valid():
            try:
                form.update()
                success = True
                changeinfo = "恭喜您修改信息成功"
                myquestion = ""
                birthday = False
                pet = False
                fathername = False
                teachername = False
                school = False
                yourself =False
                userinfo = Userinfo.objects.get(user = request.user)
                username = request.user
                realname = userinfo.realname
                mobile = userinfo.mobile
                email = userinfo.email
                telephone = userinfo.telephone
                address = userinfo.address
                workspace = userinfo.workplace
                answer = userinfo.answer
                question = userinfo.question
                try:
                    top_job = Job.objects.get(id= userinfo.job.pid_id).name
                except:
                    top_job = userinfo.job.name
                sub_job = userinfo.job.name
                if question ==u"您的生日是几月几号": birthday = True
                elif question ==u"您最喜欢的宠物的名字": pet = True
                elif question ==u"您父亲的名字": fathername = True
                elif question ==u"您高中老师的名字": teachername = True
                elif question ==u"您的小学是在哪里上的": school = True
                else:
                    yourself = True
                    myquestion = question
#                以上为用户修改后的信息，用以当用户修改成功后显示到界面
            except:
                fail = True
                changeinfo = "修改失败"
        else:
            fail = True
            changeinfo = "您有些信息不符合规范"
        return render_to_response('accounts/userinfo.html',locals(),context_instance = RequestContext(request))

    return render_to_response('accounts/userinfo.html',context_instance = RequestContext(request))

def job(request):
    value = ''
    try:
        parentid = request.GET.get('id')
        if parentid is None:
            parentjobs = Job.objects.raw_query({"pid_id":None})
            value = parentjobs.values_list('id','name')
            value = [[str(i[0]),i[1]] for i in value]#i[1]-> u'IT\u7cbe\u82f1',str(i[1])会产生UnicodeEncodeError
        else:
            childrenjobs = Job.objects.raw_query({"pid_id":ObjectId(parentid)})
            value = childrenjobs.values_list('id','name')
            value = [[str(i[0]),i[1]] for i in value]#i[1]-> u'IT\u7cbe\u82f1',str(i[1])会产生UnicodeEncodeError
    except Exception,e:
        traceback.print_exc()

    response_json = {'data':value}
    response =  HttpResponse(simplejson.dumps(response_json), mimetype='application/json')

    return response  

@login_required
def get_user_info(request):
#    以下是用户修改之前的信息，当用户进入修改界面时显示
    myquestion = ""
    birthday = False
    pet = False
    fathername = False
    teachername = False
    school = False
    yourself =False
    userinfo = Userinfo.objects.get(user = request.user)    
    username = request.user
    realname = userinfo.realname
    mobile = userinfo.mobile
    email = userinfo.email
    telephone = userinfo.telephone
    address = userinfo.address
    workspace = userinfo.workplace
    answer = userinfo.answer
    question = userinfo.question
    try:
        top_job = Job.objects.get(id= userinfo.job.pid_id).name
    except:
        top_job = userinfo.job.name
    sub_job = userinfo.job.name
    if question ==u"您的生日是几月几号": birthday = True
    elif question ==u"您最喜欢的宠物的名字": pet = True
    elif question ==u"您父亲的名字": fathername = True
    elif question ==u"您高中老师的名字": teachername = True
    elif question ==u"您的小学是在哪里上的": school = True
    else:
        yourself = True
        myquestion = question
    return render_to_response('accounts/userinfo.html',locals(),context_instance = RequestContext(request))

@login_required
def homepage(request):
    title = "主页"
    starttime = time.time()
    if User.objects.get(username = request.user).is_superuser:
        total_user = Userinfo.objects.count()
        userinfo = Userinfo.objects.get(user=request.user)
        try:
            last_login = Login.objects.filter(user=ObjectId(userinfo.id)).order_by('logintime')[0]
        except:
            last_login = ""
        end = datetime.datetime.now()
        begin = end-timedelta(days=6)
        timedict = dict()
        if begin:
            try:
                timedict["$gt"]= begin
            except Exception,e:
                traceback.print_exc()
        timedict["$lt"] = end
        filterip = dict()
        filterdict = dict()
        filterip["begintime"] = timedict
        filterdict["datetime"] = timedict
        total_ip = ResIp.objects.raw_query(filterip).count()
        total_email = ResEmail.objects.raw_query(filterdict).count()
        total_url = ResUrl.objects.raw_query(filterdict).count()
        endtime = time.time()
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>------------",(endtime-starttime)
        return render_to_response('accounts/adminhomepage.html',locals(),context_instance = RequestContext(request))
    else:
        userinfo = Userinfo.objects.get(user=request.user)
        last_login = Login.objects.filter(user=ObjectId(userinfo.id)).order_by('logintime')[0]
        end = datetime.datetime.now()
        begin = end-timedelta(days=6)
        timedict = dict()
        if begin:
            try:
                timedict["$gt"]= begin
            except Exception,e:
                traceback.print_exc()
        timedict["$lt"] = end
        filterip = dict()
        filterdict = dict()
        filterip["user_id"] = ObjectId(userinfo.id)
        filterip["begintime"] = timedict
        filterdict["datetime"] = timedict
        filterdict["user_id"] = ObjectId(userinfo.id)

        total_ip = ResIp.objects.raw_query(filterip).count()

        # total_ip = ResIp.objects.filter(begintime__range=(begin, end),user_id = ObjectId(userinfo.id))

        userid = Userinfo.objects.get(user=request.user).id
        total_email = ResEmail.objects.raw_query(filterdict).count()
        total_url = ResUrl.objects.raw_query(filterdict).count()
        endtime = time.time()
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",(endtime-starttime)
        return render_to_response('accounts/userhomepage.html',locals(),context_instance = RequestContext(request))
        
@login_required
def get_alarm_count(request):

    starttime = time.time()

    filterdict = dict()
    if User.objects.get(username = request.user).is_superuser == False:
        userinfo = Userinfo.objects.get(user=request.user)
        filterdict["user_id"] =ObjectId(userinfo.id)
    end = datetime.datetime.now() + timedelta(days=1)
    begin = datetime.datetime.now()-timedelta(days=6)
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
            traceback.print_exc()

    if timedict: filterdict["insert_time"] = timedict
    
    columnIndexNameMap = {
        0: 'insert_time', 
    }
    columnNameIndexMap = dict([[v,k] for k,v in columnIndexNameMap.items()])#将columnIndexNameMap的key,value对调
    aaData = get_highcharts_detail_records(AlarmList,columnIndexNameMap,filterdict,'insert_time')
    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d %H")+':00:00')*1000
    redata = []
    alarmdict = dict()
    for i in range(24*7):
        alarmdict[str(tempbegin)]=0
        tempbegin = tempbegin+60*60*1000
    
    for i in aaData:
        hours = i[0]
        alarmdict[str(hours)] += 1
    tempbegin = datestrtsecs(begin.strftime("%Y-%m-%d %H")+':00:00')*1000
    for i in range(24*7):
        tempdata = [0,0]
        tempdata[0]=tempbegin
        tempdata[1]=alarmdict[str(tempbegin)]
        redata.append(tempdata)
        tempbegin = tempbegin+60*60*1000

    endtime = time.time()
    print "=====================================",(endtime-starttime)
    return HttpResponse(simplejson.dumps(redata), 'application/javascript')

@login_required
def get_user_userid(request):
    userinfo = Userinfo.objects.get(user=request.user)
    return HttpResponse(simplejson.dumps(userinfo.id), 'application/javascript')

    
