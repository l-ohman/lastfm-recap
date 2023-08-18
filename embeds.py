import discord


def top_tracks_embed(username, tracks):
    embed = discord.Embed(
        title=f"{username}'s Top Tracks Last Week", color=0xD91F11, description="", url=f"https://www.last.fm/user/{username}")

    # gets data about all tracks
    total_tracks = 0
    total_listens = 0
    for track in tracks:
        total_tracks += 1
        total_listens += int(track["playcount"])
    footer = f"{username} listened to {total_tracks} unique tracks this week with {total_listens} total listens"
    embed.set_footer(text=footer)

    # formats top 3 tracks
    for track in tracks[:3]:
        title = track["name"]
        artist = track["artist"]["#text"]
        # int for coverart size = 0:small, 1:medium, 2:large
        # but it turns out, lastfm doesn't provide valid coverarts in this response anyway...
        cover_art = track["image"][1]["#text"]
        play_count = track["playcount"]

        track_details = f"- **{title}** by **{artist}** — {play_count} plays\n"
        embed.description += track_details

    return embed


def error_embed(title, reason):
    embed = discord.Embed(
        title=title, description=reason, color=0x000000
    )
    return embed
