#!/bin/bash

##############################################################
# load variables from config.toml
export SCRIPT_FOLDER_NAME=$(grep 'script_folder' config.toml | sed 's/.*=//' | tr -d '"')
export INIT_SCRIPT=$(grep 'init_script' config.toml | sed 's/.*=//' | tr -d '"')
# Step 1: Setting up environment variables in init.sh file
echo "[INFO:] Setting project environment via ${INIT_SCRIPT}"
source ${SCRIPT_FOLDER_NAME}/${INIT_SCRIPT}  # Source instead of running as a separate process
##############################################################
# Step 2: Running Python Script
echo "[INFO:] Running Python script at: ${PYTHON_FILE}"
# PRODUCTION MODE
python3 "${PYTHON_FILE}"

# TESTING MODE: where data in written locally in folder named output
#python3 "${PYTHON_FILE}" --test_run

RC1=$?
if [ ${RC1} != 0 ]; then
	echo "[DEBUG:] PYTHON RUNNING FAILED"
	echo "[ERROR:] RETURN CODE:  ${RC1}"
	echo "[ERROR:] REFER TO THE LOG FOR THE REASON FOR THE FAILURE."
	exit 1
fi

echo "PYTHON PROGRAM RUN SUCCEEDED"

deactivate

exit 0 