# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import BucketListView
urlpatterns = [
    url(r"^bucket/list/?$", BucketListView.as_view(), name="bucket_list"),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
