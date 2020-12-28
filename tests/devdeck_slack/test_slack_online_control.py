from unittest import mock

from devdeck_core.mock_deck_context import mock_context, assert_rendered

from devdeck_slack.slack_online_control import SlackOnlineControl
from tests.testing_utils import TestingUtils


class TestSlackOnlineControl:
    @mock.patch('slack_sdk.WebClient')
    def test_initialize_sets_icon(self, api_client):
        control = SlackOnlineControl(0, api_client, **{})
        with mock_context(control) as ctx:
            control.initialize()
            assert_rendered(ctx, TestingUtils.get_filename('../devdeck_slack/assets/online.png'))

    @mock.patch('slack_sdk.WebClient')
    def test_pressed_sets_presence_online(self, api_client):
        control = SlackOnlineControl(0, api_client, **{})
        with mock_context(control) as ctx:
            api_client.dnd_info.return_value = {'snooze_enabled': False}
            control.pressed()
            api_client.users_setPresence.assert_called_with(presence='auto')
            api_client.users_profile_set.assert_called_with(profile={"status_text": "", "status_emoji": ""})
            api_client.dnd_info.assert_called()
            api_client.dnd_endSnooze.assert_not_called()

    @mock.patch('slack_sdk.WebClient')
    def test_pressed_sets_presence_online_and_cancels_dnd(self, api_client):
        control = SlackOnlineControl(0, api_client, **{})
        with mock_context(control) as ctx:
            api_client.dnd_info.return_value = {'snooze_enabled': True}
            control.pressed()
            api_client.users_setPresence.assert_called_with(presence='auto')
            api_client.users_profile_set.assert_called_with(profile={"status_text": "", "status_emoji": ""})
            api_client.dnd_info.assert_called()
            api_client.dnd_endSnooze.assert_called()
