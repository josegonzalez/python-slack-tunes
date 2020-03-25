from __future__ import print_function
import json
import sys
import subprocess
import urllib.parse
import requests

def osascript(player, command):
    command = 'tell application "{0}" to {1} as string'.format(
        player,
        command
    )
    command = 'osascript -e \'{0}\''.format(command)
    return subprocess.check_output(command, shell=True).decode(sys.stdout.encoding).strip()


def is_running(player):
    command = 'if application "{0}" is running then "running"'.format(
        player
    )
    command = 'osascript -e \'{0}\''.format(command)
    try:
        return subprocess.check_output(command, shell=True).decode(sys.stdout.encoding).strip() == 'running'
    except subprocess.CalledProcessError:
        return False


def update_status(is_playing, text=None, tokens=None):
    status_text = ''
    status_emoji = ''

    if is_playing:
        status_text = text
        status_emoji = ':musical_note:'

    if tokens is None:
        return

    responses = []
    for token in tokens:
        content = {
          'profile': {
            'status_text': status_text,
            'status_emoji': status_emoji,
          },
        }

        req_headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': 'Bearer ' + token,
        }

        request = requests.post('https://slack.com/api/users.profile.set', data=json.dumps(content), headers=req_headers)
        status = request.status_code != 200

        if status:
            print('error: {0}'.format(str(request.status_code)))
        else:
            body = json.loads(request.text)
            if not body.get('ok'):
                print('error: {0}'.format(request.text))

        responses.append(status)

    return responses


def spotify_song():
    if not is_running('Spotify'):
        return None

    song = ''
    try:
        song = osascript('Spotify', 'if player state is playing then artist of current track & " __SLACK_TUNES_DELIMITER__ " & name of current track')  # pep8
    except subprocess.CalledProcessError:
        song = ''

    song = song.strip()
    if song.startswith('__SLACK_TUNES_DELIMITER__'):
        song = None
    else:
        song = song.replace('__SLACK_TUNES_DELIMITER__', '-')
    return song


def itunes_song(catalina=False):
    if catalina:
        app = 'Music'
    else:
        app = 'iTunes'

    if not is_running(app):
        return None

    try:
        return osascript(app, 'if player state is playing then artist of current track & " - " & name of current track')  # pep8
    except subprocess.CalledProcessError:
        return None


def check_song(old_status=None, first_run=False, tokens=None):
    current_status = spotify_song()
    if not current_status:
        current_status = itunes_song()
    if not current_status:
        current_status = itunes_song(catalina=True)

    if not current_status:
        if old_status or first_run:
            print('Not currently playing')
            update_status(is_playing=False, tokens=tokens)
        return None

    if old_status == current_status:
        return current_status

    print('Current status: {0}'.format(current_status))
    update_status(is_playing=True, text=current_status, tokens=tokens)

    return current_status
