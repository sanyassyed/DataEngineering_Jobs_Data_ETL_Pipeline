#!/bin/bash


##############################################################
# Project Path
# local variable with project directory path extracted from the script path by getting the grandparent directory 
script_path="$(cd "$(dirname "$(dirname "${BASH_SOURCE:-$0}")")" && pwd)"
echo "[INFO:] PROJECT DIRECTORY: ${script_path}"

##############################################################
# Setting local date variable

# date time
log_date=$(date +"%d-%m-%Y-%H-%M-%S")  

##############################################################
# Environment Variables
# project folder
export PROJECT_FOLDER="${script_path}"
# output folder
export OUTPUT_FOLDER="${PROJECT_FOLDER}/output"
# script folder & file
export SCRIPT_FOLDER="${PROJECT_FOLDER}/script"
export PYTHON_FILE_NAME="run.py"
export PYTHON_FILE="${SCRIPT_FOLDER}/${PYTHON_FILE_NAME}"
export SCRIPT_FILE_NAME="run.sh"
export SCRIPT_FILE="${SCRIPT_FOLDER}/${SCRIPT_FILE_NAME}"
# log folder & file
export LOG_FOLDER="${PROJECT_FOLDER}/logs"
export LOG_FILE_NAME="${SCRIPT_FILE_NAME}_${log_date}.log"
export LOG_FILE_NAME_PYTHON="${PYTHON_FILE_NAME}_${log_date}.log"
export LOG_FILE_PYTHON="${LOG_FOLDER}/${LOG_FILE_NAME_PYTHON}"
export LOG_FILE="${LOG_FOLDER}/${LOG_FILE_NAME}"


##############################################################
# Setting Log Rules
exec > >(tee ${LOG_FILE}) 2>&1

##############################################################
# activating virtual env
echo "[INFO:] Activating virtual env"
source ./.v_env/bin/activate

##############################################################
# Metadata:
echo "[INFO:] OUTPUT DATA FOLDER: ${OUTPUT_FOLDER}"
echo "[INFO:] SCRIPT FILE: ${SCRIPT_FILE}"
echo "[INFO:] LOG FILE FOR ${SCRIPT_FILE_NAME} IS AT: ${LOG_FILE}"

echo "[INFO:] PYTHON FILE: ${PYTHON_FILE}"
echo "[INFO:] LOG FILE FOR ${PYTHON_FILE_NAME} IS AT: ${LOG_FILE_PYTHON}"
