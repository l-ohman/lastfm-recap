import discord
from dotenv import load_dotenv
import os
from fetch import weekly_track_chart


load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$lastfm"):
        await message.channel.send("Getting your data...")
        username = "jake6969696969"

        # res = weekly_track_chart(username)
        await message.channel.send("?")


client.run(discord_token)
