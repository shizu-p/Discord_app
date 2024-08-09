import discord
import logging
logging.basicConfig(level=logging.INFO)

import openai
import os
from dotenv import load_dotenv
load_dotenv()
token = os.environ['TOKEN']
notice_channel = os.environ['channel']
notice_channel = int(notice_channel)
intents=discord.Intents.all()
client = discord.Client(intents=intents)


