# coding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import BucketListView, BucketObjectDownloadView, BucketObjectUploadView
urlpatterns = [
    url(r"^bucket/object/(?P<bucket>[a-z0-9-]+)/upload/?$", BucketObjectUploadView.as_view(), name="bucket_file_upload"),
    url(r"^bucket/object/(?P<bucket>[a-z0-9-]+)/download/?$", BucketObjectDownloadView.as_view(), name="bucket_file_download"),
    url(r"^bucket/list/?$", BucketListView.as_view(), name="bucket_list"),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
