import discord
from discord.ext import commands
import os
from googleapiclient.discovery import build
import datetime
import random
from keep_alive import keep_alive

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='uuuu!', intents=intents)


def get_channel_id(channel_name):
  youtube = build('youtube',
                  'v3',
                  developerKey=api_key,
                  static_discovery=False)
  request = youtube.search().list(part="id",
                                  q=channel_name,
                                  type="channel",
                                  maxResults=1)
  response = request.execute()
  items = response.get('items', [])
  if items:
    return items[0]['id']['channelId']
  return None


def get_last_stream_time(channel_name):
  channel_id = get_channel_id(channel_name)
  youtube = build('youtube',
                  'v3',
                  developerKey=api_key,
                  static_discovery=False)
  request = youtube.search().list(channelId=channel_id,
                                  maxResults=1,
                                  part="snippet",
                                  order='date',
                                  type='video')
  response = request.execute()
  items = response.get('items', [])
  if items:
    live_stream = items[0]

    live = live_stream['snippet']['liveBroadcastContent']
    title = live_stream['snippet']['title']
    published_at = live_stream['snippet']['publishedAt']
    channel_title = live_stream['snippet']['channelTitle']
    thumbnails = live_stream['snippet']['thumbnails']
    thumbnail_url = thumbnails['default']['url']

    if live == 'none':
      return published_at, title, channel_title, "LastLive", thumbnail_url
    elif live == 'live':
      return published_at, title, channel_title, "NowLive", thumbnail_url
  return None


def get_random_video_id(channel_id):
  youtube = build('youtube',
                  'v3',
                  developerKey=api_key,
                  static_discovery=False)
  request = youtube.search().list(
    part="snippet, id",
    channelId=channel_id,
    type="video",
    maxResults=50
  )
  response = request.execute()
  items = response.get('items', [])
  if items:
    rand = random.randint(0, len(items) - 1)
    video_id = items[rand]['id']["videoId"]
    title = items[rand]["snippet"]["title"]
    thumbnail = items[rand]["snippet"]["thumbnails"]
    thumbnail_url = thumbnail['default']['url']
    return video_id, title, thumbnail_url
  return None


def get_channel_statistics(channel_name):
  youtube = build('youtube',
                  'v3',
                  developerKey=api_key,
                  static_discovery=False)
  channel_id = get_channel_id(channel_name)
  request = youtube.channels().list(part="snippet,statistics",
                                    id=channel_id,
                                    maxResults=1)
  response = request.execute()
  items = response.get('items', [])
  if items:
    channel_info = items[0]
    statistics = channel_info.get('statistics', {})
    subscriber_count = statistics.get('subscriberCount', 'N/A')
    total_views = statistics.get('viewCount', 'N/A')
    channel_title = channel_info['snippet']['title']
    channel_description = channel_info['snippet']['description']
    profile_picture = channel_info['snippet']['thumbnails']['default']['url']
    top_videos = get_top_videos(channel_id)

    return subscriber_count, total_views, channel_title, channel_description, profile_picture, top_videos
  return None


def get_top_videos(channel_id):
  youtube = build('youtube',
                  'v3',
                  developerKey=api_key,
                  static_discovery=False)
  request = youtube.search().list(part="snippet",
                                  channelId=channel_id,
                                  maxResults=3,
                                  order="viewCount")
  response = request.execute()
  items = response.get('items', [])
  top_videos = []
  for item in items:
    video_title = item['snippet']['title']
    video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
    top_videos.append({'title': video_title, 'url': video_url})
  return top_videos


@bot.command()
async def reps(ctx, *, channel_name="CeresFauna"):
  channel_id = get_channel_id(channel_name)

  if channel_id:
    random_video_id, title, thumbnail_url = get_random_video_id(channel_id)
    if random_video_id:
      embed = discord.Embed(title="Do your reps!", color=discord.Color.blue())
      embed.set_thumbnail(url=thumbnail_url)
      embed.add_field(name="Title", value=title)
      embed.add_field(
        name="Watch this one!",
        value="https://www.youtube.com/watch?v={}".format(random_video_id))
      await ctx.send(embed=embed)
    else:
      await ctx.send("no videos found in the channel uuuuuu.")
  else:
    await ctx.send("channel not found uuuuuu.")


@bot.command()
async def hello(ctx):
  await ctx.send("hello world!")


@bot.command()
async def streamtime(ctx, *, channel_name="CeresFauna"):
  response = get_last_stream_time(channel_name)
  if response:
    last_stream_time, title, channel_title, isLive, thumbnail_url = response
    if isLive == "NowLive":
      embed = discord.Embed(title=channel_title,
                            description=title,
                            color=discord.Color.green())
      embed.set_thumbnail(url=thumbnail_url)
      embed.add_field(name="Time since last stream",
                      value=f"{channel_title} is NOW STREAMING pog")
      await ctx.send(embed=embed)
    elif isLive == "LastLive":
      now = datetime.datetime.now()
      published_time = datetime.datetime.fromisoformat(
        last_stream_time.replace('Z', ''))
      elapsed_time = now - published_time
      elapsed_hours = int(elapsed_time.total_seconds() // 3600)
      elapsed_minutes = int((elapsed_time.total_seconds() % 3600) // 60)
      elapsed_seconds = int(elapsed_time.total_seconds() % 60)

      embed = discord.Embed(title=channel_title,
                            description=title,
                            color=discord.Color.green())
      embed.set_thumbnail(url=thumbnail_url)
      embed.add_field(
        name="Time since last stream",
        value=
        f"it has been {elapsed_hours} hours, {elapsed_minutes} minutes, and {elapsed_seconds} seconds since the last stream."
      )
      await ctx.send(embed=embed)
  else:
    await ctx.send("no live streams found uuuu :(((")


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')
  print('------')


@bot.command()
async def stats(ctx, *, channel_name="CeresFauna"):
  subscriber_count, total_views, channel_title, channel_description, profile_picture, top_videos = get_channel_statistics(
    channel_name)

  if channel_title:
    embed = discord.Embed(title=channel_title,
                          description=channel_description,
                          color=discord.Color.blue())
    embed.set_thumbnail(url=profile_picture)
    embed.add_field(name="Subscriber Count", value=subscriber_count)
    embed.add_field(name="Total Views", value=total_views)

    embed.add_field(name="Top Videos", value="", inline=False)

    for video in top_videos:
      embed.add_field(name=video['title'], value=video['url'], inline=False)

    await ctx.send(embed=embed)
  else:
    await ctx.send("Channel not found.")


@bot.command()
async def commands(ctx):
  # Get the bot's profile picture
  embed = discord.Embed(title="Bot Commands",
                        description="List of available commands:",
                        color=discord.Color.blue())
  # Add commands and descriptions
  embed.add_field(
    name="uuuu!reps [channel_name]",
    value="Displays a random video from the specified YouTube channel.",
    inline=False)
  embed.add_field(name="!hello", value="Says hello to the user.", inline=False)
  embed.add_field(
    name="uuuu!streamtime [channel_name]",
    value=
    "Displays the time since the last stream of the specified YouTube channel.",
    inline=False)
  embed.add_field(
    name="uuuu!stats [channel_name]",
    value=
    "Displays statistics for the specified YouTube channel, including top 3 videos.",
    inline=False)
  await ctx.send(embed=embed)


api_key = os.environ['YOUTUBE_API_KEY']
password = os.environ['password']
keep_alive()
bot.run(password)
