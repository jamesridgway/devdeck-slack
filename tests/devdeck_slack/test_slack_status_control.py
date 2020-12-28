from unittest import mock

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
                'status_emoji': ':sandwich:'
            })
