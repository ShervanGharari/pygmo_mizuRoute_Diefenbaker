#!/bin/bash

# module and python virtual env
module restore fhimp-mods
source ~/FHIMP/virtual_env/fhimp_venv/bin/activate

cd HYPE

# create results folder
rm -rf ./results hyss*.log tests*.log
mkdir ./results

# classic version using txt input files
# the info.txt should be adjusted for reading
# or writing output as txt files
# echo "start at $( date )"
# ./hype
# echo "end at $( date)"

# netcdf enabled version using nc input files
# the info.txt should be adjusted for reading
# or writing output as nc files
# date and time
echo "start at $( date )"
./hype_nc
echo "end at $( date)"

cd ..

cd  post_processing
python HYPE.py
cd ..
