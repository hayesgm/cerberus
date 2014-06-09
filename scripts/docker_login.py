#!/usr/bin/env python
from __future__ import print_function
from os.path import expanduser
import syslog
import urllib2
import json
from user_data import get_user_data

# Logs in to docker index if auth is given (builds ~/.dockercfg)
# docker.email: Email address to login in as
# docker.auth: Base64-encoded login (username/password)

def login():
  syslog.syslog(syslog.LOG_WARNING, 'Logging in to docker..')

  user_data = get_user_data()

  docker = user_data['docker']
  auth = docker.get('auth')
  email = docker.get('email')

  if auth and email:
    home = expanduser('~')
    docker_cfg_file = open(home + '/.dockercfg','w+')

    # TODO: Right now this truncates any other login info-- consider refactoring
    auth_hash = {
      'https://index.docker.io/v1/': { 'auth': auth, 'email': email }
    }

    print(json.dumps(auth_hash), file=docker_cfg_file)

    syslog.syslog(syslog.LOG_WARNING, 'Successfully logged into docker as %s' % email)

