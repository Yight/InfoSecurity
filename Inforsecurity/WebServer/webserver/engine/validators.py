#!/usr/bin/python
#-*-coding:utf-8-*-

import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# class IdCardValidator(object):
#     message = u'请输入正确的身份证号'
#     code = 'invalid'
#     chmap = {
#         '0':0,'1':1,'2':2,'3':3,'4':4,'5':5,
#         '6':6,'7':7,'8':8,'9':9,'x':10,'X':10
#     }

#     def __init__(self, message=None, code=None):
#         if message is not None:
#             self.message = message
#         if code is not None:
#             self.code = code

#     def ch_to_num(self,ch):
#         return self.chmap[ch]

#     def verify_list(self,l):
#         sum = 0
#         for ii,n in enumerate(l):
#             i = 18-ii
#             weight = 2**(i-1) % 11
#             sum = (sum + n*weight) % 11
#         return sum==1

#     def __call__(self,value):
#         char_list = list(value)
#         num_list = [self.ch_to_num(ch) for ch in char_list]
#         if not self.verify_list(num_list):
#             raise ValidationError(self.message, code=self.code)

username_re = re.compile(r'^[a-zA-Z]{1}[\w_]+?$')
username = RegexValidator(username_re,u'用户名由字母数字下划线组成，6到16位，且第一位必须为字母','invalid')

password_re = re.compile(r'^[\w]+?$')
password = RegexValidator(password_re,u'密码由字母数字下划线组成的字符串，最少为8位','invalid')

################################deprecated################################
realname_re = re.compile(r'^[\u4e00-\u9fa5]{2,4}$')
realname = RegexValidator(realname_re,u'真实姓名必须是2-4个汉字','invalid')
################################deprecated################################

# idcard = IdCardValidator()

mobile_re = re.compile(r'^\d{11}$')
mobile = RegexValidator(mobile_re,u'请输入正确的手机号码','invalid')

telephone_re = re.compile(r'^(([0\+]\d{2,3}-)?(0\d{2,3})-)?(\d{7,8})(-(\d{3,}))?$')
telephone = RegexValidator(telephone_re,u'请输入正确的电话号码','invalid')
