import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio
import yt_dlp

# bot token
from ApyKey import BOTTOKEN # Assuming BOTTOKEN is defined in ApyKey.py

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True
client = commands.Bot(command_prefix="!", intents=intents)

voice_clients = {}
# yt_dl_options = {"format": "bestaudio/best"}
# Using a more robust configuration for yt_dlp
yt_dl_options = {
    "format": "bestaudio/best",
    "noplaylist": True, # Ensure only single videos are processed directly by play/queue
    "extract_flat": "in_playlist", # For playlist handling if you decide to implement it
    "geo_bypass": True, # Bypass geographic restrictions
    "extractor_args": {
        "youtube": {
            "skip": ["dash", "hls"],
            "player_client": ["web"],
        }
    }
}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=0.25"'
}
queues = {}

async def play_next_in_queue(ctx):
    guild_id = ctx.guild.id
    if queues.get(guild_id) and queues[guild_id]:
        voice_client = ctx.guild.voice_client
        if voice_client and not voice_client.is_playing() and not voice_client.is_paused():
            song_url = queues[guild_id].pop(0)
            await ctx.send(f"Now playing: The soundtrack to your questionable life choices 🎵 🤨 (Next in queue)")
            try:
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(song_url, download=False))
                if data and 'url' in data:
                    source_url = data['url']
                    source = FFmpegPCMAudio(source_url, **ffmpeg_options)
                    voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_in_queue(ctx), client.loop).result())
                else:
                    await ctx.send("Could not retrieve playable URL for the next song in queue.")
                    asyncio.run_coroutine_threadsafe(play_next_in_queue(ctx), client.loop).result() # Try next song
            except Exception as e:
                print(f"Error playing next song in queue: {e}")
                await ctx.send(f"Error playing the next song: {e}")
                asyncio.run_coroutine_threadsafe(play_next_in_queue(ctx), client.loop).result() # Try next song
        else:
            print("Voice client not playing or is paused, or queue empty. Waiting for current song to finish.")
    else:
        print("Queue is empty.")
        if ctx.guild.voice_client and not ctx.guild.voice_client.is_playing() and not ctx.guild.voice_client.is_paused():
            await ctx.send("Queue finished! You can add more songs with `!play` or `!queue`.")


@client.event
async def on_ready():
    print("Bot is Run")
    print("------------")

@client.command()
async def Help(ctx):
    await ctx.send("!hello       Make the bot says Hello to you.")
    await ctx.send("!goodbye     Make the bot says Goodbye to you.")
    await ctx.send("!play <link>    Make the bot enter to your voice chat and play some music, or add to queue.")
    await ctx.send("!pause    Pause the music")
    await ctx.send("!resume     Resume the music")
    await ctx.send("!stop     Make the bot exit to your voice chat and stop the music.")
    await ctx.send("!queue <link> .")
    await ctx.send("!skip     Skip the current song and play the next in queue.")


@client.command()
async def hello(ctx):
    await ctx.send("hello, nice to meet you!")

@client.command()
async def goodbye(ctx):
    await ctx.send("Goodbye!")

@client.event
async def on_member_join(member):
    # Make sure this channel ID is correct for your server
    channel = client.get_channel(123456789012345678) # Replace with your actual welcome channel ID
    if channel:
        await channel.send(f"Hello, {member.mention} welcome to my server")

@client.event
async def on_member_remove(member):
    # Make sure this channel ID is correct for your server
    channel = client.get_channel(123456789012345678) # Replace with your actual welcome channel ID
    if channel:
        await channel.send(f"Goodbye, {member.name} i'm so sorry for you")

