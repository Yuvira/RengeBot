# import
import discord
import sqlite3
from renge_utils import load_server
from renge_utils import save_server

# info cmds
async def cmds_mgmt(message, umsg, client, conn, cur):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	server = message.server
	member = message.author
	
	# prefix
	if (args[0].lower() == 'prefix'):
		
		# set prefix
		if (len(args) > 1):
			if (args[1].lower() == 'set'):
				if (member.server_permissions.manage_server == False):
					await client.send_message(channel, 'You do not have manage server permissions!')
				else:
					if (len(args) > 2):
						data = await load_server(server, conn, cur)
						data[1] = umsg[11:]
						await save_server(data, conn, cur)
						await client.send_message(channel, 'Prefix set to `' + data[1] + '`!')
					else:
						await client.send_message(channel, 'No prefix given!')
					
		# remove prefix
		if (len(args) > 1):
			if (args[1].lower() == 'reset'):
				if (member.server_permissions.manage_server == False):
					await client.send_message(channel, 'You do not have manage server permissions!')
				else:
					data = await load_server(server, conn, cur)
					data[1] = None
					await save_server(data, conn, cur)
					await client.send_message(channel, 'Custom prefix removed!')
				
		# display prefix
		else:
			data = await load_server(server, conn, cur)
			if (data[1] == None):
				await client.send_message(channel, 'This server has no custom prefix!')
			else:
				await client.send_message(channel, 'The custom prefix for this server is `' + data[1] + '`')
				
	# autorole
	if (args[0].lower() == 'autorole'):
		
		# set autorole
		if (len(args) > 1):
			if (args[1].lower() == 'set'):
				if (server.me.server_permissions.manage_server == False):
					await client.send_message(channel, 'I do not have manage server permissions!')
				elif (server.me.server_permissions.manage_roles == False):
					await client.send_message(channel, 'I do not have manage roles permissions!')
				elif (member.server_permissions.manage_server == False):
					await client.send_message(channel, 'You do not have manage server permissions!')
				elif (member.server_permissions.manage_roles == False):
					await client.send_message(channel, 'You do not have manage roles permissions!')
				else:
					if (len(args) > 2):
						check = 0
						role = None
						for r in server.roles:
							role = r
							if (args[2] == r.id):
								check = 1
								break
							elif (args[2][3:21] == r.id):
								check = 1
								break
						if (check == 0):
							r = discord.utils.find(lambda u: args[2].lower() in u.name.lower(), server.roles)
							if (r != None):
								role = r
								check = 2
						if (check > 0):
							data = await load_server(server, conn, cur)
							data[6] = role.id
							await save_server(data, conn, cur)
							await client.send_message(channel, 'Autorole set to `' + role.name + '`!')
						else:
							await client.send_message(channel, 'That role does not exist!')
					else:
						await client.send_message(channel, 'Insufficient arguments!')
					
		# remove autorole
		if (len(args) > 1):
			if (args[1].lower() == 'reset'):
				if (server.me.server_permissions.manage_server == False):
					await client.send_message(channel, 'I do not have manage server permissions!')
				elif (server.me.server_permissions.manage_roles == False):
					await client.send_message(channel, 'I do not have manage roles permissions!')
				elif (member.server_permissions.manage_server == False):
					await client.send_message(channel, 'You do not have manage server permissions!')
				elif (member.server_permissions.manage_roles == False):
					await client.send_message(channel, 'You do not have manage roles permissions!')
				else:
					data = await load_server(server, conn, cur)
					data[6] = None
					await save_server(data, conn, cur)
					await client.send_message(channel, 'Autorole removed!')
				
		# display autorole
		else:
			data = await load_server(server, conn, cur)
			if (data[6] == None):
				await client.send_message(channel, 'This server has no autorole!')
			else:
				check = 0
				for r in server.roles:
					if (r.id == data[6]):
						check = 1
						await client.send_message(channel, 'The autorole for this server is `' + r.name + '` and has id `' + r.id + '`')
						break
				if (check == 0):
					data[6] = None
					await save_server(data, conn, cur)
					await client.send_message(channel, 'The autorole for this server could not be found (it was probably deleted)!')
				
	# welcome message
	if (args[0].lower() == 'welcome'):
		
		#set welcome message
		if (len(args) > 1):
			if (args[1].lower() == 'set'):
				if (member.server_permissions.manage_server == False):
					await client.send_message(channel, 'You do not have manage server permissions!')
				else:
					if (len(args) > 2):
						check = 0
						chan = None
						for s in server.channels:
							chan = s
							if (args[2] == s.id):
								check = 1
								break
							elif (args[2][2:20] == s.id):
								check = 2
								break
						if (check == 0):
							c = discord.utils.find(lambda u: args[2].lower() in u.name.lower(), server.channels)
							if (c != None):
								chan = c
								check = 3
						if (check > 0):
							if (len(args) > 3):
								data = await load_server(server, conn, cur)
								data[2] = chan.id
								if (check == 1):
									data[3] = umsg[30:]
								elif (check == 2):
									data[3] = umsg[33:]
								else:
									data[3] = umsg[12 + len(chan.name):]
								await save_server(data, conn, cur)
								await client.send_message(channel, 'Welcome message set to `' + data[3] + '`!')
							else:
								await client.send_message(channel, 'No welcome message provided!')
						else:
							await client.send_message(channel, 'That channel does not exist!')
					else:
						await client.send_message(channel, 'Insufficient arguments!')
					
		# remove welcome message
		if (len(args) > 1):
			if (args[1].lower() == 'reset'):
				if (member.server_permissions.manage_server == False):
					await client.send_message(channel, 'You do not have manage server permissions!')
				else:
					data = await load_server(server, conn, cur)
					data[2] = None
					data[3] = None
					await save_server(data, conn, cur)
					await client.send_message(channel, 'Welcome message removed!')
				
		# display welcome message
		else:
			data = await load_server(server, conn, cur)
			if (data[3] == None):
				await client.send_message(channel, 'This server has no welcome message!')
			else:
				await client.send_message(channel, 'The welcome message for this server is `' + data[3] + '` and displays in <#' + data[2] + '>')
				
	# leave message
	if (args[0].lower() == 'leave'):
		
		#set leave message
		if (len(args) > 1):
			if (args[1].lower() == 'set'):
				if (member.server_permissions.manage_server == False):
					await client.send_message(channel, 'You do not have manage server permissions!')
				else:
					if (len(args) > 2):
						check = 0
						chan = None
						for s in server.channels:
							chan = s
							if (args[2] == s.id):
								check = 1
								break
							elif (args[2][2:20] == s.id):
								check = 2
								break
						if (check == 0):
							c = discord.utils.find(lambda u: args[2].lower() in u.name.lower(), server.channels)
							if (c != None):
								chan = c
								check = 3
						if (check > 0):
							if (len(args) > 3):
								data = await load_server(server, conn, cur)
								data[4] = chan.id
								if (check == 1):
									data[5] = umsg[28:]
								elif (check == 2):
									data[5] = umsg[31:]
								else:
									data[5] = umsg[10 + len(chan.name):]
								await save_server(data, conn, cur)
								await client.send_message(channel, 'Leave message set to `' + data[5] + '`!')
							else:
								await client.send_message(channel, 'No leave message provided!')
						else:
							await client.send_message(channel, 'That channel does not exist!')
					else:
						await client.send_message(channel, 'Insufficient arguments!')
					
		# remove leave message
		if (len(args) > 1):
			if (args[1].lower() == 'reset'):
				if (member.server_permissions.manage_server == False):
					await client.send_message(channel, 'You do not have manage server permissions!')
				else:
					data = await load_server(server, conn, cur)
					data[4] = None
					data[5] = None
					await save_server(data, conn, cur)
					await client.send_message(channel, 'Leave message removed!')
				
		# display leave message
		else:
			data = await load_server(server, conn, cur)
			if (data[5] == None):
				await client.send_message(channel, 'This server has no leave message!')
			else:
				await client.send_message(channel, 'The leave message for this server is `' + data[5] + '` and displays in <#' + data[4] + '>')
