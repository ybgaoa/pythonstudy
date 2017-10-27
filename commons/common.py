# -*- coding: utf-8 -*+
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
import logging
from keystoneclient.v3 import client
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import APIException
from cloudgo_project import settings
from commons import constant
from rest_framework import permissions
import time
import xlwt
import StringIO
from django.http import HttpResponse

from commons.dependency import get_provider
JSON_CONTENT_TYPE = "application/json"

# 初始化日志
logger = logging.getLogger('pythonstudy.common')


# 获取分页
def getPage(request, obj):
    paginator = Paginator(obj, 2)
    try:
        page = int(request.GET.get('page', 1))
        obj = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        obj = paginator.page(1)
    return obj


# datetime转化时间戳
def trans_time_format(datetime):
    mytime = time.strptime(datetime, '%Y-%m-%dT%H:%M:%S.%f')
    # tmytime = time.strftime("%Y-%m-%d %H:%M:%S", mytime)
    tmytime = time.mktime(mytime)
    return tmytime


def trans_time(datetime):
    mytime = time.strptime(datetime, '%Y-%m-%dT%H:%M:%S')
    tmytime = time.mktime(mytime)
    return tmytime


def trans_time_formation(datetime, format):
    mytime = time.strptime(datetime, format)
    tmytime = time.mktime(mytime)
    return tmytime


# 设置操作日志
# def setOperationLog(user_id, file_name, module_name, message_content):
#     op_log = OperationLog()
#     op_log.user_id = user_id
#     op_log.file_name = file_name
#     op_log.module_name = module_name
#     op_log.message_content = message_content
#     op_log.save()
#

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    # max_page_size = 50


class PorcessingException(APIException):
    """
    与业务相关的异常的基类，需要依据实际需求子类化这个基类，要在子类中提供biz_code和default_detail的属性值。
    该父类继承自Rest framework的APIException类，所以，它的status_code的值默认是500；biz_code是与业务相关的
    错误码，目前预计的设计是：1XXX是与pastry相关的异常；2XXX是云主机相关异常；3XXX是容器相关异常。。。。。
    """
    proc_code = None

    def __init__(self):
        r = {'status_code': self.status_code}
        if self.proc_code:
            r.__setitem__('proc_code', self.proc_code)
        r.__setitem__('detail', self.default_detail)
        self.detail = r

    def __str__(self):
        if self.proc_code:
            return str(self.proc_code) + "  " + super(PorcessingException, self).__str__()
        else:
            return super(PorcessingException, self).__str__()


class PServiceUnavailable(PorcessingException):
    status_code = 401
    proc_code = 1503
    default_detail = u'服务临时不可用，请稍候再试。'


class PNoContent(PorcessingException):
    status_code = 204
    proc_code = 1204
    default_detail = u'没有数据。'


class VMServiceUnavailable(PorcessingException):
    proc_code = 2503
    default_detail = u'服务临时不可用，请稍候再试。'


def get_header(request):
    head = {}
    head['token'] = request.META.get(constant.X_AUTH_TOKEN, None)
    head['workspace_id'] = request.META.get(constant.X_WORKSPACE_ID, None)
    head['region_name'] = request.META.get(constant.X_REGION_ID, None)
    #     head['user_region_id'] = request.META.get(constant.X_USER_REGION_ID,None)
    return head


def get_cloud_provider_header(request):
    cloud_provider_id = request.META.get(constant.X_CLOUD_PROVIDER_ID, None)
    return cloud_provider_id


class WorkspaceRole:
    def __init__(self):
        pass

    @property
    def owner(self):
        return 'owner'

    @property
    def manager(self):
        return 'manager'

    @property
    def member(self):
        return 'member'


class ProjectRole:
    def __init__(self):
        pass

    @property
    def owner(self):
        return 'owner'

    @property
    def manager(self):
        return 'manager'

    @property
    def member(self):
        return 'member'


class WorkspacePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        data = request.data
        workspace_id = ""
        user_id = ""
        role = "owner"

        if request.method in permissions.SAFE_METHODS:
            return True

        return role == WorkspaceRole().owner or role == WorkspaceRole().manager


class ProjectPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        data = request.data
        project_id = ""
        user_id = ""
        role = "owner"

        if request.method in permissions.SAFE_METHODS:
            return True

        return role == ProjectRole().owner or role == ProjectRole().manager


class AdminRole:
    def __init__(self):
        pass

    @property
    def admin(self):
        return 'admin'


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # if safe request，return true
        if request.method in permissions.SAFE_METHODS:
            return True
        data = request.data
        user_id = ''
        user_info = get_data_by_token(request).get('user')
        role = user_info.get('target')
        return role == AdminRole().admin


class RepoPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        permission_flag = False

        workspace_id = get_header(request)['workspace_id']
        user = get_provider('user_info_api').get_userinfo_by_token(request)
        # workspace_role = get_provider('pro_api').get_role_in_workspace(request, workspace_id)
        workspace_role = get_provider('user_info_api').get_role_in_workspace(request, workspace_id)
        if workspace_role in ['owner', 'admin']:
            permission_flag = True
        else:
            projects = get_provider('proj_api').get_pro_by_workspace(
                    user_id=user.get('id'),
                    user_type=user.get('type'),
                    workspace_id=workspace_id
            )
            project_role = None
            for project in projects:
                p_role = get_provider('user_info_api').get_role_in_project(request, project_id=project.id)
                if project_role is None or project_role == p_role or get_provider('repo_api').project_role_comp(p_role,
                                                                                                                project_role):
                    project_role = p_role

            if project_role in {'owner', 'admin', 'CMO'}:
                permission_flag = True

        return permission_flag


def get_data_by_token(request):
    endpoint = settings.AUTH_URL
    token = get_header(request).get('token')
    ks = client.Client(endpoint=endpoint, token=token)
    return ks.tokens.get_token_data(token=token).get('token')


def get_excel_response(name, titles, rows, column_widths=None, **style):
    """   edit by xbwangh 2016-12-7
    公共接口： 获取导出Excel的response对象，利用该对象可直接在浏览器实现下载功能
    *******************************注意问题******************************
    *   1, 参数titles存放在字典data中,该参数是Excel列表头,只接受list数组    *
    *   2, name是生成Excel的文件名称                                     *
    *   3, rows是Excel数据行，只接受数组方式                              *
    *   4, 该导出方式只针对于单个sheet的excel                             *
    *   5, 如果需要修改excel样式，只需将样式参数放置于style字典中即可        *
    *               Example Param Value :                              *
    *               name = eg_name                                     *
    *               titles = ['titleA', 'titleB', 'titleC']            *
    *               rows = [['rowA1', 'rowA2','rowA3'],                *
    *                       ['rowB1', 'rowB2','rowB3'],                *
    *                       ['rowC1', 'rowC2','rowC3']                 *
    *                      ]                                           *
    *               column_widths = [20, 50, 40, 0]                    *
    *               style={'horz_align':'HORZ_CENTER'}                 *
    *   6, 列宽如果想使用默认值, 则设置为0即可                             *
    ********************************************************************
    """
    # 需要注意的是：参数rows titles必须是list类型，否则抛出异常
    if isinstance(titles, list) is False:
        raise Exception('Error Data Format : Error Format Of Param Column Title')
    if isinstance(rows, list) is False:
        raise Exception('Error Data Format : Error Format Of Param Row Data')
    # 名称非空校验
    if name is None:
        raise Exception('None Param : Param Excel Name Is None')
    # 如果列宽不为空，则必须是list类型
    if column_widths is not None and isinstance(column_widths, list) is False:
        raise Exception('Error Data Format : Error Format Of Param ColumnWidths Data')
    param_horz_alignment = style.get('horz_align')
    horizen_aligments = ['HORZ_GENERAL', 'HORZ_LEFT', 'HORZ_CENTER', 'HORZ_RIGHT', 'HORZ_FILLED',
                         'HORZ_JUSTIFIED', 'HORZ_CENTER_ACROSS_SEL', 'HORZ_DISTRIBUTED']
    if param_horz_alignment is not None and param_horz_alignment not in horizen_aligments:
        raise Exception('Error Data Format : Param style.horz_align Is Not In Specify Value')
    # 这里响应对象获得了一个特殊的content_type类型, 告诉浏览器这是个excel文件不是html
    response = HttpResponse(content_type='application/vnd.ms-excel')
    # 这里响应对象获得了附加的Content-Disposition协议头,它含有excel文件的名称,文件名随意,
    # 当浏览器访问它时,会以"另存为"对话框中使用它.
    response['Content-Disposition'] = 'attachment;filename={0}.xls'.format(name)
    # 设置Excel编码为utf-8
    wb = xlwt.Workbook(encoding='utf-8')
    # 默认情况下，Excel只有一个sheet，如果有多个，依次添加即可
    sheet = wb.add_sheet('sheet1')
    if column_widths is not None:
        for index, width in enumerate(column_widths):
            # width = 256*20  256为衡量单位，20表示20个字符宽度
            # width如果设置为0则使用默认宽度
            if width != 0:
                sheet.col(index).width = 256 * width
    # 设置对齐样式，默认居中对齐
    alignment = xlwt.Alignment()
    # 水平居中
    alignment.horz = xlwt.Alignment.HORZ_CENTER if param_horz_alignment is None else param_horz_alignment
    style = xlwt.XFStyle()
    style.alignment = alignment
    # 向excel中写入行标题
    for index, title in enumerate(titles):
        sheet.write(0, index, title, style)
    # 向Excel中写入行数据
    for i, row in enumerate(rows):
        for j, column in enumerate(row):
            sheet.write(i + 1, j, column, style)
    output = StringIO.StringIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response


def get_project_user_owner(request, project_id):
    endpoint = settings.AUTH_URL
    token = get_header(request).get('token')
    ks = client.Client(endpoint=endpoint, token=token)
    list_users = ks.projects.get_users_by_project(project_id)
    if list_users:
        for user in list_users:
            for role in user.roles:
                # 这个用户对project是owner角色
                if role["name"] == "owner":
                    if user.to_dict().get("type") is None or user.to_dict().get("type") == 2:
                        return user.id
