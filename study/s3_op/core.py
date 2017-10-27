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

    def get_bucket_list(self, s3client):
        '''
        获取bucket列表
        :param s3client:
        :return:
        '''
        bucket_list = s3client.list_buckets()
        return bucket_list