@client.command()
async def play(ctx, url):
    if not ctx.author.voice:
        return await ctx.send("You are not connected to a voice channel.")

    channel = ctx.author.voice.channel
    guild_id = ctx.guild.id

    if guild_id not in voice_clients:
        await ctx.send("Knock, knock... Who's there? Music!🎶🚪")
        voice = await channel.connect()
        voice_clients[guild_id] = voice
    else:
        voice = voice_clients[guild_id]
        if voice.channel != channel:
            await ctx.send(f"I'm already in a voice channel: {voice.channel.name}. Moving to your channel.")
            await voice.move_to(channel)

    # Use a lambda function to extract info in a separate thread
    loop = asyncio.get_event_loop()
    try:
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if data is None:
            return await ctx.send("Could not retrieve information for that URL.")

        if 'entries' in data: # It's a playlist or multiple entries, just take the first one for now
            song_url = data['entries'][0]['url']
        elif 'url' in data: # Single video
            song_url = data['url']
        else:
            return await ctx.send("Could not find a playable URL from the provided link.")

        if voice.is_playing() or voice.is_paused():
            if guild_id not in queues:
                queues[guild_id] = []
            queues[guild_id].append(url) # Store the original URL for re-extraction when playing from queue
            await ctx.send(f"Added to queue: {data.get('title', 'Unknown Title')}")
        else:
            await ctx.send("Now playing: The soundtrack to your questionable life choices 🎵 🤨 ")
            source = FFmpegPCMAudio(song_url, **ffmpeg_options)
            voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_in_queue(ctx), client.loop).result())
    except Exception as e:
        await ctx.send(f"An error occurred while trying to play: {e}")
        print(f"Error in play command: {e}")


@client.command(pass_context=True)
async def pause(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Shhh! The song is thinking. 🤫 💭 🎼 ")
    else:
        await ctx.send("Nenhuma música está tocando para ser pausada.")


@client.command(pass_context=True)
async def resume(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await ctx.send("And we're back! Did you miss me? (The music, I mean)")
    else:
        await ctx.send("There isn't any music paused.")

@client.command(pass_context=True)
async def stop(ctx):
    guild_id = ctx.guild.id
    if guild_id in voice_clients and voice_clients[guild_id]:
        voice = voice_clients[guild_id]
        voice.stop() # Stop any currently playing audio
        queues[guild_id] = [] # Clear the queue
        await voice.disconnect()
        del voice_clients[guild_id]
        if guild_id in queues:
            del queues[guild_id]
        await ctx.send("My work here is done (for now). Farewell, audionauts! 👋 🚀 🎧")
    else:
        await ctx.send("I'm not in a voice chat.")


@client.command(pass_context=True)
async def queue(ctx, url):
    if not ctx.author.voice:
        return await ctx.send("You are not connected to a voice channel.")

    guild_id = ctx.guild.id
    voice = voice_clients.get(guild_id)

    if voice is None or not voice.is_connected():
        return await ctx.send("I'm not connected to a voice channel. Use `!play` to start a song.")

    # You might want to extract info here to get the title for better queue management message
    try:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if data is None:
            return await ctx.send("Could not retrieve information for that URL.")

        if 'entries' in data: # It's a playlist or multiple entries, just take the first one for now
            song_title = data['entries'][0].get('title', 'Unknown Title')
        elif 'title' in data: # Single video
            song_title = data['title']
        else:
            song_title = "Unknown Title"

        if guild_id not in queues:
            queues[guild_id] = []
        queues[guild_id].append(url) # Store the original URL for re-extraction when playing from queue
        await ctx.send(f"Added '{song_title}' to the queue. Current queue size: {len(queues[guild_id])}")
    except Exception as e:
        await ctx.send(f"Error adding to queue: {e}")
        print(f"Error in queue command: {e}")

@client.command(pass_context=True)
async def skip(ctx):
    guild_id = ctx.guild.id
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop() # This will trigger the 'after' callback and play the next song
        await ctx.send("Skipping current song...")
    elif queues.get(guild_id) and queues[guild_id]:
        await ctx.send("No song is currently playing, but there are songs in the queue. Playing next song...")
        asyncio.run_coroutine_threadsafe(play_next_in_queue(ctx), client.loop).result()
    else:
        await ctx.send("No song is currently playing or in the queue to skip.")


client.run(BOTTOKEN)