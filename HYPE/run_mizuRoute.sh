#!/bin/bash

# module and python virtual env
module restore fhimp-mods

# cd to mizuRoute setup folder
cd mizuRoute

# create results folder
rm -rf ./output ./input
mkdir ./output ./input

# pass the HYPE timeLOFF.nc to input
cp ../HYPE/results/timeLOFF.nc ./input/timeLOFF.nc
find ./input/ -type f -exec basename {} \; | grep -v 'input_files.txt' > ./input/input_files.txt
cp ./ancillary_data/param.nml.default ./input/param.nml.default

# date and time
echo "start at $( date )"
./route_runoff.cesm_coupling.exe ./settings/control_file.control
echo "end at $( date)"

# merge various files into one
cd output
module load cdo; cdo mergetime *.nc outfile.nc
cd ..

# cd back
cd ..
