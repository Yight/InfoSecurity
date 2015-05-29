#!/usr/bin/python
#-*- coding:utf-8 -*-

from django.db import models
import datetime
from django.contrib.auth.models import User
from time import strftime,localtime
from django_mongodb_engine.contrib import MongoDBManager


ALARM_CHOICES = (
    ('00','没告警'),
    ('01','邮件'),
    ('10','短信'),
    ('11','邮件+短信'),
)

DATATYPE_CHOICES = (
    ('0','ip'),
    ('1','http'),
    ('2','email'),
)

RESTYPE_CHOICES = (
    ('0','正常'),
    ('1','可疑'),
    ('2','非法'),
)

IPPROTOCOL_CHOICES = (
    ('0','TCP'),
    ('1','UDP'),
)

RANK_CHOICES = (
    ('1','风险等级1'),
    ('2','风险等级2'),
    ('3','风险等级3'),
    ('4','风险等级4'),
)

TYPE_CHOICES = (
    ('0','木马传输'),
    ('1','非法地址'),
)

VERIFY_CHOICES = (
    ('0','未审核'),
    ('1','通过'),
    ('2','拒绝'),
)
CASTATUS_CHOICES = (
    ('-1','未生成'),
    ('1','已生成'),
)

FLOW_CHOICES = (
    ("0","上行"),
    ("1","下行")
)

class AlarmList(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'alarmlist_userid',verbose_name = u'用户id')
    riskvalue = models.IntegerField(u'风险值')
    blackdata = models.CharField(u'黑名单数据',max_length=256)
    datatype = models.CharField(u'类型',choices = DATATYPE_CHOICES,max_length = 1)
    datapk_id = models.CharField(u'外键id',max_length=24)
    isfigured = models.BooleanField(u'是否已计算',default=False)
    insert_time = models.DateTimeField(u'插入日期',default=datetime.datetime.now)
    objects = MongoDBManager()
    def __unicode__(self):
        return self.user.realname 
    
    class Meta:
        db_table = u'alarmlist'

class Alarminfo(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'alarm_userid',verbose_name = u'用户id')
    rank = models.CharField(u'等级',choices = RANK_CHOICES,max_length = 3)
    content = models.CharField(u'报警内容',max_length=256)
    suggestion = models.CharField(u'报警建议',max_length=256)
    
    def __unicode__(self):
        return self.user.realname + '-'*5 + dict(RANK_CHOICES)[self.rank]
    class Meta:
        db_table = u'alarminfo'

class AlarmPre(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'alarmpre_userid',verbose_name = u'用户id')
    # rank = models.CharField(u'等级',choices = RANK_CHOICES,max_length = 3)
    # "您所在组内有人访问黑名单中的"+content
    datacontent = models.CharField(u'预警内容',max_length=256)
    datatype = models.CharField(u'类型',choices = DATATYPE_CHOICES,max_length = 1)
    # suggestion = models.CharField(u'预警建议',max_length=256)
    isalarmed = models.BooleanField(u'是否预警',default=False)
    insert_time = models.DateTimeField(u'插入日期',default=datetime.datetime.now)
    objects = MongoDBManager()
    def __unicode__(self):
        return self.user.realname + '-'*5 + self.datacontent
    
    class Meta:
        db_table = u'alarmpre'

class BlackEmail(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'blackemail_userid',verbose_name = u'用户id')
    blackemail = models.EmailField(u'邮件地址',max_length=64)
    emailtype = models.CharField(u'地址类型',choices = TYPE_CHOICES,max_length = 1)
    riskvalue = models.IntegerField(u'风险值')
    addtime = models.DateTimeField(u'日期',default=datetime.datetime.now)
    description = models.CharField(u'详细描述',max_length=256,null=True,blank=True)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.blackemail
    
    class Meta:
        db_table = u'black_email'

class BlackIp(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'blackip_userid',verbose_name = u'用户id')
    blackip = models.IPAddressField(u'IP')
    iptype = models.CharField(u'地址类型',choices = TYPE_CHOICES,max_length = 1)
    riskvalue = models.IntegerField(u'风险值')
    addtime = models.DateTimeField(u'日期',default=datetime.datetime.now)
    description = models.CharField(u'详细描述',max_length=256,null=True,blank=True)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.blackip
    class Meta:
        db_table = u'black_ip'

