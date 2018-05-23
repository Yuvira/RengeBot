# import
import discord
import time
import random
import importlib
import logging
import sqlite3
import datetime
import asyncio

# modules
import cmds_action
import cmds_currency
import cmds_games
import cmds_info
import cmds_mgmt
import cmds_misc
import cmds_mod
import cmds_owner

# commands
from renge_utils import load_server
from renge_utils import create_profile

# client
client = discord.Client()

# database
conn = sqlite3.connect('renge.db')
cur = conn.cursor()

# startup variables
prefix = 'prefix'
token = 'token'

# song of the day values
sotd_t1 = datetime.datetime.now().day
sotd_t2 = sotd_t1

# message received
@client.event
async def on_message(message):
	
	# update name in profile
	try:
		await create_profile(message.author, conn, cur)
		t = (message.author.name + '#' + message.author.discriminator, message.author.id)
		cur.execute('UPDATE profiles SET name=? WHERE id=?', t)
		conn.commit()
	except:
		pass
	
	# variables
	log_channel = discord.Object('314283195866677251')
	dm_log = discord.Object('342097197443317760')
	
	# check message source
	botMsg = True
	usrMsg = False
	if (message.author.bot == False):
		botMsg = False
		if (message.server is None):
			usrMsg = True
			await client.send_message(dm_log, 'Received DM from `' + message.author.name + '#' + message.author.discriminator + '`: ' + message.content)
	
	# if message received from user
	if (botMsg == False):
		
		# retrieve server prefix
		custom_prefix = prefix
		if (usrMsg == False):
			data = await load_server(message.server, conn, cur)
			if data[1] != None:
				custom_prefix = data[1]
		
		# shorten variable name
		umsg = message.content
		
		# check prefix
		if (umsg.startswith(prefix) or umsg.startswith(custom_prefix)):
			
			# more formatting
			if umsg.startswith(custom_prefix):
				umsg = umsg[len(custom_prefix):]
			else:
				umsg = umsg[1:]
			
			# command lists
			await cmds_action.cmds_action(message, umsg, client)
			await cmds_currency.cmds_currency(message, umsg, client, conn, cur)
			await cmds_games.cmds_games(message, umsg, client, conn, cur)
			await cmds_info.cmds_info(message, umsg, client)
			await cmds_mgmt.cmds_mgmt(message, umsg, client, conn, cur)
			await cmds_misc.cmds_misc(message, umsg, client, conn, cur)
			await cmds_mod.cmds_mod(message, umsg, prefix, client)
			await cmds_owner.cmds_owner(message, umsg, client, conn, cur)
			
			# reload module
			if (message.author.id == '188663897279037440'):
				args = umsg.split(' ')
				if (args[0].lower() == 'reload' and len(args) == 2):
					try:
						if (args[1].lower() == 'action'):
							importlib.reload(cmds_action)
						elif (args[1].lower() == 'currency'):
							importlib.reload(cmds_currency)
						elif (args[1].lower() == 'games'):
							importlib.reload(cmds_games)
						elif (args[1].lower() == 'info'):
							importlib.reload(cmds_info)
						elif (args[1].lower() == 'mgmt'):
							importlib.reload(cmds_mgmt)
						elif (args[1].lower() == 'misc'):
							importlib.reload(cmds_misc)
						elif (args[1].lower() == 'mod'):
							importlib.reload(cmds_mod)
						elif (args[1].lower() == 'owner'):
							importlib.reload(cmds_owner)
						else:
							raise Exception
						await client.send_message(message.channel, 'Reloaded ' + args[1] + ' command module successfully!')
					except:
						await client.send_message(message.channel, 'Failed to load module!')

# log server join
@client.event
async def on_server_join(server):
	log_channel = discord.Object('314283195866677251')
	await client.send_message(log_channel, 'Joined server `' + server.name + '`, owned by `' + server.owner.name + '#' + server.owner.discriminator + '`')

# log server leave
@client.event
async def on_server_remove(server):
	log_channel = discord.Object('314283195866677251')
	await client.send_message(log_channel, 'Left server `' + server.name + '`, owned by `' + server.owner.name + '#' + server.owner.discriminator + '`')

# member join
@client.event
async def on_member_join(member):
	data = await load_server(member.server, conn, cur)
	if (data[2] != None and data[3] != None):
		channel = discord.Object(data[2])
		data[3] = data[3].replace('!user.mention!', member.mention)
		data[3] = data[3].replace('!user.name!', member.name)
		await client.send_message(channel, data[3])

# member leave
@client.event
async def on_member_remove(member):
	data = await load_server(member.server, conn, cur)
	if (data[4] != None and data[5] != None):
		channel = discord.Object(data[4])
		data[5] = data[5].replace('!user.mention!', member.mention)
		data[5] = data[5].replace('!user.name!', member.name)
		await client.send_message(channel, data[5])
	
# song of the day updater
async def sotd():
	global sotd_t1
	global sotd_t2
	await client.wait_until_ready()
	while not client.is_closed:
		await asyncio.sleep(60)
		sotd_t1 = sotd_t2
		sotd_t2 = datetime.datetime.now().day
		if (sotd_t1 != sotd_t2):
			cur.execute('DELETE FROM sotd WHERE rowid=(SELECT MIN(rowid) FROM sotd)')
			conn.commit()

# startup
@client.event
async def on_ready():
	print('Logged in as:')
	print(client.user.name)
	print(client.user.id)
	print('------')
	await client.change_presence(game=discord.Game(type=0, name=prefix+'help | Nyanpasuuu~'), status=None, afk=False)
	log_channel = discord.Object('314283195866677251')
	await client.send_message(log_channel, 'Booted successfully!')

# logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs.txt', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# run
random.seed(time.time())
client.loop.create_task(sotd())
client.run(token)
