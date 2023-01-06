# postgres_singularity

To create and run a postgres database in a singularity container on rivanna:

1. Copy/edit the postgres_rundb.sh file, setting the &lt;partition name&gt; and &lt;account name&gt; in the SBATCH header to the appropriate values.

2. Update also the DB, DBUSER, and DBPASS variables to the desired values.

3. Run postgres_rundb.sh at the command-line, as follows, with the target directory as a commandline paramater:

(base) -bash-4.2$sbatch postgres_rundb.sh /scratch/alw4ey/database_dir

4. Run squeue to get the NODELIST(REASON) value -- you will need this to access your database:

(base) -bash-4.2$squeue -u &lt;computeID&gt;

             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
             
           5023347       bii postgres   alw4ey  R       0:49      1 udc-aj38-11c0

5. Run psql with the NODELIST(REASON) value as the hostname, as in the example below:

(base) -bash-4.2$psql -h udc-aj38-11c0 -U testuser test

Password for user testuser: 

(Note: this may fail if the database is not fully mounted. You can check the status of the database in the slurm-&lt;id&gt;.out)

6. To shut down database type scancel -b -s SIGINT <SLURM_ID>, ie:

scancel -b -s SIGINT 5023347

## pgbouncer
Looks for DATAROOT/pgbounce with pgbouncer.ini  userlist.txt specified.

At present pgbouncer requires specifying host to connect to e.g. 
```
psql -p 6432 -h 0.0.0.0 -d epihiper_db -U epihiper
```

