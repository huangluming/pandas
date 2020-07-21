#coding=utf-8
from bs4 import BeautifulSoup
import re
import requests
from parsel import Selector
import pandas as pd
import time
#############################################################
'''
这个模块爬取链家网福田区的二手房信息；仅仅爬取了前100页的数据
为了避免反爬虫策略，设定每5秒钟抓取一页信息
@time=2017-10-24
@author=wq
'''
 
###########################################################
# 进行网络请求的浏览器头部
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.7 Safari/537.36'}
# pages是不同页码的网址列表
pages=['https://sz.lianjia.com/ershoufang/futianqu/pg{}/'.format(x) for x in range(1,10)]
############################################################
 
#############################################################
lj_futian = pd.DataFrame(columns=['code','dec','img'])
count=0
def l_par_html(url):
    # 这个函数是用来获取链家网福田区二手房的信息
    wr=requests.get(url,headers=headers,stream=True)
    sel=Selector(wr.text)
    # describ用来获取房源的文字信息
    describ=sel.xpath('//li[@class="clear"]//text()').extract()
    new_information=([x for x in describ if x != '关注'and x != '加入对比' ])
    sep_infor=' '.join(new_information).split(r'/平米')[:-1]
    # hou_code用来获取房源的编号
    hou_code=sel.xpath('//li[@class="clear"]/a/@data-housecode').extract()
    # hou_image用来获取房源的图片
    hou_image=sel.xpath('//li[@class="clear"]/a/img/@data-original').extract()
    # 将信息形成表格全部写到一起
    pages_info=pd.DataFrame(list(zip(hou_code,sep_infor,hou_image)),columns=['code','dec','img'])
    print (pages_info)
    return pages_info
 
for page in pages:
    a=l_par_html(page)
    count=count+1
    print ('the '+str(count)+' page is sucessful')
    #time.sleep(5)
    lj_futian=pd.concat([lj_futian,a],ignore_index=True)
 
# 将表格数据输出到excel文件
lj_futian.to_excel('d:\\lianjia_ershou_futian_100.xlsx')