#coding=utf-8
import requests
import re
import json
from lxml import etree
from urllib import parse
class ZuoPin():
    def __init__(self):
        self.s=requests.session()
        self.s.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }
        self.url="https://baike.baidu.com/item/%E8%8A%88%E6%9C%88%E4%BC%A0/73703"
        self.item={}
    def write(self,item):
        print(item)
        fname=parse.unquote(self.url.split("/")[-2])+'.json'
        with open(fname,"w",encoding='utf-8') as f:
            f.write(json.dumps(item,indent=4,ensure_ascii=False))
    #解析主页
    def parse_url(self):
        res=self.s.get(self.url)
        res.encoding="utf-8"
        self.item["百科链接"]=parse.unquote(self.url)
        html=res.text
        self.parse_des(html)
        self.parse_shuxing(html)
        self.parse_mulu(html)
        #print(self.item)
        self.write(self.item)
    #作品描述
    def parse_des(self,html):
        html = etree.HTML(html)
        des=html.xpath('.//div[@class="lemma-summary"]')[0].xpath('string(.)').replace("\xa0","")
        des=re.sub('\[.*?\]',"",des).replace("\n","")
        self.item["des"]=des
    #解析属性
    def parse_shuxing(self,html):
        html = etree.HTML(html)
        all_datas=html.xpath('.//div[@class="basic-info cmn-clearfix"]')
        names=all_datas[0].xpath('.//dt')
        values=all_datas[0].xpath('.//dd')
        for index,name1 in enumerate(names):
            name=name1.xpath('string(.)').replace("\xa0","")
            self.item[name]=values[index].xpath('string(.)').replace("\n","").replace("\xa0","")

    #解析目录,通过h2对html切割
    def parse_mulu(self,html):
        h2_lists=html.split('<div class="para-title level-2" label-module="para-title">')
        if h2_lists:
            h2_list=h2_lists[1::]
            for h2_html in h2_list:
                #判断是否有小标题
                if '<h3 class="title-text">' in h2_html:
                    self.parse_h3('<div class="para-title level-2" label-module="para-title">'+h2_html)
                else:
                    self.parse_h2('<div class="para-title level-2" label-module="para-title">'+h2_html)
    #解析h3目录
    def parse_h3(self,html):
        h3_htmls=html.split('<div class="para-title level-3" label-module="para-title">')
        if h3_htmls:
            h3_html=h3_htmls[1::]
            for h3 in h3_html:
                self.parse_h3_mulu('<div class="para-title level-3" label-module="para-title">'+h3)
    #解析h2目录
    def parse_h2(self,html):
        #剧集介绍
        if 'class="dramaSerialList"' in html:
            self.parse_juji(html)
        #角色介绍
        elif 'class="lemmaWgt-roleIntroduction"' in html:
            self.parse_juese(html)
        #解析音乐原声
        elif '</span>音乐原声' in html:
            self.parse_yinyue(html)
        #解析获奖记录
        elif 'name="rongyujilu"' in html:
            self.parse_huojiang(html)
        #解析其他table
        elif 'class="table-view log-set-param"' in html:
            self.parse_bochu(html)
        #解析文本
        else:
            self.parse_para(html)
    #解析播出信息
    def                                                                                                                                         parse_bochu(self,html):
        html=etree.HTML(html)
        h2_name=html.xpath('.//h2[@class="title-text"]/text()')[0]
        tables=html.xpath('.//table//tr')
        names=tables[0].xpath('.//th/text()')
        td_names = tables[0].xpath('.//td/text()')
        if names:
            print(names)
            table_list=[]
            for table in tables[1::]:
                values=table.xpath('.//td/text()')
                if values and len(values)==len(names):
                    table_item = {}
                    for index,value in enumerate(values):

                        table_item[names[index]]=value
                    table_list.append(table_item)
            self.item[h2_name]=table_list
        elif td_names:
            table_list=[]
            for table in tables[1::]:
                values=table.xpath('.//td/text()')
                if values and len(values)==len(td_names):
                    table_item = {}
                    for index,value in enumerate(values):
                        table_item[td_names[index]]=value
                    table_list.append(table_item)
            print(table_list)
            self.item[h2_name]=table_list

        else:
            self.item[h2_name]=""
    #解析获奖记录
    def parse_huojiang(self,html):
        html = etree.HTML(html)
        h2_name=html.xpath('.//h2[@class="title-text"]/text()')[0]
        huojiang_names=html.xpath('.//td[@class="normal title-td"]/text()')
        huojiang_lists=html.xpath('.//ul[@class="list-module j-common-module"]')
        all_list=[]
        for index,i in enumerate(huojiang_lists):
            ul_item={}
            li_list=[]
            for j in i.xpath('.//li'):
                li_item={}
                li_item["date"]=j.xpath('.//span[@class="first column"]')[0].xpath('string(.)').replace("\r","").replace("\n","").replace('\xa0',"")
                li_item["des"]=j.xpath('.//span[@class="column"]')[0].xpath('string(.)').replace("\r","").replace("\n","").replace('\xa0',"")
                li_list.append(li_item)
            ul_item[huojiang_names[index].replace('\n',"")]=li_list
            all_list.append(ul_item)
        self.item[h2_name]=all_list
    #解析音乐原声
    def parse_yinyue(self,html):
        html=etree.HTML(html)
        h2_name=html.xpath('.//h2[@class="title-text"]/text()')[0]

        #标题列表
        titles=html.xpath('.//table/tr/th')
        titles=[i.xpath('string(.)').replace("\r","").replace("\n","") for i in titles]
        #数据列表
        values=html.xpath('.//table/tr')
        yuansheng_lists=[]
        if values and len(values)>1:

            for values in values[1::]:

                yuansheng_item={}


                all_values=values.xpath('.//td')
                if len(all_values) !=len(titles):
                    continue
                print(len(all_values),len(titles))
                for index,all_value in enumerate(all_values):
                    yuansheng_item[titles[index]]=all_value.xpath('string(.)').replace("\r","").replace("\n","").replace('\xa0',"")
                yuansheng_lists.append(yuansheng_item)
        self.item[h2_name]=yuansheng_lists
    #解析文本
    def parse_para(self,html):
        html='<div class="aa">'+html+'</div>'
        html=etree.HTML(html)
        h2_name=html.xpath('.//h2[@class="title-text"]/text()')[0]
        datas=html.xpath('.//div[@class="aa"]/div[@class="para"]|.//li[@class="list-dot list-dot-paddingleft"]/div[@class="para"]')
        data_list=[]
        for data in datas:
            data1=data.xpath('string(.)').replace('\xa0',"")
            data1=re.sub("\[.*\]","",data1)
            data_list.append(data1)
        datass="".join(data_list)

        self.item[h2_name]=datass
    #解析h3小标题
    def parse_h3_mulu(self,html):
        #演员表
        if 'marqueeViewport_actor' in html:
            self.parse_yanyuan(html)
        #职员表
        elif 'class="staff-list"' in html:
            self.parse_zhiyuan(html)
        #票房table
        elif 'class="table-view log-set-param"' in html:
            self.parse_other(html)
        else:
            html = etree.HTML(html)
            h3_name = html.xpath('.//h3[@class="title-text"]/text()')[0]
            datas=html.xpath('.//div[@class="para"]')
            datas=[i.xpath('string(.)').replace('\xa0',"") for i in datas]
            self.item[h3_name] = "".join(datas)

    def parse_other(self,htmls):
        html=etree.HTML(htmls)
        h3_name = html.xpath('.//h3[@class="title-text"]/text()')[0]
        all_keys=html.xpath('.//table//tr')
        if all_keys:
            lists=[]
            keys=all_keys[0].xpath('.//th/text()')
            for i in all_keys[1::]:
                all_data=i.xpath('.//td')
                if len(all_data) != len(keys):
                    continue
                if "上映日期" in htmls and len(all_data)==4:
                    data_item = {}
                    for index, data in enumerate(all_data[:2]):
                        data_item[keys[index]] = data.xpath('string(.)').replace('\xa0', "").replace("\n", "")
                    lists.append(data_item)
                    data_item = {}
                    for index, data in enumerate(all_data[2:4]):
                        data_item[keys[index]] = data.xpath('string(.)').replace('\xa0', "").replace("\n", "")
                    lists.append(data_item)
                else:
                    data_item={}
                    for index,data in enumerate(all_data):
                        data_item[keys[index]]=data.xpath('string(.)').replace('\xa0',"").replace("\n","")
                    lists.append(data_item)
            self.item[h3_name]=lists
        else:
            print(22222222)
    #解析角色介绍
    def parse_juese(self,html):
        html=etree.HTML(html)
        h2_name=html.xpath('.//h2[@class="title-text"]/text()')[0]
        juese_lists=html.xpath('.//ul/li')
        juese_all_lists=[]
        for j in juese_lists:
            juese_item={}
            juese_item["name"]=j.xpath('.//div[@class="role-name"]')[0].xpath('string(.)').replace("\n", "").replace("\xa0","")
            juese_item[j.xpath('.//div[@class="role-actor"]/span[@class="item-key"]/text()')[0]]=j.xpath('.//div[@class="role-actor"]/span[@class="item-value"]')[0].xpath('string(.)').replace("\n", "").replace("\xa0","")
            try:
                juese_item[j.xpath('.//div[@class="role-voice"]/span[@class="item-key"]/text()')[0]] = \
                j.xpath('.//div[@class="role-voice"]/span[@class="item-value"]/text()')[0].replace("\n", "").replace("\xa0","")
            except:
                juese_item["配音"]=""
            juese_item["desc"]=j.xpath('.//dd[@class="role-description"]/text()')[0].replace("\n", "").replace("\xa0","")
            juese_all_lists.append(juese_item)
        self.item[h2_name]=juese_all_lists

    #解析职员表
    def parse_zhiyuan(self,html):
        html=etree.HTML(html)
        h3_name = html.xpath('.//h3[@class="title-text"]/text()')[0]
        keys=html.xpath('.//table[@class="staff-list"]//td[@class="list-key"]')
        values=html.xpath('.//table[@class="staff-list"]//td[@class="list-value"]')
        zhiyuan_item={}
        for index, name1 in enumerate(keys):
            name = name1.xpath('string(.)').replace("\xa0", "")
            zhiyuan_item[name] = values[index].xpath('string(.)').replace("\n", "").replace("\xa0","")
        other_zhiyuan=html.xpath('.//table[@class="table-view log-set-param"]//td')
        if other_zhiyuan:
            for index,i in enumerate(other_zhiyuan[::2]):
                zhiyuan_item[other_zhiyuan[index].xpath('string(.)').replace("\xa0","")]=other_zhiyuan[index+1].xpath('string(.)'.replace("\xa0",""))
        self.item[h3_name]=zhiyuan_item
    #解析演员
    def parse_yanyuan(self,html):
        html=etree.HTML(html)
        h3_name=html.xpath('.//h3[@class="title-text"]/text()')[0]
        lists=html.xpath('.//li[@class="listItem"]')
        yanyuan_lists=[]
        for i in lists:
            yanyuan_item={}
            #百科链接
            url=i.xpath('./a[1]/@href')
            if url:
                yanyuan_item["url"]='https://baike.baidu.com'+url[0]
            else:
                yanyuan_item["url"]=""
            #饰演角色
            name=i.xpath('.//dt')[0].xpath('string(.)').replace("\xa0","")
            yanyuan_item["name"]=name
            #配音
            peiyin=i.xpath('.//dd')
            if peiyin:
                peiyin=peiyin[-1].xpath('string(.)')
                if "配音" in peiyin:
                    peiyins=peiyin.split('  ')
                    yanyuan_item[peiyins[0]]=peiyins[1].replace("\xa0","")
                #yanyuan_item["peiyin"]=i.xpath('.//dd')[-1]
                else:
                    yanyuan_item["配音"] = ""

            else:
                yanyuan_item["配音"]=""
            yanyuan_lists.append(yanyuan_item)
        self.item[h3_name]=yanyuan_lists

    #解析剧集
    def parse_juji(self,html):
        html=etree.HTML(html)
        juji_item={}
        h2_name=html.xpath('.//h2[@class="title-text"]/text()')[0]
        names=html.xpath('.//ul[@class="dramaSerialList"]//dt')
        values=html.xpath('.//ul[@class="dramaSerialList"]//dd')
        for index, name1 in enumerate(names):
            name = name1.xpath('string(.)').replace("\xa0", "")
            juji_item[name] = values[index].xpath('string(.)').replace("\n", "").replace("\xa0","")
        self.item[h2_name]=juji_item
if __name__=="__main__":
    zp=ZuoPin()
    zp.parse_url()