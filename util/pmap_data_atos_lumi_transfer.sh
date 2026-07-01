#!/bin/bash
#SBATCH --time=48:00:00

SSH_KEY_LUMI_ATOS="/home/nhad/.ssh/lumi_transfer"  #with your LUMI ssh key on ATOS
SOURCE_DATA_LUMI="/projappl/project_465000527/benacchi/jobs/pmap-real_cases-shared/lumi/real_cases/faroer_500m_nx1501_ny1501_DE2401202500_init06UTC/single/mpi/dacegpu/data_*.nc" # PMAP output data on ATOS
#
DEST_FLD_ATOS="/ec/res4/hpcperm/nhad/PMAP_LAM_evolution_task_output/500m_faroe_20250124/PMAP_real_cases_single/" # destination folder on ATOS 
LUMI_USR="benacchi"


scp -i $SSH_KEY_LUMI_ATOS -r "$LUMI_USR@lumi.csc.fi:$SOURCE_DATA_LUMI" $DEST_FLD_ATOS
