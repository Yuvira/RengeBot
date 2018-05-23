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
			
		# count members in server
		if (args[0].lower() == 'usercount'):
			await client.send_message(channel, 'Total users: ' + str(len(server.members)) + '\nBot users: ' + str(len([member for member in server.members if member.bot])))
			
		# count total severs
		if (args[0].lower() == 'servercount'):
			await client.send_message(channel, 'Total servers: ' + str(len(client.servers)) + '\nBot servers: ' + str(len([server for server in client.servers if len([member for member in server.members if member.bot]) > len([member for member in server.members if not member.bot])])))
			
		# add song to table
		if (args[0].lower() == 'addsotd'):
			try:
				sdata = umsg[8:].split(' | ')
				t = (sdata[0], sdata[1], sdata[2], sdata[3])
				cur.execute('INSERT INTO sotd VALUES (?,?,?,?)', t)
				conn.commit()
				await client.send_message(channel, 'Added ' + sdata[1] + ' by ' + sdata[0] + ' to the song table!')
			except:
				await client.send_message(channel, 'You did something wrong!')
		
		# force next song
		if (args[0].lower() == 'forcesotdupdate'):
			try:
				cur.execute('DELETE FROM sotd WHERE rowid=(SELECT MIN(rowid) FROM sotd)')
				conn.commit()
				await client.send_message(channel, 'Song of the Day successfully updated!')
			except:
				await client.send_message(channel, 'Something went wrong!')
		
		# give credits
		if (args[0].lower() == 'givecredits'):
			try:
				user = await client.get_user_info(args[1])
				t = int(args[2])
				data = await load_profile(user, conn, cur)
				data[3] = str(int(data[3]) + t)
				await save_profile(data, conn, cur)
				await client.send_message(channel, 'Gave ' + args[2] + ' credits to ' + str(user) + '!')
			except:
				await client.send_message(channel, 'You did something wrong!')
				
		# shutdown
		if (args[0].lower() == 'shutdown'):
			await client.send_message(channel, '*Shutting down...*')
			conn.close()
			await client.logout()
			sys.exit(0)
