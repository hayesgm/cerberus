#!/bin/bash

# This is going to be a simple script to our instance up to date
sleep 5 # issues accessing apt-get?

# Update our package system
sudo apt-get update -qq

# Install pip for python packges
sudo apt-get install python-pip -y

# Install latest stable version of docker
sudo apt-get install docker.io -y
sudo ln -sf /usr/bin/docker.io /usr/local/bin/docker

# Make sure we run docker with -r to not start previous containers
sudo sh -c "echo 'DOCKER_OPTS=\"-r=false\"' > /etc/default/docker"

# Add ubuntu user to docker group
sudo usermod -a -G docker ubuntu

# Run docker
sudo service docker.io start

# Let's pull some base docker images now
sudo docker pull base

# Install python packages
sudo pip install python-simple-hipchat