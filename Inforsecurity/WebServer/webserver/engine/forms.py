#!/usr/bin/python
#-*- coding:utf-8 -*-

from models import RESTYPE_CHOICES,TYPE_CHOICES
from django import forms
from captcha.fields import CaptchaField
from django.template import RequestContext
from models import Userinfo,Job
from django.db.models import Q
from django.conf import settings
import random
from django.contrib.auth.models import User
from django.utils.hashcompat import md5_constructor
from engine.fields import UsernameField,PasswordField,RealnameField,MobileField,TelephoneField

SELECT_QUESTION_CHOICES = (
    ('您的生日是几月几号','0'),
    ('您的小学是在哪里上的','1'),
    ('您最喜欢的宠物的名字','2'),
    ('您父亲的名字','3'),
    ('您高中老师的名字','4'),
    ('自己输入问题','5'),
)

_MAX_USERID_KEY = 18446744073709551616L


class Norender_Form(forms.Form):
    '''
        a base form inherit from forms.Form,it is used for translate brower data to form datas.use it by inherit it.
    '''
    REAL_VALUE = None

    def _clean_fields(self):
        for name, field in self.fields.items():
            value = REAL_VALUE[name]
            try:
                if isinstance(field, FileField):
                    initial = self.initial.get(name, field.initial)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError, e:
                self._errors[name] = self.error_class(e.messages)
                if name in self.cleaned_data:
                    del self.cleaned_data[name]

    def full_clean(self):
        """
        Cleans all of self.data and populates self._errors and
        self.cleaned_data.
        """
        self._errors = ErrorDict()
        if not self.is_bound: # Stop further processing.
            return
        self.cleaned_data = {}
        # If the form is permitted to be empty, and none of the form data has
        # changed from the initial data, short circuit any validation.
        if self.empty_permitted:
            return
        self._clean_fields()
        self._clean_form()
        self._post_clean()
        if self._errors:
            del self.cleaned_data                   


