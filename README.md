## 阿里飞燕web接口sdk

## 快速开始
```python
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

    res = client.cloud_thing_product_list_get(params=params)  # 调用接口
    print(res)

```

## 特点
* 自动管理token
> 可以使用feiyan.session.redisstorage中的RedisStorage，
也可以自定义 Storage, 将token放在你想放的地方

```python
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

```
* 接口对应函数名灵活
> 对于接口 **/cloud/thing/productList/get**

```
可以使用 client.cloud_thing_productlist_get
也可以使用 client.cloud_thing_productList_get
也可以使用 client.cloud_thing_product_list_get 进行调用
其实只要，函数名中的字符串(不包含/ - _)和接口中的字符串一致即可(不包含/ - _)
使用client.cloudthingproductlistget 也可以完成调用
```

### 阿里飞燕文档

[阿里飞燕云端接口文档地址](https://living.aliyun.com/doc?spm=a2c7x.12548000.0.0.688b7946xoqUml#xm15ag.html)


