import requests
import re
from bs4 import BeautifulSoup

def generate_allurl(user_in_nub):
    url = 'http://gy.lianjia.com/ershoufang/pg{}/'
    for url_next in range(1,int(user_in_nub)):
        yield url.format(url_next)

def get_allurl(generate_allurl):
    get_url = requests.get(generate_allurl,)
    if get_url.status_code == 200:
        re_set = re.compile('<li.*?class="clear">.*?<a.*?class="img.*?".*?href="(.*?)"')
        re_get = re.findall(re_set,get_url.text)
        return re_get

def open_url(re_get):  # 分析详细url获取所需信息
    res = requests.get(re_get)
    if res.status_code == 200:
        info = {}
        soup = BeautifulSoup(res.text, 'lxml')
        info['标题'] = soup.select('.main')[0].text
        info['总价'] = soup.select('.total')[0].text + '万'
        info['每平方售价'] = soup.select('.unitPriceValue')[0].text
        info['参考总价'] = soup.select('.taxtext')[0].text
        info['建造时间'] = soup.select('.subInfo')[2].text
        info['小区名称'] = soup.select('.info')[0].text
        info['所在区域'] = soup.select('.info a')[0].text + ':' + soup.select('.info a')[1].text
        info['链家编号'] = str(re_get)[33:].rsplit('.html')[0]
        for i in soup.select('.base li'):
            i = str(i)
            if '</span>' in i or len(i) > 0:
                key, value = (i.split('</span>'))
                info[key[24:]] = value.rsplit('</li>')[0]
        for i in soup.select('.transaction li'):
            i = str(i)
            if '</span>' in i and len(i) > 0 and '抵押信息' not in i:
                key, value = (i.split('</span>'))
                info[key[24:]] = value.rsplit('</li>')[0]
        print(info)
        return info

 
def writer_to_text(list):  # 储存到text
    with open('链家二手房.text', 'a', encoding='utf-8')as f:
        f.write(json.dumps(list, ensure_ascii=False) + '\n')
        f.close()


def main():
    user_in_nub = input('输入生成页数：')
    writer_to_text(open_url(url))    #储存到text文件
 
if __name__ == '__main__':
    main()