class RegisterForm(forms.Form):
    username = UsernameField(required=True,max_length=16,min_length=6)
    password = PasswordField(required=True,max_length=16,min_length=8)
    repassword = PasswordField(required=True,max_length=16,min_length=8)
    realname = forms.CharField(required=True,min_length=2,error_messages={
        'required':u"真实姓名必须要填",
        'min_length':u'真实姓名必须是2-4个汉字'})

    email = forms.EmailField(required=True,error_messages={
        'invalid':'请输入正确格式的email',
        'required':'邮箱必须要填'})
    mobile = MobileField(required=True)
    telephone = TelephoneField(required=False)
    workspace = forms.CharField(required=False)
    address = forms.CharField(required=False)
    job1 = forms.CharField(required=True)
    job2 = forms.CharField(required=True)
    select_question = forms.ChoiceField(required=True,choices=SELECT_QUESTION_CHOICES,error_messages={'invalid':u'请您正确选择下拉框'})
    custom_question = forms.CharField(required=False)
    answer = forms.CharField(required=True,error_messages={'required':u'提示问题答案必须要填'})
    captcha = CaptchaField(required=True,error_messages={'invalid':u"您输入的验证码不正确"})

    # def clean_username(self):
    #     username = self.cleaned_data["username"]
    #     try:
    #         user = User.objects.get(username = username)
    #         Userinfo.objects.get(user=user)
    #     except Userinfo.DoesNotExist:
    #         return username
    #     raise forms.ValidationError(u"该用户名已经存在")

    def clean_repassword(self):
        password = self.cleaned_data.get("password","")
        repassword = self.cleaned_data['repassword']
        if password != repassword:
            raise forms.ValidationError(u'此处必须输入和上栏密码相同的内容')
        return repassword

    def clean_job2(self):
        job1 = self.cleaned_data['job1']
        job2 = self.cleaned_data['job2']
        try:
            Job.objects.get(Q(pid__exact=job1)&Q(id__exact=job2))
            return job2
        except Job.DoesNotExist:
            raise forms.ValidationError(u'请正确选择职位')

    def clean_custom_question(self):
        select_question = self.cleaned_data['select_question']
        custom_question = self.cleaned_data['custom_question']
        if select_question == u"自己输入问题" and not custom_question:
            raise forms.ValidationError(u'现在你必须输入问题')
        return custom_question

    def save(self):
        user = User(username=self.cleaned_data['username'],email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password'])
        user.save()
        job = Job.objects.get(Q(pid__exact=self.cleaned_data['job1'])&Q(id__exact=self.cleaned_data['job2']))
        userid = md5_constructor("%s%s"%(random.randrange(0, _MAX_USERID_KEY), settings.SECRET_KEY)).hexdigest()
        question = self.cleaned_data['custom_question'] if self.cleaned_data['select_question'] == u"自己输入问题" and self.cleaned_data['custom_question'] else self.cleaned_data['select_question']
        userinfo = Userinfo(user=user,realname=self.cleaned_data['realname'],
                mobile=self.cleaned_data['mobile'],telephone=self.cleaned_data['telephone'],
                address=self.cleaned_data['address'],workplace=self.cleaned_data['workspace'],
                job=job,question=question,answer=self.cleaned_data['answer'],riskvalue=0,
                email=self.cleaned_data['email'])
        userinfo.save()
#更新用户信息的数据验证
class UpdateUserinfoForm(forms.Form):
    realname = forms.CharField(required=True)
    email = forms.EmailField(required=True,error_messages={
        'invalid':'请输入正确格式的email',
        'required':'邮箱必须要填'})
    mobile = MobileField(required=True)
    telephone = TelephoneField(required=False)
    workspace = forms.CharField(required=False)
    address = forms.CharField(required=False)
    job1 = forms.CharField(required=False)
    job2 = forms.CharField(required=False)
    select_question = forms.ChoiceField(required=True,choices=SELECT_QUESTION_CHOICES,error_messages={'invalid':u'请您正确选择下拉框'})
    custom_question = forms.CharField(required=False)
    answer = forms.CharField(required=True,error_messages={'required':u'提示问题答案必须要填'})
#    def clean_job2(self):
#        job1 = self.cleaned_data['job1']
#        job2 = self.cleaned_data['job2']
#        try:
#            Job.objects.get(Q(pid__exact=job1)&Q(id__exact=job2))
#            return job2
#        except Job.DoesNotExist:
#            raise forms.ValidationError(u'请正确选择职位')
    def clean_custom_question(self):
        select_question = self.cleaned_data['select_question']
        custom_question = self.cleaned_data['custom_question']
        if select_question == u"自己输入问题" and not custom_question:
            raise forms.ValidationError(u'现在你必须输入问题')
        return custom_question
    def update(self):
        question = self.cleaned_data['custom_question'] if self.cleaned_data['select_question'] == u"自己输入问题" and self.cleaned_data['custom_question'] else self.cleaned_data['select_question']
        user = Userinfo.objects.get(realname = self.cleaned_data['realname'])
        user.mobile=self.cleaned_data['mobile']
        user.telephone=self.cleaned_data['telephone']
        user.address=self.cleaned_data['address']
        user.workplace=self.cleaned_data['workspace']
        user.question=question
        user.answer=self.cleaned_data['answer']
        user.email=self.cleaned_data['email']
        try:
            job = Job.objects.get(Q(pid__exact=self.cleaned_data['job1'])&Q(id__exact=self.cleaned_data['job2']))
            user.job=job
            user.save()
        except:
            user.save()
        
class ResEmail_Search(forms.Form):
    '''
        verification for ResEmail_Search.
    '''
    emailtypes = forms.MultipleChoiceField(required=False,choices=RESTYPE_CHOICES,error_messages={'invalid':'请正确选择复选框'})
    begintime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    endtime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    sip = forms.IPAddressField(required=False,error_messages={'invalid':'请输入正确格式的ip'})
    dip = forms.IPAddressField(required=False,error_messages={'invalid':'请输入正确格式的ip'})
    sender = forms.EmailField(required=False,error_messages={'invalid':'请输入正确格式的email'})
    receiver = forms.EmailField(required=False,error_messages={'invalid':'请输入正确格式的email'})
    riskvalue = forms.IntegerField(required=False,error_messages={'invalid':'请输入数字'})

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ResEmail_Search, self).__init__(*args, **kwargs)

    #判断用户是否至少选择了一项
    def clean(self):
        has_data = False
        for k,v in dict(self.request.POST).items():
            if k not in ['csrfmiddlewaretoken',] and v != [u'']:
                has_data = True

        if not has_data: 
            raise forms.ValidationError("至少选择一项进行搜索")
        return self.cleaned_data
        
