#!/bin/bash

# This is going to be a simple script to our instance up to date
sleep 5 # issues accessing apt-get?

# Update our package system
sudo apt-get update -qq

# Install pip for python packges
sudo apt-get install python-pip -y

# Install latest stable version of `docker`

# Add docker repository key to apt-key for package verification
sudo sh -c "wget -qO- https://get.docker.io/gpg | apt-key add -"

# Add the docker repository to aptitude sources
sudo sh -c "echo deb http://get.docker.io/ubuntu docker main\ > /etc/apt/sources.list.d/docker.list"

# Install key
sudo sh -c "apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9"

# Update the repository with the new addition
sudo apt-get update

# Finally, download and install docker
sudo apt-get install lxc-docker -y

# Make sure we run docker with -r to not start previous containers
sudo sh -c "echo 'DOCKER_OPTS=\"-r=false\"' > /etc/default/docker"

# Add ubuntu user to docker group
sudo usermod -a -G docker ubuntu

# Run docker
sudo service docker start

# Let's pull some base docker images now
sudo docker pull base
sudo docker pull phusion/baseimage

# Install python packages
sudo pip install python-simple-hipchat