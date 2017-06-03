# import
import discord
import sqlite3
import sys
from renge_utils import load_profile
from renge_utils import save_profile

# info cmds
async def cmds_owner(message, umsg, client, conn, cur):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	server = message.server
	member = message.author
	
	# check owner
	if (member.id == '188663897279037440'):
		
		# get user by id
		if (args[0] == 'getuser'):
			try:
				user = await client.get_user_info(args[1])
				await client.send_message(channel, 'User is `' + user.name + '#' + user.discriminator + '`')
			except:
				await client.send_message(channel, 'User not found!')
			
		# list servers
		if (args[0] == 'serverlist'):
			msg = '**Renge Server List**'
			for server in client.servers:
				msg = msg + '\n`' + server.name + '` owned by `' + server.owner.name + '#' + server.owner.discriminator + '`'
			await client.send_message(channel, msg)
			
		# count members in server
		if (args[0] == 'usercount'):
			t = 0
			for member in server.members:
				t += 1
			await client.send_message(channel, 'There are ' + str(t) + ' users in this server')
			
		# give credits
		if (args[0] == 'givecredits'):
			try:
				user = await client.get_user_info(args[1])
				t = int(args[2])
				data = await load_profile(user, conn, cur)
				data[3] = data[3] + t
				if (data[3] > 9200000000000000000):
					data[3] = 9200000000000000000
					await client.send_message(channel, 'pls')
				await save_profile(user, data, conn, cur)
				await client.send_message(channel, 'Gave ' + args[2] + ' credits to ' + user.name + '!')
			except:
				await client.send_message(channel, 'You did something wrong!')
				
		# shutdown
		if (args[0] == 'shutdown'):
			await client.send_message(channel, '*Shutting down...*')
			conn.close()
			await client.logout()
			sys.exit(0)
