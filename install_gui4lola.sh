#!/bin/bash

############################################
#### Ubuntu 20.04 install of Ros Noetic ####
############################################


git clone https://github.com/gramuah/gui4lola.git

sudo apt install python3-pip -y

sudo apt-get install python3-tk

pip install python-vlc pillow

python3 -m pip install --upgrade Pillow

#python3 -m pip install --upgrade python-vlc
sudo apt-get install vlc -y

# Install Anaconda on Ubuntu 20.04
sudo apt update && sudo apt upgrade

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

bash Miniconda3-latest-Linux-x86_64.sh

rm Miniconda3-latest-Linux-x86_64.sh
