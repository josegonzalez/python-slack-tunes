from __future__ import print_function
import json
import sys
import subprocess
import urllib
import urllib2


PY3 = sys.version_info[0] == 3
bad_chars = str("").join([chr(i) for i in range(128, 256)])  # ascii dammit!
if PY3:
    translation_table = dict((ord(c), None) for c in bad_chars)
    unicode = str


def asciionly(s):
    if PY3:
        return s.translate(translation_table)
    else:
        return s.translate(None, bad_chars)


def asciidammit(s):
    if type(s) is str:
        return asciionly(s)
    elif type(s) is unicode:
        return asciionly(s.encode('ascii', 'ignore'))
    else:
        return asciidammit(unicode(s))


def osascript(player, command):
    command = 'tell application "{0}" to {1} as string'.format(
        player,
        command
    )
    command = "osascript -e '{0}'".format(command)
    return subprocess.check_output(command, shell=True).strip()


def is_running(player):
    command = 'if application "{0}" is running then "running"'.format(
        player
    )
    command = "osascript -e '{0}'".format(command)
    try:
        return subprocess.check_output(command, shell=True).strip() == "running"
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
        content = urllib.urlencode({
          'token': token,
          'profile': {
            "status_text": status_text,
            "status_emoji": status_emoji,
          },
        })

        opener = urllib2.build_opener(urllib2.HTTPHandler)
        url = 'https://slack.com/api/users.profile.set'
        request = urllib2.Request(url, data=content)
        request.get_method = lambda: 'POST'
        url = opener.open(request)
        status = int(url.getcode()) != 200
        if status:
            print("error: {0}".format(url.getcode()))
        responses.append(status)

    return responses


def spotify_song():
    if not is_running('Spotify'):
        return None

    try:
        return osascript('Spotify', 'if player state is playing then artist of current track & " - " & name of current track')  # pep8
    except subprocess.CalledProcessError:
        return None


def itunes_song():
    if not is_running('iTunes'):
        return None

    try:
        return osascript('iTunes', 'if player state is playing then artist of current track & " - " & name of current track')  # pep8
    except subprocess.CalledProcessError:
        return None


def check_song(old_status=None, first_run=False, tokens=None):
    current_status = spotify_song()
    if not current_status:
        current_status = itunes_song()

    if current_status:
        current_status = asciidammit(current_status)

    if not current_status:
        if old_status or first_run:
            print('Not currently playing')
            update_status(is_playing=False, tokens=tokens)
        return None

    if old_status == current_status:
        return current_status

    print("Current status: {0}".format(current_status))
    update_status(is_playing=True, text=current_status, tokens=tokens)

    return current_status
