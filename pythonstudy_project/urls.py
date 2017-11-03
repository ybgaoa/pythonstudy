# coding: utf-8
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "index.html", {'hello':"hello!"})

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^v1/s3/', include('study.s3_op.urls')),
    url(r'^', index),
]
urlpatterns = format_suffix_patterns(urlpatterns)
