# discord-voicemessage-moderation
Moderation for Discord's newest Voice-Message feature.

## Features
* Badword detection
* Earrape detection
* Speech-to-text command (/speech-to-text <channel> <message-id/message-link/audio-link>)

![grafik](https://user-images.githubusercontent.com/67586349/232165774-8ef8b84c-d56e-4095-a390-c58691c2ef63.png)
![grafik](https://user-images.githubusercontent.com/67586349/232165671-0bc28036-574b-4fbf-9884-cec30d3f324d.png)

## Setup
### Config.json

You should set a language in the "language" field (format: en, de, pl) to get better results

To get started you need to get your bot token on the discord developer site, and just add badwords to the list.
If you want to use non-latin letters, then you must add them yourself in main.py to `valid_chars`

