# DevDeck - Slack
![CI](https://github.com/jamesridgway/devdeck-slack/workflows/CI/badge.svg?branch=main)

Slack deck and controls for  [DevDeck](https://github.com/jamesridgway/devdeck).

In this example, you can manage your presence, status and do-not-disturb settings from your StreamDeck:

![Stream Deck - Slack Integration using DevDeck](https://www.jamesridgway.co.uk/content/images/2020/12/streamdeck-slack.jpg)


## Installing
Simplify install *DevDeck - Slack* into the same python environment that you have installed DevDeck.

    pip install devdeck-slack

You can then update your DevDeck configuration to use decks and controls from this package.

## Configuration

Example configuration:

    decks:
      - serial_number: "ABC123"
        name: 'devdeck.decks.single_page_deck_controller.SinglePageDeckController'
        settings:
          controls:
            - name: 'devdeck_slack.slack_deck.SlackDeck'
              key: 0
              settings:
                api_key: 'YOUR_API_KEY_GOES_HERE'
                actions:
                  - action: online
                    key: 0
                  - action: away
                    key: 1
                  - action: status
                    key: 2
                    text: At my desk
                    emoji: ':desktop_computer:'
                    clear_dnd: true
                  - action: status
                    key: 5
                    text: In a meeting
                    emoji: ':calendar:'
                  - action: status
                    key: 6
                    text: Lunch
                    emoji: ':sandwich:'
                  - action: status
                    key: 7
                    text: Off sick
                    emoji: ':face_with_thermometer:'
                    until: tomorrow at 8am
                  - action: status
                    key: 8
                    text: On holiday
                    emoji: ':palm_tree:'
                  - action: dnd
                    key: 10
                    duration: 15
                  - action: dnd
                    key: 11
                    duration: 30
                  - action: dnd
                    key: 12
                    duration: 45
                  - action: dnd
                    key: 13
                    duration: 60
                  - action: dnd
                    key: 14
                    duration: 120


## Registering your app and creating permissions
This plugin requires a Slack API key to function.

Head over to https://api.slack.com/apps to create your app.

Once you have created your app you will be able to access your OAuth Access Token under **OAuth & Permissions** - this
is your `api_key` value.

### Scopes
Under **User Token Scopes** you need want to enable the following scopes:

* `dnd:read`
* `dnd:write`
* `users.profile:write`
* `users:write`
