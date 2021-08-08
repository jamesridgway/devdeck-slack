import logging
import math
import time

import parsedatetime
import tzlocal

from devdeck_core.controls.deck_control import DeckControl


class SlackStatusControl(DeckControl):
    def __init__(self, key_no, api_client, **kwargs):
        self.api_client = api_client
        self.__logger = logging.getLogger('devdeck')
        self.cal = parsedatetime.Calendar(
            version=parsedatetime.VERSION_CONTEXT_STYLE)
        super().__init__(key_no, **kwargs)

    def initialize(self):
        with self.deck_context() as context:
            with context.renderer() as r:
                r.emoji(self.settings['emoji'])\
                    .end()

    def pressed(self):
        expires = 0  # 0 = never
        if 'duration' in self.settings:
            expires = int(time.time()) + self.settings['duration'] * 60
        elif 'until' in self.settings:
            dt, _ = self.cal.parseDT(self.settings['until'],
                                     tzinfo=tzlocal.get_localzone())
            if dt is None:
                self.__logger.error("Could not parse until: %s",
                                    self.settings['until'])
            else:
                expires = int(dt.timestamp())
        dnd = self.settings.get('dnd', False)
        clear_dnd = self.settings.get('clear_dnd', False)
        self.api_client.users_profile_set(profile={
            "status_text": self.settings['text'],
            "status_emoji": self.settings.get('emoji_slack',
                                              self.settings['emoji']),
            "status_expiration": expires
        })
        if dnd:
            if expires > 0:
                minutes = int(math.ceil((expires - time.time()) / 60))
                self.api_client.dnd_setSnooze(num_minutes=minutes)
            else:
                self.api_client.dnd_setSnooze()
        elif clear_dnd:
            self.api_client.dnd_endDnd()

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
