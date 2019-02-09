#!/usr/bin/env python
# coding: utf-8

# In[4]:


import json
import numpy as np
import matplotlib.pyplot as plt


# In[49]:


### resultfps(1), resultlat(1) -> ROS Raw Image and Depth. (1) -> Depth
### comfps(1), comlat(1) -> ROS Compressed Image and Depth (1) -> Depth


# In[5]:


with open("./result(480)/resultfps.json","r") as inputfile:
    fps = json.load(inputfile)
with open("./result(480)/resultLat.json","r") as inp:
    lat = json.load(inp)
with open("./result(480)/resultfps1.json","r") as inputfile:
    fps1 = json.load(inputfile)
with open("./result(480)/resultLat1.json","r") as inp:
    lat1 = json.load(inp)
with open("./result(480)/comfps.json","r") as inputfile:
    cfps = json.load(inputfile)
with open("./result(480)/comlat.json","r") as inp:
    clat = json.load(inp)
with open("./result(480)/comfps1.json","r") as inputfile:
    cfps1 = json.load(inputfile)
with open("./result(480)/comlat1.json","r") as inp:
    clat1 = json.load(inp)    
    


# In[11]:


import pandas as pd
df = pd.DataFrame({"time":np.arange(0,505,5),"color_raw":fps,"color_c":cfps,"dep_raw":fps1,"dep_c":cfps1})
df.to_csv("480_fps.csv")

df = pd.DataFrame({"time":np.arange(0,505,5),"color_raw":lat,"color_c":clat,"dep_raw":lat1,"dep_c":clat1})


# In[11]:


def lineplot(x,y,x_label="",y_label="",title=""):
    _, ax = plt.subplots()
    ax.plot(x,y,lw=2,color="#539caf",alpha=1)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)


# In[12]:


lineplot(np.arange(0,505,5),fps, "Sec", "FPS","Color Raw FPS Rate")
lineplot(np.arange(0,505,5),fps1, "Sec", "FPS","Depth Raw FPS Rate")
lineplot(np.arange(0,505,5),np.multiply(lat,1000), "ms", "Latency(s)","Color Raw Latency")
lineplot(np.arange(0,505,5),np.multiply(lat1,1000), "ms", "Latency(s)","Depth Raw Latency")


# In[13]:


lineplot(np.arange(0,505,5),cfps, "Sec", "FPS","Color C FPS Rate")
lineplot(np.arange(0,505,5),cfps1, "Sec", "FPS","Depth C FPS Rate")
lineplot(np.arange(0,505,5),np.multiply(clat,1000), "ms", "Latency(s)","Color C Latency")
lineplot(np.arange(0,505,5),np.multiply(clat1,1000), "ms", "Latency(s)","Depth C Latency")


# In[44]:




