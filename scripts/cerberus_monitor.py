#!/usr/bin/env python
import syslog
from subprocess import call, check_output
from time import sleep
import urllib2
import json
import re
from user_data import get_user_data

# Monitors the Docker repo and sees if new versions of repo are available
# If so, we'll restart the Cerberus docker container service
# Expected user data:
# docker.repo: Docker repo to check

syslog.syslog(syslog.LOG_WARNING, 'Monitoring cerberus container...')

user_data = get_user_data()

docker = user_data['docker']
repo = docker['repo']
tag = docker.get('tag', 'latest')

# This script is going to poll to see if there's a an updated version of the repo with tag available
# If so, we'll restart the cerberus-container service

def get_running_container_version():
  syslog.syslog(syslog.LOG_WARNING, 'Checking running container version')
  containers = check_output(['docker','ps','-q','--no-trunc']).split('\n')

  # TODO: Multiple running images?
  container = containers[0]

  if not container:
    None
  else:
    container_info = json.loads(check_output(['docker','inspect',container]))[0]

    return container_info['Image'] # return current image

def get_available_container_version():
  syslog.syslog(syslog.LOG_WARNING, 'Checking available container version')

  # Pull repository data from index using basic auth if nesc
  request = urllib2.Request("https://index.docker.io/v1/repositories/%s/tags" % repo)
  if docker.get('auth'):
    request.add_header("Authorization", "Basic %s" % docker['auth'])   
  
  index_data_raw = urllib2.urlopen(request).read()
  repo_info = json.loads(index_data_raw)

  # TODO: We might want to make this more functional
  for tag_info in repo_info:
    if tag_info['name'] == tag:
      return tag_info['layer']

  return None

while True: # infinite loop
  service_info = check_output(['sudo','service','cerberus-container','status'])

  if re.search('cerberus-container start/running, process \d+',service_info): # Ensure the service is running
    running_version = get_running_container_version()
    available_version = get_available_container_version()

    syslog.syslog(syslog.LOG_WARNING, 'Running version: %s, available_version %s' % (running_version, available_version))

    if available_version != None and running_version != None and not running_version.startswith(available_version):
      # update service
      syslog.syslog(syslog.LOG_WARNING, 'New version of %s:%s (%s->%s), restarting cerberus-container' % (repo, tag, running_version, available_version))
      if call(['sudo','service', 'cerberus-container', 'restart']) != 0: # restart service
        raise Exception("Failed to restart cerberus-container service")
      syslog.syslog(syslog.LOG_WARNING, 'Service restarted')
      # Note, we may want to wait for this to have time to start-up
      # We may also want to see docker starts correctly
      # Also, we may want to use a tag and only pull whatever the tag is for the repo
      # E.g. could be latest, or any tag
  else:
    syslog.syslog(syslog.LOG_WARNING, 'Not monitoring as container not running')

  # Sleep even if we have restarted
  sleep(15) # sleep then loop
