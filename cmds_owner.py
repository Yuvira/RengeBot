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
	server = message.guild
	member = message.author
	
	# check owner
	if (member.id == 188663897279037440):
			
		# count members in server
		if (args[0].lower() == 'usercount'):
			await channel.send('Total users: ' + str(len(server.members)) + '\nBot users: ' + str(len([member for member in server.members if member.bot])))
			
		# count total severs
		if (args[0].lower() == 'servercount'):
			await channel.send('Total servers: ' + str(len(client.guilds)) + '\nBot servers: ' + str(len([server for server in client.guilds if len([member for member in server.members if member.bot]) > len([member for member in server.members if not member.bot])])))
			
		# add song to table
		if (args[0].lower() == 'addsotd'):
			try:
				sdata = umsg[8:].split(' | ')
				t = (sdata[0], sdata[1], sdata[2], sdata[3])
				cur.execute('INSERT INTO sotd VALUES (?,?,?,?)', t)
				conn.commit()
				await channel.send('Added ' + sdata[1] + ' by ' + sdata[0] + ' to the song table!')
			except:
				await channel.send('You did something wrong!')
		
		# force next song
		if (args[0].lower() == 'updatesotd'):
			try:
				cur.execute('DELETE FROM sotd WHERE rowid=(SELECT MIN(rowid) FROM sotd)')
				conn.commit()
				await channel.send('Song of the Day successfully updated!')
			except:
				await channel.send('Something went wrong!')
		
		# list tracks
		if (args[0].lower() == 'listsotd'):
			msg = 'List'
			cur.execute('SELECT * FROM sotd ORDER BY rowid')
			for a in range(0,10):
				t = cur.fetchone()
				if (t == None):
					break
				else:
					msg = msg + '\n' + str(a+1) + ': ' + t[0] + ' - ' + t[1]
			embed = discord.Embed(title = 'SOTD List', type = 'rich', description = msg)
			await channel.send(content = None, embed = embed)
		
		# give credits
		if (args[0].lower() == 'givecredits'):
			try:
				user = await client.fetch_user(args[1])
				t = int(args[2])
				data = await load_profile(user, conn, cur)
				data[3] = str(int(data[3]) + t)
				await save_profile(data, conn, cur)
				await channel.send('Gave ' + args[2] + ' credits to ' + str(user) + '!')
			except:
				await channel.send('You did something wrong!')
				
		# shutdown
		if (args[0].lower() == 'shutdown'):
			await channel.send('*Shutting down...*')
			conn.close()
			await client.logout()
			sys.exit(0)
