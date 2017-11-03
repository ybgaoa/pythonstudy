# coding: utf-8
import logging
from pythonstudy_project import settings
from commons.dependency import provider
import boto3
from botocore.client import Config

logger = logging.getLogger('study.s3_op.core')

@provider('s3_client_api')
class BaseManager():
    def __init__(self):
        pass

    def create_client(self):
        # 创建s3链接，如果s3服务器是第四代，则需要设置signature_version='s3v4'
        s3_client = boto3.client('s3', endpoint_url=settings.s3_endpoint_url,
                                 aws_access_key_id=settings.s3_aws_access_key_id,
                                 aws_secret_access_key=settings.s3_aws_secret_access_key,
                                 region_name=settings.s3_region_name,
                                 config=Config(signature_version=settings.s3_signature_version))
        print settings.s3_endpoint_url
        print s3_client
        return s3_client


@provider('s3_api_manager')
class S3ApiManager:
    def __init__(self):
        pass
    # 获取bucket列表
    def get_bucket_list(self, s3client):
        '''
        获取bucket列表
        :param s3client:
        :return:
        '''
        bucket_list = s3client.list_buckets()
        return bucket_list
    # 判断bucket是否存在
    def isExist_bucket(self, bucket_name, s3client):
        try:
            bucket = s3client.head_bucket(Bucket=bucket_name)
            if bucket:
                return True
            else:
                return False
        except Exception as e:
            return False

    # 创建bucket（bucket名称中不能包含‘/’或者‘\’）
    def create_bucket(self, bucket_name, s3client):
        bucket = s3client.create_bucket(Bucket=bucket_name)
        return bucket

    # 删除bucket
    def delete_bucket(self, bucket_name, s3client):
        bucket = s3client.delete_bucket(Bucket=bucket_name)
        return bucket
    #获取bucket信息
    def get_bucket(self, bucket_name, s3client):
        bucket = s3client.head_bucket(Bucket=bucket_name)
        return bucket

    #根据bucket名称获取当前bucket下面的object列表
    def get_object_list_by_bucket(self, bucket_name, s3client):
        object_list = s3client.list_objects(Bucket=bucket_name)
        return object_list

    # 判断bucket下的object是否存在,key为上传文件对应的key值
    def isExist_bucket_object(self, bucket_name, key, s3client):
        try:
            bucket_object = s3client.get_object(Bucket=bucket_name, Key=key)
            if bucket_object:
                return True
            else:
                return False
        except Exception as e:
            return False

    # 获取bucket下面的object信息
    def get_bucket_object(self, bucket_name, key, s3client):
        bucket_object = s3client.get_object(Bucket=bucket_name, Key=key)
        return bucket_object

    # 上传文件并创建文件对应的key
    # file_upload_source：需要上传的文件地址
    # bucket：bucket名称
    # key：上传文件在s3中对应的key
    # s3client：s3客户端
    # extra_args扩展属性，如果不传，这里默认文件权限是公有只读
    # callback：回调类方法
    def upload_file(self, file_upload_source, bucket, key, s3client, extra_args=None, callback=None):
        if extra_args is None:
            extra_args = {'ACL': 'public-read'}
        s3client.upload_file(file_upload_source, bucket, key, ExtraArgs=extra_args, Callback=callback)

    # 删除object
    def delete_object(self, bucket, key, s3client):
        object_info = s3client.delete_object(Bucket=bucket, Key=key)
        return object_info
    # 下载文件
    # file_download_source：文件需要下载到的地址名称
    # bucket：bucket名称
    # key：上传文件在s3中对应的key
    # s3client：s3客户端
    # extra_args扩展属性，如果不传，这里默认文件权限是公有只读
    # callback：回调类方法
    def download_file(self, bucket, key, file_download_source, s3client, extra_args=None, callback=None):
        s3client.download_file(bucket, key, file_download_source, ExtraArgs=extra_args, Callback=callback)


