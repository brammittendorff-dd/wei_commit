import requests
from urllib import parse
class ReSou():

    def __init__(self):
        self.s=requests.session()
        self.s.verify=False
        self.s.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }
        self.url='https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=pos%3D0_0%26mi_cid%3D100103%26cate%3D10103%26filter_type%3Drealtimehot%26c_type%3D30%26display_time%3D1569465149&luicode=10000011&lfid=231583'
    def get_page(self):
        url=parse.unquote(self.url)
        res=self.s.get(self.url).json()
        
#https://m.weibo.cn/api/container/getIndex?containerid=106003type=25&t=3&disable_hot=1&filter_type=realtimehot&title=微博热搜&extparam=pos=0_0&mi_cid=100103&cate=10103&filter_type=realtimehot&c_type=30&display_time=1569464702&luicode=10000011&lfid=231583
#https://m.weibo.cn/api/container/getIndex?containerid=106003type=25&t=3&disable_hot=1&filter_type=realtimehot&title=微博热搜&extparam=pos=0_0&mi_cid=100103&cate=10103&filter_type=realtimehot&c_type=30&display_time=1569464702&luicode=10000011&lfid=231583
#https://m.weibo.cn/p/index?containerid=106003type=25&t=3&disable_hot=1&filter_type=realtimehot&title=微博热搜&extparam=pos=0_0&mi_cid=100103&cate=10103&filter_type=realtimehot&c_type=30&display_time=1569465149&luicode=10000011&lfid=231583
#
# if __name__=="__main__":
#     ReSou().get_page()

#
# res="https://m.weibo.cn/detail/4426228439984803"
# resq="https://m.weibo.cn/detail/4425024863789551"
# import re
# while True:
#     res=requests.get("https://m.weibo.cn/detail/4425024863789551").text
#
#     if "微博内打开" in res:
#         print(1)
#     try:
#         print(1111111111)
#         created_at = re.search('"created_at": "(.*?)"', res).group(1)
#         print(created_at)
#     except:
#         if not res:
#             print(3333333333333333)
#         print(222222222222222222)
#         print(res)
# res=requests.get("http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0&city=0&yys=0&port=11&pack=67493&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=")
# data=res.json()["data"][0]
# ip=data["ip"]
# port=data["port"]
# proxies = {
#     "http": "http://"+str(ip)+":"+str(port),
#     "https": "https://"+str(ip)+":"+str(port),
# }
# print(proxies)
import re
import time
import datetime
class HH():
    def __init__(self):
        self.s=requests.session()
        self.s.verify = False
        self.s.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }
        # res=requests.get("http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0&city=0&yys=0&port=11&pack=67493&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=")
        # data=res.json()["data"][0]
        # ip=data["ip"]
        # port=data["port"]
        # self.proxies = {
        #     "http": "http://"+str(ip)+":"+str(port),
        #     "https": "https://"+str(ip)+":"+str(port),
        # }
        # print(self.proxies)
    def parse(self):
        burl="https://m.weibo.cn/detail/4415397891509511"
        #burl = "https://www.baidu.com"
        self.s.proxies = self.parse_ip()
        print(self.s.proxies)
        if not self.s.proxies:
            return
        time.sleep(3)
        try:
            res = self.s.get(burl).text
            time.sleep(1)
            if "微博内打开" in res:
                return 500
            created_at = re.search('"created_at": "(.*?)"', res).group(1)
            date = datetime.datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
            # print(int(time.mktime(date.timetuple())))
            print(date)
            #return int(time.mktime(date.timetuple()))
        except Exception as e:
            print(e)


    def parse_ip(self):
        try:
            res=requests.get("http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0&city=0&yys=0&port=11&pack=67493&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=")
            data=res.json()["data"][0]
            ip=data["ip"]
            port=data["port"]
            proxies = {
                "http": "http://"+str(ip)+":"+str(port),
                "https": "https://"+str(ip)+":"+str(port),
            }
            return proxies
            #return {'http': 'http://115.213.172.63:4223', 'https': 'https://115.213.172.63:4223'}
        except:
            return

# hh=HH()
# num=1
# while True:
#     print(num)
#     hh.parse()
#     num+=1
# res=requests.get("https://wx1.sinaimg.cn/large/61e7f4aaly1g7x05zfr2eg20ef07zqv7.gif",verify = False).content
# with open("1.gif","wb") as f:
#     f.write(res)
