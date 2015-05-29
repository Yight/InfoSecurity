#!/usr/bin/python
#-*-coding:utf-8-*-
import pymongo
import time,datetime
import traceback
import logging
import os
from urlparse import urlparse
from bson.objectid import ObjectId

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getuserbyid(userid):
	users = db.userinfo.find({"_id":userid})
	if users.count()>0:
		return users[0]
	else:
		return None
	
def alarmlist(db,logger):
	#search the lastest updatetime
	print('alarmpre begin')
	logger.info("alarmpre begin")
	blackdict = {}
	for i in db.alarmlist.find():
		if(i['datatype']== '1'):
			blackkey = urlparse(i['blackdata']).netloc 
		else:
			blackkey = i['blackdata']
		user = getuserbyid(i["user_id"])
		print "--------------begin----------------------"
		if not user["workplace"]:
			continue
		for user in db.userinfo.find({"job_id":user["job_id"],	
							"workplace":user["workplace"],
							"user_id":{"$ne":i["user_id"]}
			}):
			res = db.alarmpre.find({"user_id":user["_id"],"datacontent":blackkey,"datatype":i['datatype']})
			if res.count()==0:
				print user["realname"]
				print "-------------------insert---------------------"
				insertdata = {'user_id': ObjectId(user["_id"]),'datacontent':blackkey,
											'isalarmed': False, 'datatype': i['datatype'],
											'insert_time':datetime.datetime.now()}
				print "insertdata",insertdata
				db.alarmpre.insert(insertdata)
		print "--------------end----------------------"

			# print i["realname"]
		# db.alarmpre.find({"datatype":i['datatype'],})


	# 	if blackkey in blackdict:
	# 		if i['user_id'] not in blackdict[blackkey]["users"]:
	# 			blackdict[blackkey]["users"].append(i['user_id'])
	# 	else:
	# 		alarmdict = dict()
	# 		alarmdict["users"] = [i['user_id']]
	# 		alarmdict["datatype"] = i['datatype']
	# 		blackdict[blackkey] = alarmdict

	# for i in blackdict:
	# 	print i,blackdict[i]

	# #print blackdict
	# #print blackdict build userinfodict
	# userinfodict = {}
	# Subkey = ''
	# for i in db.userinfo.find():
	# 	if(i['workplace'] in userinfodict):
	# 		for j in db.job.find({'_id': i['job_id']}):
	# 			if(j['pid_id']!=None):
	# 				for k in db.job.find({'_id': j['pid_id']}):
	# 					Subkey = k['name']
	# 			else:
	# 				Subkey = j['name']
	# 			if(Subkey in userinfodict[i['workplace']]):
	# 				userinfodict[i['workplace']][Subkey].append(i['_id'])
	# 			else:
	# 				userinfodict[i['workplace']][Subkey] = [i['_id']]
	# 	else:
	# 		for j in db.job.find({'_id': i['job_id']}):
	# 			if(j['pid_id']!=None):
	# 				for k in db.job.find({'_id': j['pid_id']}):
	# 					Subkey = k['name']
	# 			else:
	# 				Subkey = j['name']
	# 			userinfodict[i['workplace']]={Subkey:[i['_id']]}
	# #print userinfodict
	# for i in blackdict:
	# 	blackset = set(blackdict[i])
	# 	for j in userinfodict:
	# 		for k in userinfodict[j]:
	# 			userset = set(userinfodict[j][k])
	# 			resset = userset & blackset
	# 			if(len(resset)>0):
	# 				for m in userset:
	# 					content = "您所在组内有人访问黑名单中的"+i
	# 					sign = 1
	# 					for n in db.alarmpre.find({'user_id': ObjectId(m),'blackdata': i}):
	# 						sign = 0
	# 					if(sign):
	# 						db.alarmpre.insert({'user_id': ObjectId(m),'rank': '1','content':content,
	# 										'suggestion': '请注意保护组织内部隐私',
	# 										'isalarmed': False, 'blackdata': i,'datatype': '0',
	# 										'insert_time':datetime.datetime.now()})
	# 						print "insert alarmpre"
	# 						logger.info("insert alarmpre")
						
	# #insert the lastest time
	# print('alarmlist end')
	# logger.info("alarmlist end")


