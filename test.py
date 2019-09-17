# -*- coding: utf-8 -*-
import scrapy
import json
import os
import random
import re
import sys
import time
import datetime
import requests
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support.wait import WebDriverWait
from db import session
from model import Cookies,Commit


class CommitsSpider():
    # name = 'commits'
    # allowed_domains = ['m.weibo.cn']
    # start_urls = ["https://m.weibo.cn/detail/4414309176527148", "https://m.weibo.cn/detail/4413161250214670",
    #               "https://m.weibo.cn/detail/4415278761113511"]

    # start_urls = ['https://m.weibo.cn/comments/hotflow?id=4408547318040846&mid=4408547318040846&max_id_type=0']

    def __init__(self):
        self.commit_url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&{}max_id_type=0"
        # https://m.weibo.cn/comments/hotflow?id=4414569407372021&mid=4414569407372021&max_id=139250354826359&max_id_type=0
        # https://m.weibo.cn/comments/hotflow?id=4414569407372021&mid=4414569407372021&max_id=138838037500247&max_id_type=0
        # self.since_id = None
        self.BASE_URL = "https://m.weibo.cn"
        self.s = requests.session()
        self.s.verify=False
        self.s.headers={
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }
   #     # self.current_timestamp = 0
    def get_bid(self,mid):
        all_models=session.query(Commit).filter(Commit.mid==mid).all()
        all_models_list=[]
        if all_models:
            all_models_list=[i.bid for i in all_models]
        return all_models_list
    def starts(self,urls):
        if not urls:
            return
        # for url in urls:
        self.up_cookies()
        #print(self.s.cookies)
        # self.s.cookies=requests.utils.cookiejar_from_dict(cookies)
        response=self.s.get(url)
        # #print(response.text)

        self.parse(response)
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

    def parse(self, response):
        url = response.url
        mid = url.split("/")[-1]
        bid_lists = self.get_bid(mid)
        # if "max_id" in url:
        #     commit_url = self.commit_url.format(mid, mid, max_id)
        #     yield scrapy.Request(url=commit_url, callback=self.detail)
        # else:
        commit_url = self.commit_url.format(mid, mid, "")
        html=self.s.get(commit_url).json()
        self.detail(html,mid,bid_lists)

    def detail(self, html,mid,bid_lists):
        if html["ok"] == 0:
            return
        datas = html["data"]["data"]
        if datas and int(datas[0]["like_count"]) < 1:
            print("没有数据了")
            return
        else:
            for i in datas:
                item = {}
                # 详情页唯一标示
                item["mid"] = mid
                item["detail_url"]="https://m.weibo.cn/detail/"+str(mid)
                # 评论唯一标示
                item["bid"] = i.get("bid")
                if item["bid"] in bid_lists:
                    print("数据已存在")
                    continue
                # item["floor_number"]=i.get("floor_number")
                # 赞
                item["like_count"] = int(i.get("like_count"))
                if item["like_count"] < 1:
                    continue

                # 评论内容
                text = i.get("text")
                item["text"] = re.sub("<.*?>", "", text)
                if not item["text"]:
                    continue
                # 评论时间
                creates_at = i.get("created_at")
                if "+0800" in creates_at:
                    item["created_at"] = self.trans_format(creates_at)
                else:
                    item["created_at"] = creates_at

                # pic=i.get("pic")
                # if pic:
                #     images_list=[]
                #     try:
                #         image_item={}
                #         image_item["url"]=pic["large"]["url"]
                #         image_item["width"]=pic["large"]["geo"]["width"]
                #         image_item["height"] = pic["large"]["geo"]["height"]
                #         images_list.append(image_item)
                #     except:
                #         print("链接为------------------------------------------------")
                #         print(pic)
                # else:
                #     images_list=[]
                # item["media"]=images_list
                # 评论者id
                item["user_id"] = i["user"]["id"]
                # 评论人昵称
                item["screen_name"] = i["user"]["screen_name"]
                # 评论人头像
                item["profile_image_url"] = i["user"]["profile_image_url"]
                print(item)
                self.save_model(item)
            max_id = html["data"]["max_id"]
            if max_id:
                commit_url = self.commit_url.format(mid, mid, "max_id=" + str(max_id) + "&")
                html=self.s.get(commit_url).json()
                self.detail(html,mid,bid_lists)
    def save_model(self,item):

        commit_models=session.query(Commit).filter(Commit.bid==item.get("bid")).all()
        if commit_models:
            commit_model=commit_models[0]
        else:
            commit_model=Commit()
        commit_model.mid=int(item.get("mid"))
        commit_model.detail_url=item.get("detail_url")
        commit_model.bid = item.get("bid")
        commit_model.like_count = int(item.get("like_count"))
        commit_model.created_at = item.get("created_at")
        commit_model.text = item.get("text")
        commit_model.user_id = int(item.get("user_id"))
        commit_model.screen_name = item.get("screen_name")
        commit_model.profile_image_url = item.get("profile_image_url")
        session.add(commit_model)
        try:
            session.commit()
            print("插入数据成功")
        except Exception as e:
            print(e)
            print("插入数据失败")
            session.rollback()


    def trans_format(self, time_string, from_format="%a %b %d %H:%M:%S +0800 %Y"):
        """
        @note 时间格式转化
        :param time_string:
        :param from_format:
        :param to_format:
        :return:
        """
        time_struct = time.strptime(time_string, from_format)
        #times = int(time.mktime(time_struct))
        # times = time.strftime(to_format, time_struct)
        return time_struct

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
        self.driver.quit()
        display.stop()
        return cookies_dict

if __name__=="__main__":
    com=CommitsSpider()
    print(sys.argv)
    url=sys.argv[1]
    # print(url)
    #url="https://m.weibo.cn/detail/4415278761113511"
    com.starts(url)

