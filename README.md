# PMAP-LES real cases (DMI/LAM)

This repository collects PMAP-LES installation procedures and real-case setups.
General installation instructions are below; case-specific walkthroughs live in
the [Cases](#cases) section.

## PMAP-LES installation on ATOS 

### 1: Download PMAP: 

```
git clone git@github.com:PMAP-Project/PMAP-real_cases-shared.git
cd PMAP-real_cases-shared/
```
### 2: Create a virtual python environment:

```
module load python3
python3 -m venv venv
```

### 3: Copy this slurm script into `pmap_install.sh`:

```
#!/bin/bash 
#SBATCH --job-name=pmap_install
#SBATCH --output=pmap_install-%J.out
#SBATCH --error=pmap_install-%J.out

module load prgenv/intel
module load intel-mpi
module load hdf5-parallel
module load netcdf4

source venv/bin/activate

pip install -r requirements-dev-mpi.txt && pip install -e .
```
and run

```
sbatch pmap_install.sh
```


## PMAP-LES installation on LUMI using `hpc-scripts`

This installation procedure uses the scripts from the `hpc-scripts` repository.  

First get an interactive allocation on dev-g

```
salloc --account=$ACCOUNT --exclusive --nodes=1 --ntasks-per-node=8 --partition=dev-g --time=01:00:00 --gpus-per-node=8
```
where `$ACCOUNT` is the LUMI project account.

Then run these installation steps to install PMAP-LES for both cpu's and gpu's.


```
mkdir pmap-les
cd pmap-les
git clone git@github.com:PMAP-Project/PMAP-real_cases-shared.git main
cd ..

git clone git@github.com:stubbiali/hpc-scripts.git

ln -s hpc-scripts/src/lumi/make_build_hdf5.py
ln -s hpc-scripts/src/lumi/make_build_netcdf.py
ln -s hpc-scripts/src/lumi/make_prepare_pmap_les.py make_prepare_pmap_les.py
ln -s hpc-scripts/src/lumi/select_gpu.sh select_gpu.sh
 

chmod +x make_build_hdf5.py
chmod +x make_build_netcdf.py
chmod +x make_prepare_pmap_les.py 
chmod +x select_gpu.sh 

module --force purge
module load cray-python/3.10.10

./make_build_hdf5.py
chmod +x build_hdf5.sh
./build_hdf5.sh

./make_build_netcdf.py
chmod +x build_netcdf.sh
./build_netcdf.sh

./make_prepare_pmap_les.py --project-root-dir=pmap-les/ --branch=main
. prepare_pmap_les.sh

PMAP_NUM_THREADS_COMPILATION=56 GT_BACKEND=gt:cpu_kfirst srun --ntasks=1 --cpus-per-task=56 python scripts/build_gtcache.py
PMAP_NUM_THREADS_COMPILATION=56 GT_BACKEND=gt:gpu        srun --ntasks=1 --cpus-per-task=56 python scripts/build_gtcache.py
```


## Cases

- [Eowyn storm around the Faroe Islands, 2025-01-24](cases/faroe_eowyen_storm_20250124/README.md)
