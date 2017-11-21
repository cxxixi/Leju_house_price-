#-*- coding:utf-8 -*-

import re
import requests
import time
import pandas as pd
import numpy as np 
import csv
import sys
import matplotlib.pyplot as plt
from time import strptime
from chardet import detect

#import data and assign names to columns
df = pd.read_csv('D:\my_documents\python\scrape\house_price\leju\house\\house1_utf8.csv',encoding='utf8',error_bad_lines=False,nrows=2950)
columns = ['index','title','update_time','total_price','unit_price','house_type','propriety','area','inner_type','level','decoration']
columns +=['direction','management_fee','block','address','community_name','community_city','community_district','community_address']
columns +=['type_distribution','price_distribution','year','builder','management','total_square','num_family','num_parking_space','greenery','plot_ratio']
df.columns = columns

#since I used several devices to scrape data, there are 20 files. Need to concatenate these files.
for i in xrange(2,20):
    # try:
    path = 'D:\my_documents\python\\scrape\house_price\leju\house\\house'+str(i)+'_utf8.csv'
    df1 = pd.read_csv(path,error_bad_lines=False,nrows=2950,encoding='utf8')
    df1.columns = columns
    df = pd.concat([df,df1])
    print i

##drop duplicates
df =  df.drop(['index'],axis=1)
df = df.drop_duplicates()
# titleset = np.unique(np.array(df.title.values))
# print len(titleset)

#drop update_time
df =  df.drop(['update_time'],axis=1)

#clean 'unit_price'
unit_price = df.unit_price.values
for i in range(len(unit_price)):
    unit_price[i]= unit_price[i][3:-5]
df.unit_price = unit_price

#clean house_type
house_type = df.house_type.values
for i in range(len(house_type)):
	house_type[i] = house_type[i][3:].strip()
house_type_set = np.unique(house_type)
house_type_set = house_type_set[house_type_set!=u'暂无']
for i in np.arange(len(house_type_set)):
	# print house_type_set[i],i+1
	df.house_type[df.house_type==house_type_set[i]] = i+1
df.house_type[df.house_type==u'暂无'] = None

# clean propriety
propriety = df.propriety.values
for i in range(len(propriety)):
    propriety[i]= propriety[i][3:].strip()
propriety_set = set(propriety)
none_feature = set([u'暂无',u'甲级',u'精装',u'简装',u'乙级',u'毛坯',u'其他',u'清水',u'中装',u'豪装'])
propriety_set = list(propriety_set.difference(none_feature))
for i in np.arange(len(propriety_set)):
  # print propriety_set[i],i+1
  df.propriety[df.propriety==propriety_set[i]] = i+1
for feature in none_feature:
    df.propriety[df.propriety == feature] = None

#clean area 
area = df.area.values
for i in range(len(area)):
    area[i]= area[i][3:-2].strip()
df.area = area

# clean inner_type 
inner_type = df.inner_type.values
num_bedroom = df.inner_type.values.copy()
num_livingroom = df.inner_type.values.copy()
num_bathroom = df.inner_type.values.copy()
for i in range(len(inner_type)):
    try:
        num_bedroom[i] = inner_type[i][3]
        num_livingroom[i] = inner_type[i][5]
        num_bathroom[i] = inner_type[i][7]
        if num_bedroom[i] not in list(u'0123456789'):
            num_bedroom[i] = None
        if num_livingroom[i] not in list(u'0123456789'):
            num_livingroom[i] = None            
        if num_bathroom[i] not in list(u'0123456789'):
            num_bathroom[i] = None            
    except IndexError:
        #continue
        num_bedroom[i] = None
        num_livingroom[i] = None
        num_bathroom[i] = None 

df['num_bedroom'] = num_bedroom
df['num_livingroom'] = num_livingroom
df['num_bathroom'] = num_bathroom 
df = df.drop('inner_type',axis=1)

# clean level
level = df.level.values
particular_level = df.level.values.copy()
total_level = df.level.values.copy()
level = df.level.values
for i in range(len(level)):
    level[i]= level[i][3:].strip()
    try:
        level[i] = level[i].split(u'/')
        particular_level[i] = level[i][0]
        total_level[i] = level[i][1][:-1]
    except :
        particular_level[i] = None
        total_level[i] = None
    if particular_level[i]!=None and not particular_level[i].isdigit():#startswith(match):
        if particular_level[i] == u'低楼层':#.decode('utf8'):
            particular_level[i] = int(int(total_level[i])/6.0)
        else:
            if particular_level[i] == u'中楼层':#.decode('utf8'):
                particular_level[i] = int(int(total_level[i])/2.0)
            else:
                if particular_level[i] == u'高楼层':
                    particular_level[i] = int(5*int(total_level[i])/6.0)
                else:
                    particular_level[i] = None

