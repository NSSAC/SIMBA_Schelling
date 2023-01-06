#!/bin/bash -l

#SBATCH --job-name=epihiperdb
#SBATCH -t 72:00:00
#SBATCH -p bii 
#SBATCH -A bii_nssac
#SBATCH --exclusive

DATAFOLDER=$1
HOSTNAME=$(hostname)
IMG=/project/biocomplexity/singularity_images/postgres-11.4.simg
DB=epihiper_db
DBUSER=epihiper
DBPASS=epihiper

# Echo the starting date (if this works)
echo "Starting instance ..."
date

# create the database data directory locally
mkdir -p $DATAFOLDER

# start instance
echo "Start Instance"
singularity instance start --bind $DATAFOLDER:/data $IMG $SLURM_JOB_ID

echo "Start postgresql"
singularity run --app start instance://$SLURM_JOB_ID 

# run createdb
echo "Create DB $DB"
singularity run --app createdb instance://$SLURM_JOB_ID $DB

# run createuser args are <user> <pass> <database>
singularity run --app createuser instance://$SLURM_JOB_ID $DBUSER $DBPASS $DB

# get connection host and port
CONNECTION=$(singularity run --app connection instance://$SLURM_JOB_ID)

#DO Stuff with the db 
echo "DB running on $CONNECTION"
sleep 20000

#shutdown the db cleanly
echo "Stop DB"
singularity run --app stop instance://$SLURM_JOB_ID

# stop the singularity instance
echo "Stop Singularity Instance"
singularity instance.stop $SLURM_JOB_ID
