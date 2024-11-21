# Project Creation

# Project Server & Repo
* EC2 instance on AWS named `MiniProject`
* Git Project [Repo](https://github.com/sanyassyed/DataEngineering_Jobs_Data_ETL_Pipeline)


## Project Layout
* Create the project layout as follows:
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

## Creating Project Repo
* Connect to git repo
```bash
git init
# generate a ssh key pair 
ssh-keygen -t rsa
# keys created here: /home/ubuntu/.ssh/id_rsa
# Add the public key to git
# Goto GitHub and create a repo of the name DataEngineering_Jobs_Data_ETL_Pipeline
git remote add origin git@github.com:sanyassyed/DataEngineering_Jobs_Data_ETL_Pipeline.git
git branch -M main
git add .
git commit -m "ADD:Initial commit"
git push -u origin main
```
## Creating Virtual Env
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

## Creating Project Script
* Create the run.py file
* Use the sarah_de `Access Key` and `Secret Key` from AWS:
    * 
