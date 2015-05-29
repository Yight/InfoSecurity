#!/usr/bin/python
#-*-coding:utf-8-*-

from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext


def test_form_layouts(request):
    return render_to_response('templates/form_layouts.html',None,context_instance = RequestContext(request))

def test_form_elements(request):
    return render_to_response('templates/form_elements.html',None,context_instance = RequestContext(request))

def test_form_wizard(request):
    return render_to_response('templates/form_wizard.html',None,context_instance = RequestContext(request))
