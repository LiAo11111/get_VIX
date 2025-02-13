#!/usr/bin/env python
# coding: utf-8

# In[132]:


from typing import Dict, List, Tuple, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import empyrical as ep
from data_service import (get_interpld_shibor, get_shibor_data, prepare_data,
                          query_china_shibor_all)
from jqdatasdk import *

from scr.calc_func import (CVIX, prepare_data2calc, get_n_next_ret,
                           get_quantreg_res,create_quantile_bound)

from scr.plotting import (plot_group_ret, plot_hist2d, plot_indicator,
                          plot_quantreg_res)

from scr.utils import load_csv
# 设置字体 用来正常显示中文标签
mpl.rcParams['font.sans-serif'] = ['SimHei']
#mpl.rcParams['font.family'] = 'serif'
# 用来正常显示负号
mpl.rcParams['axes.unicode_minus'] = False


# In[161]:


# from jqdatasdk import *
# auth("18746950003","Asdlkj0011")

# 算法代码可参考：
# >《20180707_东北证券_金融工程_市场波动风险度量：vix与skew指数构建与应用》

# ---

# In[179]:


# # # 数据获取
# start, end = '2021-01-01', '2023-12-31'
# # # opt_data = prepare_data('510050.XSHG', start, end)  # 上证etf50
# # # opt_data = prepare_data('000300.XSHG', start, end)  # 沪深300 CCFX  000300.XSHG
# # # opt_data = prepare_data('000016.XSHG', start, end) # 上证50—CCFX 000016.XSHG
# # # opt_data = prepare_data('000852.XSHG', start, end) # 中证1000 CCFX 000852.XSHG
# #
# # # # opt_data = pd.read_csv('.csv')
# shibor_df = get_shibor_data(start, end)
# # #
# # # # 插值
# interpld_shibor = get_interpld_shibor(shibor_df)

# In[180]:


# # # # 数据储存
# # # opt_data.to_csv(r'./Data/opt_data_zz1000.csv')
# interpld_shibor.to_csv(r'./Data/interpld_shibor_sz50etf.csv')

# ---

# # 数据已经获取完毕 可直接读取

# In[197]:


# 数据读取 hs300 sz50  sz50etf zz1000
opt_data: pd.DataFrame = pd.read_csv(r'Data/opt_data_sz50etf.csv',
                                     index_col=[0],
                                     parse_dates=['date'])

interpld_shibor: pd.DataFrame = pd.read_csv(r'Data/interpld_shibor_sz50etf.csv',
                                            index_col=[0],
                                            parse_dates=True)

interpld_shibor.columns = list(map(int, interpld_shibor.columns))


# In[198]:


# 前期数据整理
data_all = prepare_data2calc(opt_data, interpld_shibor)

# In[199]:


# 加载模块
vix_func = CVIX(data_all)

# In[200]:


# 计算vix
vix: pd.Series = vix_func.vix()
vix.to_csv('sz50etf_vix.csv')  # sz50  sz50etf zz1000

# 绘制VIX变化曲线
plt.figure(figsize=(14, 7))
plt.plot(vix.index, vix.values, label='sz50etf VIX', color='blue')
plt.title('sz50etf VIX Over Time')
plt.xlabel('Date')
plt.ylabel('VIX Value')
plt.legend()
plt.grid(True)

# 保存图表为PNG文件
plt.savefig('sz50etf_vix.png')
plt.close()  # 关闭图表以释放内存

# 计算skew
skew: pd.Series = vix_func.skew()
skew.to_csv('sz50etf_skew.csv') # sz50  sz50etf zz1000

# 绘制Skew变化曲线
plt.figure(figsize=(14, 7))
plt.plot(skew.index, skew.values, label='sz50etf Skew', color='red')
plt.title('sz50etf Skew Over Time')
plt.xlabel('Date')
plt.ylabel('Skew Value')
plt.legend()
plt.grid(True)

# 保存图表为PNG文件
plt.savefig('sz50etf_skew.png')
plt.close()  # 关闭图表以释放内存

print("VIX and Skew calculations completed and images saved.")
# In[ ]:



