# import
import discord
import sqlite3

# info cmds
async def cmds_profile(message, umsg, client, conn, cur):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	
	# create profile if not exist
	t = (member.id,)
	cur.execute('SELECT * FROM profiles WHERE id=?', t)
	t = cur.fetchone()
	if (t == None):
		data = (member.id, member.name + '#' + member.discriminator, 'Nothing to see here')
		cur.execute('INSERT INTO profiles VALUES (?,?,?)', data)
		conn.commit()
	
	# profile
	if (args[0] == 'profile'):
		
		# load data
		t = (member.id,)
		cur.execute('SELECT * FROM profiles WHERE id=?', t)
		data = cur.fetchone()
				
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
		t = (member.id,)
		cur.execute('DELETE FROM profiles WHERE id=?', t)
		cur.execute('INSERT INTO profiles VALUES (?,?,?)', data)
		conn.commit()
