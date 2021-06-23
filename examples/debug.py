import bubblebox.api.sample as box

basedir   = '/home/akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/'
prefix    = 'INS_Pool_Boiling_hdf5_'

filetag   = 5
filename  = "".join([basedir,prefix,str(filetag).zfill(4)])

dataset   = box.read_dataset(filename)

"""
Run some operations
"""

dataset.inputfile.close()
