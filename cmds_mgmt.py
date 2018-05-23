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
						for s in server.channels:
							if (args[2] == s.id):
								check = 1
								break
							elif (args[2][2:20] == s.id):
								args[2] = args[2][2:20]
								check = 2
								break
						if (check > 0):
							if (len(args) > 3):
								data = await load_server(server, conn, cur)
								data[2] = args[2]
								if (check == 1):
									data[3] = umsg[30:]
								else:
									data[3] = umsg[33:]
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
						for s in server.channels:
							if (args[2] == s.id):
								check = 1
								break
							elif (args[2][2:20] == s.id):
								args[2] = args[2][2:20]
								check = 2
								break
						if (check > 0):
							if (len(args) > 3):
								data = await load_server(server, conn, cur)
								data[4] = args[2]
								if (check == 1):
									data[5] = umsg[28:]
								else:
									data[5] = umsg[31:]
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
