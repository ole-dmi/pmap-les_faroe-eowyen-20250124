#!/bin/bash

ROOT_DIR=$1
PMAP_DIR=$2

CONFIG_DIR=$ROOT_DIR/config/pmap_les_config

NPOINTS="251 501"

for NP in $NPOINTS; do

	CASE=500000x500000_${NP}x${NP}
	CONFIG_FILE=$CONFIG_DIR/faroe_eowyn_20250124_$CASE.yml
	OUTPUT_DIR=$ROOT_DIR/output/$CASE
	LOG_FILE=$OUTPUT_DIR/pmap-les.log
 
       	echo "[$0] Starting pmap ..." 
	echo "[$0] pmap directory:          $PMAP_DIR"
	echo "[$0] pmap configuration file: $CONFIG_FILE"
	echo "[$0] output directory:        $OUTPUT_DIR"
	echo "[$0] log file:                $LOG_FILE"

	sbatch -e $LOG_FILE -o $LOG_FILE pmap_driver.sh $OUTPUT_DIR $CONFIG_FILE $PMAP_DIR
done
