# coding=utf-8
from django.test import TestCase

import boto3
from botocore.client import Config
import os
import sys
import threading

#创建s3链接，如果s3服务器是第四代，则需要设置signature_version='s3v4'
s3_client = boto3.client('s3', endpoint_url='http://10.156.129.136:80',
                         aws_access_key_id='ETRVKPSYFOT5X2NDJC5Q',
                         aws_secret_access_key='EQw91OPbD5XuGgQ7M17gWi13UGeRoSgxOhSoEX+8',
                         region_name='cn-north-1',
                         config=Config(signature_version='s3'))
print s3_client
#创建bucket
# bucket = s3_client.create_bucket(Bucket='ybgaoatest')
# print bucket
#获取bucket
# bucket_info = s3_client.head_bucket(Bucket='ybgaoatest')
# print bucket_info
#查看bucket列表
# bucket_list = s3_client.list_buckets()
# print bucket_list
# #删除bucket
# bucket_delete = s3_client.delete_bucket(Bucket='ybgaoatest')
# print bucket_delete
#上传文件
class ProgressPercentage(object):
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
s3_client.upload_file("E:/download/tools/jdk_1.8.0.0_64.exe", "ybgaoatest", "download/tools/jdk_1.8.0.0_64.exe",
                      ExtraArgs={'ACL': 'public-read'},
                      Callback=ProgressPercentage("E:/download/tools/jdk_1.8.0.0_64.exe"))
# s3_client.upload_file("E:/mytest.txt", "ybgaoatest", "tmp/tmp01/a/b", ExtraArgs={'ACL': 'public-read'})
#查看bucket下的object列表
# object_list = s3_client.list_objects(Bucket='ybgaoatest')
# print object_list
#查看bucket下的object
# object_info = s3_client.get_object(Bucket='ybgaoatest', Key='tmp/tmp01/b')
# print object_info
#删除object
# object_delete = s3_client.delete_object(Bucket='ybgaoatest',Key='tmp/tmp01/b')
# print object_delete
#删除object列表
# object_list_delete = s3_client.delete_objects(
#     Bucket='ybgaoatest',
#     Delete={
#         'Objects': [
#             {
#                 'Key': 'tmp/tmp01/a'
#             },
#         ],
#         'Quiet': True
#     }
# )
# print object_list_delete
#下载文件
# s3_client.download_file("ybgaoatest", "download/tools/jdk_1.8.0.0_64.exe", "E:/jdk_1.8.0.0_64.exe")