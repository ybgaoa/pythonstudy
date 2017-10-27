# coding: utf-8
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from commons.dependency import get_provider
# 初始化日志
logger = logging.getLogger('study.s3_op.views')

class BucketListView(APIView):
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
