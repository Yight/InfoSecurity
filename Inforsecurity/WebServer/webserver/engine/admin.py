#!/usr/bin/python
#-*-coding:utf-8-*-

from django.contrib import admin
from models import Alarminfo,BlackEmail,BlackIp,BlackTrojan,BlackUrl,\
        Job,Login,ResEmail,ResIp,ResUrl,Userinfo,\
        WhiteEmail,WhiteIp,WhiteUrl,WhiteProcesss,UserPC,PcAssess,Userloginvalid,AlarmList,\
        NetBehaviour,DriverBehaviour,AlarmPre
class AlarmListAdmin(admin.ModelAdmin):
    list_display = ['user','riskvalue','blackdata','datatype','datapk_id','isfigured','insert_time']
    list_per_page = 20
    search_fields = ['user','insert_time','riskvalue']
    list_filter = ('isfigured',)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id','pid','name']
    list_per_page = 20
    search_fields = ['name']
class AlarminfoAdmin(admin.ModelAdmin):
    list_display = ['user','rank','content','suggestion']
    list_per_page = 20
    search_fields = ['user','rank']
class BlackEmailAdmin(admin.ModelAdmin):
    list_display = ['user','blackemail','emailtype','riskvalue','addtime','description']
    list_per_page = 20
    search_fields = ['user','blackemail','riskvalue']
class BlackIpAdmin(admin.ModelAdmin):
    list_display = ['user','blackip','iptype','riskvalue','addtime','description']
    list_per_page = 20
    search_fields = ['user','blackip','riskvalue']
class BlackUrlAdmin(admin.ModelAdmin):
    list_display = ['user','blackurl','urltype','riskvalue','addtime','description']
    list_per_page = 20
    search_fields = ['user','blackurl','riskvalue']
class LoginAdmin(admin.ModelAdmin):
    list_display = ['user','userip','logintime']
    list_per_page = 20
    search_fields = ['user','userip']
class ResEmailAdmin(admin.ModelAdmin):
    list_display = ['user','pc','sip','dip','sport','dport','sendfrom','sendto','datetime','riskvalue','subject','iswhite']
    list_per_page = 20
    search_fields = ['user','sip','dip','sendfrom','sendto','subject']
    list_filter = ('iswhite',)
class ResIpAdmin(admin.ModelAdmin):
    list_display = ['user','pc','sip','dip','sport','dport','flow','datetime','riskvalue','iptype','iswhite','processname','processmd5']
    list_per_page = 20
    search_fields = ['user','sip','dip']
    list_filter = ('iswhite',)
class ResUrlAdmin(admin.ModelAdmin):
    list_display = ['user','pc','sip','dip','sport','dport','url','datetime','riskvalue','urltype','iswhite']
    list_per_page = 20
    search_fields = ['user','sip','dip','url']
    list_filter = ('iswhite',)
class UserPCAdmin(admin.ModelAdmin):
    list_display = ['user','pcname','pcid','addtime']
    list_per_page = 20
    search_fields = ['user','pcname']
class UserinfoAdmin(admin.ModelAdmin):
    list_display = ['id','user','realname','mobile','email','telephone','address','workplace','question',
    'answer','riskvalue','ifverify','regtime','emailalarmvalue','urlalarmvalue','ipalarmvalue',
    'emailalarmtype','urlalarmtype','ipalarmtype','export_pwd','castatus']
    list_per_page = 20
    search_fields = ['user','realname','address']
    list_filter = ('castatus',)
class PcAssessAdmin(admin.ModelAdmin):
    list_display = ['user','pc','datetime','riskvalue']
    list_per_page = 20
    search_fields = ['user','pc']
class WhiteEmailAdmin(admin.ModelAdmin):
    list_display = ['user','email','addtime']
    list_per_page = 20
    search_fields = ['user','email']
class WhiteIpAdmin(admin.ModelAdmin):
    list_display = ['user','ip','addtime']
    list_per_page = 20
    search_fields = ['user','ip']
class WhiteUrlAdmin(admin.ModelAdmin):
    list_display = ['url','addtime']
    list_per_page = 20
    search_fields = ['user','url']
    list_filter = ('addtime',)
class WhiteProcesssAdmin(admin.ModelAdmin):
    list_display = ['user','processname','addtime']
    list_per_page = 20
    search_fields = ['user','processname']
    list_filter = ('addtime',)
class UserloginvalidAdmin(admin.ModelAdmin):
    list_display = ['user','sendtime','validvalue']
    list_per_page = 20
    search_fields = ['user']
class NetBehaviourAdmin(admin.ModelAdmin):
    list_display = ['user','datetime','level','version']
    list_per_page = 20
    search_fields = ['user']
class DriverBehaviourAdmin(admin.ModelAdmin):
    list_display = ['user','datetime','driver','program']
    list_per_page = 20
    search_fields = ['user']  
class AlarmPreAdmin(admin.ModelAdmin):
    list_display = ['user','datacontent']
    list_per_page = 20
    search_fields = ['user']  

admin.site.register(AlarmList,AlarmListAdmin)
admin.site.register(Alarminfo,AlarminfoAdmin)
admin.site.register(BlackEmail,BlackEmailAdmin)
admin.site.register(BlackIp,BlackIpAdmin)
#admin.site.register(BlackTrojan,BlackTrojanAdmin)
admin.site.register(BlackUrl,BlackUrlAdmin)
admin.site.register(Job,JobAdmin)
admin.site.register(Login,LoginAdmin)
admin.site.register(ResEmail,ResEmailAdmin)
admin.site.register(PcAssess,PcAssessAdmin)
admin.site.register(ResIp,ResIpAdmin)
#admin.site.register(ResTrojan,ResTrojanAdmin)
admin.site.register(ResUrl,ResUrlAdmin)
admin.site.register(UserPC,UserPCAdmin)
admin.site.register(Userinfo,UserinfoAdmin)
admin.site.register(WhiteEmail,WhiteEmailAdmin)
admin.site.register(WhiteIp,WhiteIpAdmin)
admin.site.register(WhiteUrl,WhiteUrlAdmin)
admin.site.register(WhiteProcesss,WhiteProcesssAdmin)
admin.site.register(Userloginvalid,UserloginvalidAdmin)
admin.site.register(NetBehaviour,NetBehaviourAdmin)
admin.site.register(DriverBehaviour,DriverBehaviourAdmin)
admin.site.register(AlarmPre,AlarmPreAdmin)
