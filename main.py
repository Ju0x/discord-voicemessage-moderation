import json
import os

import discord
from discord.ext import commands, tasks
import string
from detections import earrape, speech

valid_chars = string.ascii_letters + string.digits + "äöüß"  # Add more if you want
command_path = "commands"

with open("config.json", "r") as fp:
    data = json.load(fp)


def cleanup(text: str):
    return "".join(char if char in valid_chars else "" for char in text).lower()


class Bot(commands.Bot):
    async def on_ready(self):
        print(f"{self.user} - Started!")

        # Load commands
        for file in os.listdir(f"./{command_path}"):
            if file.endswith(".py"):
                await self.load_extension(f"{command_path}.{file.strip('.py')}")

        await self.sync()

    async def sync(self):
        await bot.tree.sync()

        for guild in self.guilds:
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)

    async def on_message(self, message):
        if message.author.bot:
            return

        if not speech.get_audio(message):
            return

        if earrape.is_earrape():
            await message.reply(
                embed=discord.Embed(
                    description=f"**⚠️ Voice-message might contain an earrape!**",
                    color=discord.Color.yellow()
                )
            )

        recog = speech.to_text()

        for badword in data["badwords"]:
            if badword.lower() in cleanup(recog.text):
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
