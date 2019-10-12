import requests
import json
import time
import pandas
import re
from urllib import parse
def get_id(res):

    resp=re.search('<a href="/planet/talk\?lemmaId=(.*?)"',res).group(1)
    return resp
def request_url():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    page = 0
    _time = str(time.time()).replace('.', '')[:13]
    while True:
        try:
            url = f'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28266&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=%E4%B8%AD%E5%9B%BD%E6%98%8E%E6%98%9F&sort_key=&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn={page}&rn=12&cb=jQuery11020607750700402305_1568945529863&_={_time}'
            page += 12
            response = requests.get(url=url, headers=headers, verify=False).text
            response = re.search('jQuery11020607750700402305_1568945529863\((.*?)\)', response).group(1)
            # print(response)
            #print(json.loads(response)['data'])
            if not json.loads(response)['data'][0]:
                break
            data = json.loads(response)['data'][0]['result']
            # if page > 300:
            #     break
            for word in data:
                print(word)
                image = word['pic_4n_78']
                name = word['ename']
                res=requests.get("https://baike.baidu.com/item/"+parse.quote(name)).text
                ids=str(get_id(res))

                detail_url = word['url']
                dic = [[name, ids, image, detail_url]]
                # dic = [[name], [image], [detail_url]]
                print(dic)
                # lis = []
                # lis.append(dic)

                pandas.DataFrame(dic).to_csv('B.csv', encoding='utf_8_sig', mode='a', index=False, header=False)
        except Exception as e:
            print(e)
            print(url)




if __name__ == '__main__':
    request_url()
    #get_id()


