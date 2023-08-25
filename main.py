import os
from dotenv import load_dotenv
import discord
from embeds import generate_response


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
    if not message.content.startswith("$lastfm"):
        return
    await message.add_reaction("🔄")

    # actually fetch data and send message
    args = message.content.split()
    response = generate_response(args)

    # this is....not good
    if type(response) is list:
        emoji = response[0].emoji
        for embed_res in response:
            embed = embed_res.embed
            output_message = await message.channel.send(embed=embed)
    else:
        embed = response.embed
        emoji = response.emoji
        output_message = await message.channel.send(embed=embed)

    bot_user = output_message.author
    await message.remove_reaction("🔄", bot_user)
    await message.add_reaction(emoji)


client.run(discord_token)
