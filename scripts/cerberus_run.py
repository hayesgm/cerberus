#!/usr/bin/env python
import syslog
from subprocess import call
import urllib2
import json
import re
import docker_login
from user_data import get_user_data

# Starts a docker run for a given repo
# This will effectively call `docker run <flags> <repo>`
# This service is monitored by Upstart
# User Data
# docker.repo: Repo to run
# docker.flags: Flags to send to `docker run` (e.g. -p 8888:8888)

syslog.syslog(syslog.LOG_WARNING, 'Running docker container...')

user_data = get_user_data()

docker = user_data['docker']
repo = docker['repo']
flags = docker.get('flags', [])

# Allow flags to be a string or an array
if isinstance(flags,basestring):
  flags = [flags]

flags = map(lambda flag: re.sub('-(\w)\s', r'-\1=', flag), flags) # Change `-x ...` to `-x=...`

# Call Python Login Script
syslog.syslog(syslog.LOG_WARNING, 'Logging in to docker')
docker_login.login()

syslog.syslog(syslog.LOG_WARNING, 'Pulling %s docker image' % repo)
if call(['docker','pull',repo]) != 0:
  raise Exception("Failed to pull docker repo %s" % repo)

syslog.syslog(syslog.LOG_WARNING, 'Booting %s with %s...' % (repo, flags))
if call(['docker','run','--cidfile=/var/run/docker/container.cid'] + flags + [repo]) != 0:
  raise Exception("Failed to run docker repo %s" % repo)
