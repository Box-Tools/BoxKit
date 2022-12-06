#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import numpy
import boxkit

dataset_blocks=boxkit.api.read.dataset("/Users/Akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/heater2D/blocks/INS_Pool_Boiling_Heater_hdf5_0030")
dataset_oneblk=boxkit.api.read.dataset("/Users/Akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/heater2D/oneblk/INS_Pool_Boiling_Heater_hdf5_0030")
reshaped_dataset=boxkit.api.create.reshaped_dataset(dataset_blocks, "phi", nthreads=1)
