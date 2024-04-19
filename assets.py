
import os
import shutil
import multiprocessing


###########################
# replacing string function
def replace_string (file, string_old, string_replaced):
    with open(file, "r+") as text_file:
        texts = text_file.read()
        texts = texts.replace(string_old, string_replaced)
    with open(file, "w") as text_file:
        text_file.write(texts)

###########################
# match the folders
def copy_folderA_to_folderB (path_org, path_target):
    # Copy the contents of folder original path_org into folder target path_target
    if not os.path.isdir(path_target):
        shutil.copytree(path_org, path_target)
    else:
        # Remove any files or folders in folder path_target that are not present in folder path_org
        for root, dirs, files in os.walk(path_target):
            for name in files + dirs:
                path = os.path.join(root, name)
                if not os.path.exists(os.path.join(path_org, os.path.relpath(path, path_target))):
                    os.remove(path)
        # Add any files or folder to folder path_target that is not in path_org
        for root, dirs, files in os.walk(path_org):
            for name in files + dirs:
                source_path = os.path.join(root, name)
                target_path = os.path.join(path_target, os.path.relpath(source_path, path_org))
                if not os.path.exists(target_path):
                    if os.path.isdir(source_path):
                        os.makedirs(target_path)
                    else:
                        shutil.copy2(source_path, target_path)
                    
###########################
# get the number of processor
def GetNumProcessor (MaxCPUAllowed = None):

    # set the number of CPUs for possible parallel computing
    num_processes = multiprocessing.cpu_count()  # Use the number of available CPU cores
    num_processes = max (num_processes-1, 1) # reserve one cpu outside
    if MaxCPUAllowed is not None:
        num_processes = min (MaxCPUAllowed, num_processes)  # Limit the worker to number of cpu provided
    num_processes = max (num_processes, 1) # make sure max is 1
    # check if inside a job
    schedulers = {
                "SLURM": ['SLURM_JOBID', 'SLURM_JOB_NAME', 'SLURM_NODELIST'],
                "PBS": ['PBS_JOBID', 'PBS_JOBNAME', 'PBS_NODEFILE'],
                "LSF": ['LSB_JOBID', 'LSB_JOBNAME', 'LSB_MCPU_HOSTS'],
                "Kubernetes": ['KUBERNETES_SERVICE_HOST', 'KUBERNETES_SERVICE_PORT'],
                # Add more schedulers and their respective environment variables as needed
            }
    for scheduler, env_vars in schedulers.items():
        detected_vars = [var for var in env_vars if var in os.environ]
        if detected_vars:
            print(f"Running within a {scheduler} job.")
            print(f"{scheduler} environment variables found:", detected_vars)
            num_processes = len(os.sched_getaffinity(0))
            num_processes = max (num_processes, 1) # make sure max is 1
    # return
    return num_processes
