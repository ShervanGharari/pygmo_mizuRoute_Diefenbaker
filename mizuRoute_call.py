from assets import *
import hydrant.ObjectiveFucntions.ObjectiveFucntions as obj
import xarray as xr
import numpy as np
import os

def run_mizuRoute (UPDClass, X, pid):
    
    print(X, pid)
    print(UPDClass.CaseName)
    print(UPDClass.ParametersNames)
    print(UPDClass.ParametersNames)
    print(type(UPDClass.ParametersNames))
    

    import xarray as xr
    import glob
    import pandas as pd
    import os
    import numpy as np
    import shutil
    
    # working path
    working_path = UPDClass.WorkingFolder+pid+'/'
    
    print(working_path)
    
    # first copy the models folder into working directory
    copy_folderA_to_folderB (UPDClass.ModelSetupFolder, working_path)
    
    # change directory to the folder
    os.chdir(working_path)
    
    # replace the parameter name in the files
    for index, file in enumerate(UPDClass.ParametersFile):
        replace_string (UPDClass.ParametersFile[index],\
                        UPDClass.ParametersNames[index],\
                        "%.6f" % X[index])
    
    os.system('bash run_HYPE.sh')

    
    # Objective function manupulation
    observation  = xr.open_dataset('./observation/observation.nc') # station at Saskatoon
    simulation   = xr.open_dataset('./HYPE/results/timeCOUT.nc')
    Objective = obj.ObjectiveFunction(observation,
                                      simulation,
                                      info_obs={'var': 'Flow',
                                                'var_id': 'MERIT_SEG',
                                                'dim_id': 'STATION_NUMBER',
                                                'var_time': 'time',
                                                'dim_time': 'time'},
                                      info_sim={'var': 'COUT',
                                                'var_id': 'id',
                                                'dim_id': 'id',
                                                'var_time': 'time',
                                                'dim_time': 'time'},
                                      TimeStep='daily')
    obj = 1-sum(Objective['KGE'].values)
    
    # remove the changed file to be populated in the next itteration
    for index, file in enumerate(UPDClass.ParametersFile):
        os.remove(file)
        
    
    # save the record before leaving
    os.chdir(UPDClass.WorkingFolder)
    if not os.path.isfile(pid+'.csv'):
        
    else:
        
    
    

    # params
    return obj