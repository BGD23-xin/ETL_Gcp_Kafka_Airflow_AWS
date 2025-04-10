#!/bin/bash

set -e

echo "Intalling anaconda"
# Install Anaconda
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
mv Anaconda3-2021.11-Linux-x86_64.sh anaconda.sh
bash anaconda.sh -b -p $HOME/anaconda3
echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
echo "Anaconda installed."



echo "Installing Docker"
# Install Docker

sudo apt-get update
sudo apt-get install docker.io

# Add your user to the docker group
if ! getent group docker > /dev/null; then
  sudo groupadd docker
fi
sudo gpasswd -a $USER docker
newgrp docker  # 立即应用组变更（避免重启）



echo "checking correct installation of docker"
docker run hello-word

