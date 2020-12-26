from devdeck_core.controls.deck_control import DeckControl


class SlackDndControl(DeckControl):
    def __init__(self, key_no, api_client, **kwargs):
        self.api_client = api_client
        super().__init__(key_no, **kwargs)

    def initialize(self):
        with self.deck_context() as context:
            with context.renderer() as r:
                r.emoji('zzz')\
                    .end()\
                .badge_count(str(self.settings['duration']))\
                    .end()

    def pressed(self):
        self.api_client.dnd_setSnooze(num_minutes=self.settings['duration'])

    def settings_schema(self):
        return {
            'duration': {
                'type': 'integer',
                'required': True,
            }
        }