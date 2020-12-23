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
