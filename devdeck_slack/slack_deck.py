import os

from devdeck_core.decks.deck_controller import DeckController
from slack_sdk import WebClient

from devdeck_slack.slack_away_control import SlackAwayControl
from devdeck_slack.slack_dnd_control import SlackDndControl
from devdeck_slack.slack_online_control import SlackOnlineControl
from devdeck_slack.slack_status_control import SlackStatusControl


class SlackDeck(DeckController):
    def __init__(self, key_no, **kwargs):
        self.actions = {
            'online': SlackOnlineControl,
            'away': SlackAwayControl,
            'status': SlackStatusControl,
            'dnd': SlackDndControl
        }
        super().__init__(key_no, **kwargs)

    def initialize(self):
        with self.deck_context() as context:
            with context.renderer() as r:
                r.image(os.path.join(os.path.join(os.path.dirname(__file__), "assets", 'slack.png'))).end()

    def deck_controls(self):
        api_client = WebClient(token=self.settings['api_key'])

        for action_setting in self.settings['actions']:
            action_control_class = self.actions[action_setting['action']]

            control_settings = dict(action_setting)
            del control_settings['action']
            del control_settings['key']
            self.register_control(action_setting['key'], action_control_class, api_client=api_client, **control_settings)

    def settings_schema(self):
        return {
            'api_key': {
                'type': 'string',
                'required': True,
            },
            'actions': {
                'type': 'list',
                'required': True,
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'action': {
                            'type': 'string',
                            'required': True
                        },
                        'key': {
                            'type': 'integer',
                            'required': True
                        },
                        'text': {
                            'type': 'string',
                            'required': False
                        },
                        'emoji': {
                            'type': 'string',
                            'required': False
                        },
                        'emoji_slack': {
                            'type': 'string',
                            'required': False
                        },
                        'dnd': {
                            'type': 'boolean',
                            'required': False,
                            'excludes': 'clear_dnd'
                        },
                        'clear_dnd': {
                            'type': 'boolean',
                            'required': False,
                            'excludes': 'dnd'
                        },
                        'duration': {
                            'type': 'integer',
                            'min': 1,
                            'required': False,
                            'excludes': 'until',
                        },
                        'until': {
                            'type': 'string',
                            'required': False,
                            'excludes': 'duration'
                        }
                    }
                }
            },
        }
