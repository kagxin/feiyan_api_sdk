from feiyan.client.client import DefaultClient
from feiyan.client.request import Request
from feiyan.common import constant
from feiyan.exceptions import GetTokenException, GetDataException
from functools import partial

URLS = (
    '/cloud/thing/productList/get',  # 查询物的产品列表
    '/cloud/thing/product/get',  # 查询物的产品
    '/cloud/amount/device/generate',  # 云端开放的产品量产接口
    '/cloud/device/name/upload',  # 上传三元组设备名称列表获取批次号
    '/cloud/name/device/generate',  # 云端开放的产品量产接口
    '/cloud/thing/properties/get',  # 获取物的属性
    '/cloud/thing/tsl/get',  # 获取物的模板
    '/cloud/thing/service/invoke',  # 触发物的服务
    '/cloud/thing/properties/set',  # 设置物的属性
    '/cloud/thing/status/get',  # 获取物的连接状态
    '/cloud/thing/info/get',  # 获取物的基本信息
    '/cloud/things/get',  # 批量获取物
    '/cloud/thing/event/timeline/get',  # 获取物的事件timeline数据
    '/cloud/thing/property/timeline/get',  # 获取物的属性timeline数据
    '/cloud/account/queryIdentityByPage',  # 分页查询用户列表
    '/cloud/account/getByOpenId',  # 通过三方外标查询账号信息
    '/cloud/device/queryByUser',  # 获取用户绑定的设备列表（包括设备详情）详情内容
    '/cloud/user/device/unbind',  # 解绑用户和设备
    '/cloud/account/openId/getByIdentityId',  # 根据身份id获取第三方openid
    '/living/user/device/binding/query',  # 根据设备查找所有绑定的用户
    '/cloud/account/getByIdentityId',  # 通过identityid查询账户的详细信息
    '/cloud/account/getByIdentityId',  # 通过identityid查询账户的详细信息
    '/user/account/info/update',  # 更新自有账号系统在飞燕内的用户昵称
)


def es_string(s, *sep):
    """
    es_string(s_str, '_', '-', ':', '：', '-')
    去除s_str中的'_', '-', ':', '：', '-'
    :param s:
    :param sep:
    :return:
    """
    for se in sep:
        s = ''.join(s.split(se))
    return s


class FyClient(DefaultClient):
    def __init__(self, app_key, app_secret, project_res, host='https://api.link.aliyun.com',
                 storage=None):
        super(FyClient, self).__init__(app_key=app_key, app_secret=app_secret)
        self.project_res = project_res
        self.storage = storage
        self.host = host
        self.urls = {(''.join(url.split('/'))).lower(): url for url in URLS}

    def _execute(self, url, params=None, token=None, version=None):
        token = token if token else self.access_token
        fy_request = Request()
        fy_request.set_host(self.host)
        fy_request.set_method('post')
        fy_request.set_protocol(constant.HTTPS)
        fy_request.set_content_type(constant.CONTENT_TYPE_JSON)
        fy_request.set_url(url)
        fy_request.set_cloud_token(token)
        fy_request.set_params(params)
        fy_request.format_params()
        if version:
            fy_request.set_api_ver(version)
        response = super().execute(fy_request)
        if response.status_code != 200:
            raise GetDataException('get data failed.')
        data = response.json()
        return data

    @property
    def access_token_key(self):
        return '{0}_access_token'.format(self.project_res)

    def get_token(self, version='1.0.0'):
        """
        获取token
        :param version:
        :return:
        """
        url = '/cloud/token'
        params = {
            'grantType': 'project',
            'res': self.project_res
        }
        fy_request = Request()
        fy_request.set_host(self.host)
        fy_request.set_method('post')
        fy_request.set_protocol(constant.HTTPS)
        fy_request.set_content_type(constant.CONTENT_TYPE_JSON)
        fy_request.set_url(url)
        fy_request.set_params(params)
        fy_request.format_params()
        fy_request.set_api_ver(version)
        res = super().execute(fy_request)
        if res.status_code != 200:
            raise GetDataException('get data failed.')

        data = res.json()
        code = data['code']
        if code != 200:
            GetTokenException('get token failed. code:{}'.format(code))
        return data['data']['cloudToken'], data['data']['expireIn']

    @property
    def access_token(self):
        """
        从storage中获取token，过期更新token，没有配置storage就直接通过接口获取
        :return:
        """
        if self.storage:
            access_token = self.storage.get(self.access_token_key)
            if not access_token:
                access_token, expires = self.get_token()
                self.storage.set(self.access_token_key, access_token, expires - 10)
        else:
            access_token, _ = self.get_token()

        return access_token

    def __getattr__(self, item):

        url = (es_string(item, '_')).lower()

        if url not in self.urls:
            raise AttributeError('not such attr {}'.format(item))

        return partial(self._execute, self.urls[url])
