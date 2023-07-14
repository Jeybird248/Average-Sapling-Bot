# Average Sapling Bot
![GitHub repo size](https://img.shields.io/github/repo-size/Jeybird248/Average-Sapling-Bot)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A Discord bot that integrates with the YouTube API to provide various functionalities related to YouTube channels and videos.
Inspiration goes to [saplinganon](https://github.com/saplinganon)'s [imissfauna.com](https://imissfauna.com/)

## Features

- Display a random video from a specified YouTube channel
- Check the time since the last stream of a YouTube channel
- Retrieve statistics for a YouTube channel, including top 3 videos

## Prerequisites

- Python 3.7 or higher
- Discord.py library
- Google API Client library
- YouTube Data API key (Get one from the [Google Developers Console](https://console.developers.google.com/))

## Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/your-repo-name.git
```

2. Set up your Discord bot:
    Create a new Discord application and bot in the Discord Developer Portal.
    Copy the bot token.
    Invite the bot to your server using the generated OAuth2 URL.

3. Set up the YouTube Data API:
    Create a project in the Google Developers Console.
    Enable the YouTube Data API for your project.
    Generate an API key.

4. Configure the bot:
    Rename the config.example.py file to config.py.
    Replace YOUR_DISCORD_BOT_TOKEN with your Discord bot token in config.py.
    Replace YOUR_YOUTUBE_API_KEY with your YouTube Data API key in config.py.

5. Run the bot:

```bash
python bot.py
```

## Usage
- Use the command !reps [channel_name] to display a random video from the specified YouTube channel.
- Use the command !streamtime [channel_name] to check the time since the last stream of the specified YouTube channel.
- Use the command !stats [channel_name] to retrieve statistics for the specified YouTube channel, including top 3 videos.
- Use the command !help to display a list of available commands.
