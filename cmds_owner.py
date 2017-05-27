# import
import discord
import sqlite3
import sys

# info cmds
async def cmds_owner(message, umsg, client, conn):
	
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
			await client.send_message(channel, 'There are ' + t + ' users in this server')
				
		# shutdown
		if (args[0] == 'shutdown'):
			await client.send_message(channel, '*Shutting down...*')
			conn.close()
			await client.logout()
			sys.exit(0)
