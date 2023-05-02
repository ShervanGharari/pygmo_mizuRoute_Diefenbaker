#!/bin/bash
#SBATCH --account=rpp-kshook
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=1G
#SBATCH --time=00:10:00           # time (DD-HH:MM)
#SBATCH --job-name=pygmo_test_parallel
#SBATCH --error=errors1

module purge
module load gcc/9.3.0
module load pagmo/2.18.0
module load python/3.8
rm -rf $HOME/pygmo-env
virtualenv $HOME/pygmo-env
source $HOME/pygmo-env/bin/activate
pip install --no-index --upgrade pip
pip install --no-index --upgrade matplotlib
pip install --no-index --upgrade pandas
pip install --no-index 'pygmo==2.18.0'
# srun python test_gmo_parallel.py
python test_gmo_parallel.py
