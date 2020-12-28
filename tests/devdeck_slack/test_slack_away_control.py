from unittest import mock

from devdeck_core.mock_deck_context import mock_context, assert_rendered

from tests.testing_utils import TestingUtils

from devdeck_slack.slack_away_control import SlackAwayControl


class TestSlackAwayControl:
    @mock.patch('slack_sdk.WebClient')
    def test_initialize_sets_icon(self, api_client):
        control = SlackAwayControl(0, api_client, **{})
        with mock_context(control) as ctx:
            control.initialize()
            assert_rendered(ctx, TestingUtils.get_filename('../devdeck_slack/assets/away.png'))

    @mock.patch('slack_sdk.WebClient')
    def test_pressed_sets_presence_away(self, api_client):
        control = SlackAwayControl(0, api_client, **{})
        with mock_context(control) as ctx:
            control.pressed()
            api_client.users_setPresence.assert_called_with(presence='away')
