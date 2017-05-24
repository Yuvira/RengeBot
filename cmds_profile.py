# import
import discord
import sqlite3
from renge_db import conn, c

# info cmds
async def cmds_profile(message, umsg, client):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	
	# create profile if not exist
	t = (member.id,)
	c.execute('SELECT * FROM profiles WHERE id=?', t)
	t = c.fetchone()
	if (t == None):
		profile = (member.id, member.name + '#' + member.discriminator, 'Nothing to see here')
		c.execute('INSERT INTO profiles VALUES (?,?,?)', profile)
		conn.commit()
	
	# profile
	if (args[0] == 'profile'):
		
		# load data
		t = (member.id,)
		c.execute('SELECT * FROM profiles WHERE id=?', t)
		data = c.fetchone()
				
		# profile commands
		if (len(args) > 1):
			
			# description set
			if (args[1] == 'desc'):
				if (len(args) > 2):
					data[2] = umsg[13:]
					await client.send_message(channel, 'Description set to `' + data[2] + '`!')
				else:
					await client.send_message(channel, 'You need to enter a description!')
		
		# show profile
		else:
			embed = discord.Embed(title=member.name + "'s profile", type='rich', description=data[2])
			await client.send_message(channel, content=None, embed=embed)
		
		# save profile
		c.execute('UPDATE profiles SET id=?, name=?, desc=?', data)
		conn.commit()
