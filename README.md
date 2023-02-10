# SIMBA_Schelling

## Summary
This git repository contains code for demonstrating the SIMBA framework in the context of the Schelling model for segregation. It is applied to Richmond, VA for which there is accompanying data. 

## Preliminaries
The following preparatory steps are required:
- Download the git repository: https://github.com/NSSAC/SIMBA\_Schelling into a base diretory <yournamehere>.
- From the folder https://net.science/files/0c7ae1b6-13d3-4a97-8851-95e3b0e909f8/ download:
  - The person/household synthetic_richmond.csv
  - The boundary data file geo_reference.csv

## Requirements
The code minimally requires Python 3.8, Pandas 1.3.5, Geopandas 0.10.2, and Requests 2.28.1. Currently, it has only been tested under Linux.


## Running the Simba-Schelling model
NEED UPDDATES HERE
  
- Execute run.sh to start SIMBA service
- data/config.json to define module paths and execution order
- Edit the configuration script to reference Schelling environment path and execution variables as defined in simba\_schelling/data/config.json. 
- Edit configuration script for slurm execution parameters - account details, run times, etc. 
- Run SIMBA/Schelling through run.sh launcher script; SIMBA assumes the default path to the configuration script to be under data/config.json. In the event other configuration files are created, they can be passed as an argument during execution. 

To verify the successful run of the SIMBA Schelling integration, a visualization of the segregated houshold locations can be generated through schelling/visualize\_run.py. 


  
## Licenses
The code in the SIMBA_Schelling repository uses the Apache 2.0 license, see https://www.apache.org/licenses/LICENSE-2.0.html. The two data files (a and b) are made available under the CC-BY-4.0 license, see https://creativecommons.org/licenses/by/4.0/. 

## References
- Anderson, T., Leung, A., Dragicevic, S., Perez, L.: Modeling the geospatial dynamics of residential segregation in three Canadian cities: An agent-based approach. Transactions in GIS 25(2), 948–967 (2021)
- The geographic boundary data geo_reference.csv was derived from TIGER/Line data, see https://catalog.data.gov/dataset/tiger-line-shapefile-2017-2010-state-virginia-2010-census-block-state-based  



