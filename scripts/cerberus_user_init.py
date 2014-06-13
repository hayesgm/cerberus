#!/usr/bin/env python
import syslog
from user_data import get_user_data
import tempfile
from subprocess import call
import os
import stat

# Pull the init script out of user data if it exists
user_data = get_user_data()

if not user_data.get('init'):
  syslog.syslog(syslog.LOG_WARNING, 'Skipping init script (non-given)...')
  exit(0)

init_script = user_data['init'].lstrip()

if not init_script.startswith('#!'):
  syslog.syslog(syslog.LOG_WARNING, 'Skipping init script (does not start with shebang #!)...')
  exit(0)

script_file = tempfile.NamedTemporaryFile(delete=False)

try:
    script_file.write(init_script)
    script_file.close()
    os.chmod(script_file.name, stat.S_IXUSR | stat.S_IRUSR)

    # We have the file, now let's run it
    syslog.syslog(syslog.LOG_WARNING, 'Running init script (%s)...' % script_file.name)
      
    # Note, this runs as root
    if call([script_file.name]) != 0:
      syslog.syslog(syslog.LOG_WARNING, "Failed to successfully run init script")
    else:
      syslog.syslog(syslog.LOG_WARNING, 'Init script run successfully')
finally:
    os.remove(script_file.name)