def emailvalue(db,logger):
	print('email begin')
	logger.info("email begin")
	blackemaildict = {}
	userinfodict = {}
	for blackemail in db.black_email.find():
		blackemaildict[blackemail['blackemail']] = blackemail['riskvalue']
	for res_userinfo in db.userinfo.find():
		userinfodict[res_userinfo['_id']] = {'emailalarmvalue': res_userinfo['emailalarmvalue']}
	for i in db.res_email.find({'riskvalue':-1}):
		i['riskvalue']=0
		emailtolist = list()
		emailtolist+=[email for email in i['sendto'].split(";") if email.find("@")!=-1]
		emailtolist+=[email for email in i['sendcc'].split(";") if email.find("@")!=-1]
		emailtolist+=[email for email in i['sendbcc'].split(";") if email.find("@")!=-1]
		for email in emailtolist:
			try:
				if email in blackemaildict:
					if i['user_id'] in userinfodict: 
						if(blackemaildict[email]>= userinfodict[i['user_id']]['emailalarmvalue']):
							db.alarmlist.insert({'user_id': i['user_id'], 'riskvalue': blackemaildict[email], 
												'blackdata': email, 'datatype': '2', 'datapk_id': i['_id']})
							print 'insert email alarminfo'
							logger.info("insert email alarminfo")
					if blackemaildict[email]>i['riskvalue']:
						i['riskvalue'] = blackemaildict[email]
			except:
				currenttime = datetime.datetime.now()
				logger.error(currenttime.strftime("%Y-%m-%d %H:%M:%S"))
				logger.error(traceback.print_exc())
				i['riskvalue'] = 0
		db.res_email.update({'_id': i['_id']}, i)
	print('email end')
	logger.info("email end")

def ipvalue(db,logger):
	print('ip begin1')
	logger.info("ip begin")
	count = 0
	blackipdict = {}
	userinfodict = {}
	for blackip in db.black_ip.find():
		blackipdict[blackip['blackip']] = blackip['riskvalue']
	for res_userinfo in db.userinfo.find():
		userinfodict[res_userinfo['_id']] = {'ipalarmvalue': res_userinfo['ipalarmvalue']}

	collections =  list(db.res_ip.find({"riskvalue":-1}))+ \
 						list(db.net_behaviour.find({"riskvalue":-1,"appprotc":"IP"}))

	for i in collections:
		# print "start",datetime.datetime.now()
		# print i
		print 'in circle'
		i['riskvalue'] = 0
		try:
			print 'in try'
			if i['flow'] == '0':
				findip = i['dip']
			else:
				findip = i['sip']
			print "findip",findip
			print blackipdict
			try:
				if findip in blackipdict:
					print 'in findip'
					i['riskvalue'] = blackipdict[findip]
					if i['user_id'] in userinfodict:
						if i['riskvalue']>=userinfodict[i['user_id']]['ipalarmvalue']:
							db.alarmlist.insert({'user_id': i['user_id'], 'riskvalue': i['riskvalue'], 
											'blackdata': findip, 'datatype': '0', 'datapk_id': i['_id']})
							print 'insert ip alarminfo'
							logger.info("insert ip alarminfo")
			except:
				traceback.print_exc()
			print 'end if'
		except:

			traceback.print_exc()
			currenttime = datetime.datetime.now()
			logger.error(currenttime.strftime("%Y-%m-%d %H:%M:%S"))
			looger.error(traceback.print_exc())
			traceback.print_exc()
			i['riskvalue'] = 0
		print "riskvalue",i["riskvalue"]
		if "appprotc" in i:
			db.net_behaviour.update({'_id': i['_id']}, {"$set":{"riskvalue":i['riskvalue']}})	
		else:
			db.res_ip.update({'_id': i['_id']}, {"$set":{"riskvalue":i['riskvalue']}})	
		print 'end circle'
	print('ip end')
	logger.info('ip end')

def urlvalue(db,logger):
	print('url begin1')
	logger.info('url begin')
	userinfodict = {}
	for res_userinfo in db.userinfo.find():
		userinfodict[res_userinfo['_id']] = {'urlalarmvalue': res_userinfo['urlalarmvalue']}

	collections =  list(db.res_url.find({'riskvalue': -1}))+ \
						list(db.net_behaviour.find({"riskvalue":-1,"appprotc":"http"}))
	for i in collections:
		i['riskvalue'] = 0
		if "appprotc" in i:
			url = i["content"]
		else:
			url = i["url"]
		host = urlparse(url).netloc
		blackurl = db.black_url.find({'blackurl': {'$regex': host}})
		if blackurl.count(True)>0:
			blackurl = blackurl[0]
			i['riskvalue'] = blackurl['riskvalue']
			#for res_userinfo in db.userinfo.find({'_id': i['user_id']}):
			if i['user_id'] in userinfodict:
				if i['riskvalue']>=userinfodict[res_userinfo['_id']]['urlalarmvalue']:
					db.alarmlist.insert(
						{
							'user_id': i['user_id'], 
							'riskvalue': i['riskvalue'], 
							'blackdata': url, 
							'datatype': '1', 
							'datapk_id': i['_id']})
					print('insert url alarminfo')
					logger.info("insert url alarminfo")
		else:
			i['riskvalue'] = 0
		if "appprotc" in i:
			db.net_behaviour.update({'_id': i['_id']}, i)
		else:
			db.res_url.update({'_id': i['_id']}, i)
	print('url end')
	logger.info('url end')


