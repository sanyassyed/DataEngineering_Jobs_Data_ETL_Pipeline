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
# from config.toml file
export OUTPUT_FOLDER_NAME=$(grep 'output_folder' config.toml | sed 's/.*=//' | tr -d '"')
export LOG_FOLDER_NAME=$(grep 'log_folder' config.toml | sed 's/.*=//' | tr -d '"')
export PYTHON_FILE_NAME=$(grep 'py_script' config.toml | sed 's/.*=//' | tr -d '"')
export SCRIPT_FILE_NAME=$(grep 'sh_script' config.toml | sed 's/.*=//' | tr -d '"')
export VIRTUAL_ENV_PATH=$(grep 'virtual_env_path' config.toml | sed 's/.*=//' | tr -d '"')
# project folder
export PROJECT_FOLDER="${script_path}"
# output folder
export OUTPUT_FOLDER="${PROJECT_FOLDER}/${OUTPUT_FOLDER_NAME}"
# script folder & file
export SCRIPT_FOLDER="${PROJECT_FOLDER}/${SCRIPT_FOLDER_NAME}"
export PYTHON_FILE="${SCRIPT_FOLDER}/${PYTHON_FILE_NAME}"
export SCRIPT_FILE="${SCRIPT_FOLDER}/${SCRIPT_FILE_NAME}"
# log folder & file
export LOG_FOLDER="${PROJECT_FOLDER}/${LOG_FOLDER_NAME}"
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
source ${VIRTUAL_ENV_PATH}

##############################################################
# Metadata:
echo "[INFO:] Metadata:"
echo "[INFO:] Output data folder: ${OUTPUT_FOLDER}"
echo "[INFO:] Script file: ${SCRIPT_FILE}"
echo "[INFO:] Python file: ${PYTHON_FILE}"
echo "[INFO:] Log file for ${SCRIPT_FILE_NAME} at: ${LOG_FILE}"
echo "[INFO:] Log file for ${PYTHON_FILE_NAME} at: ${LOG_FILE_PYTHON}"
