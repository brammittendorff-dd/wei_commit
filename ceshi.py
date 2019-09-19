import requests
#TODO 测试结果杨幂微博 抓取数据365条 用时30分钟 一个进程16个线程
for i in range(20):
    url="https://m.weibo.cn/api/container/getIndex?uid=5187664653&luicode=10000011&lfid=100103type%3D1%26q%3D%E9%82%93%E8%B6%85&type=uid&value=5187664653&containerid=1076035187664653&page="+str(i)
    res=requests.get(url).json()
    print(res["data"]["cardlistInfo"])
