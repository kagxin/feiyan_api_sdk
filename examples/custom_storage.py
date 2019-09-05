from feiyan.session import SessionStorage
from django.core.cache import cache
from feiyan.fy_client import FyClient


class CustomStorage(SessionStorage):
    """
    使用django cache 存储token, 实现 get,set,delete 三个函数
    """
    def get(self, key, default=None):
        return cache.get(key)

    def set(self, key, value, ttl=None):
        cache.set(key, value, timeout=ttl)

    def delete(self, key):
        cache.delete(key)


if __name__ == '__main__':
    FEIYAN_TMALL_API_APP_KEY = ''
    FEIYAN_TMALL_API_APP_SECRET = ''
    FEIYAN_TMALL_PROJECT_ID = ''

    redis_storage = CustomStorage()  # 使用 redis 存储 token
    client = FyClient(app_key=FEIYAN_TMALL_API_APP_KEY, app_secret=FEIYAN_TMALL_API_APP_SECRET,
                      project_res=FEIYAN_TMALL_PROJECT_ID, storage=redis_storage)
