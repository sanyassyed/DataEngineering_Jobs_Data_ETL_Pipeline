#!/bin/bash

##############################################################
# Step 1: Setting up environment variables in init.sh file
echo "[INFO:] SETTING ENVIRONMENT VARIABLES IN init.sh"
source script/init.sh  # Source instead of running as a separate process

##############################################################
# Step 2: Running Python Script
echo "[DEBUG:] PYTHON_FILE is set to: ${PYTHON_FILE}"
echo "[INFO:] RUNNING PYTHON SCRIPT ${PYTHON_FILE}"
python3 "${PYTHON_FILE}"

# Check if the Python script ran successfully
if [ $? -eq 0 ]; then
    echo "[INFO:] Python script executed successfully."
else
    echo "[ERROR:] Failed to execute Python script."
    exit 1
fi