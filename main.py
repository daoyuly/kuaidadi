#!/usr/bin/python
#coding: utf-8

from spider_2 import kuaidadiSpider

urlList = []
point = 'http://v.kuaidadi.com/point?cityId=110100&scope=city&date=0&dimension=satisfy&num=300'
area = 'http://restapi.amap.com/v3/geocode/regeo?key=28d67f7de0e3b3621b1e1b1746bbd68d&s=rsv3&location=116.3894,39.9737&radius=1000&platform=JS&logversion=2.0&sdkversion=1.3&appname=http%3A%2F%2Fv.kuaidadi.com%2F&csid=A4AF9286-5FE5-4536-92A8-F327415243AF'

dimension_list = ['distribute','satisfy','demand','response']

#2015.3.11-2015.3.20==(-417,-410)

for dimension in dimension_list:
    print dimension
    for i in range(0,2):
        fileName = '%s.csv' %(dimension)
        dadi = kuaidadiSpider(fileName)
        area = 'http://v.kuaidadi.com/point?cityId=110100&scope=city&date=%d&dimension=%s&num=10'%(i,dimension)
        content = dadi.open_url(area)
        dadi.writeFile(content)


