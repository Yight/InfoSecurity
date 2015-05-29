#!/usr/bin/python
#-*-coding:utf-8-*-

from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from models import ResEmail,Userinfo,ResUrl,BlackEmail,BlackIp,BlackUrl,Job
from django.template.loader import render_to_string
from models import ALARM_CHOICES,RESTYPE_CHOICES,TYPE_CHOICES
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from django.template import RequestContext
from engine.utils import get_datatables_records
from django.db.models import Q
from forms import ResEmail_Search,BlackEmail_Search,BlackEmail_Add,BlackEmail_Edit,BlackIp_Add,BlackIp_Edit,BlackUrl_Add,BlackUrl_Edit
import traceback
import datetime
from bson.objectid import ObjectId  
import urllib

@login_required
def dashboard(request):
    return render_to_response('dashboard/general.html',{"title":'主页'},context_instance = RequestContext(request))

