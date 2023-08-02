#!/bin/bash

# ******************************************
# Initial setup and dependency installation
# ******************************************

# Check for root privileges
if [ "$EUID" -ne 0 ]
  then echo "PLEASE RUN THIS SCRIPT WITH ROOT PRIVILEGES"
  exit
fi

cd ..
mkdir -p data keys

# Install and setup python environment
REQUIRED_PYTHON="python3.11"
echo Checking for $REQUIRED_PYTHON
if [ $(dpkg-query -W -f='${Status}' $REQUIRED_PYTHON 2>/dev/null | grep -c "install ok installed") -eq 0 ];
then
    echo Installing $REQUIRED_PYTHON
    add-apt-repository -y ppa:deadsnakes/ppa
    apt -y update
    apt -y install python3.11
fi

# Check if the virtual environment already exists
VENV_FILE=venv/bin/activate
if ! test -f "$VENV_FILE"; then
    echo Initalizing python virtual environment
    python3.11 -m venv --without-pip venv
    source $VENV_FILE
    apt-get -y install python3.11-distutils
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
    rm get-pip.py
    deactivate
fi

# Install python dependencies
source $VENV_FILE
pip install -r requirements.txt
echo "$(pwd)/shared" > venv/lib/python3.11/site-packages/shared.pth

# Install Node Version Manager
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
source ~/.bashrc

# Install latest version of node and install dependencies
nvm install node
cd frontend
npm install