class ResUrl_Search(forms.Form):
    '''
        verification for ResUrl_Search.
    '''
    urltypes = forms.MultipleChoiceField(required=False,choices=RESTYPE_CHOICES,error_messages={'invalid':'请正确选择复选框'})
    begintime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    endtime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    sip = forms.IPAddressField(required=False,error_messages={'invalid':'请输入正确格式的ip'})
    dip = forms.IPAddressField(required=False,error_messages={'invalid':'请输入正确格式的ip'})
    url = forms.URLField(required=False,error_messages={'invalid':'请输入正确格式的url'})
    riskvalue = forms.IntegerField(required=False,error_messages={'invalid':'请输入数字'})

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ResUrl_Search, self).__init__(*args, **kwargs)

    #判断用户是否至少选择了一项
    def clean(self):
        has_data = False
        for k,v in dict(self.request.POST).items():
            if k not in ['csrfmiddlewaretoken',] and v != [u'']:
                has_data = True

        if not has_data: 
            raise forms.ValidationError("至少选择一项进行搜索")
        return self.cleaned_data

class ResIp_Search(forms.Form):
    '''
        verification for ResUrl_Search.
    '''
    iptypes = forms.MultipleChoiceField(required=False,choices=RESTYPE_CHOICES,error_messages={'invalid':'请正确选择复选框'})
    begintime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    endtime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    sip = forms.IPAddressField(required=False,error_messages={'invalid':'请输入正确格式的ip'})
    dip = forms.IPAddressField(required=False,error_messages={'invalid':'请输入正确格式的ip'})
    ip = forms.IPAddressField(required=False,error_messages={'invalid':'请输入正确格式的ip'})
    riskvalue = forms.IntegerField(required=False,error_messages={'invalid':'请输入数字'})

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ResIp_Search, self).__init__(*args, **kwargs)

    #判断用户是否至少选择了一项
    def clean(self):
        has_data = False
        for k,v in dict(self.request.POST).items():
            if k not in ['csrfmiddlewaretoken',] and v != [u'']:
                has_data = True

        if not has_data: 
            raise forms.ValidationError("至少选择一项进行搜索")
        return self.cleaned_data


class BlackEmail_Search(forms.Form):
    '''
        verification for BlackEmail_Search.
    '''
    blackemailtype = forms.MultipleChoiceField(required=False,choices=TYPE_CHOICES,error_messages={'invalid':'请正确选择复选框'})
    begintime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    endtime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    blackemail = forms.EmailField(required=False,error_messages={'invalid':'请输入正确格式的email'})
    riskvalue = forms.IntegerField(required=False,max_value=100,min_value=0,error_messages={
        'invalid':'请输入数字',
        'max_value':'风险值最大为100',
        'min_value':'风险值最小为0'})

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(BlackEmail_Search, self).__init__(*args, **kwargs)

    #判断用户是否至少选择了一项
    def clean(self):
        has_data = False
        for k,v in dict(self.request.POST).items():
            if k not in ['csrfmiddlewaretoken',] and v != [u'']:
                has_data = True

        if not has_data: 
            raise forms.ValidationError("至少选择一项进行搜索")
        return self.cleaned_data