df = df.drop(['level'],axis=1)
df['particular_level'] = particular_level
df['total_level'] = total_level

# clean decoration
decoration = df.decoration.values
for i in range(len(decoration)):
    decoration[i]= decoration[i][3:].strip()
decoration_set = set([u'精装',u'简装',u'毛坯',u'清水',u'中装',u'豪装'])
none_feature = list(set(decoration).difference(decoration_set))
for i in np.arange(len(decoration_set)):
    # print list(decoration_set)[i],i+1
    df.decoration[df.decoration==list(decoration_set)[i]] = i+1
for feature in none_feature:
    df.decoration[df.decoration == feature] == None

# direction
direction = df.direction.values
for i in range(len(direction)):
    try:
        direction[i]= direction[i][3:].strip()
        if u'东' not in direction[i] and u'南'not in direction[i] and u'西' not in direction[i] and u'北'not in direction[i]:
            direction[i] = u'暂无'
    except AttributeError:
        continue
direction_set = np.unique(direction)
direction_set = direction_set[direction_set!=u'暂无']
for i in np.arange(len(direction_set)):
    #print direction_set[i],i+1
    df.direction[df.direction==direction_set[i]] = int(i+1)
df.direction[df.direction==u'暂无'] = None


# management_fee
management_fee = df.management_fee.values
for i in range(len(management_fee)):
    try:
        management_fee[i] = management_fee[i][3:-5].strip()
        if (management_fee[i]!= None)and(management_fee[i][0] not in list(u'0123456789')):
            management_fee[i] = None
    except:
        management_fee[i] = None
df.management_fee = management_fee

# block   (建筑时间和区市的位置可能可分析)
df = df.drop(['block'],axis=1)

# address 
address = df.address.values
for i in range(len(address)):
    try:
        address[i] = address[i][5:].strip()
    except:
        address[i] = None
address[address==u'暂无'] = None    
df.address = address

#community_name
community_name = df.community_name.values
for i in range(len(community_name)):
    try:
        community_name[i] = community_name[i].strip()
    except:
        community_name[i] = None
community_name[community_name==u'暂无'] = None    
df.community_name = community_name
# 18
df = df.drop(['community_address'],axis=1)

# type_distribution
room1 = df.type_distribution.values.copy()
room2 = df.type_distribution.values.copy()
room3 = df.type_distribution.values.copy()
room4 = df.type_distribution.values.copy()
room5 = df.type_distribution.values.copy()
room6 = df.type_distribution.values.copy()
feature_dic = {1:room1,2:room2,3:room3,4:room4,5:room5,6:room6}
type_distribution = df.type_distribution.values
for i in range(len(type_distribution)):
    try:

        type_distribution[i] = type_distribution[i].split(u',')[:-1]
        f = {u'一室（':lambda x:1,u'二室（':lambda x:2,u'三室（':lambda x:3,u'四室（':lambda x:4,u'五室（':lambda x:5,u'五室以':lambda x:6}
        index_list = [f[head[0:3]](0) for head in type_distribution[i]]
        value_list = [int(type_distribution[i][k].split(u'（')[1][:-2]) for k in range(len(type_distribution[i]))]
        _dic = {index_list[k]:value_list[k] for k in range(len(index_list))}
        for k in xrange(1,7):
            if k in _dic.keys():
                feature_dic[k][i] = _dic[k]
            else:
                feature_dic[k][i] = None
    except:
        for k in xrange(1,7):
            feature_dic[k][i] = None

df['room1'] = feature_dic[1]
df['room2'] = feature_dic[2]
df['room3'] = feature_dic[3]
df['room4'] = feature_dic[4]
df['room5'] = feature_dic[5]
df['room6'] = feature_dic[6]
df = df.drop(['type_distribution'],axis=1)

