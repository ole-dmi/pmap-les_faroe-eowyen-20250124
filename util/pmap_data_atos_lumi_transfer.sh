#!/bin/bash
#SBATCH --time=12:00:00

# Blueprint for transferring Eowyn PMAP data from ATOS to LUMI 

# SSH key for lumi login on ATOS
#ATOS_TO_LUMI_SSH_KEY=/home/nhad/.ssh/lumi_transfer

# Folder with PMAP data on ATOS
#PMAP_DATA_ATOS_FLD=/ec/project/pmap/de_330/faroer_500m_nx1501_ny1501_2401202500_init06UTC

#LUMI_USR=benacchi
#LUMI_TARGET_FLD=/projappl/project_465000527/benacchi/

scp  -i $ATOS_TO_LUMI_SSH_KEY -r $PMAP_DATA_ATOS_FLD  $LUMI_USR@lumi.csc.fi:$LUMI_TARGET_FLD