class WhiteList_Add(forms.Form):
    '''
        verification for WhiteList_Add.
    '''
    white_ip = forms.IPAddressField(required=False,error_messages={
        'invalid':'请输入正确格式的IP',
        'required':'请输入IP地址',
    })
    white_email = forms.EmailField(required=False,error_messages={
        'invalid':'请输入正确格式的Email',
        'required':'请输入Email地址',
    })
    white_url = forms.URLField(required=False,error_messages={
        'invalid':'请输入正确格式的Url',
        'required':'请输入Url地址',
    })

class WhiteProcess_Add(forms.Form):
    '''
        verification for WhiteProcess_Add.
    '''
    processname = forms.CharField(max_length = 100)
    addtime = forms.DateTimeField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    md5 = forms.CharField(required=False,max_length = 32)
    description = forms.CharField(required=False,max_length=256)
    version= forms.CharField(required=False,max_length=256)

class WhiteProcess_Edit(WhiteProcess_Add):
    pass

class WhiteProcess_Search(forms.Form):
    '''
        verification for WhiteProcess_Search.
    '''
    begintime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    endtime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    processname = forms.CharField(required=False,max_length = 100)
    md5 = forms.CharField(required=False,max_length = 32)
    version= forms.CharField(required=False,max_length=256)


    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(WhiteProcess_Search, self).__init__(*args, **kwargs)

    #判断用户是否至少选择了一项
    def clean(self):
        has_data = False
        for k,v in dict(self.request.POST).items():
            if k not in ['csrfmiddlewaretoken',] and v != [u'']:
                has_data = True

        if not has_data: 
            raise forms.ValidationError("至少选择一项进行搜索")
        return self.cleaned_data


class BlackEmail_Add(forms.Form):
    '''
        verification for BlackEmail_Add.
    '''
    blackemailtype = forms.ChoiceField(required=True,choices=TYPE_CHOICES,error_messages={
        'invalid':'请正确选择单选框',
        'required':'请选择邮件类型',
    })
    blackemail = forms.EmailField(required=True,error_messages={
        'invalid':'请输入正确格式的email',
        'required':'请输入邮件地址',
    })
    riskvalue = forms.IntegerField(required=True,max_value=100,min_value=0,error_messages={
        'invalid':'请输入数字',
        'required':'请输入风险值',    
        'max_value':'风险值最大为100',
        'min_value':'风险值最小为0'})
    description = forms.CharField(required=False)

class BlackEmail_Edit(BlackEmail_Add):
    pass
    
class Blackip_Search(forms.Form):
    '''
        verification for BlackEmail_Search.
    '''
    blackiptype = forms.MultipleChoiceField(required=False,choices=TYPE_CHOICES,error_messages={'invalid':'请正确选择复选框'})
    begintime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    endtime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    blackip = forms.IPAddressField(required=False,error_messages={'invalid':'请输入正确格式的ip'})
    riskvalue = forms.IntegerField(required=False,max_value=100,min_value=0,error_messages={
        'invalid':'请输入数字',
        'max_value':'风险值最大为100',
        'min_value':'风险值最小为0'})

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(Blackip_Search, self).__init__(*args, **kwargs)

    #判断用户是否至少选择了一项
    def clean(self):
        has_data = False
        for k,v in dict(self.request.POST).items():
            if k not in ['csrfmiddlewaretoken',] and v != [u'']:
                has_data = True

        if not has_data: 
            raise forms.ValidationError("至少选择一项进行搜索")
        return self.cleaned_data
