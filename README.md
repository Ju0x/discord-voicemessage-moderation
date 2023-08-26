# discord-voicemessage-moderation
Moderation for Discord's newest Voice-Message feature.

![BANNER](https://user-images.githubusercontent.com/67586349/232247416-521cca52-ca19-41ac-b576-bd964f030ed1.png)


## Features
* Badword detection
* Earrape detection
* Speech-to-text command (/speech-to-text <channel> <message-id/message-link/audio-link>)

## Setup

At first discord.py, pydub and whisper must be installed.

https://github.com/Rapptz/discord.py
```
pip install discord
```

https://github.com/jiaaro/pydub
```
pip install pydub
```

https://github.com/openai/whisper/
```
pip install openai-whisper
```

### Config.json

You should set a language in the "language" field (format: en, de, pl) to get better results

To get started you need to get your bot token on the discord developer site, and just add badwords to the list.
If you want to use non-latin letters, then you must add them yourself in main.py to `valid_chars`

