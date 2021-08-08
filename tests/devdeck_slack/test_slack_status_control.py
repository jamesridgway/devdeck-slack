import math
from unittest import mock
import time

import parsedatetime
import tzlocal

from devdeck_core.mock_deck_context import mock_context, assert_rendered
from devdeck_core.renderer import Renderer

from devdeck_slack.slack_status_control import SlackStatusControl


class TestSlackStatusControl:
    @mock.patch('slack_sdk.WebClient')
    def test_initialize_sets_icon(self, api_client):
        control = SlackStatusControl(0, api_client, **{'emoji': ':sandwich:', 'text': 'On lunch'})
        with mock_context(control) as ctx:
            control.initialize()
            assert_rendered(ctx, Renderer().emoji('sandwich').end())

    @mock.patch('slack_sdk.WebClient')
    def test_pressed_sets_status(self, api_client):
        control = SlackStatusControl(0, api_client, **{'emoji': ':sandwich:', 'text': 'On lunch'})
        with mock_context(control) as ctx:
            control.pressed()
            api_client.users_profile_set.assert_called_with(profile={
                'status_text': 'On lunch',
                'status_emoji': ':sandwich:',
                'status_expiration': 0
            })
            api_client.dnd_setSnooze.assert_not_called()

    @mock.patch('slack_sdk.WebClient')
    def test_pressed_sets_status_alt_emoji(self, api_client):
        control = SlackStatusControl(0, api_client, **{
            'emoji': ':sandwich:', 'text': 'On lunch', 'emoji_slack': ':test:'
        })
        with mock_context(control) as ctx:
            control.pressed()
            api_client.users_profile_set.assert_called_with(profile={
                'status_text': 'On lunch',
                'status_emoji': ':test:',
                'status_expiration': 0
            })
            api_client.dnd_setSnooze.assert_not_called()

    @mock.patch('slack_sdk.WebClient')
    def test_dnd_set_without_timeout(self, api_client):
        control = SlackStatusControl(0, api_client, **{
            'emoji': ':calendar:', 'text': 'Busy', 'dnd': True
        })
        with mock_context(control) as ctx:
            control.pressed()
            api_client.users_profile_set.assert_called_with(profile={
                'status_text': 'Busy',
                'status_emoji': ':calendar:',
                'status_expiration': 0
            })
            api_client.dnd_setSnooze.assert_called_with()

    @mock.patch('slack_sdk.WebClient')
    def test_dnd_set_with_duration(self, api_client):
        control = SlackStatusControl(0, api_client, **{
            'emoji': ':calendar:', 'text': 'Busy', 'dnd': True, 'duration': 5
        })
        with mock_context(control) as ctx:
            control.pressed()
            api_client.users_profile_set.assert_called_with(profile={
                'status_text': 'Busy',
                'status_emoji': ':calendar:',
                'status_expiration': int(time.time()) + 300
            })
            api_client.dnd_setSnooze.assert_called_with(num_minutes=5)

    @mock.patch('slack_sdk.WebClient')
    def test_dnd_set_with_until(self, api_client):
        control = SlackStatusControl(0, api_client, **{
            'emoji': ':calendar:', 'text': 'Busy', 'dnd': True,
            'until': 'tomorrow at 7am'
        })
        c = parsedatetime.Calendar(version=parsedatetime.VERSION_CONTEXT_STYLE)
        ts, _ = c.parseDT('tomorrow at 7am', tzinfo=tzlocal.get_localzone())
        minutes = int(math.ceil((ts.timestamp() - time.time()) / 60))
        with mock_context(control) as ctx:
            control.pressed()
            api_client.users_profile_set.assert_called_with(profile={
                'status_text': 'Busy',
                'status_emoji': ':calendar:',
                'status_expiration': int(ts.timestamp())
            })
            api_client.dnd_setSnooze.assert_called_with(num_minutes=minutes)

    @mock.patch('slack_sdk.WebClient')
    def test_dnd_cleared(self, api_client):
        control = SlackStatusControl(0, api_client, **{
            'text': '', 'emoji': ':desktop_computer:', 'clear_dnd': True
        })
        with mock_context(control) as ctx:
            control.pressed()
            api_client.dnd_endDnd.assert_called()
