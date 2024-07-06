import discord
import fetch
from time import sleep


class EmbedResponse:
    def __init__(self, embed, emoji):
        self.embed = embed
        self.emoji = emoji


# Returns an embed for the message and an emoji for the status
def generate_response(args):
    # No args -> help message
    if (len(args) == 1 or len(args) == 2):
        embed = helper("List of commands")
        return EmbedResponse(embed, "❔")
    command = args[1]

    # "user" command
    if (command == "user"):
        user_embeds = []
        for username in args[2:]:
            res = fetch.weekly_track_chart(username)

            if "error" in res:
                embed = error(title="Error contacting Last.FM API",
                              reason=res["message"])
                return EmbedResponse(embed, "⛔")

            tracklist = res["weeklytrackchart"]["track"]
            embed = user_recap(username, tracklist)
            user_embeds.append(EmbedResponse(embed, "✅"))
        return user_embeds

    # todo: "compare" command
    elif (command == "compare"):
        if (len(args) < 4):
            embed = error(title="Invalid comparison",
                          reason="Please add 2 or more usernames to compare.")
            return EmbedResponse(embed, "⛔")
        # todo: get data for each user (unsure what we will be comparing yet xd)

        usernames = args[2:]
        embed = user_compare(usernames)

        return EmbedResponse(embed, "✅")

    else:
        embed = helper("List of commands")
        return EmbedResponse(embed, "❔")


### util embeds ###

def helper(title):
    embed = discord.Embed(
        title=title, color=0x000000
    )
    embed.description = "- **user**: recap of a single user's stats for the past week\n- **compare**: compare last week's status for any number of users _(not yet implemented)_"
    return embed


def error(title, reason):
    embed = discord.Embed(
        title=title, description=reason, color=0x000000
    )
    embed.set_footer(
        text="Use `$lastfm` with no arguments to see a help message")
    return embed


### functional embeds ###
lastfm_red = 0xD91F11


def user_recap(username, tracks):
    embed = discord.Embed(
        title=f"{username}'s Music This Week", color=lastfm_red, description="", url=f"https://www.last.fm/user/{username}")

    # gets data about all tracks
    artists_map = {}
    total_tracks = 0
    total_listens = 0
    for track in tracks:
        playcount = int(track["playcount"])
        total_tracks += 1
        total_listens += playcount

        artist = track["artist"]["#text"]
        if artist not in artists_map:
            artists_map[artist] = playcount
        else:
            artists_map[artist] += playcount

    embed.description += "**Top Tracks**\n"
    # formats top 3 tracks
    for track in tracks[:3]:
        title = track["name"]
        artist = track["artist"]["#text"]
        play_count = track["playcount"]

        track_details = f"- **{title}** by **{artist}** — {play_count} plays\n"
        embed.description += track_details

    artists = [{"artist": k, "count": v} for (k, v) in artists_map.items()]
    artists.sort(key=lambda x: x["count"], reverse=True)
    # formats top 3 artists
    embed.description += "------------------------------------------------------\n**Top Artists**\n"
    for artist in artists[:3]:
        name = artist["artist"]
        count = artist["count"]
        artist_details = f"- **{name}** — {count} plays\n"
        embed.description += artist_details

    footer = f"{total_listens} total listens — {total_tracks} unique tracks — {len(artists)} unique artists"
    embed.set_footer(text=footer)

    return embed


# this function does not belong here but whatever
def seconds_to_hours(est_seconds):
    est_minutes = est_seconds//60
    
    est_hours = est_minutes//60
    est_minutes %= 60

    # xd = lambda x: "0" + str(x) if x<10 else str(x)
    # est_duration = f"{xd(est_hours)}:{xd(est_minutes)}"

    # i changed my mind on how i want this to be displayed
    return [est_hours, est_minutes]


# some overlap with the `user_recap` fn but eh
def user_compare(usernames):
    tracklists = {}
    for user in usernames:
        res = fetch.weekly_track_chart(user)
        tracklists[user] = res["weeklytrackchart"]["track"]
        sleep(0.5)

    title = ", ".join(usernames)
    embed = discord.Embed(
        title=f"Last Week for {title}", color=lastfm_red, description="")
    
    # add each user to embed
    for user in usernames:
        # count listens and artists
        unique_tracks = scrobbles = 0
        artists = set()
        for track in tracklists[user]:
            unique_tracks += 1
            scrobbles += int(track["playcount"])
            artists.add(track["artist"]["#text"])
        
        # avg song length on spotify in 2020 was 3:17
        est_hours, est_mins = seconds_to_hours(scrobbles * 197)
        
        embed.description += f"**{user}** — {scrobbles} total listens\n"
        embed.description += f"- {unique_tracks} unique tracks\n"
        embed.description += f"- {len(artists)} different artists\n"
        if est_hours>0:
            embed.description += f"- {est_hours} hours and {est_mins} minutes of music*\n\n"
        else:
            embed.description += f"- {est_mins} of music*\n\n"
    
    embed.set_footer(text="*Estimate uses an average song length of 3:17")

    return embed
