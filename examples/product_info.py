from feiyan.fy_client import FyClient
from feiyan.session.redisstorage import RedisStorage
import redis

if __name__ == '__main__':
    FEIYAN_TMALL_API_APP_KEY = ''
    FEIYAN_TMALL_API_APP_SECRET = ''
    FEIYAN_TMALL_PROJECT_ID = ''

    redis_storage = RedisStorage(redis.Redis())  # 使用 redis 存储 token
    client = FyClient(app_key=FEIYAN_TMALL_API_APP_KEY, app_secret=FEIYAN_TMALL_API_APP_SECRET,
                      project_res=FEIYAN_TMALL_PROJECT_ID, storage=redis_storage)

    params = {
        'productInfoQuery': {
            "pageNo": 1,
            "pageSize": 10
        }
    }
    """
    调用接口 /cloud/thing/productList/get
    把接口地址的的 '/' 去掉换为 '_' 即为函数名， 函数名不区分大小写
    cloud_thing_productlist_get
    cloud_thing_productList_get  都可以
    """
    res = client.cloud_thing_productlist_get(params=params)  # 调用接口
    print(res)
