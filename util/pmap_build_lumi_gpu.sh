export GT_BACKEND=gt:gpu
export PMAP_PRECISION=single
export CC=mpicc
export CXX=mpicxx
export MPICC=$CC
export MPICXX=$CXX
export HDF5_DIR=$HDF5_DIR
export NETCDF4_DIR=$NETCDF_DIR
export GHEX_USE_GPU=True
export GHEX_GPU_TYPE=AMD
export GHEX_GPU_ARCH=x86_64
export CUPY_INSTALL_USE_HIP=1
export ROCM_HOME=$ROCM_PATH
export HCC_AMDGPU_TARGET=x86_64

pip install -e .[gpu-rocm]
