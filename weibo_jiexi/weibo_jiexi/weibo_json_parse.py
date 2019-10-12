#coding=utf-8
import time
from database.models import Dynamic,Dynamicsource,Media,MediaManyDyanmic
from database.db import session
#from PIL import Image

from imagehash import phash, average_hash,hex_to_hash
import requests
from PIL import Image
from io import BytesIO
import imagehash
lists={'release_time': 1570502423, 'release_state': None, 'is_repost': None, 'weibo': 1, 'data': '#荷兰弟寸头# 近日，“荷兰弟”汤姆·霍兰德在新片《Cherry》中的造型曝光，他将原先的卷毛剃成了寸头，看起来硬气十足。《Cherry》由罗素兄弟执导，改编自Nico Walker的同名小说，讲述了荷兰弟饰演的男主角因PTSD影响，从一名军医变成抢劫银行的盗贼的故事。荷兰弟新片演军人剃成圆寸头 守望好莱坞的微博视频 ',
       'share_image_url': '', 'create_time': None, 'media_id': [{'url': 'https://ww3.sinaimg.cn/bmiddle/75b45de6ly1g71foxotjij20p018gwj1.jpg', 'is_video': False}],
       'label_id': None, 'other_keyword': None, 'source': '新浪娱乐', 'star_keyword': None, 'dynamicsource_id': 1, 'url': 'https://m.weibo.cn/detail/44093sy83s4s55'}
class JsonParser():
    def __init__(self,lists):
        self.lists=lists

    def get_dynamic(self):
        if not lists:
            return
        url = self.lists.get("url")
        all_data=session.query(Dynamic).filter(Dynamic.url==url).all()
        if all_data:
            return
        dy_model=Dynamic()
        dy_model.url = url
        dy_model.release_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.lists.get('release_time')))
        dy_model.release_state= 0
        dy_model.weibo = self.lists.get("weibo")
        dy_model.data = self.lists.get("data")
        dy_model.share_image_url = self.lists.get("share_image_url")
        dy_model.create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        dy_model.source = self.lists.get("source")
        dy_model.dynamicsource_id = self.lists.get("dynamicsource_id")
        dy_model.description=self.lists.get("description")
        dy_model.correct_state=0
        dy_model.read_amount=0
        dy_model.updata_data=dy_model.data
        session.add(dy_model)
        try:
            session.flush()
        except:
            session.rollback()
        if self.lists.get("media_id") and dy_model.id:
            medias=self.lists.get("media_id")
            self.save_media(dy_model,medias)
        try:
            session.commit()
        except:
            session.rollbock()
    #图片视频存库
    def save_media(self,dy_model,medias):
        if not medias:
            return
        for media in medias:
            #视频存库
            if media.get("is_video") == True:
                media_model = Media()
                media_model.is_picture=0
                url=media.get("url")
                if not url:
                    continue
                media_model.url = media.get("url")
                media_model.hash = None
                session.add(media_model)
                try:
                    session.flush()
                except:
                    session.rollback()
                md = MediaManyDyanmic()
                md.media_id = media_model.id
                md.dynamic_id = dy_model.id
                session.add(md)
            #图片存库
            else:
                url = media.get("url")
                if not url:
                    continue
                #生成图片哈希值
                hash_value = self.get_hash(url)
                #判断图片哈希值相似度
                media_id=self.parse_hash(hash_value)
                #存在相似图片
                if media_id:
                    md=MediaManyDyanmic()
                    md.media_id=media_id
                    md.dynamic_id=dy_model.id
                    session.add(md)
                #不存在相似图片
                else:
                    media_model = Media()
                    media_model.hash=str(hash_value)
                    media_model.url = url
                    media_model.is_picture = 1
                    session.add(media_model)
                    try:
                        session.flush()
                    except:
                        session.rollback()
                    md=MediaManyDyanmic()
                    md.media_id=media_model.id
                    md.dynamic_id=dy_model.id
                    session.add(md)
    #比较hash值
    def parse_hash(self,hash1):
        models=session.query(Media).all()
        for model in models:
            if model.is_picture==1 and model.hash:
                hash2=hex_to_hash(model.hash)
                value = 1 - (hash1 - hash2) / len(hash1.hash) ** 2
                if value > 0.9:
                    return model.id
        return None
    #获取hash值
    def get_hash(self,url):
        content=requests.get(url).content
        image1 = Image.open(BytesIO(content))
        hash = (phash(image1, highfreq_factor=4))
        return hash
if __name__=="__main__":
    js=JsonParser(lists)
    js.get_dynamic()

#itemid=1001030111_0_0_seqid:1856695219|type:1|t:|pos:1-0-0|q:新浪电影|ext:&cate=1&uid=1623886424&qri=0&qtime=1570527248&
#itemid=1001030111_0_0_seqid:1331644219|type:1|t:|pos:1-0-0|q:新浪体育|ext:&cate=1&uid=1638781994&qri=524288&qtime=1570527568&



# content = requests.get('https://ww2.sinaimg.cn/bmiddle/75b45de6ly1g71foxotjij20p018gwj1.jpg').content
# image1 = Image.open(BytesIO(content))
# conteng2 = requests.get('https://ww2.sinaimg.cn/bmiddle/75b45de6ly1g71foxotjij20p018gwj1.jpg').content
conteng2 = requests.get('https://ww2.sinaimg.cn/bmiddle/75b45de6ly1g71foxzwwzj20p018g43h.jpg').content
image2 = Image.open(BytesIO(conteng2))
# hash1 = (phash(image1, highfreq_factor=4))
# print(hash1)
# from imagehash import hex_to_hash
# hash1="81337fa468d9269e"
# hash1=hex_to_hash(hash1)
# hash2 = (phash(image2, highfreq_factor=4))
# value=1 - (hash1 - hash2)/len(hash1.hash)**2
# print(value)