#20 price_distribution
_range1 = df.price_distribution.values.copy()
_range2 = df.price_distribution.values.copy()
_range3 = df.price_distribution.values.copy()
_range4 = df.price_distribution.values.copy()
_range5 = df.price_distribution.values.copy()
_range6 = df.price_distribution.values.copy()
_range7 = df.price_distribution.values.copy()
feature_dic = {1:_range1,2:_range2,3:_range3,4:_range4,5:_range5,6:_range6,7:_range7}
price_distribution = df.price_distribution.values
for i in range(len(price_distribution)):
    try:
        price_distribution[i] = price_distribution[i].split(u',')[:-1]
        f = {u'100万':lambda x:1,u'100-':lambda x:2,u'200-':lambda x:3,u'300-':lambda x:4,u'500-':lambda x:5,u'800-':lambda x:6,u'1000':lambda x:7}
        index_list = [f[head[0:4]](0) for head in price_distribution[i]]
        value_list = [int(price_distribution[i][k].split(u'（')[1][:-2]) for k in range(len(price_distribution[i]))]
        _dic = {index_list[k]:value_list[k] for k in range(len(index_list))}
        for k in xrange(1,8):
            if k in _dic.keys():
                feature_dic[k][i] = _dic[k]
            else:
                feature_dic[k][i] = None
    except:
        for k in xrange(1,8):
            feature_dic[k][i] = None

df['_range1'] = feature_dic[1]
df['_range2'] = feature_dic[2]
df['_range3'] = feature_dic[3]
df['_range4'] = feature_dic[4]
df['_range5'] = feature_dic[5]
df['_range6'] = feature_dic[6]
df['_range7'] = feature_dic[7]
df = df.drop('price_distribution',axis=1)

# 21 year
year = df.year.values
for i in range(len(year)):
    try:
        year[i] = year[i].strip()
        #print year[i]
        if u'暂' != year[i][0]:
            year[i] = year[i][:-1]
            year[i] = year[i].replace(u'年',u'-')
            year[i] = year[i].replace(u'月',u'-')
            if year[i][-1] == u'-':
                year[i] = year[i][:-1]
            year[i] = int(strptime(year[i],'%Y-%m')[0])
        else:
            year[i] = None
    except:
        year[i] = None
    print year[i]
df.year = year


# 23 builder
builder = df.builder.values
for i in range(len(builder)):
    try:
        builder[i] = builder[i].strip()
        if u'暂' == builder[i][0]:
            builder[i] = None
    except:
        builder[i] = None
df.builder = builder

# 24 management
management = df.management.values
for i in range(len(management)):
    try:
        management[i] = management[i].strip()
        if u'暂' == management[i][0]:
            management[i] = None
    except:
        management[i] = None
df.management = management

# 25 total square
total_square = df.total_square.values
for i in range(len(total_square)):
    try:
        total_square[i] = total_square[i].strip().split(u'平')[0]
        if u'暂' == total_square[i][0]:
            total_square[i] = None
    except:
        total_square[i] = None
df.total_square = total_square

# num family
num_family = df.num_family.values
for i in range(len(num_family)):
    try:
        num_family[i] = num_family[i].strip().split(u'户')[0]
        if u'暂' == num_family[i][0]:
            num_family[i] = None
    except:
        num_family[i] = None
df.num_family = num_family

#num parking space
num_parking_space = df.num_parking_space.values
for i in range(len(num_parking_space)):
    try:
        num_parking_space[i] = num_parking_space[i].strip()
        if u'暂' == num_parking_space[i][0]:
            num_parking_space[i] = None
    except:
        num_parking_space[i] = None
df.num_parking_space = num_parking_space

# greenery
greenery = df.greenery.values
for i in range(len(greenery)):
    try:
        greenery[i] = greenery[i].strip()[:-1]
        if u'暂' == greenery[i][0]:
            greenery[i] = None
    except:
        greenery[i] = None
df.greenery = greenery

# plot ratio
plot_ratio = df.plot_ratio.values
for i in range(len(plot_ratio)):
    try:
        plot_ratio[i] = plot_ratio[i].strip()[:-1]
        if u'暂' == plot_ratio[i][0]:
            plot_ratio[i] = None
    except:
        plot_ratio[i] = None
df.plot_ratio = plot_ratio

#df = df.dropna(thresh=30)
df.to_csv('D:\my_documents\python\scrape\house_price\leju\house_info.csv',encoding='gbk')
