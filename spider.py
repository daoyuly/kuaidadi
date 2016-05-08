#!/usr/bin/python
#coding: utf-8

import urllib2  # functions and classes which help in opening URLs
import bs4      # extract data from HTML or XML files
import chardet  # detect encoding character of HTML file
import re
import urlparse
import json
import codecs

class kuaidadiSpider:
    def __init__(self,fileName):
        self.__headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
        self.fileName = fileName

    def open_url(self, url):
        try:
           opener = urllib2.build_opener()           
           opener.addheaders = [self.__headers]      
           content = opener.open(url).read()
      
           #encoding = chardet.detect(content)['encoding']
           #content = content.decode(encoding, 'ignore')
           content = json.loads(content)
        except Exception, e:
            content = e
        else:
            pass
        finally:
            pass
        return content

    def getLocal(self,longitude,latitude):
        area = 'http://restapi.amap.com/v3/geocode/regeo?key=28d67f7de0e3b3621b1e1b1746bbd68d&s=rsv3&location='+str(longitude)+','+str(latitude)+'&radius=1000&platform=JS&logversion=2.0&sdkversion=1.3&appname=http%3A%2F%2Fv.kuaidadi.com%2F&csid=A4AF9286-5FE5-4536-92A8-F327415243AF'
        opener = urllib2.build_opener()
        opener.addheaders = [self.__headers]    
        content = opener.open(area).read()
        encoding = chardet.detect(content)['encoding']
        content = content.decode(encoding, 'ignore')
        content = json.loads(content)
        #print content['regeocode']['formatted_address']
        print '.'
        return content['regeocode']['formatted_address']

    def writeFile(self, data):
        #name = '%dfile'%(fname)
        localFile = codecs.open('data/'+self.fileName, 'a', 'utf-8')
        cityID = data['result']['cityID']
        date = data['result']['date']
        realDate = data['result']['realDate']
        collection = data['result']['data']
        index = 0
        dataFormat = 'id,city,date,hour,longitude,latitude,value,address\n\r'
        localFile.write(dataFormat)

        hour = 0
        for item in collection:
            hour = hour + 1;
            for i in item:
              index = index + 1
              longitude = i[1]
              latitude = i[2]
              value = i[3]
              address = ''#self.getLocal(longitude,latitude);
              #dataFormat = index+','+cityID+','+date+','+hour+','+longitude+','+latitude+','+value
              dataFormat = '%d,%s,%s,%s,%s,%s,%s,%s\n\r' %(index,cityID,date,hour,longitude,latitude,value,address)
              localFile.write(dataFormat)
        localFile.close()

    def to_csv(self,key,json_d,prefix='data/'):
        data=json_d['result']['data']
        city_id=json_d['result']['cityID']
        date=json_d['result']['date']
        dimension=key[3]
        fname='_'.join([dimension,date,city_id,'.csv'])
        fname=fname.replace('/','.')
        fname=prefix+fname
        cdata=[]
        for hour,section in enumerate(data):
            for record in section:
                cdata.append([hour]+record[1:])
        df=pd.DataFrame(cdata,columns=['hour','longitude','latitude','value'])
        df.to_csv(fname)