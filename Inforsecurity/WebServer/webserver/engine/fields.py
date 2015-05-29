#!/usr/bin/python
#-*-coding:utf-8-*-

from django.forms.fields import Field,CharField
from validators import username,password,realname,mobile,telephone

class UsernameField(CharField):
    default_error_messages = {
        'invalid':u'用户名由字母数字下划线组成，6到16位，且第一位必须为字母',
        'required':u'用户名必须要填(字母数字下划线组成，6到16位，且第一位必须为字母)',
        'max_length':u'用户名至多为16位',
        'min_length':u'用户名至少为6位'
    }
    default_validators = [username]

    def clean(self,value):
        value = self.to_python(value).strip()
        return super(UsernameField, self).clean(value)

class PasswordField(CharField):
    default_error_messages = {
        'invalid':u'密码由字母数字下划线组成的字符串，最少为8位',
        'required':u'密码必须要填(由字母数字下划线组成的字符串，最少为8位)',
        'max_length':u'密码至多为16位',
        'min_length':u'密码至少为8位'
    }
    default_validators = [password]

################################deprecated################################
class RealnameField(CharField):
    default_error_messages = {
        'invalid':u'真实姓名必须是2-4个汉字',
        'required':u'真实姓名必须要填（2-4个汉字）',
    }
    default_validators = [realname]

    def clean(self,value):
        value = self.to_python(value).strip()
        return super(RealnameField, self).clean(value)
# ################################deprecated################################

# class IdCardField(CharField):
#     default_error_messages = {
#         'invalid':u'请输入正确的身份证号',
#         'required':u'身份证号必须要填',
#     }
#     default_validators = [idcard]

class MobileField(CharField):
    default_error_messages = {
        'invalid':u'请输入正确的手机号码',
        'required':u'手机号码必须要填',
    }
    default_validators = [mobile]

    def clean(self,value):
        value = self.to_python(value).strip()
        return super(MobileField, self).clean(value)

class TelephoneField(CharField):
    default_error_messages = {
        'invalid':u'请输入正确的电话号码',
    }
    default_validators = [telephone]

    def clean(self,value):
        value = self.to_python(value).strip()
        return super(TelephoneField, self).clean(value)