class BlackIp_Add(forms.Form):
    '''
        verification for BlackIp_Add.
    '''
    blackiptype = forms.ChoiceField(required=True,choices=TYPE_CHOICES,error_messages={
        'invalid':'请正确选择单选框',
        'required':'请选择Ip类型',
    })
    blackip = forms.IPAddressField(required=True,error_messages={
        'invalid':'请输入正确格式的Ip',
        'required':'请输入邮件地址',
    })
    riskvalue = forms.IntegerField(required=True,max_value=100,min_value=0,error_messages={
        'invalid':'请输入数字',
        'required':'请输入风险值',    
        'max_value':'风险值最大为100',
        'min_value':'风险值最小为0'})
    description = forms.CharField(required=False)
    
class BlackIp_Edit(BlackIp_Add):
    pass
class BlackUrl_Search(forms.Form):
    '''
        verification for BlackEmail_Search.
    '''
    blackurltype = forms.MultipleChoiceField(required=False,choices=TYPE_CHOICES,error_messages={'invalid':'请正确选择复选框'})
    begintime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    endtime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    blackurl = forms.URLField(required=False,error_messages={'invalid':'请输入正确格式的url'})
    riskvalue = forms.IntegerField(required=False,max_value=100,min_value=0,error_messages={
        'invalid':'请输入数字',
        'max_value':'风险值最大为100',
        'min_value':'风险值最小为0'})

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(BlackUrl_Search, self).__init__(*args, **kwargs)

    #判断用户是否至少选择了一项
    def clean(self):
        has_data = False
        for k,v in dict(self.request.POST).items():
            if k not in ['csrfmiddlewaretoken',] and v != [u'']:
                has_data = True

        if not has_data: 
            raise forms.ValidationError("至少选择一项进行搜索")
        return self.cleaned_data
class BlackUrl_Add(forms.Form):
    '''
        verification for BlackIp_Add.
    '''
    blackurltype = forms.ChoiceField(required=True,choices=TYPE_CHOICES,error_messages={
        'invalid':'请正确选择单选框',
        'required':'请选择Url类型',
    })
    blackurl = forms.URLField(required=True,error_messages={
        'invalid':'请输入正确格式的Url',
        'required':'请输入邮件地址',
    })
    riskvalue = forms.IntegerField(required=True,max_value=100,min_value=0,error_messages={
        'invalid':'请输入数字',
        'required':'请输入风险值',    
        'max_value':'风险值最大为100',
        'min_value':'风险值最小为0'})
    description = forms.CharField(required=False)
    
class BlackUrl_Edit(BlackUrl_Add):
    pass

class ResetPwdForm(forms.Form):
    '''
        verification for ResetPwdForm.
    '''

    oripwd = forms.CharField(required=True)
    newpwd1 = forms.CharField(required=True)
    newpwd2 = forms.CharField(required=True)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ResetPwdForm, self).__init__(*args, **kwargs)

    #判断用户是否至少选择了一项
    def clean(self):
        has_data = False
        for k,v in dict(self.request.POST).items():
            if k not in ['csrfmiddlewaretoken',] and v != [u'']:
                has_data = True

        if not has_data:
            raise forms.ValidationError("至少选择一项进行搜索")
        if self.request.POST["newpwd1"]!=self.request.POST["newpwd2"]:
            raise forms.ValidationError("new password not equal")
        return self.cleaned_data

class NetBehaviour_Search(forms.Form):
    '''
        verification for NetBehaviour_Search.
    '''
    begintime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    endtime = forms.DateField(required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':'请输入正确格式的日期'})
    level = forms.IntegerField(required=False)
    tick = forms.FloatField(required=False)
    version= forms.CharField(required=False)
    transfprotc = forms.CharField(required=False)
    appprotc = forms.CharField(required=False)
    nettype = forms.CharField(required=False)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(NetBehaviour_Search, self).__init__(*args, **kwargs)

    #判断用户是否至少选择了一项
    def clean(self):
        has_data = False
        for k,v in dict(self.request.POST).items():
            if k not in ['csrfmiddlewaretoken',] and v != [u'']:
                has_data = True

        if not has_data: 
            raise forms.ValidationError("至少选择一项进行搜索")
        return self.cleaned_data