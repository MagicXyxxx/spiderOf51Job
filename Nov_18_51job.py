import re
import requests
from lxml import etree
import csv
import time
import random

fp = open('51job.csv','wt',newline='',encoding='GBK',errors='ignore')
writer = csv.writer(fp)
'''title,salary,company,place,exp,edu,num,time,comment,url'''
writer.writerow(('职位','薪水','公司','地区','经验','学历','数量','时间','要求','url'))

def parseInfo(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)

    title = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/text()')
    salary = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()')
    company = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/text()')
    place = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[1]')
    exp = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[2]')
    edu = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[3]')
    num = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[4]')
    time = selector.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[5]')
    comment = selector.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/p/text()')
    url = res.url

    print(title,salary,company,place,exp,edu,num,time,comment,url)
    writer.writerow((title,salary,company,place,exp,edu,num,time,comment,url))

def getUrl(url):
    print(url)
    res = requests.get(url)
    res.encoding = 'GBK'
    if res.status_code == requests.codes.ok:
        selector = etree.HTML(res.text)
        urls = selector.xpath('//*[@id="resultList"]/div/p/span/a/@href')
        for url in urls:
            parseInfo(url)
            time.sleep(random.randrange(1, 4))


if __name__ == '__main__':
    key = '大数据'
    # #     第一页
    url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,'+key+',2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=4&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    getUrl(url)
    # #     后页[2,i)
    urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,'+ key + ',2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='.format(i) for i in range(2,50)]
    for url in urls:
        getUrl(url)