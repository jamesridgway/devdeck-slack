# DevDeck - Slack
![CI](https://github.com/jamesridgway/devdeck-slack/workflows/CI/badge.svg?branch=main)

Slack deck and controls for  [DevDeck](https://github.com/jamesridgway/devdeck).

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
                    key: 5
                    text: In a meeting
                    emoji: ':calendar:'
                  - action: status
                    key: 6
                    text: Lunch
                    emoji: ':sandwich:'

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
