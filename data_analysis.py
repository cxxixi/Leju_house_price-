#-*- coding:utf-8 -*-

import time
import pandas as pd
import numpy as np 
import sys
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('D:\my_documents\python\scrape\house_price\leju\house_info.csv',encoding='gbk')

data.shape
data.head()

data.ix[:,1:].describe()

##Distribution of Total Price (price below 10,000,000)

# print 1.0*data['total_price'][data['total_price']<=1000].count()/data['total_price'].count()
# plt.figure(figsize=(6,4))
# sns.distplot(data['total_price'][data['total_price']<=1000],kde=False,color='b',hist_kws={'alpha':0.8})
# plt.title('Distribution of Total Price (price below 10,000,000)')
# plt.ylabel('Number')
# plt.show()

#Distribution of unit Price

# plt.figure(figsize=(18,6))
# ax1 = plt.subplot(1,2,1)
# sns.distplot(data['unit_price'][data['unit_price']<=100000],kde=False,color='b',hist_kws={'alpha':0.8})
# plt.title('Distribution of Unit Price')
# plt.ylabel('Number')
# ax2 = plt.subplot(1,2,2)
# sns.distplot(data['unit_price'][data['unit_price']<=60000],kde=False,color='b',hist_kws={'alpha':0.8})
# plt.title('Distribution of Unit Price (Zoomed In)')
# plt.ylabel('Number')
# plt.show()#Distribution of unit Price

# plt.figure(figsize=(18,6))
# ax1 = plt.subplot(1,2,1)
# sns.distplot(data['unit_price'][data['unit_price']<=100000],kde=False,color='b',hist_kws={'alpha':0.8})
# plt.title('Distribution of Unit Price')
# plt.ylabel('Number')
# ax2 = plt.subplot(1,2,2)
# sns.distplot(data['unit_price'][data['unit_price']<=60000],kde=False,color='b',hist_kws={'alpha':0.8})
# plt.title('Distribution of Unit Price (Zoomed In)')
# plt.ylabel('Number')
# plt.show()

## Correlation
# plt.figure(figsize=(20,20))
# corr = data.select_dtypes(include=['float64','int64']).ix[:,1:-13].corr()
# sns.heatmap(corr,annot=True,linecolor='k',cbar=True,square=True)
# plt.title('Correlation of Features of All House types')
# plt.show()

## Correlation housetype=16 普通住宅
# plt.figure(figsize=(20,20))
# corr = data.select_dtypes(include=['float64','int64'])[data['house_type']==16].ix[:,1:-13].corr()
# sns.heatmap(corr,annot=True,linecolor='k',cbar=True,square=True)
# plt.title('Correlation of Features of All House types')

##
# k=10
# cols = corr.nlargest(k,'total_price')['total_price'].index
# df = data[cols].dropna()
# corrmax = np.corrcoef(df.values.T)
# sns.heatmap(corrmax,annot=True,cbar=True,square=True,fmt='.2f',annot_kws={'size':10},cmap='Reds')
# plt.title('Correlation of N Most Relational Features with Total Price')
# plt.show()
#Colormap 8 is not recognized. Possible values are: Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spectral, spectral_r, spring, spring_r, summer, summer_r, terrain, terrain_r, viridis, viridis_r, winter, winter_r


##let's how unit price and total price distribute

# fig = plt.figure(figsize=(14,6))
# ax1 = fig.add_subplot(1,2,1)
# X = data['unit_price']
# Y = data['total_price']
# plt.scatter(X,Y,color='orange',alpha=0.2)
# ax1.set_xlim([0,120000])
# ax1.set_ylim([0,2500])
# plt.xlabel('Unit Price Yuan/m^2')
# plt.ylabel('Total Price 10k Yuan')
# plt.title('Distribution of unit price and total price')

##and area and total price.....

# ax2 = fig.add_subplot(1,2,2)
# X = data['area']
# Y = data['total_price']
# plt.scatter(X,Y,color='orange',alpha=0.2)
# ax2.set_xlim([0,500])
# ax2.set_ylim([0,2500])
# plt.xlabel('Area m^2')
# plt.ylabel('Total Price 10k Yuan')
# plt.title('Distribution of area and total price')
# plt.show()

##
# ax = plt.subplots(figsize=(8,6))
# ax = sns.boxplot(x='total_price',y='house_type',data=data,whis=1.5,orient='h')
# ax.axis(xmax=2000)
# ax.set_yticklabels([(u'商业综合体楼').encode('gbk'),u'纯写字楼',u'酒店写字楼',u'别墅',u'别墅|双拼',u'别墅|叠拼',u'别墅|独栋',u'别墅|联排',u'商住楼',u'商铺|专项卖场',u'商铺|临街门面',u'商铺|住宅底商',u'商铺|写字楼底商',u'商铺|商业街商铺',u'商铺|购物中心、百货',u'普通住宅',u'酒店式公寓'])
# plt.show()

##  尝试下violin 
# ax = plt.subplots(figsize=(14,6))
# ax = sns.boxplot(x='year',y='total_price',data=data,whis=1.5)
# ax.axis(ymax=3000)
# plt.xticks(rotation=90)
# plt.show()

cols = ['total_price', 'area', 'unit_price', 'num_bathroom', 'num_bedroom',
       'num_livingroom', 'plot_ratio', 'particular_level']
plt.figure(figsize=(10,10))
sns.pairplot(data[cols].dropna())
plt.show()

# execfile('D:\my_documents\python\scrape\house_price\leju\data_analysis.py')