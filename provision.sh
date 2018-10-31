#!/bin/bash

# Install common dependencies

apt-get update
apt-get install -y apt-transport-https \
                   ca-certificates \
                   curl \
                   gnupg2 \
                   software-properties-common

# Install Python 3.7



# Install Docker CE
# Instructions located at https://docs.docker.com/install/linux/docker-ce/debian/#install-using-the-repository
echo "Installing Docker CE..."

curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

apt-get update
apt-get install -y docker-ce
