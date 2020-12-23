from devdeck_core.controls.deck_control import DeckControl


class SlackStatusControl(DeckControl):
    def __init__(self, key_no, api_client, **kwargs):
        self.api_client = api_client
        super().__init__(key_no, **kwargs)

    def initialize(self):
        with self.deck_context() as context:
            with context.renderer() as r:
                r.emoji(self.settings['emoji'])\
                    .end()

    def pressed(self):
        self.api_client.users_profile_set(profile={
            "status_text": self.settings['text'],
            "status_emoji": self.settings['emoji']
        })

    def settings_schema(self):
        return {
            'text': {
                'type': 'string',
                'required': True,
            },
            'emoji': {
                'type': 'string',
                'required': True,
            },
        }