#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bokeh.io import output_notebook, output_file
from bokeh.plotting import figure, show, ColumnDataSource, curdoc
import pandas as pd
from bokeh.models import CategoricalColorMapper, HoverTool
from bokeh.embed import components
from bokeh.layouts import column, row, widgetbox
import numpy as np
import json


# In[2]:


#data I need high, low, open, close, volume, percent change, symbol for 9/25/2020
#4 categories
#Equities: ES, NQ, RTY, YM
#Energys: CL, NG, HO
#Metals: Gold, Silver, Copper, Platinum
#Currencies: DXY, Euro, Australian Dollar, Japanese Yen, Swiss Franc, Canadian Dollar, British Pound


# In[3]:


# Importing Equities Data
es = pd.read_csv('./data/ES=F.csv')
es['symbol'] = 'ES'
nq = pd.read_csv('./data/NQ=F.csv')
nq['symbol'] = 'NQ'
rty = pd.read_csv('./data/RTY=F.csv')
rty['symbol'] = 'RTY'
ym = pd.read_csv('./data/YM=F.csv')
ym['symbol'] = 'YM'


# In[4]:


# Joining Equities Tables, dropping 9/24 rows, adding percent change column, add Category column
equities = es.append([nq, rty, ym])
equities['Category'] = 'Equity'
equities = equities[equities.Date=='2020-09-25']
equities['percent_change'] = ((equities['Close']-equities['Open'])/equities['Open'])*100
equities


# In[5]:


# Importing Energies Data
cl = pd.read_csv('./data/CL=F.csv')
cl['symbol'] = 'CL'
ng = pd.read_csv('./data/NG=F.csv')
ng['symbol'] = 'NG'
ho = pd.read_csv('./data/HO=F.csv')
ho['symbol'] = 'HO'


# In[6]:


# Joining Energies Tables, dropping 9/24 rows, adding percent change column, add Category column
energies = cl.append([ng, ho])
energies['Category'] = 'Energy'
energies = energies[energies.Date=='2020-09-25']
energies['percent_change'] = ((energies['Close']-energies['Open'])/energies['Open'])*100
energies


# In[7]:


# Importing Metals Data
gc = pd.read_csv('./data/GC=F.csv')
gc['symbol'] = 'GC'
si = pd.read_csv('./data/SI=F.csv')
si['symbol'] = 'SI'
pl = pd.read_csv('./data/PL=F.csv')
pl['symbol'] = 'PL'
hg = pd.read_csv('./data/HG=F.csv')
hg['symbol'] = 'Hg'


# In[8]:


# Joining metals Tables, dropping 9/24 rows, adding percent change column, add Category column
metals = gc.append([si, pl, hg])
metals['Category'] = 'Metal'
metals = metals[metals.Date=='2020-09-25']
metals['percent_change'] = ((metals['Close']-metals['Open'])/metals['Open'])*100
metals


# In[9]:


# Importing Currencies Data
a = pd.read_csv('./data/6A=F.csv')
a['symbol'] = '6A'
b = pd.read_csv('./data/6B=F.csv')
b['symbol'] = '6B'
c = pd.read_csv('./data/6C=F.csv')
c['symbol'] = '6C'
e = pd.read_csv('./data/6E=F.csv')
e['symbol'] = '6E'
j = pd.read_csv('./data/6J=F.csv')
j['symbol'] = '6J'
s = pd.read_csv('./data/6S=F.csv')
s['symbol'] = '6S'


# In[10]:


# Joining Currencies Tables, dropping 9/24 rows, adding percent change column, add Category column
currencies = a.append([b, c, e, j, s])
currencies['Category'] = 'Currency'
currencies = currencies[currencies.Date=='2020-09-25']
currencies['percent_change'] = ((currencies['Close']-currencies['Open'])/currencies['Open'])*100
currencies


# In[11]:


#adding all the tables together
futures = equities.append([energies, metals, currencies]).reset_index().drop('index', axis=1).reset_index()
futures['size'] = pd.cut(futures.Volume, bins = [0, 500, 5000, 50000, 500000, 5000000], labels = [15,30,45,60,75])
futures


# In[12]:


# Convert df to a ColumnDataSource: source
source = ColumnDataSource(futures)

# Make a CategoricalColorMapper object: color_mapper
color_mapper = CategoricalColorMapper(factors=['Equity', 'Energy', 'Metal', 'Currency'],
                                      palette=['red', 'purple', 'blue', 'green'])

p = figure(y_range=(-3,4), x_axis_label = "Futures Products", y_axis_label = "Percent Change", title = "Percent Changes in Futures Market for 9/25/2020")

# Add a circle glyph to the figure p
p.circle('index', 'percent_change', source=source,
         color=dict(field='Category', transform=color_mapper),
         legend_group='Category', size='size', alpha=.5,
         hover_fill_color='pink', hover_alpha=.5,
         hover_line_color='white')

p.background_fill_color = ("white")

tt = tooltips = [("Symbol", "@symbol"),
                       ("Category", "@Category"),
                       ("Percent Change", "@percent_change{0.00}"),
                       ("Open", "@Open{0.00}"),
                       ("Close", "@Close{0.00}"),
                       ("High", "@High{0.00}"),
                       ("Low", "@Low{0.00}"),
                       ("Volume", "@Volume{0.00}")]
hover = HoverTool(tooltips=tt)
p.add_tools(hover)


# In[13]:


# output_notebook()


# In[14]:


# show(p)


# In[15]:


curdoc().add_root(column(p))
curdoc().title = "Sliders"


# In[16]:


# !jupyter nbconvert --to script Index.ipynb
# !bokeh serve --show Index.py --port 8000 --allow-websocket-origin=*


# In[ ]:





# In[ ]:




