from unittest import mock

from devdeck_core.mock_deck_context import mock_context, assert_rendered
from devdeck_core.renderer import Renderer

from devdeck_slack.slack_dnd_control import SlackDndControl


class TestSlackDndControl:
    @mock.patch('slack_sdk.WebClient')
    def test_initialize_sets_icon(self, api_client):
        control = SlackDndControl(0, api_client, **{'duration': 15})
        with mock_context(control) as ctx:
            control.initialize()
            assert_rendered(ctx, Renderer().emoji('zzz').end().badge_count(15).end())

    @mock.patch('slack_sdk.WebClient')
    def test_pressed_sets_snooze(self, api_client):
        control = SlackDndControl(0, api_client, **{'duration': 15})
        with mock_context(control) as ctx:
            control.pressed()
            api_client.dnd_setSnooze.assert_called_with(num_minutes=15)
