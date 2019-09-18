import sys
# sys.path.append('/home/xiangmu/bitexiangmu/hanyu')
import redis
from urllib import parse
import time
import datetime
from weibos.database.models import Source
from weibos.database.db import session


class Master():

    def __init__(self):
        self.r = redis.Redis(host="47.110.95.150", port=6379, password="Bitgraph818")
        self.CELEBRITY_NEWS_API_URL = 'https://m.weibo.cn/api/container/getIndex?uid={}&luicode=10000011&lfid=100103type%3D1%26q%3D{}&type=uid&value={}&containerid={}&page={}'

    def weibo_redis(self):
        models = session.query(Source).all()
        for model in models:
            if model.container_id:
                weiboid = parse.quote(model.weibo_id)
                weibo_burl = self.CELEBRITY_NEWS_API_URL.format(str(model.weibo_additional_id), weiboid,
                                                                str(model.weibo_additional_id), model.container_id, "")
                self.r.rpush("weibo:start_urls", weibo_burl)



ms = Master()
ms.weibo_redis()


