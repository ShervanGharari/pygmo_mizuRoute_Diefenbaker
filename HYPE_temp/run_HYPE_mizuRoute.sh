#!/bin/bash

# module and python virtual env
module restore fhimp-mods

# run HYPE
bash run_HYPE.sh

# run mizuRoute
bash run_mizuRoute.sh
