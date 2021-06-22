import bubblebox.api.sample as box

basedir   = '/home/akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/'
prefix    = 'INS_Pool_Boiling_hdf5_'

filetags  = [0,5,10,15,20,25,30,35,40,45,50,55]  
filenames = ["".join([basedir,prefix,str(filetag).zfill(4)]) for filetag in filetags]

datasets  = [box.read_dataset(filename) for filename in filenames]

"""
Run some operations
"""

[dataset.inputfile.close() for dataset in datasets]
