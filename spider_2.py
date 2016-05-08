#!/usr/bin/python
#coding: utf-8

import urllib2  # functions and classes which help in opening URLs
import bs4      # extract data from HTML or XML files
import chardet  # detect encoding character of HTML file
import re
import urlparse
import json

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

    def writeFile(self, data):
        #name = '%dfile'%(fname)
        localFile = open('data/'+self.fileName, 'a')
        cityID = data['result']['cityID']
        date = data['result']['date']
        realDate = data['result']['realDate']
        collection = data['result']['data']
        index = -1
        dataFormat = 'id,city,date,hour,longitude,latitude,value\n\r'
        localFile.write(dataFormat)

        hour = -1
        for item in collection:
            hour = hour + 1;
            for i in item:
              index = index + 1
              longitude = i[1]
              latitude = i[2]
              value = i[3]
              #dataFormat = index+','+cityID+','+date+','+hour+','+longitude+','+latitude+','+value
              dataFormat = '%d,%s,%s,%s,%s,%s,%s\n\r' %(index,cityID,date,hour,longitude,latitude,value)
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