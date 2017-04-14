python-slack-tunes
--------------------

send slack music notifications from itunes or spotify

Requirements
============

- OS X
- iTunes or Spotify

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

    export SLACK_API_TOKEN="YOUR_TOKEN"
    slack-tunes

Slack tunes will run in the foreground, and can be terminated at any time. It will update the status at most every 10 seconds, and will clear your status if no music is playing.


You can also specify multiple tokens via comma-delimiter. This is useful for notifying multiple slack teams.

.. code-block:: shell

    export SLACK_API_TOKEN="YOUR_TOKEN,YOUR_OTHER_TOKEN"
    slack-tunes

.. image:: https://cdn.rawgit.com/josegonzalez/python-slack-tunes/2383034e/demo.png
    :width: 1010px
    :align: center
    :height: 382px
    :alt: demo of slack-tunes output
