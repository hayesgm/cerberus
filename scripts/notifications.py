#!/usr/bin/env python
import sys
import hipchat
from user_data import get_user_data
import requests

# This script performs notifications as specified by the user-data
# E.g. an HTTP post or XMPP notification

def notify_rest(msg, endpoint):
  print("Notifying REST at %s..." % endpoint)

  requests.post(url=endpoint, data=msg)

def notify_hipchat(msg, token, room):
  print("Notifying Hipchat room %s..." % room)

  hipster = hipchat.HipChat(token=token)
  hipster.message_room(room, 'Docker Notifications', msg)

def notify(msg):
  if not msg:
    raise Exception("Missing message for notify")

  user_data = get_user_data()

  # Just skip if we don't have notifications in user-data
  if not user_data.get('notifications'):
    return False

  notifications = user_data['notifications']

  if notifications.get('rest'):
    notify_rest(msg, notifications['rest'])

  if notifications.get('hipchat'):
    hipchat = notifications['hipchat']
    notify_hipchat(msg, hipchat.get('token'), hipchat.get('room'))

# Allow to be called from command-line
if __name__ == "__main__":
  notify(sys.argv[1])
  