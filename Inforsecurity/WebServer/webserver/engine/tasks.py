#!/usr/bin/python
#-*-coding:utf-8-*-

from django.conf import settings
from django.core.mail import send_mail


from celery.task.schedules import crontab  
from celery.decorators import periodic_task  
from celery import task

from engine.models import Userinfo,ResUrl,ResEmail,ResIp,\
					BlackEmail,BlackIp,BlackUrl,UserPC,PcAssess,AlarmList,AlarmPre
from bson.objectid import ObjectId
import time,datetime
from urlparse import urlparse

from engine.utils import gen_random_pwd
import os


def emailvalue():
	for i in ResEmail.objects.raw_query({"riskvalue":-1}):
		emailtolist = list()
		emailtolist+=[email for email in i.sendto.split(";") if email.find("@")!=-1]
		emailtolist+=[email for email in i.sendcc.split(";") if email.find("@")!=-1]
		emailtolist+=[email for email in i.sendbcc.split(";") if email.find("@")!=-1]
		for email in emailtolist:
			try:
				blackemail = BlackEmail.objects.get(blackemail=email)
				i.riskvalue = blackemail.riskvalue
				if i.riskvalue>=i.user.emailalarmvalue:
					alarmdata = AlarmList(user=i.user,riskvalue=i.riskvalue,blackdata=email,datatype="2",datapk_id=i.pk)
					alarmdata.save()
				break
			except:
				i.riskvalue = 0
		i.save()


def ipvalue():
	for i in ResIp.objects.raw_query({"riskvalue":-1}):
		try:
			blackip = BlackIp.objects.get(blackip =i.suspiciousip)
			i.riskvalue = blackip.riskvalue
			i.save()
			if i.riskvalue>=i.user.ipalarmvalue:
				alarmdata = AlarmList(user=i.user,riskvalue=i.riskvalue,blackdata=i.suspiciousip,datatype="0",datapk_id=i.pk)
				alarmdata.save()
		except:
			i.riskvalue = 0
			i.save()

def urlvalue():
	for i in ResUrl.objects.raw_query({"riskvalue":-1}):
		host = urlparse(i.url).netloc
		blackurl = BlackUrl.objects.raw_query({"blackurl":{'$regex':host}})
		if len(blackurl):
			blackurl = blackurl[0]
			i.riskvalue = blackurl.riskvalue
			i.save()
			if i.riskvalue>=i.user.urlalarmvalue:
				alarmdata = AlarmList(user=i.user,riskvalue=i.riskvalue,blackdata=i.url,datatype="1",datapk_id=i.pk)
				alarmdata.save()
		else:
			i.riskvalue = 0
			i.save()


def machinevalue():
	allpcs = UserPC.objects.all()
	try:
		lastupdate = PcAssess.objects.order_by("-datetime")[0].datetime
		lastupdate = lastupdate - datetime.timedelta(seconds=lastupdate.second)
	except:
		lastupdate = datetime.datetime.now()

	nowtime = datetime.datetime.now()
	nowtime = nowtime - datetime.timedelta(seconds=nowtime.second)

	for i in range((nowtime-lastupdate).seconds/60+1):
		currtime = lastupdate + datetime.timedelta(minutes=i)
		totime = currtime + datetime.timedelta(minutes=1)
		for pc in allpcs:
			try:
				ipriskvalue = ResIp.objects.raw_query({"pc_id":ObjectId(pc.id),
									"riskvalue":{"$ne":-1},
									"begintime":{"$gt":currtime,"$lt":totime}}).order_by("-riskvalue")[0].riskvalue
			except:
				ipriskvalue = 0
			try:
				urlriskvalue = ResUrl.objects.raw_query({"pc_id":ObjectId(pc.id),
									"riskvalue":{"$ne":-1},
									"datetime":{"$gt":currtime,"$lt":totime}}).order_by("-riskvalue")[0].riskvalue
			except:
				urlriskvalue = 0
			try:
				emailriskvalue = ResEmail.objects.raw_query({"pc_id":ObjectId(pc.id),
									"riskvalue":{"$ne":-1},
									"datetime":{"$gt":currtime,"$lt":totime}}).order_by("-riskvalue")[0].riskvalue
			except:
				emailriskvalue = 0

			curr_riskvalue = urlriskvalue if urlriskvalue-ipriskvalue else ipriskvalue
			curr_riskvalue = curr_riskvalue if curr_riskvalue-emailriskvalue else emailriskvalue
			assess = PcAssess(user=pc.user,pc=pc,datetime=currtime,riskvalue=curr_riskvalue)
			assess.save()

#@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*")) 	
#def run():
#	emailvalue()
#	ipvalue()
#	urlvalue()
#	machinevalue()

@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def checkalarm():

	userlist = {}
	subject = "风险提醒"

	for item in AlarmList.objects.raw_query({"isfigured":False}):
		if item.user not in userlist.keys():
			userlist[item.user] = 1
		else:
			userlist[item.user] += 1
		item.isfigured = True
		item.save()

	for user in userlist:
		sendstr = body = "您的机器存在风险，共有%d条风险记录。"%userlist[user]		
		if settings.IFEMSMODEL:
			sendsms.delay(user.mobile,sendstr)
		sendemail.delay(subject,body,[user.email])

	return True

