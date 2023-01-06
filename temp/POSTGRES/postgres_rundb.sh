#!/bin/bash -l

#SBATCH --job-name=psqlsing
#SBATCH -t 72:00:00
#SBATCH -p bii	
#SBATCH -A gidi_ml
#SBATCH --exclusive
#SBATCH --nodes=1

# JWD=`pwd`
# INPUT=$JWD/input
# DATAFOLDER=$INPUT/_db
DATAFOLDER=$1
HOSTNAME=$(hostname)
IMG=/project/biocomplexity/singularity_images/postgres-11.4.sif
DB=test_db
DBUSER=testuser
DBPASS=testpass
INTERFACE=ib0

module load singularity
#module --ignore-cache load "singularity/3.1.1"
# create the database data directory locally
#mkdir -p $DATAFOLDER

# let retval=$?
# [ ${retval} != 0 ] && exit ${retval}

# start instance
echo "Start Instance"
singularity instance start --bind $DATAFOLDER:/data $IMG $SLURM_JOB_ID
let retval=$?
[ ${retval} != 0 ] && exit ${retval}

echo "Start postgresql"
singularity run --app start instance://$SLURM_JOB_ID
let retval=$?
[ ${retval} != 0 ] && exit ${retval}

# run createdb
echo "Create DB $DB"
singularity run --app createdb instance://$SLURM_JOB_ID $DB

# run createuser args are <user> <pass> <database>
singularity run --app createuser instance://$SLURM_JOB_ID $DBUSER $DBPASS $DB

# get connection host and port
# singularity --app connection returns the hostname:port
CONNECTION=$(singularity run --app connection instance://$SLURM_JOB_ID)
#extract the port from the connection return from singularity
PORT=$(echo $CONNECTION |  awk '{split($0,a,":"); print a[2]}')
#get the ip address of the interface we want db consumers to target
IFIP=`ip addr show $INTERFACE | grep -o "inet [0-9]*\.[0-9]*\.[0-9]*\.[0-9]*" | grep -o "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*"`

CONN=$IFIP:5432
echo "Write connection and status to sciduct.status.json"
echo '{"host":"'$CONN'", "progress": 1, "status": "READY"}' > db.status.json

#DO Stuff with the db 
echo "DB running on $CONN"

handler()
{
  echo "Closing Database..."
  #shutdown the db cleanly
  echo "Stop DB"
  singularity run --app stop instance://$SLURM_JOB_ID

  # stop the singularity instance
  echo "Stop Singularity Instance"
  singularity instance stop $SLURM_JOB_ID
  echo '{"host":"'$CONN'", "progress": 100, "status": "CLOSED"}' > db.status.json

}

trap 'handler' SIGINT

echo "Waiting for DB Completion..."
while [ -e $DATAFOLDER/postgres/postmaster.pid ] ;do
  sleep 2
done;


