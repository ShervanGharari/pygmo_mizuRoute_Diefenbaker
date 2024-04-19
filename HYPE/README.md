## HYPE model simulation

There are two version of HYPE model, one that support text input and output and one that support netcdf input and ouput.


### HYPE

To simulate HYPE without nc support one can run `./hype`. In the `info.txt` the line `readformat	4` and `netcdfoutput variable` should be commneted by `!! ` while the line `timeoutput variable` should be uncommented.

### HYPE nc

To simulate HYPE with nc support one can run `./hype_nc`. In the `info.txt` the line `readformat	4` and `netcdfoutput variable` should be uncommneted while the line `timeoutput variable` should be commented by `!! `.

### The output

Will be saved to `results` folder
