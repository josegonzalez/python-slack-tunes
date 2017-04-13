python-slack-tunes
--------------------

send slack music notifications from spotify

Requirements
============

- OS X
- Spotify

Installation
============

Using PIP via PyPI::

    pip install slack-tunes

Using PIP via Github::

    pip install git+https://github.com/josegonzalez/python-slack-tunes.git#egg=slack-tunes

Usage
=====

Export a ``SLACK_API_TOKEN``, as shown on their `tokens page <https://get.slack.help/hc/en-us/articles/215770388-Create-and-regenerate-API-tokens>`_, and then execute the binary:

.. code-block:: shell

    export SLACK_API_TOKEN=YOUR_TOKEN
    slack-tunes

Slack tunes will run in the foreground, and can be terminated at any time. It will update the status at most every 10 seconds, and will clear your status if no music is playing.

.. image:: demo.png
    :width: 1010px
    :align: center
    :height: 382px
    :alt: demo of slack-tunes output