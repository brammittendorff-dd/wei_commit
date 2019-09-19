# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/commit/wei_commit/weibos')
import scrapy
import redis
import re
import json
import requests
import datetime
import time
import random
import os
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support.wait import WebDriverWait
from urllib import parse
from scrapy_redis.spiders import RedisSpider
from weibos.database.db import session
from weibos.database.models import Source,Dynamic,Cookies
from weibos.items import WeibosItem
class WeiboSpider(RedisSpider):

    name = 'weibo'
    allowed_domains = ['weibo.cn']
    #start_urls = ['https://m.weibo.cn/']
    redis_key = 'weibo:start_urls'
    CELEBRITY_NEWS_API_URL = 'https://m.weibo.cn/api/container/getIndex?uid={}&luicode=10000011&lfid=100103type%3D1%26q%3D{}&type=uid&value={}&containerid={}&page={}'
                            #'https://m.weibo.cn/api/container/getIndex?uid={}&luicode=10000011&lfid=100103type%3D1%26q%3D{}&type=uid&value={}&containerid={}&page={}
    # CELEBRITY_NEWS_API_URL = 'https://m.weibo.cn/api/container/getIndex?uid=' + str(
    #     model.weibo_additional_id) + '&luicode=10000011&lfid=100103type%3D1%26q%3D' + weiboid + '&type=uid&value=' + str(
    #     model.weibo_additional_id) + '&containerid=' + model.container_id
    custom_settings = {
        "CONCURRENT_REQUESTS": 5,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        },
        #'COOKIES_ENABLED': False,

        "ITEM_PIPELINES": {
            'weibos.pipelines.WeibosPipeline': 1,
            'scrapy_redis.pipelines.RedisPipeline': 100,
        },
        "LOG_LEVEL": "DEBUG",
        "SCHEDULER_QUEUE_CLASS": "scrapy_redis.queue.SpiderPriorityQueue",
        "SCHEDULER_PERSIST": True,
        "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        # #     # 先进先出队列
        # "SCHEDULER_QUEUE_CLASS" : "scrapy_redis.queue.SpiderQueue",
        # #
        #     # 先进后出栈
        # "SCHEDULER_QUEUE_CLASS" : "scrapy_redis.queue.SpiderStack",
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        "REDIS_HOST": '47.110.95.150',
        "REDIS_PORT": 6379,
        # "REDIS_URL":"redis://root:123456789@39.106.214.65",
        "REDIS_PARAMS" :{
        'password': 'Bitgraph818'
    }
    }
    def __init__(self):
        self.r = redis.Redis(host="47.110.95.150", port=6379,password="Bitgraph818")
        self.s = requests.session()
        self.s.verify=False
        self.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"

        }
        self.BASE_URL = "https://m.weibo.cn"
    #从redis拿取链接抓取
    def start_requests(self):
        res=self.r.lpop('weibo:start_urls')
        if not res:
            return
        url=res.decode()



        yield scrapy.Request(url=url,callback=self.parse,headers=self.headers,dont_filter=True)

    def parse(self, response):
        cookies = self.up_cookies()
        print(response.meta)
        meta = response.meta
        #匹配containerid
        con_id=re.search('containerid=(.*?)&',response.url).group(1)
        #搜索此id在source表中model
        model=session.query(Source).filter(Source.container_id == con_id).first()
        onepage=re.search('&page=(.*)',response.url).group(1)
        # #判断是否为首页
        #TODO 链接去重
        if not onepage:
            if model:
                lists=[]
                #拿到此id所有动态
                models = session.query(Dynamic).filter(Dynamic.source_id == model.id).all()
                for i in models:
                    if i.tw_or_ins == 3:
                        lists.append(i.weibo_url)
                if lists:
                    meta["urls"] = lists
                else:
                    meta["urls"] = []
        meta["model"]=model
        #meta["type"] = json.dumps(["hanyu"])
        res=json.loads(response.text)
        #print(res)
        if res['ok'] == 1:
            cards = res['data']['cards']
        else:
            return
        for card in cards:
            if card['card_type'] == 9:
                mblog = card.get('mblog')
                if not mblog:
                    return
                if 'retweeted_status' in mblog:
                    #print(22222222222222222)
                    item=self.parse_retweet(mblog, meta)
                    if not item:
                        continue
                    if item==100:
                        return
                    item=self.to_item(item)
                    #print(item)
                    yield item
                else:
                    item = self.parse_status(mblog, meta)
                    if not item:
                        continue
                    item=self.to_item(item)
                    if item==100:
                        return
                    #print(item)
                    yield item

        try:
            print(res['data']['cardlistInfo'])
            page = res['data']['cardlistInfo']['page']
            print(page)
            if page and page<11:
                weiboid = parse.quote(model.weibo_id)
                #meta = {"model": model}
                url = self.CELEBRITY_NEWS_API_URL.format(str(model.weibo_additional_id), weiboid,
                                                         str(model.weibo_additional_id), model.container_id, str(page))
                yield scrapy.Request(url=url, meta=meta, headers=self.headers,callback=self.parse,dont_filter=True
                                     )
        except:
            print("数据已抓取完")
            session.rollback()
            return
    def now_timestamp(self,release_time):
        #this_date = datetime.datetime.strptime(str(release_time), "%Y-%m-%d %H:%M:%S")
        timeArray = time.strptime(str(release_time), "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    def parse_retweet(self, mblog: dict, meta):
        model = self.parse_status(mblog, meta)
        if not model:
            return
        model["is_repost"] = True
        retweeted_status = mblog.get('retweeted_status')
        retweeted_model = self.parse_status(retweeted_status,meta)
        model["retweeted_status"] = retweeted_model
        # model.source_id = retweeted_model.id
        # session.add(model)
        #print(model)
        return model


    def parse_status(self, mblog, model=None):
        item={}
        try:
            mid=mblog.get('mid')
            item["weibo_url"]="https://m.weibo.cn/detail/"+str(mid)
            if item["weibo_url"] in model["urls"]:
                print(5555555555555555)
                return
            item["release_time"] = self.generate_timestamp(mblog)
            #print(item["release_time"],model["model"].last_weibo_timestamp)
            # if int(item["release_time"]) < model["model"].last_weibo_timestamp:
            #     return
            #时间戳判断爬去
            # if int(item["release_time"]) < 1564773839:
            #     print(66666666666)
            #     return
            #self.update(model["model"],item)
            item["weibo_id"] = mblog.get('user').get('id')
            item["nick_name"] = mblog.get('user').get('screen_name')
            avatar_url = mblog.get('user').get('profile_image_url')
            # target_path=os.path.join(os.getcwd()+"/weibo",str(model["model"].id))
            # if not os.path.isdir(target_path):
            #     os.mkdir(target_path)
            # avatar_url = upload_weibo_media(avatar_url,target_path)
            item["avatar_url"] = avatar_url
            #os.remove(avatar_url[0].replace("\\", "/"))
            item["tw_or_ins"] = 3
            item["author_id_rl"] = model["model"].id
            # model.mid = mblog.get('mid')
            text = mblog.get('text')
            str_first = re.sub('<.*?>', "", text)
            item["data_en"] = str_first
            item["type"]=json.dumps(["hanyu"])
            # model["data_ch"] = ""
            # model["data_en"]=""
            models = self.replace_media_url(model["model"],mblog)
            item["media_id"] = models
            item["is_repost"] = False
            #print(item)
            # print(model)
            return item
        except:
            return

    def generate_timestamp(self, mblog):
        #burl = "https://m.weibo.cn/status/{}".format(mblog.get('mid'))


        created_at = mblog.get('created_at')
        print(created_at)
        if not created_at:
            return int(time.time())
        if "+0800" not in created_at:
            burl = "https://m.weibo.cn/detail/{}".format(mblog.get('mid'))
            try:
                res = self.s.get(burl).text
                created_at = re.search('"created_at": "(.*?)"', res).group(1)
            except:
                time.sleep(2)
                try:
                    res = self.s.get(burl).text
                    created_at = re.search('"created_at": "(.*?)"', res).group(1)
                except:
                    print(burl)
                    print("ip被封了。。。。。。。。。")
                    created_at=int(time.time())
                    return created_at
        # print(created_at)
        if len(created_at.split(' ')) > 5:
            date = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
            # print(int(time.mktime(date.timetuple())))
            return int(time.mktime(date.timetuple()))
    def make_time(self, created_at, param):
        value = int(re.search('\d+', created_at).group())
        params = {param: value}
        post_time = (datetime.datetime.now() - datetime.timedelta(params))
        return int(time.mktime(post_time.timetuple()))

    def replace_media_url(self,model, mblog):
        result = list()
        #target_path = os.path.join(os.getcwd()+"/weibo", str(model.id))
        if not mblog:
            return mblog
        # if not os.path.isdir(target_path):
        #     os.mkdir(target_path)
        if 'pics' in mblog:
            for pic_list in mblog['pics']:
                item_model = dict()
                #result1 = upload_weibo_media( pic_list['url'], target_path)
                item_model["url"] = pic_list['url']
                item_model["pic_width"] = pic_list['geo']['width']
                item_model["pic_height"] = pic_list['geo']['height']
                item_model["is_video"]=False
                # model.large_width = pic_list['large']['geo']['width']
                # model.large_height = pic_list['large']['geo']['height']
                # url = pic_list['large']['url']
                # real_url = upload_media(url, self.target_path, large=True)
                #model.large_url = real_url
                #os.remove(result1[0].replace("\\", "/"))
                result.append(item_model)
        if 'page_info' in mblog and mblog['page_info']['type'] == 'video':
            media_info = mblog['page_info']['media_info']
            #cover_img_url = upload_media(mblog['page_info']['page_pic']['url'], self.target_path)
            if media_info['mp4_hd_url']:
                video_url = media_info['mp4_hd_url']
                #result = upload_weibo_media(self.s, media_info['mp4_hd_url'], self.target_path)
                #model["url"] = upload(result[0].replace("\\", "/"))
            elif media_info['mp4_720p_mp4']:
                video_url = media_info['mp4_720p_mp4']
                #result = upload_weibo_media(self.s, media_info['mp4_720p_mp4'], self.target_path)
                #model["url"] = upload(result[0].replace("\\", "/"))
            elif media_info['mp4_sd_url']:
                video_url = media_info['mp4_sd_url']
                #result = upload_weibo_media(self.s, media_info['mp4_sd_url'], self.target_path)
                #model["url"] = upload(result[0].replace("\\", "/"))
            else:
                return
            item_model = {}
            #model["url"] = cover_img_url
            # res = requests.get(video_url)
            # filename = video_url.split('/')[-1].split('?')[0]
            # video_name = os.path.join(target_path,  filename)
            #
            # with open(video_name, "wb") as f:
            #     f.write(res.content)
            item_model["url"] = video_url
            #os.remove(video_name.replace("\\","/"))
            item_model["is_video"]=True
            result.append(item_model)
        return result

    def to_item(self,item):
        twr_item=WeibosItem()
        #twr_item["author_id"] = scrapy.Field()
        #twr_item["source_id"] = scrapy.Field()
        twr_item["release_time"] = item.get("release_time")
        twr_item["release_state"] = item.get("release_state")
        #twr_item["read_amount"] = scrapy.Field()
        twr_item["is_repost"] = item.get("is_repost")
        twr_item["weibo_id"]=item.get("weibo_id")
        twr_item["tw_or_ins"] = item.get("tw_or_ins")
        twr_item["nick_name"]=item.get("nick_name")
        twr_item["author_id_rl"]=item.get("author_id_rl")
        #twr_item["correct_state"] = scrapy.Field()
        twr_item["data_en"] = item.get("data_en")
        twr_item["avatar_url"]=item.get("avatar_url")
        twr_item["media_id"] = item.get("media_id")
        twr_item["retweeted_status"]=item.get("retweeted_status")
        twr_item["type"] = item.get("type")
        twr_item["weibo_url"]=item.get("weibo_url")
        # twr_item["data_ch"] = scrapy.Field()
        # twr_item["share_image_url"] = scrapy.Field()
        # twr_item["create_time"] = scrapy.Field()
        # twr_item["description"] = scrapy.Field()
        return twr_item
    def update(self, model,item):
        release_time = item["release_time"]
        if release_time > model.last_weibo_timestamp:
            model.last_weibo_timestamp = release_time
            #session.commit()
        else:
            pass
    def up_cookies(self):

        cook = self.getcookies()
        username = cook.username
        #print(username)
        password = cook.password
        # self.star = star
        # self.target_path = os.path.join(os.getcwd(), str(3))

        # self.driver = webdriver.Chrome()
        cookies = self.get_cookie_from_db(cook)
        if not self.is_valid_cookie(cookies):
            print("正在登陆")
            cookies = self.login(cook, username, password)
            if not self.is_valid_cookie(cookies):
                cook = self.getcookies()
                username = cook.username
                # print(username)
                password = cook.password
                cookies = self.login(cook, username, password)
        # cookies = self.login()
        # TODO 将新获取的cookies存库
        #self.update_params()
        return cookies
        # self.sign_if_needed(cookies)
    def getcookies(self):
        cooks = session.query(Cookies).all()
        cook = random.choice(cooks)
        return cook

    # def fetch_scraped_mblog(self):
    #     result = session.execute('select mid from informations_sdynamicswb where star_id={}'.format(self.star.id)).fetchall()
    #     scraped_mblog_list = [str(item[0]) for item in result]
    #     return scraped_mblog_list
    #
    # def sign_if_needed(self, cookies):
    #     self.driver.get(CELEBRITY_NEWS_URL.format(self.star.container_id))
    #     for key, value in cookies.items():
    #         cookie = dict()
    #         cookie['name'] = key
    #         cookie['value'] = value
    #         self.driver.add_cookie(cookie)
    #
    #     self.driver.get(CELEBRITY_NEWS_URL.format(self.star.container_id))
    #     try:
    #         WebDriverWait(self.driver, 3).until(lambda d: d.find_element_by_class_name('nav-main'))
    #         WebDriverWait(self.driver, 3).until(lambda d: d.find_element_by_class_name('color-orange'))
    #         self.driver.find_element_by_css_selector('div[inline="1"]').click()
    #         time.sleep(1)
    #     except:
    #         pass
    #     finally:
    #         self.driver.quit()

    def update_params(self):
        base_headers = dict()
        # TODO 从存储地（数据库或代理地）获取UA
        # ua = self.fetch_from_somewhere()
        base_headers.update({'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 '
                                           'Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                                           'like Gecko) Chrome/73.0.3683.86 Mobile '
                                           'Safari/537.36'})
        base_headers.update({'MWeibo-Pwa': '1'})
        base_headers.update({'X-Requested-With': 'XMLHttpRequest'})
        base_headers.update({'Referer': 'https://m.weibo.cn/sw.js'})
        self.s.headers.update(base_headers)

    def is_valid_cookie(self, cookie):
        self.s.cookies = requests.utils.cookiejar_from_dict(cookie)
        #self.s.cookies=cookie
        self.s.verify = False
        st = self.get_st()
        if st:
            return True
        return False

    def get_st(self):
        res = self.s.get(self.BASE_URL).text
        try:
            st = re.search(r"st: '(.*?)'", res).group()
            st = st.split('\'')[1]
        except:
            return None
        print(st)
        return st

    def get_cookie_from_db(self, cook):
        if cook.cookies:
            #print(cook.cookies)
            cookie = json.loads(cook.cookies.replace("'", '"'))
            return cookie
        return
        # 数据库中获取随机标识为可用的cookie
        # cookie = session.execute()
        # return json.loads(cookie)
        # return {'WEIBOCN_FROM': '1110006030', '_T_WM': '53276231542',
        #         'SCF': 'AtOrnnbOrSMftKgXU8q8C3f0diZLKVzFI_17P-ZpUhDOQU3cpgt40WY8vgoL4vs5S15Kk1OiYR0C_I4fYHMgkrk.',
        #         'SSOLoginState': '1559935179', 'MLOGIN': '1', 'M_WEIBOCN_PARAMS': 'uicode%3D20000174',
        #         'XSRF-TOKEN': '24d4a0',
        #         # 'SSOLoginState': '1559935179', 'MLOGIN': '1', 'M_WEIBOCN_PARAMS': 'uicode%3D20000174', 'XSRF-TOKEN': '24d4a0',
        #         'SUHB': '010GWLNc_cDAD6',
        #         'SUB': '_2A25x_sibDeRhGeFP7lcT9ifFzT6IHXVTAOjTrDV6PUJbkdAKLVXMkW1NQQ4QAH7m7bidP6CNpN0AfPOJIVBgIDRM'}
        #

    def login(self, cook, username, password):
        display = Display(visible=0, size=(800, 600))
        display.start()
        self.driver = webdriver.Firefox()
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # # self.driver = webdriver.Chrome(chrome_options=options)
        # self.driver = webdriver.Chrome(executable_path=r"C:\Temp\phantomjs-2.1.1-windows\chromedriver.exe",
        #                                chrome_options=options)

        self.driver.get('https://passport.weibo.cn/signin/login')
        time.sleep(3)
        WebDriverWait(self.driver, 10, 2).until(lambda driver: driver.find_element_by_xpath('//*[@id="loginAction"]'))
        time.sleep(3)
        # Input username and password
        username_area = self.driver.find_element_by_xpath('//*[@id="loginName"]')
        username_area.send_keys(username)
        time.sleep(3)
        psw_area = self.driver.find_element_by_xpath('//*[@id="loginPassword"]')
        psw_area.send_keys(password)

        # Submit
        btn = self.driver.find_element_by_xpath('//*[@id="loginAction"]')
        btn.click()

        from time import sleep
        sleep(5)
        # if their is a CAPTCHA, then crack it.
        if 'CAPTCHA' in self.driver.current_url:
            print('need crack')
            # TODO 处理验证码 如果处理失败标注对应数据库内是否可用字段值为不可用
            # cookies = crack(driver)
        else:
            cookies = self.driver.get_cookies()
        cookies_dict = {}
        for d in cookies:
            cookies_dict[d['name']] = d['value']
        cook.cookies = json.dumps(cookies_dict)
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cook.create_time = dt
        session.add(cook)
        #driver.close()
        try:
            session.commit()

        except:
            print("数据库更新cookies失败")
            session.rollback()
        # self.driver.quit()
        # display.stop()
        return cookies_dict