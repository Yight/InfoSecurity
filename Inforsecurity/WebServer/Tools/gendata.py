#!/usr/bin/env python
#encoding=utf-8

    # user = models.ForeignKey('Userinfo',related_name = 'resip_userid',verbose_name = u'用户id')
    # pc = models.ForeignKey('UserPC',related_name = 'resip_pcid',verbose_name = u'pcid')
    # sip = models.IPAddressField(u'源ip')
    # dip = models.IPAddressField(u'目的ip')
    # sport = models.IntegerField(u'源端口')
    # dport = models.IntegerField(u'目的端口')
    # suspiciousip = models.IPAddressField(u'可疑ip')
    # begintime = models.DateTimeField(u'begin time',default=datetime.datetime.now)
    # endtime = models.DateTimeField(u'end time',default=datetime.datetime.now)
    # riskvalue = models.IntegerField(u'风险值')
    # protocol = models.CharField(u'协议类型',choices = IPPROTOCOL_CHOICES,max_length = 1)
    # iptype = models.CharField(u'类型',choices = RESTYPE_CHOICES,max_length = 3)
    # iswhite = models.BooleanField(u'是否在白名单中')
    # # length = models.IntegerField(u'数据包大小',null=True, blank=True)
    # count = models.IntegerField(u'count')


    # user = models.ForeignKey('Userinfo',related_name = 'resurl_userid',verbose_name = u'用户id')
    # pc = models.ForeignKey('UserPC',related_name = 'resurl_pcid',verbose_name = u'pcid')
    # sip = models.IPAddressField(u'源ip')
    # dip = models.IPAddressField(u'目的ip')
    # sport = models.IntegerField(u'源端口')
    # dport = models.IntegerField(u'目的端口')
    # url = models.URLField(u'URL')
    # datetime = models.DateTimeField(u'发送时间',default=datetime.datetime.now)
    # riskvalue = models.IntegerField(u'风险值')
    # urltype = models.CharField(u'类型',choices = RESTYPE_CHOICES,max_length = 3)
    # iswhite = models.BooleanField(u'是否在白名单中')


# class ResEmail(models.Model):
#     user = models.ForeignKey('Userinfo',related_name = 'resemail_userid',verbose_name = u'用户id')
#     pc = models.ForeignKey('UserPC',related_name = 'resemail_pcid',verbose_name = u'pcid')
#     sip = models.IPAddressField(u'源ip')
#     dip = models.IPAddressField(u'目的ip')
#     sport = models.IntegerField(u'源端口')
#     dport = models.IntegerField(u'目的端口')
#     sendfrom = models.EmailField(u'发送者',max_length=64)
#     sendto = models.TextField(u'接受者',max_length=300)
#     sendcc = models.TextField(u'接受者',max_length=300)
#     sendbcc = models.TextField(u'接受者',max_length=300)
#     datetime = models.DateTimeField(u'发送时间',default=datetime.datetime.now)
#     riskvalue = models.IntegerField(u'风险值')
#     subject = models.CharField(u'主题',max_length=512, null=True)
#     iswhite = models.BooleanField(u'是否在白名单中')
#     emailtype = models.CharField(u'类型',choices = RESTYPE_CHOICES,max_length = 3)


import random 
from django.core.management import setup_environ
import sys
sys.path.append("../webserver")    # django项目所在的目录
import settings
setup_environ(settings)
import datetime

from engine.models import Userinfo,ResIp,ResUrl,ResEmail  # 导入Model
import string

def id_generator(size=6, chars=string.ascii_letters):
	return ''.join(random.choice(chars) for x in range(size))


def main():
	insertcount = 0
	timescount = 1
	while insertcount<10000000:
		for i in ResIp.objects.all():
			ip_sip = "%d.%d.%d.%d"%(random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
			ip_dip = "%d.%d.%d.%d"%(random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
			ip_suspiciousip = ip_sip if random.randint(1,10)%2  else ip_dip
			ip_begintime  = i.begintime+datetime.timedelta(seconds=random.randint(1,100000)*timescount)
			ip_endtime  = ip_begintime+datetime.timedelta(seconds=random.randint(0,20)*timescount)
			ip_count = random.randint(1,100)
			# print sip,dip,suspiciousip,begintime
			ip_protocol = 1 if random.randint(1,10)%2  else 0

			obj = ResIp(user=i.user,pc=i.pc,sip=ip_sip,dip=ip_dip,sport=i.sport,dport=i.dport,
						suspiciousip=ip_suspiciousip,begintime=ip_begintime,endtime=ip_endtime,
						riskvalue=i.riskvalue,protocol=ip_protocol,iptype=i.iptype,
						iswhite=i.iswhite,count=ip_count)
			obj.save()
			# print i.user.realname

			url_datetime  = i.begintime+datetime.timedelta(seconds=random.randint(0,20)*timescount)
			if random.randint(1,10)%2:
				url_sip = "%d.%d.%d.%d"%(random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
				url_dip = "%d.%d.%d.%d"%(random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
			else:
				url_sip = i.sip
				url_dip = i.dip
			url_url = "http://www.%s.com"%(id_generator(size=random.randint(7,20)))
			obj = ResUrl(user=i.user,pc=i.pc,sip=url_sip,dip=url_dip,sport=i.sport,dport=i.dport,
						datetime=url_datetime,riskvalue=i.riskvalue,urltype=0,url=url_url,
						iswhite=i.iswhite)
			obj.save()
			# print url,i.user.realname


			email_datetime  = i.begintime+datetime.timedelta(seconds=random.randint(0,20)*timescount)
			if random.randint(1,10)%2:
				email_sip = "%d.%d.%d.%d"%(random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
				email_dip = "%d.%d.%d.%d"%(random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
			else:
				email_sip = i.sip
				email_dip = i.dip
			email_sendfrom = "%s@163.com"%(id_generator(size=random.randint(5,15)))
			email_sendto = "%s@163.com"%(id_generator(size=random.randint(5,15)))
			email_sendcc = "%s@163.com"%(id_generator(size=random.randint(5,15)))
			email_sendbcc = "%s@163.com"%(id_generator(size=random.randint(5,15)))
			email_subject = "%s"%(id_generator(size=random.randint(30,50)))
			obj = ResEmail(user=i.user,pc=i.pc,sip=email_sip,dip=email_dip,sport=i.sport,dport=i.dport,
						datetime=email_datetime,riskvalue=i.riskvalue,emailtype=0,sendfrom=email_sendfrom,
						sendto=email_sendto,sendcc=email_sendcc,sendbcc=email_sendbcc,subject=email_subject,
						iswhite=i.iswhite)
			obj.save()
			timescount+=1
			insertcount+=1
			print insertcount
		# print locals()

if __name__ == '__main__':
	main()