@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def checkalarmpre():
	userlist = {}
	subject = "风险提醒"

	for item in AlarmPre.objects.raw_query({"isalarmed":False}):
		user = item.user
		sendstr = body = "预警提示:您所在组内有人访问黑名单中的%s"%item.datacontent
		try:
			mobile = user.mobile
			if settings.IFEMSMODEL:
				sendsms.delay(user.mobile,sendstr)
		except:
			pass
		sendemail.delay(subject,body,[user.email])
		item.isalarmed = True
		item.save()
	return True


@task()
def generate_ca(userid):

	user = Userinfo.objects.raw_query({"_id":ObjectId(userid)})
	if not len(user):
		return
	user = user[0]
	email = user.email
	mobile = user.mobile

	ca_pwd = gen_random_pwd(10)
	export_pwd = gen_random_pwd(10)
	commonName = "user:%s"%user.user.username

	staticdirpath = os.path.join(settings.PROJECT_ROOT,"static")
	CAdirpath = os.path.join(staticdirpath,"CA")

	if not os.path.exists(CAdirpath):
		os.mkdir(CAdirpath)
	
	userdirpath = os.path.join(CAdirpath,userid)

	if os.path.exists(userdirpath):
		os.system("rm -rf %s"%userdirpath)
	os.mkdir(userdirpath)

	ca_crt_path = os.path.join(CAdirpath,"ca.crt")
	setup_exe_path = os.path.join(CAdirpath,"Setup.exe")
	client_key_path = os.path.join(userdirpath,"client.key")
	client_csr_path = os.path.join(userdirpath,"client.csr")
	client_crt_path = os.path.join(userdirpath,"client.crt")
	client_pfx_path = os.path.join(userdirpath,"client.pfx")
	password_txt_path = os.path.join(userdirpath,"password.txt")
	addreg_reg_path = os.path.join(userdirpath,"addreg.bat")
	cakey_pem_path = os.path.join(CAdirpath,"demoCA/private/cakey.pem")
	cacert_pem_path = os.path.join(CAdirpath,"demoCA/cacert.pem")

	# os.system("rm -rf client.key client.csr client.crt client.pfx")
	commandGenrsa = "openssl genrsa -out %s -des3 -passout pass:%s 4096"%(client_key_path,ca_pwd)
	commandReq = "openssl req -new -key %s -out %s -passin pass:%s -subj \
/countryName=cn\
/stateOrProvinceName=cn\
/organizationName=cn\
/organizationalUnitName=cn\
/commonName=%s\
/emailAddress=%s"%(client_key_path,client_csr_path,ca_pwd,commonName,email)

	commandCa = "openssl ca -in %s -out %s -passin pass:123456\
 -batch -keyfile %s -cert %s"%(client_csr_path,client_crt_path,cakey_pem_path,cacert_pem_path)

	commandPfx = "openssl pkcs12 -passin pass:%s \
-export -clcerts -in %s -inkey %s \
-out %s  -passout pass:%s "%(ca_pwd,client_crt_path,client_key_path,client_pfx_path,export_pwd)

	# print "commandGenrsa",commandGenrsa
	os.system(commandGenrsa)
	# print "commandReq",commandReq
	os.system(commandReq)
	# print "commandCa",commandCa
	os.system(commandCa)
	# print "commandPfx",commandPfx
	os.system(commandPfx)

	addregstr = open(os.path.join(CAdirpath,"addreg.template")).read().replace("#USER#",userid)
	addregstr = addregstr.replace("#PWD#",export_pwd)
	open(addreg_reg_path,"w").write(addregstr)

	open(password_txt_path,"w").write(export_pwd)

	ca_zip_path = os.path.join(userdirpath,"setup.zip")
	zipcmd = "zip  -j %s %s %s %s %s %s"%(ca_zip_path,
		addreg_reg_path,
		client_pfx_path,
		ca_crt_path,
		password_txt_path,
		setup_exe_path)

	# print "zipcmd",zipcmd
	os.system(zipcmd)

	# msg = "your password is: "+export_pwd
	user.export_pwd = export_pwd
	user.userstatus = "1"
	user.save()
	# if mobile:
	# 	# sendsms(mobile,msg)
	# 	self.insert_CA_info(userid,ca_pwd,export_pwd,1)
	# else:
	# 	self.insert_CA_info(userid,ca_pwd,export_pwd,0)

@task()
def sendsms(mobile,sendstr):
	command = "echo -n \"%s\" | gnokii --sendsms %s > /dev/null"%(sendstr,mobile)
	os.system(command)
	return True

@task()
def sendemail(subject,body,tolist):
	try:
		send_mail(subject,body,settings.EMAIL_HOST_USER,tolist,fail_silently=True)
		return True
	except:
		return False


