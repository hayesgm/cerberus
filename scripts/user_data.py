#!/usr/bin/env python
import urllib2
import json
import os

# This should pull user data from different areas based on who we are
def get_user_data():
  if os.environ.get('USER_DATA'):
    return json.loads(os.environ['USER_DATA'])
  else:
    user_data_plain = urllib2.urlopen('http://169.254.169.254/latest/user-data/').read()
    return json.loads(user_data_plain)