class BlackTrojan(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'blacktrojan_userid',verbose_name = u'用户id')
    name = models.CharField(u'木马名称',max_length=32)
    begin = models.IntegerField(u'开始特征')
    feature = models.TextField(u'特征值')
    addtime = models.DateTimeField(u'日期',default=datetime.datetime.now)
    description = models.CharField(u'详细描述',max_length=256,null=True,blank=True)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = u'black_trojan'

class BlackUrl(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'blackurl_userid',verbose_name = u'用户id')
    blackurl = models.URLField(u'URL')
    urltype = models.CharField(u'地址类型',choices = TYPE_CHOICES,max_length = 1)
    riskvalue = models.IntegerField(u'风险值')
    addtime = models.DateTimeField(u'日期',default=datetime.datetime.now)
    description = models.CharField(u'详细描述',max_length=256,null=True,blank=True)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.blackurl
    
    class Meta:
        db_table = u'black_url'

class Job(models.Model):
    pid = models.ForeignKey('self',verbose_name = '上级工作分类',default=0,blank=True,null=True)
    name = models.CharField(u'工作名称',max_length=11)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.name
    
    class Meta:
        db_table = u'job'

class Login(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'login_userid',verbose_name = u'用户id')
    logintime = models.DateTimeField(u'登录时间',default=datetime.datetime.now)
    userip = models.IPAddressField(u'登录ip')
    
    def __unicode__(self):
        return self.user.realname
    
    class Meta:
        db_table = u'login'

class PcAssess(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'PcAssess_userid',verbose_name = u'用户id')
    pc = models.ForeignKey('UserPC',related_name = 'PcAssess_pcid',verbose_name = u'pcid')
    datetime = models.DateTimeField(u'时间')
    riskvalue = models.IntegerField(u'风险值')
    objects = MongoDBManager()

    def __unicode__(self):
        return self.user.realname
    
    class Meta:
        db_table = u'pc_assess'

class ResEmail(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'resemail_userid',verbose_name = u'用户id')
    pc = models.ForeignKey('UserPC',related_name = 'resemail_pcid',verbose_name = u'pcid')
    sip = models.IPAddressField(u'源ip')
    dip = models.IPAddressField(u'目的ip')
    sport = models.IntegerField(u'源端口')
    dport = models.IntegerField(u'目的端口')
    sendfrom = models.EmailField(u'发送者',max_length=64)
    sendto = models.TextField(u'接受者',max_length=300)
    sendcc = models.TextField(u'接受者',max_length=300)
    sendbcc = models.TextField(u'接受者',max_length=300)
    datetime = models.DateTimeField(u'发送时间',default=datetime.datetime.now)
    riskvalue = models.IntegerField(u'风险值')
    subject = models.CharField(u'主题',max_length=512, null=True)
    iswhite = models.BooleanField(u'是否在白名单中')
    emailtype = models.CharField(u'类型',choices = RESTYPE_CHOICES,max_length = 3)
    processname = models.CharField(u'进程名',max_length =100,null=True,blank=True)
    processmd5 = models.CharField(u'进程md5',max_length = 32,null=True,blank=True)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.user.realname
    
    class Meta:
        db_table = u'res_email'

# class ResIp(models.Model):
#     user = models.ForeignKey('Userinfo',related_name = 'resip_userid',verbose_name = u'用户id')
#     pc = models.ForeignKey('UserPC',related_name = 'resip_pcid',verbose_name = u'pcid')
#     sip = models.IPAddressField(u'源ip')
#     dip = models.IPAddressField(u'目的ip')
#     sport = models.IntegerField(u'源端口')
#     dport = models.IntegerField(u'目的端口')
#     suspiciousip = models.IPAddressField(u'可疑ip')
#     begintime = models.DateTimeField(u'begin time',default=datetime.datetime.now)
#     endtime = models.DateTimeField(u'end time',default=datetime.datetime.now)
#     riskvalue = models.IntegerField(u'风险值')
#     protocol = models.CharField(u'协议类型',choices = IPPROTOCOL_CHOICES,max_length = 1)
#     iptype = models.CharField(u'类型',choices = RESTYPE_CHOICES,max_length = 3)
#     iswhite = models.BooleanField(u'是否在白名单中')
#     # length = models.IntegerField(u'数据包大小',null=True, blank=True)
#     count = models.IntegerField(u'count')
#     objects = MongoDBManager()
#     def __unicode__(self):
#         return self.sip + ':' + self.dip
    
