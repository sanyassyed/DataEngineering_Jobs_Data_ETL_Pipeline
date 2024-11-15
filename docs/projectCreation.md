# Project Creations
* Create the project template as follows:
```bash
DataEngineering_Jobs_Data_ETL_Pipeline/
├── docs/
├── config.toml
├── .env
├── .v_env
├── requirements.txt
├── init.sh
├── run.sh
├── run.py
├── .gitignore
```
* Create a python virtual environment
```bash
# update and upgrade apt
sudo apt update
sudo apt upgrade -y
# install virtual environment package
sudo apt install python3.12-venv
# create a python virtual env
python3 -m venv ./.v_env
# activate the virtual env
source .v_env/bin/activate
# to deactivate use
deactivate
```
* Create the run.py file
* 