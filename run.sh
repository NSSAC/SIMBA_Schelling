#!/bin/bash

LOC="runs_"$(date +%s)
mkdir $LOC


#ADDR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $LOC
mkdir "logs"

chmod -R 755 "logs"

sbatch ../simba/bin/main.slurm ../config.json

