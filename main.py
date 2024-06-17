# this code was skidded using DarkWeb AI. Severity is the founder of DarkWeb AI.

import discord
import aiohttp
import json
from discord.ext import commands

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN = config.get('TOKEN', '')
source_channel_ids = config.get('source_channel_ids', {})
webhook_urls = config.get('webhook_urls', {})
allowed_mentions = config.get('allowed_mentions', [])  
intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return  

    for source_id, channel_id in source_channel_ids.items():
        if str(message.channel.id) == str(channel_id):  
            content = message.content
            author_name = message.author.display_name
            avatar_url = message.author.avatar.url if message.author.avatar else None
            
            files = []
            
            if message.attachments:
                attachment = message.attachments[0] 
                file = await attachment.to_file()
                files.append(file)

            async with aiohttp.ClientSession() as session:
                webhook_url = webhook_urls.get(source_id, '')
                if webhook_url:
                    if any(word in content for word in ['@everyone', '@here']):
                        if message.author.id not in allowed_mentions:
                            print(f"Unauthorized attempt by {author_name} to mention @everyone or @here.")
                            return  

                    webhook = discord.Webhook.from_url(webhook_url, session=session)
                    await webhook.send(content=content, 
                                       username=author_name, 
                                       avatar_url=avatar_url,
                                       files=files)

            print(f"Message from {author_name} in channel {source_id} sent to webhook successfully.")

bot.run(TOKEN)
