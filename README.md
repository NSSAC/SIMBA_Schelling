# SIMBA_Schelling
## A framework for creating and implementing agent based models

# Running Simba
Execute run.sh to start SIMBA service
data/config.json to define module paths and execution order




\medskip\noindent
\textbf{Instructions.}
\begin{itemize}
%%
\item Obtain the source from: \texttt{https://github.com/NSSAC/SIMBA\_Schelling} 
%%
\item Download the population data (\url{synthetic_richmond.csv}) and boundary data (\url{geo_reference.csv}) into Schelling directory from "" \hsm{tbd} 
%%
\item Edit the configuration script to reference Schelling environment path and execution variables as defined in simba\_schelling/data/config.json. \hsm{more detail may be needed}
%%
\item Edit configuration script for slurm execution parameters - account details, run times, etc. 
\hsm{Can it run without slurm?}
%%
\item Run SIMBA/Schelling through run.sh launcher script; SIMBA assumes the default path to the configuration script to be under data/config.json. In the event other configuration files are created, they can be passed as an argument during execution. 

\hsm{Does it take arguments? Does it expect config files with conventions for where to look?}
\end{itemize}
%%
To verify the successful run of the SIMBA Schelling integration, a visualization of the segregated houshold locations can be generated through schelling/visualize\_run.py. 



The code minimally requires Python 3.8, Pandas 1.3.5, Geopandas 0.10.2, and Requests 2.28.1 and has been tested on Linux. Full details on the installation and run procedure are given here: 


\hsm{Hosting of data.} Can point to a URL for the admin region shapefiles. \hsm{Ian will provide.} Check size of CSV files after removal of unused columns + compress.


The source code for the SIMBA/Schelling implementation is made available under the Apache 2.0 license~\footnote{Apache 2.0 license \url{https://www.apache.org/licenses/LICENSE-2.0.html}} and the population data (\url{synthetic_richmond.csv}) is provided under the Creative Commons CC-BY-4.0 license\footnote{CC-BY-4.0~\url{https://creativecommons.org/licenses/by/4.0/}}. Geographic boundary data (\url{geo_reference.csv}) was derived from TIGER/Line data\footnote{https://catalog.data.gov/dataset/tiger-line-shapefile-2017-2010-state-virginia-2010-census-block-state-based}. 
