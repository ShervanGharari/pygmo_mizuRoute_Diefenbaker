    #!/cvmfs/soft.computecanada.ca/easybuild/software/2017/Core/python/3.5.4/bin/python

def run_mizuRoute (velocity, diffusivity, pid_path):

    import xarray as xr
    import glob
    import pandas as pd
    import os
    import numpy as np
    import shutil

    #########################
    # location of parameter file
    path_setup_temp = './folder_setup_temp/' # path were the temp set up is located
    path_setup      = './folder_setup_runs/'+pid_path+'/' # path were the temp set up will be saved
    # file that should be replaced with parameters
    file_name_tmp1  = 'param.nml.default.tmp' # the file that includes the string to be replaced
    file_name1      = 'param.nml.default' # the file that is used to be saved for model simulation
    old_strings     = ["velocity","diffusivity"]
    # file that should be replaced with case name
    file_name_tmp2  = 'param.nml.default.tmp' # the file that includes the string to be replaced
    file_name2      = 'param.nml.default' # the file that is used to be saved for model simulation
    old_strings     = ["case_name"]
    # name of he exe file and settgin file
    name_of_exe     = './route_runoff.cesm_coupling.exe'


    ###########################
    # replacing string function
    def replace_string (file_in, file_out, string_old, string_replaced):
        with open(file_in, "r+") as text_file:
            texts = text_file.read()
            for i in np.arange(len(string_old)):
                texts = texts.replace(string_old[i], string_replaced[i])
        with open(file_out, "w") as text_file:
            text_file.write(texts)

    ###########################
    # replacing string function
    def copy_folderA_to_folderB (path_org, path_target):
        # Copy the contents of folder A into folder B
        if not os.path.isdir(path_target):
            shutil.copytree(path_org, path_target)
        else:
            # Remove any files or folders in folder B that are not present in folder A
            for root, dirs, files in os.walk(path_target):
                for name in files + dirs:
                    path = os.path.join(root, name)
                    if not os.path.exists(os.path.join(folder_a, os.path.relpath(path, folder_b))):
                        os.remove(path)

    # move file from path_setup_temp to path_setup
    copy_folderA_to_folderB (path_setup_temp, path_setup)

    # replace the parameters and run mizuRoute
    V = "%.2f" % velocity
    D = "%.0f" % diffusivity
    case_name = 'V_'+V+'_D_'+D

    # update the parameter file
    replace_string (path_setup_temp+file_name_tmp1,path_setup+file_name1, old_strings, [V,D]) # replacing velocity and diffusivity
    replace_string (path_setup_temp+file_name_tmp2,path_setup+file_name2, old_strings, case_name) # replacing case name

    # execute mizuRoute
    os.system('chmod +x '+name_of_exe)
    os.system(name_of_exe+' '+path_setup+control)

    ## read the simulation
    file_name = sorted(glob.glob('./output/test/*mizuroute.h.2013-06-01*.nc'))
    file_name = file_name[0]
    ds = xr.open_dataset(file_name)
    simulated = ds.IRFroutedRunoff[:,15].values # for segment at Saskatoon in network topoogy

    # read the observation and pass that to the model
    observation  = pd.read_csv('./observation/observation_05HG001.csv') # station at Saskatoon
    observation  = np.array(observation ['Flow'])

    # root mean square error
    obj = ( (sum((simulated-observation)**2)/len(observation))**0.5 )

    # params
    return obj