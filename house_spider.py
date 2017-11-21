#-*- coding:utf-8 -*-

from urllib2 import Request,urlopen,HTTPError,URLError,ProxyHandler,build_opener,install_opener
from bs4 import BeautifulSoup
import socket
import re
import requests
import time
import pandas as pd
import numpy as np 
import csv
import sys

def set_params():
    global headers_list,url_list,csv_writer
    url_list = []
    csv_file = open("D:\my_documents\python\scrape\house_price\leju\house.csv","wb")
    csv_writer = csv.writer(csv_file, delimiter=',')
#  previously stored links to houses in link.txt
    file = open('D:\\my_documents\\python\\scrape\\house_price\\leju\\link.txt')
    obj = file.read().replace('http',' http')
    obj = obj.split()
    for link in obj:
        url_list.append(link)
    print len(url_list)
    url_list = set(url_list)
    print len(url_list)

    headers_list = [{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
{'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}\
,{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},{'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},{'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36 '},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14 '},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'}]

   
    get_obj() 
    
def get_obj():

    count = 1 
    while (count<=30):

        link = url_list.pop()
        print link
        random_num = np.random.randint(0,9)
        req = Request(link,headers=headers_list[random_num])
        response = urlopen(req)
        soup = BeautifulSoup(response,'html.parser')
        
    ## search for infos we need
        try:
            title = soup.find('h1').get_text()
        except:
            title = None  
        try:
            update_time = soup.find('div',{'class':'h-item g-line'})
            update_time = update_time.findAll('span',{'class':'fl'})[0].font.get_text()
        except:
            update_time = None
        try:
            tag_list = soup.find('span',{'class':'ft-lb fl'}).findAll('em')
            tag = ''
            for item in tag_list:
                _tag = item.get_text().strip()
                tag = tag+_tag+','
        except:
            tag = None
        try:
            total_price = soup.find('dt',{'class':'h-fir'}).find('span',{'class':'s2'}).get_text()
        except:
            total_price = None
        try:
            unit_price = soup.find('dd').get_text()#.find('span',{'class':'s1'}).get_text()
        except:
            unit_price = None
        try:
            table = soup.find('div',{'class':'panelB '})
            table = table.table.findAll('td')
        except:
            table = None
        try:
            house_type = table[0].get_text()
        except:
            house_type = None
        try:
            propriety = table[1].get_text()
        except:
            propriety = None
        try:
            area = table[2].get_text()
        except:
            area = None
        try:
            inner_type = table[3].get_text()
        except:
            inner_type = None
        try:
            level = table[4].get_text()
        except:
            level = None
        try:
            decoration = table[5].get_text()
        except:
            decoration = None
        try:
            direction = table[6].get_text()
        except:
            direction = None
        try:
            wuye_fee = table[7].get_text()
        except:
            wuye_fee = None
        try:
            block = table[8].get_text()
        except:
            block = None
        try:
            address = table[9].get_text()
        except:
            address = None
        try:
            agent = soup.find('div',{'class':'i-right g-e'}).dl.dd.get_text().strip()
        except:
            agent = None
        try:
            company = soup.find('div',{'class':'i-right g-e'}).ul.findAll('li')
            company = company[1].a.get_text().strip()
        except:
            company = None
            
        try:
            community_name = soup.find('div',{'class':'basic_info_in'}).find('h4').get_text()
        except:
            community_name = None
        try:
            community_city = soup.find('div',{'class':'_pos'}).span.get_text()
            community_district = soup.find('div',{'class':'_pos'}).em.get_text()
        except:
            community_city = None
            community_district = None
        try:
            community_address = soup.find('div',{'class':'basic_info_in'}).p.get_text()
        except:
            community_address = None
        try:
            _type_distri = soup.find('div',{'class':'house_type clearfix'}).ul.findAll('li')
            type_distribution = ''
            for item in _type_distri:
                item = item.a.get_text()
                type_distribution = type_distribution+item+','
        except:
            type_distribution = None
        try:
            _price_distri = soup.find('div',{'class':'house_price clearfix'}).ul.findAll('li')
            price_distribution = ''
            for item in _price_distri:
                item = item.a.get_text()
                price_distribution = price_distribution+item+','
        except:
            price_distribution = None
        left_part = soup.find('ul',{'class':'left_part '}).findAll('li')
        try:
            year = left_part[0].em.get_text()
        except:
            year = None
        try:
            builder = left_part[3].em.get_text()
        except:
            builder = None
        try:
            management = left_part[4].em.get_text()
        except:
            management = None
        right_part = soup.find('ul',{'class':'right_part'}).findAll('li')
        try:
            total_square = right_part[0].em.get_text()
        except:
            total_square = None    
        try:
            num_family = right_part[1].em.get_text()
        except:
            num_family = None
        try:
            num_parking_space = right_part[2].em.get_text()
        except:
            num_parking_space = None
        try:
            greenery = right_part[3].em.get_text()
        except:
            greenery = None
        try:
            plot_ratio = right_part[4].em.get_text()
        except:
            plot_ratio = None
            
        features= [title,update_time,total_price,unit_price,house_type,propriety,area,inner_type,level,decoration,direction,wuye_fee,block,address]
        features += [community_name,community_city,community_district,community_address,type_distribution,price_distribution]
        features += [year,builder,management,total_square,num_family,num_parking_space,greenery,plot_ratio]
        csv_writer.writerow(features)   

        count +=1
           
if __name__=='__main__':

    set_params()
