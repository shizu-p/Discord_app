import asyncio
from dis_cli import client,token,notice_channel
import os
import random

@client.event
async def on_message(message):
	if message.author.bot :
		return
	
	msg = message.content
	if message.content.startswith('/dice'):
		parts = msg.split(' ')
		if len(msg) <= 5 :
			await message.channel.send('invalid')
		dicemax = parts[1]
		if not dicemax.isdigit() :
			await message.channel.send('invalid')
		dicemax = int(dicemax)
		
		dice_res = random.randint(1,dicemax)
		print(dice_res)
		dice_res = str(dice_res)
		await message.channel.send(f'Result is {dice_res}')

@client.event
async def on_ready() :
	print(f'Logged in as {client.user}')
	channel = client.get_channel(notice_channel)
	await channel.send('test')


client.run(token)