#     class Meta:
#         db_table = u'res_ip'

class ResIp(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'resip_userid',verbose_name = u'用户id')
    pc = models.ForeignKey('UserPC',related_name = 'resip_pcid',verbose_name = u'pcid')
    sip = models.IPAddressField(u'源ip')
    dip = models.IPAddressField(u'目的ip')
    sport = models.IntegerField(u'源端口')
    dport = models.IntegerField(u'目的端口')
    flow = models.CharField(u'流量方向',choices = FLOW_CHOICES,max_length = 3)
    datetime = models.DateTimeField(u'begin time',default=datetime.datetime.now)
    riskvalue = models.IntegerField(u'风险值')
    protocol = models.CharField(u'协议类型',choices = IPPROTOCOL_CHOICES,max_length = 1)
    iptype = models.CharField(u'类型',choices = RESTYPE_CHOICES,max_length = 3)
    iswhite = models.BooleanField(u'是否在白名单中')
    length = models.IntegerField(u'数据包大小',null=True, blank=True)
    processname = models.CharField(u'进程名',max_length =100,null=True,blank=True)
    processmd5 = models.CharField(u'进程md5',max_length = 32,null=True,blank=True)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.sip + ':' + self.dip

    class Meta:
        db_table = u'res_ip'

class ResUrl(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'resurl_userid',verbose_name = u'用户id')
    pc = models.ForeignKey('UserPC',related_name = 'resurl_pcid',verbose_name = u'pcid')
    sip = models.IPAddressField(u'源ip')
    dip = models.IPAddressField(u'目的ip')
    sport = models.IntegerField(u'源端口')
    dport = models.IntegerField(u'目的端口')
    url = models.URLField(u'URL')
    datetime = models.DateTimeField(u'发送时间',default=datetime.datetime.now)
    riskvalue = models.IntegerField(u'风险值')
    urltype = models.CharField(u'类型',choices = RESTYPE_CHOICES,max_length = 3)
    iswhite = models.BooleanField(u'是否在白名单中')
    processname = models.CharField(u'进程名',max_length =100,null=True,blank=True)
    processmd5 = models.CharField(u'进程md5',max_length = 32,null=True,blank=True)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.url
    
    class Meta:
        db_table = u'res_url'


class UserPC(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'UserPC',verbose_name = u'用户id')
    pcname = models.CharField(u'pc name',max_length=16)
    pcid = models.CharField(u'pcid',max_length=16)
    addtime = models.DateTimeField(u'注册日期',default=datetime.datetime.now)
#    objects = MongoDBManager()
    def __unicode__(self):
        return self.pcid
    class Meta:
        db_table = u'userpc'

class Userinfo(models.Model):
    user = models.OneToOneField(User)
    realname = models.CharField(u'真实姓名',max_length=16)
    mobile = models.CharField(u'手机号码',max_length=32)
    email = models.EmailField(u'邮箱')
    telephone = models.CharField(u'固定电话',max_length=32,null=True,blank=True)
    address = models.CharField(u'地址',max_length=256, null=True,blank=True)
    workplace = models.CharField(u'工作单位',max_length=128, null=True,blank=True)
    job = models.ForeignKey(Job,verbose_name="工作")
    question = models.CharField(u'问题',max_length=128)
    answer = models.CharField(u'答案',max_length=128)
    riskvalue = models.IntegerField(u'风险值', null=True,blank=True)
    ifverify = models.NullBooleanField(u'是否通过审核')
    regtime = models.DateTimeField(u'注册日期',default=datetime.datetime.now)
    emailalarmvalue = models.IntegerField(u'邮件报警阈值', default=30,null=True,blank=True)
    urlalarmvalue = models.IntegerField(u'HTTP报警阈值', default=30,null=True,blank=True)
    ipalarmvalue = models.IntegerField(u'IP报警阈值', default=30,null=True,blank=True)
    emailalarmtype = models.CharField(u'Email报警',choices = ALARM_CHOICES,max_length = 2,default='00')
    urlalarmtype = models.CharField(u'HTTP报警',choices = ALARM_CHOICES,max_length = 2,default='00')
    ipalarmtype = models.CharField(u'IP报警',choices = ALARM_CHOICES,max_length = 2,default='00')

    export_pwd = models.CharField(u'export_pwd',null=True,blank=True,max_length=20)
    castatus = models.CharField(u'castatus',choices = CASTATUS_CHOICES,default="-1",null=True,blank=True,max_length=2)

    objects = MongoDBManager()

    def __unicode__(self):
        return self.user.username
    
    class Meta:
        db_table = u'userinfo'

