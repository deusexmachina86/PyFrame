import h5py as h5
import numpy as np
from scipy.interpolate import interp1d
import os, glob
import statistics
from statistics import mean 
import utilities.utilities as utils
import matplotlib.pyplot as plt
import re 
import chunking
import plottings 
import pickle
import pandas as pd 
import getcarid 
import plottings_no_spdlimt

def get_carid(filename):
        car_id = filename.split('_')
        return f'Car_{car_id[1]}'


#Specify the needed signals here
test = utils.Utilities()
# signal_names    = ['VehSpdLgtSafe','SpdLimFirst','EngSpdDispd','TrsmVehSpd','ALgt1','DrvrDesDir',
#                     'HiWay','AccSts','AsySftyDecelReq','SteerAsscCtrlActv','RngOfTar','TiToTarIndcn','SftyCchDstToTar',
#                     'EmgyBrkDstParkAut','BrkPedlNotPsdSafe','BrkPedlPsd','DstInfoTar','DrvrDecelReq','ObjThreatTiToCllsn',
#                     'RngRateOfTar', 'SftyCchAccStsActv','AsySftyEnaDecel', 'RoadIncln']

# interp_strategy = ['zero', 'zero',  'zero',  'zero', 'zero', 'zero','zero','zero', 'zero','zero',
#                     'zero', 'zero',  'zero',  'zero', 'zero', 'zero','zero','zero', 'zero','zero',
#                     'zero', 'zero',  'zero'] 

signal_names    = ['VehSpdLgtSafe','DrvrDesDir', 'AccSts','ALgt1',
                    'RngOfTar','TiToTarIndcn',
                    'DrvrDecelReq','ObjThreatTiToCllsn',
                  'AsySftyEnaDecel', 'RoadIncln','DstInfoTar']

interp_strategy = ['zero','zero','zero','zero','zero','zero','zero','zero','zero','zero','zero'] 

# signal_names    = ['VehSpdLgtSafe', 'AccSts',
#                      'ALgt1','AsySftyEnaDecel']

# interp_strategy = ['zero','zero','zero','zero'] 

# - Get filepaths in a folder and get the datafiles in a list called 'files' which have to be trimmed as it could contain 
# folder names also
# The following code crawls through the whole month of data and fecthes the names of all data files in a list
# In order to scale this code for the whole WICE data, we can wait for the cloud solution to be ready as processing
# the whole data uwill consume too much of computtaional/storage resources 
directory=r'/home/pamadmin/WICE/2022-09'

files = []
for filename in glob.iglob(directory+ '**/**', recursive=True):
    files.append(filename)
files_trm = []
for fs in range(len(files)):
    if(files[fs].endswith('.sydata')):
        files_trm.append(files[fs])
    else:
        continue
carids = [get_carid(i) for i in files_trm]   
unique_ids = []
for id in carids:
    if id not in unique_ids:
        unique_ids.append(id)
# Filling complete filenames of a the same id in one list

	list_of_lists= []      
	for id in range(len(unique_ids)):
	    slider = 0
	    temp_list = []
	    for f in range(len(files_trm)):
	        match = re.search(unique_ids[id][0], files_trm[f])
	        if match:
	          print(f'id:{id}')
	          print(f'f:{f}')
	          print(f'slider:{slider}')
	          print('found')
	          ff = files_trm[f]
	          temp_list.append(ff)
	          slider+=1
	        else:
	           print('did not find')
	    list_of_lists.append(temp_list)        
        
##################################################################################
# Set here how many cars you want to analyze with respect to their size of 
#drive measurements data; the selection will be made starting from max size 
nth_value = 50

fleet_sizes = []
for lists in range(len(list_of_lists)):
    fleet_sizes.append(len(list_of_lists[:][lists]))
sorted_fleet_sizes = sorted(fleet_sizes,reverse=True) 

top_nth =  sorted_fleet_sizes[nth_value] 
    

# Analysis will be done only on the car ids who have higher and equal to top_nth measurement files. 
# Indices carries the index of such car_ids in list_of_lists
indices = []
for lists in range(len(list_of_lists)):
    if len(list_of_lists[:][lists]) >= top_nth:
        indices.append(lists)
        nr_measurement_files = len(list_of_lists[:][lists])
        print(nr_measurement_files)


selected_files = [list_of_lists[i][:] for i in indices]
####################################################################### 
#######################################################################################

# carids = ['Car_2562']
fs = 1
for cars in range(len(carids)):
    current_car = carids[cars][0]
    # selected_files = [x for x in files_trm if current_car in x]    
    tables_tst, mis_signals_tst = test.execute(selected_files, signal_names, interp_strategy, fs)
    with open("tables_tst"+f"_{current_car}", "wb") as fp:   #Pickling
        pickle.dump(tables_tst, fp)
    with open("mis_signals_tst"+f"_{current_car}", "wb") as fp:   #Pickling
        pickle.dump(mis_signals_tst, fp)
    
    





