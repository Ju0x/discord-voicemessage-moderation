import discord
from discord import app_commands
from discord.ext import commands
from detections import speech


class SpeechToText(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="speech-to-text",
        description="Speech Recognition for Voicemessages"
    )
    @app_commands.describe(
        channel="The channel where the message is in",
        message_id="The message ID or Link, or direct link to the Voicemessage (.ogg extension)",
    )
    async def stt(self, interaction, channel: discord.TextChannel, message_id: str):
        msg = None
        author = None

        await interaction.response.defer()

        direct_link = False

        if message_id.startswith("https://"):
            if message_id.endswith(".ogg"):
                direct_link = True
                author = "link"

            else:
                message_id = message_id.split("/")[-1]

        async def message_not_found():
            await interaction.followup.send(
                embed=discord.Embed(
                    description="**Error:** Message cannot be found!",
                    color=discord.Color.red()
                )
            )

        try:
            if not direct_link:
                msg = await channel.fetch_message(int(message_id))

                if not speech.get_audio(msg):
                    await message_not_found()
                    return

                author = msg.author
            else:
                speech.get_audio(direct_url=message_id)

        except discord.NotFound:
            await message_not_found()
            return

        text = speech.to_text().text
        _max = 4095

        descriptions = [text[i:i + _max] for i in range(0, len(text), _max)]

        for n, description in enumerate(descriptions):
            await interaction.followup.send(
                embed=discord.Embed(
                    title=f"Voicemessage-text from {author}",
                    url=msg.jump_url if msg is not None else "",
                    color=discord.Color.blurple(),
                    description=description
                )
            )

            # To prevent spam
            if n == 3:
                return


async def setup(bot):
    await bot.add_cog(SpeechToText(bot))
