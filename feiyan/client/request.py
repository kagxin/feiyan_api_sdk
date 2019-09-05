from feiyan.common import constant
import time
import json


class Request:
    content_md5 = "Content-MD5"
    content_length = "Content-Length"
    content_type = "Content-Type"

    def __init__(self, host=None, protocol=constant.HTTPS, headers=None, url=None, method=None, time_out=None):
        if headers is None:
            headers = {}
        self.__host = host
        self.__url = url
        self.__method = method
        self.__time_out = time_out
        self.__headers = headers
        self.__body = None
        self.__content_type = None
        self.__query_str = None
        self.__protocol = protocol
        self.__params = dict()
        self.__cloudToken = None
        self.__version = '1.0'
        self.__apiVer = '1.0.0'

    def get_protocol(self):
        return self.__protocol

    def set_protocol(self, protocol):
        self.__protocol = protocol

    def get_method(self):
        return self.__method

    def set_method(self, method):
        self.__method = method.upper()

    def get_host(self):
        return self.__host

    def set_host(self, host):
        self.__host = host

    def get_url(self):
        return self.__url

    def set_url(self, url):
        self.__url = url

    def get_time_out(self):
        return self.__time_out

    def set_time_out(self, time_out):
        self.__time_out = time_out

    def get_content_type(self):
        return self.__content_type

    def set_content_type(self, content_type):
        self.__content_type = content_type

    def get_headers(self):
        return self.__headers

    def set_headers(self, headers=None):
        if headers is None:
            headers = {}
        self.__headers = headers

    def get_query_str(self):
        return self.__query_str

    def set_query_str(self, query_str=None):
        self.__query_str = query_str

    def set_body(self, body):
        self.__body = body

    def get_body(self):
        return self.__body

    def set_version(self, version):
        self.__version = version

    def get_version(self):
        return self.__version

    def set_api_ver(self, api_ver):
        self.__apiVer = api_ver

    def get_api_ver(self):
        return self.__apiVer

    def set_cloud_token(self, cloud_token):
        self.__cloudToken = cloud_token

    def get_cloud_token(self):
        return self.__cloudToken

    def add_param(self, k, v):
        self.__params[k] = v

    def set_params(self, params):
        self.__params = params

    def get_params(self):
        return self.__params

    def format_params(self):
        body = {
            "id": int(time.time() * pow(10, 6)),
            "version": self.get_version(),
            "request": {
                "apiVer": self.get_api_ver(),

            },
            "params": self.get_params()
        }
        token = self.get_cloud_token()
        if token:
            body['request'].update({"cloudToken": self.get_cloud_token()})
        self.set_body(json.dumps(body))
