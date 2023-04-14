import json

import discord
import requests
from discord.ext import commands
import whisper
import string

valid_chars = string.ascii_letters + string.digits + "äöüß"  # Add more if you want

with open("config.json", "r") as fp:
    data = json.load(fp)


def cleanup(text: str):
    return "".join(char if char in valid_chars else "" for char in text).lower()


class Bot(commands.Bot):
    async def on_ready(self):
        print(f"{self.user} - Started!")

    async def on_message(self, message):
        if message.author.bot:
            return
        voice_messages = []

        for attachment in message.attachments:
            if attachment.filename.endswith(".ogg"):
                voice_messages.append(attachment)

        if len(voice_messages) == 0:
            return

        response = requests.get(voice_messages[0].url)

        with open("audio.ogg", "wb") as fp:
            fp.write(response.content)

        model = whisper.load_model("base")

        audio = whisper.load_audio("audio.ogg")
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        if data["language"] == "auto":
            _, probs = model.detect_language(mel)
            options = whisper.DecodingOptions(fp16=False)
        else:
            options = whisper.DecodingOptions(fp16=False, language=data["language"])
            
        result = whisper.decode(model, mel, options)

        for badword in data["badwords"]:
            if badword.lower() in cleanup(result.text):
                await message.delete()
                await message.channel.send(
                    embed=discord.Embed(
                        description=f"**Voice-message from {message.author} has been deleted.**\n"
                                    f"**Reason:** Contains profanity",
                        color=discord.Color.red()
                    )
                )


bot = Bot(command_prefix="!", intents=discord.Intents.all())

bot.run(data["token"])
