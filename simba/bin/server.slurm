#!/bin/bash
#SBATCH -t 1:00:00
#SBATCH -o logs/service.txt
#SBATCH -p bii
#SBATCH --mem=64000
#SBATCH -A gidi_ml


python ../simba/bin/modules/server.py $1
