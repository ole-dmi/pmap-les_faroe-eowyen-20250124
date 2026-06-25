#!/bin/bash -l
#SBATCH --job-name=pmap-les         # Job name
#SBATCH --partition=standard-g           # Partition (queue) name
#SBATCH --nodes=1                   # Total number of nodes
#SBATCH --ntasks=1                  # Total number of mpi tasks
#SBATCH --gpus-per-task=1           # Total number of mpi tasks
#SBATCH --mem=0                     # Allocate all the memory on the node
#SBATCH --time=0-03:00:00           # Run time (d-hh:mm:ss)
#SBATCH --mail-type=all             # Send email at begin and end of job
#SBATCH --account=project_465000527 # Project for billing
#SBATCH --mail-user=oli@dmi.com     # Any other commands must follow the #SBATCH directives


#OMP_NUM_THREADS=32
#OMP_PLACES=cores 
#OMP_PROC_BIND=close

module load PrgEnv-amd
module load rocm
module load cray-hdf5-parallel
module load cray-netcdf-hdf5parallel

source  $3/venv/bin/activate

echo "[$0] running $0 ..."
echo "[$0] output directory   : $1"
echo "[$0] configuration file : $2"
echo "[$0] running pmap-les ..."

srun pmap-les -o $1 $2 # Use srun instead of mpirun or mpiexec

echo "[$0] done"
