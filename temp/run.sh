#!/bin/bash
#SBATCH -t 1:00:00
#SBATCH -o main.txt
#SBATCH -p bii
#SBATCH --mem=64000
#SBATCH -A gidi_ml

#module load gcc/9.2.0 anaconda/2020.11-py3.8
source activate model

python test.py