def machinevalue(db,logger):
	print('machinevalue begin')
	logger.info('machinevalue begin')
	try:
		datelist = db.pc_assess.distinct('datetime')
		datelist.sort(reverse = True)
		lastupdate = datelist[0] - datetime.timedelta(seconds=datelist[0].second)-datetime.timedelta(microseconds= datelist[0].microsecond)
	except:
		currenttime = datetime.datetime.now()
		logger.error(currenttime.strftime("%Y-%m-%d %H:%M:%S"))
		logger.error(traceback.print_exc())
		lastupdate = datetime.datetime.now()

	nowtime = datetime.datetime.now()
	nowtime = nowtime - datetime.timedelta(seconds=nowtime.second)-datetime.timedelta(microseconds = nowtime.microsecond)

	#print (nowtime-lastupdate).seconds/60+1+(nowtime-lastupdate).days*24*60*60
	userpcdict = {}
	riskvaluedict = {}
	for pc in db.userpc.find():
		userpcdict[pc['_id']]=pc['user_id']
	
	collection_list = (db.res_ip,db.res_url,db.res_email)
	print lastupdate
	print nowtime

	for collection in collection_list:
		print('collection begin')
		try:
			for i in collection.find({'riskvalue': {'$ne':-1},'datetime':{'$gt':lastupdate,'$lt': nowtime}}):
				colldatetime = i['datetime'] - datetime.timedelta(seconds = i['datetime'].second) - datetime.timedelta(microseconds= i['datetime'].microsecond)
				colldatetime = colldatetime+datetime.timedelta(minutes=1)
				if i['pc_id'] in riskvaluedict:
					if colldatetime in riskvaluedict[i['pc_id']]:
					 	if riskvaluedict[i['pc_id']][colldatetime]<i['riskvalue']:
					 		riskvaluedict[i['pc_id']][colldatetime] = i['riskvalue']
					else:
						riskvaluedict[i['pc_id']][colldatetime] = i['riskvalue']
				else:
					riskvaluedict[i['pc_id']]= {colldatetime: i['riskvalue']}
		except:
			traceback.print_exc()
		print('collection end')
	try:
		for i in riskvaluedict:
			for j in riskvaluedict[i]:
				db.pc_assess.insert({'pc_id':i, 'user_id': userpcdict[i], 'datetime': j, 'riskvalue': riskvaluedict[i][j]})
				print 'insert pc_assess'
				logger.info('insert pc_assess')
	except:
		traceback.print_exc()
	print('machinevalue end')
	logger.info('machinevalue end')

def run(db):
	logger = logging.getLogger()
	handler = logging.FileHandler('/var/log/crontasks.log')
	logger.addHandler(handler)
	logger.setLevel(logging.NOTSET)
	#logger.info("running net_behaviour")
	#netbehaviour(db,logger)
	logger.info("running emailvalue")
	emailvalue(db,logger)
	logger.info("running ipvalue")
	ipvalue(db,logger)
	logger.info("running urlvalue")
	urlvalue(db,logger)
	logger.info("running machinevalue")
	machinevalue(db,logger)
	logger.info("running alarmlist")
	alarmlist(db,logger)
	logger.info("end")


if __name__ == '__main__':

	pidfile = "/etc/init.d/crontask.pid"
	try:
		lastpid = open(pidfile).read()
		if os.path.exists("/proc/%s"%lastpid):
			print "last process is still run!"
			sys.exit(-1)
		else:
			open(pidfile,"w").write(str(os.getpid()))
			conn = pymongo.Connection('192.168.0.234', 27017)
			db = conn.InfoSecurity
			run(db)
			conn.disconnect()
	except:
		traceback.print_exc()
	#collection = db.pc_assess
	#datelist = collection.distinct('datetime')
	#datelist.sort(reverse = True)
	#print(datetime.timedelta(seconds=datelist[0].second))
	#nowtime = datetime.datetime.now()
	#print(nowtime)
	#nowtime = nowtime - datetime.timedelta(seconds=nowtime.second)
	#print(nowtime)
	#print("hello world")
