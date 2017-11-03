# coding: utf-8
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from commons.dependency import get_provider
import sys
import threading
import os
# 初始化日志
logger = logging.getLogger('study.s3_op.views')

class BucketListView(APIView):
    #获取bucket列表
    def get(self, request):
        params = request.query_params
        try:
            s3client = get_provider('s3_client_api').create_client()
            bucket_list = get_provider('s3_api_manager').get_bucket_list(s3client)
            return Response(data={'retCode': 0, 'message': 'success', 'result': bucket_list}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error('Failed to error: %s' % e.message)
            return Response(data={'retCode': 500, 'message': '失败', 'result': ''},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BucketObjectDownloadView(APIView):
    #下载s3上的文件
    def post(self, request, **kwargs):
        bucket = kwargs.get('bucket')
        data = request.data
        key = data.get('key')
        file_download_source = data.get('file_download_source')
        try:
            s3client = get_provider('s3_client_api').create_client()
            get_provider('s3_api_manager').download_file(bucket, key, file_download_source, s3client, callback=_DownloadProgressPercentage(file_download_source))
            return Response(data={'retCode': 0, 'message': 'success', 'result': ''}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error('Failed to error: %s' % e.message)
            return Response(data={'retCode': 500, 'message': '失败', 'result': ''},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BucketObjectUploadView(APIView):
    #上传文件到s3
    def post(self, request, **kwargs):
        bucket = kwargs.get('bucket')
        data = request.data
        key = data.get('key')
        file_upload_source = data.get('file_upload_source')
        try:
            s3client = get_provider('s3_client_api').create_client()
            get_provider('s3_api_manager').upload_file(file_upload_source, bucket, key, s3client, callback=_UploadProgressPercentage(file_upload_source))
            return Response(data={'retCode': 0, 'message': 'success', 'result': ''}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error('Failed to error: %s' % e.message)
            return Response(data={'retCode': 500, 'message': '失败', 'result': ''},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class _DownloadProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            sys.stdout.write(
                "\r%s --> %s bytes transferred" % (
                    self._filename, self._seen_so_far))
            sys.stdout.flush()

class _UploadProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()
