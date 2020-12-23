import os

from devdeck_core.controls.deck_control import DeckControl


class SlackOnlineControl(DeckControl):
    def __init__(self, key_no, api_client, **kwargs):
        self.api_client = api_client
        super().__init__(key_no, **kwargs)

    def initialize(self):
        with self.deck_context() as context:
            context.set_icon(os.path.join(os.path.dirname(__file__), "../assets", 'online.png'))

    def pressed(self):
        self.api_client.users_setPresence(presence='auto')
        self.api_client.users_profile_set(profile={"status_text": "", "status_emoji": ""})
