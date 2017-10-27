# coding: utf-8
from django.db import models


# 操作日志
# class OperationLog(models.Model):
#     user_id = models.IntegerField(verbose_name='操作人id')
#     op_date = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
#     file_name = models.CharField(max_length=64, verbose_name='文件名称')
#     module_name = models.CharField(max_length=64, verbose_name='模块名称')
#     message_content = models.TextField(verbose_name='信息内容')
#
#     class Meta:
#         verbose_name = '操作日志'
#         verbose_name_plural = verbose_name
#         db_table = 'pastry_log'
#
#     def __unicode__(self):
#         return str(self.user_id)
#

# 基础抽象模型
class BaseModel(models.Model):
    """
    abstract base class, 提供创建人，创建时间和修改人，修改时间四个通用的field
    """
    created_by = models.CharField(max_length=64, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by = models.CharField(max_length=64, blank=True, null=True, verbose_name='修改人')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='修改时间',null=True)

    class Meta:
        abstract = True
