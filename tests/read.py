# Import libraries
import h5py
import numpy
import bubblebox

# Read the hdf5 file
file_path  = '/home/akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/INS_Pool_Boiling_hdf5_0054'
input_file = h5py.File(file_path,'r')

# Create data object
data3D = bubblebox.Data(input_file['quantities'])

# Extract axes index and total number of blocks
iaxis,jaxis,kaxis = [0,1,2]
lblocks = input_file['numbox'][iaxis]*input_file['numbox'][jaxis]*input_file['numbox'][kaxis]

# Create blocks
block3D = []
for lblock in range(lblocks):

    block_attributes = {'nxb'  : input_file['sizebox'][iaxis],
                        'nyb'  : input_file['sizebox'][jaxis],
                        'nzb'  : input_file['sizebox'][kaxis],
                        'xmin' : input_file['boundbox/min'][lblock,iaxis],
                        'ymin' : input_file['boundbox/min'][lblock,jaxis],
                        'zmin' : input_file['boundbox/min'][lblock,kaxis],
                        'xmax' : input_file['boundbox/max'][lblock,iaxis],
                        'ymax' : input_file['boundbox/max'][lblock,jaxis],
                        'zmax' : input_file['boundbox/max'][lblock,kaxis],
                        'tag'  : lblock}

    block3D.append(bubblebox.Block(block_attributes,data3D))


# Create grid
grid_attributes = {'xmin' : -2.0,
                   'ymin' :  0.0,
                   'zmin' : -5.0,
                   'xmax' :  5.0,
                   'ymax' : 10.0,
                   'zmax' :  5.0}

grid3D = bubblebox.Grid(grid_attributes,block3D)

print(grid3D.lbx,grid3D.lby,grid3D.lbz)
