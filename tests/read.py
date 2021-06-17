# Import libraries
import h5py
import bubblebox

# Read the hdf5 file
file_path  = '/home/akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/INS_Pool_Boiling_hdf5_0054'
input_file = h5py.File(file_path,'r')

# Create data object
data = bubblebox.data(input_file['quantities'])

iaxis,jaxis,kaxis = [0,1,2]

lblocks = input_file['numbox'][iaxis]*input_file['numbox'][jaxis]*input_file['numbox'][kaxis]
blocks  = []

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

    blocks.append(bubblebox.block(block_attributes,data))


grid_attributes = {'xmin' : -2.5,
                   'ymin' :  2.5,
                   'zmin' : -2.5,
                   'xmax' :  2.5,
                   'ymax' :  9.0,
                   'zmax' :  2.5}

grid = bubblebox.grid(grid_attributes,blocks)

