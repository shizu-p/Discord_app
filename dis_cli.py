import discord
import logging
logging.basicConfig(level=logging.INFO)

import openai
import os
from dotenv import load_dotenv
load_dotenv()
token = os.environ['TOKEN']

intents=discord.Intents.all()
client = discord.Client(intents=intents)

notice_channel = 452272367167864833

