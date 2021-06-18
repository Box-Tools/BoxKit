# Import libraries
import h5py
import numpy
import bubblebox

# Read the hdf5 file
file_path  = '/home/akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/INS_Pool_Boiling_hdf5_0054'
input_file = h5py.File(file_path,'r')

# Create data object
lblocks = input_file['numbox'][0]*input_file['numbox'][1]*input_file['numbox'][2]
data_attributes = {'lblocks' : lblocks,
                   'nxb'     : input_file['sizebox'][0],
                   'nyb'     : input_file['sizebox'][1],
                   'nzb'     : input_file['sizebox'][2],
                   'xmin'    : input_file['boundbox/min'][:,0],
                   'ymin'    : input_file['boundbox/min'][:,1],
                   'zmin'    : input_file['boundbox/min'][:,2],
                   'xmax'    : input_file['boundbox/max'][:,0],
                   'ymax'    : input_file['boundbox/max'][:,1],
                   'zmax'    : input_file['boundbox/max'][:,2]}

data3D = bubblebox.core.Data(attributes=data_attributes, variables=input_file['quantities'])

# Create block objects
block_attributes = [ {'nxb'  : data3D.nxb,
                      'nyb'  : data3D.nyb,
                      'nzb'  : data3D.nzb,
                      'xmin' : data3D.xmin[lblock],
                      'ymin' : data3D.ymin[lblock],
                      'zmin' : data3D.zmin[lblock],
                      'xmax' : data3D.xmax[lblock],
                      'ymax' : data3D.ymax[lblock],
                      'zmax' : data3D.zmax[lblock],
                      'tag'  : lblock} for lblock in range(data3D.lblocks)]

blocks3D = [bubblebox.core.Block(attributes=block_attr, data=data3D) for block_attr in block_attributes]

# Create grid object
grid_attributes = {'xmin' : -2.5,
                   'ymin' :  2.5,
                   'zmin' : -2.5,
                   'xmax' :  2.5,
                   'ymax' : 10.0,
                   'zmax' :  2.5}

grid3D = bubblebox.core.Grid(attributes=grid_attributes, blocks=blocks3D)

print(grid3D.data.variables,blocks3D[0].data.variables,blocks3D[100].data.variables,data3D.variables)
print(grid3D.blocks[0].tag,grid3D.blocks[10].tag)