class Userloginvalid(models.Model):
    user = models.OneToOneField("Userinfo")
    sendtime = models.DateTimeField(u'发送时间',default=datetime.datetime.now)
    validvalue = models.IntegerField(u'验证值', null=True,blank=True)
    
    def __unicode__(self):
        return self.user.realname
    
    class Meta:
        db_table = u'userloginvalid'

class WhiteEmail(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'whiteemail_userid',verbose_name = u'用户id')
    email = models.EmailField(verbose_name = u'email')
    addtime = models.DateTimeField(u'日期',default=datetime.datetime.now)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.email
    
    class Meta:
        db_table = u'white_email'

class WhiteIp(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'whiteip_userid',verbose_name = u'用户id')
    ip = models.IPAddressField(verbose_name = u'ip')
    addtime = models.DateTimeField(u'日期',default=datetime.datetime.now)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.ip
    
    class Meta:
        db_table = u'white_ip'

class WhiteUrl(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'whiteurl_userid',verbose_name = u'用户id')
    url = models.URLField(verbose_name = u'url')
    addtime = models.DateTimeField(u'日期',default=datetime.datetime.now)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.url
    
    class Meta:
        db_table = u'white_url'

class WhiteProcesss(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'whiteprocesss_userid',verbose_name = u'用户id')
    processname = models.CharField(u'进程名',max_length=100)
    addtime = models.DateTimeField(u'日期',default=datetime.datetime.now)
    md5 = models.CharField(u'进程md5',max_length = 32,null=True,blank=True)
    description = models.CharField(u'详细描述',max_length=256,null=True,blank=True)
    version= models.CharField(u'版本号',max_length=256,null=True,blank=True)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.processname
    
    class Meta:
        db_table = u'white_process'


class NetBehaviour(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'netbehaviour_userid',verbose_name = u'用户id')
    datetime = models.DateTimeField(u'date time',default=datetime.datetime.now)
    level = models.IntegerField(u'级别',null=True,blank=True)
    tick = models.FloatField(u'tick',null=True,blank=True)
    flow = models.CharField(u'流向',max_length = 3,null=True,blank=True)
    version= models.CharField(u'版本号',max_length=256,null=True,blank=True)
    transfprotc = models.CharField(u'传输协议类型',max_length = 10,null=True,blank=True)
    appprotc = models.CharField(u'应用协议类型',max_length = 10,null=True,blank=True)
    nettype = models.CharField(u'事件类型',max_length = 10,null=True,blank=True)
    content = models.TextField(u'内容',null=True,blank=True)
    riskvalue = models.IntegerField(u'风险值',null=True,blank=True)
    sip = models.IPAddressField(u'源ip',null=True,blank=True)
    dip = models.IPAddressField(u'目的ip',null=True,blank=True)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.version

    class Meta:
        db_table = u'net_behaviour'

class DriverBehaviour(models.Model):
    user = models.ForeignKey('Userinfo',related_name = 'driverbehaviour_userid',verbose_name = u'用户id')
    driver = models.CharField(u'驱动',max_length = 10,null=True,blank=True)
    dritype = models.CharField(u'类型',max_length = 10,null=True,blank=True)
    program = models.CharField(u'程序',max_length = 20,null=True,blank=True)
    flow = models.CharField(u'流向',max_length = 3,null=True,blank=True)
    commnum = models.CharField(u'联系号码',max_length = 15,null=True,blank=True)
    smscontent = models.TextField(u'内容',null=True,blank=True)
    riskvalue = models.IntegerField(u'风险值',null=True,blank=True)

    datetime = models.DateTimeField(u'date time',default=datetime.datetime.now)
    objects = MongoDBManager()

    def __unicode__(self):
        return self.driver

    class Meta:
        db_table = u'driver_behaviour'
