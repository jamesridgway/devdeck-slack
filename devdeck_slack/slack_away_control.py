import os

from devdeck_core.controls.deck_control import DeckControl


class SlackAwayControl(DeckControl):
    def __init__(self, key_no, api_client, **kwargs):
        self.api_client = api_client
        super().__init__(key_no, **kwargs)

    def initialize(self):
        with self.deck_context() as context:
            with context.renderer() as r:
                r.image(os.path.join(os.path.dirname(__file__), "assets", 'away.png')).end()

    def pressed(self):
        self.api_client.users_setPresence(presence='away')