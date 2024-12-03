#!/bin/bash

# install specific python version to make sure all the work env for various server are the same.
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt install python3.12 -y
sudo apt install python3.12-distutils -y

# install awscli
sudo apt  install awscli -y

# Create a virtual environment for specific python3.8 version
sudo apt install python3-virtualenv -y
virtualenv --python="/usr/bin/python3.12" .v_env  
source .v_env/bin/activate 

# Install dependencies
pip install -r requirements.txt

deactivate # deactivate your sandbox

chmod a+x script/run.sh # make run.sh executable

mkdir -p log # create log directory if it doesn't exist