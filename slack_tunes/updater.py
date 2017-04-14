import json
import subprocess
import urllib
import urllib2



def osascript(player, command):
    command = 'tell application "{0}" to {1} as string'.format(
        player,
        command
    )
    command = "osascript -e '{0}'".format(command)
    return subprocess.check_output(command, shell=True).strip()


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
            print "error: {0}".format(url.getcode())
        responses.append(status)

    return responses


def spotify_song():
    return osascript('Spotify', 'if player state is playing then name of current track & " - " & artist of current track')  # pep8


def itunes_song():
    return osascript('iTunes', 'if player state is playing then name of current track & " - " & artist of current track')  # pep8


def check_song(old_status=None, first_run=False, tokens=None):
    current_status = spotify_song()
    if not current_status:
        current_status = itunes_song()

    if not current_status:
        if old_status or first_run:
            print 'Not currently playing'
            update_status(is_playing=False, tokens=tokens)
        return None

    if old_status == current_status:
        return current_status

    print "Current status: {0}".format(current_status)
    update_status(is_playing=True, text=current_status, tokens=tokens)

    return current_status
