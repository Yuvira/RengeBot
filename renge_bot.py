# import
import discord
import time
import random
import logging
import sqlite3
from cmds_info import cmds_info
from cmds_mod import cmds_mod
from cmds_action import cmds_action
from cmds_currency import cmds_currency
from cmds_games import cmds_games
from cmds_misc import cmds_misc
from cmds_owner import cmds_owner

# client
client = discord.Client()

# database
conn = sqlite3.connect('renge.db')
cur = conn.cursor()

# message received
@client.event
async def on_message(message):
	
	# variables
	log_channel = discord.Object('314283195866677251')
	
	# check message source
	check = True
	try:
		if (message.server.name != ''):
			check = True
	except AttributeError:
		if (message.author.bot == False):
			await client.send_message(log_channel, 'Received DM from `' + message.author.name + '#' + message.author.discriminator + '`: ' + message.content)
			check = True
	if (message.author.bot == True):
		check = False
	
	# if message received from server
	if (check == True):
		
		# transfer message to variable and format
		umsg = message.content
		umsg.lower()
		
		# check prefix
		if umsg.startswith('$'):
			
			# more formatting
			umsg = umsg[1:]
			
			# command lists
			await cmds_info(message, umsg, client)
			await cmds_mod(message, umsg, client)
			await cmds_action(message, umsg, client)
			await cmds_currency(message, umsg, client, conn, cur)
			await cmds_games(message, umsg, client, conn, cur)
			await cmds_misc(message, umsg, client, conn, cur)
			await cmds_owner(message, umsg, client, conn, cur)

# server join
@client.event
async def on_server_join(server):
	log_channel = discord.Object('314283195866677251')
	await client.send_message(log_channel, 'Joined server `' + server.name + '`, owned by `' + server.owner.name + '#' + server.owner.discriminator + '`')

# server leave
@client.event
async def on_server_remove(server):
	log_channel = discord.Object('314283195866677251')
	await client.send_message(log_channel, 'Left server `' + server.name + '`, owned by `' + server.owner.name + '#' + server.owner.discriminator + '`')

# startup
@client.event
async def on_ready():
	print('Logged in as:')
	print(client.user.name)
	print(client.user.id)
	print('------')
	await client.change_presence(game=discord.Game(name='$help | Nyanpasuuu~'), status=None, afk=False)
	cur.execute('DELETE FROM games')
	conn.commit()

# logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs.txt', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# run
random.seed(time.time())
client.run('token')
