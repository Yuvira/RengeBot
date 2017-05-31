# import
import discord
import sqlite3

# create blank profile
async def create_profile(member, conn, cur):
	t = (member.id,)
	cur.execute('SELECT * FROM profiles WHERE id=?', t)
	t = cur.fetchone()
	if (t == None):
		profile = (member.id, member.name + '#' + member.discriminator, 'Nothing to see here', 0)
		cur.execute('INSERT INTO profiles VALUES (?,?,?,?)', profile)
		conn.commit()
	t = (member.id,)
	cur.execute('SELECT * FROM ratelimits WHERE id=?', t)
	t = cur.fetchone()
	if (t == None):
		ratelimit = (member.id, member.name + '#' + member.discriminator, 0, 0)
		cur.execute('INSERT INTO ratelimits VALUES (?,?,?,?)', ratelimit)
		conn.commit()

# info cmds
async def cmds_profile(message, umsg, client, conn, cur):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	
	# create profile if not exist
	await create_profile(member, conn, cur)
	
	# profile
	if (args[0] == 'profile'):
		
		# show other person's profile
		if (len(args) == 2 and len(message.mentions) > 0):
			await create_profile(message.mentions[0])
			embed = discord.Embed(title=message.mentions[0].name + "'s profile", type='rich', description=data[2], colour=message.mentions[0].colour)
			if (message.mentions[0].avatar_url == ''):
				embed.set_thumbnail(url=message.mentions[0].default_avatar_url)
			else:
				embed.set_thumbnail(url=message.mentions[0].avatar_url)
			await client.send_message(channel, content=None, embed=embed)
				
		# profile commands
		elif (len(args) > 1):
		
			# load data
			t = (member.id,)
			cur.execute('SELECT * FROM profiles WHERE id=?', t)
			profile = cur.fetchone()
			data = list(profile)
			
			# description set
			if (args[1] == 'desc'):
				if (len(args) > 2):
					data[2] = umsg[13:]
					await client.send_message(channel, 'Description set to `' + data[2] + '`!')
				else:
					await client.send_message(channel, 'You need to enter a description!')
		
			# save profile
			t = (member.id,)
			profile = tuple(data)
			cur.execute('DELETE FROM profiles WHERE id=?', t)
			cur.execute('INSERT INTO profiles VALUES (?,?,?,?)', profile)
			conn.commit()
		
		# show profile
		else:
			embed = discord.Embed(title=member.name + "'s profile", type='rich', description=data[2], colour=member.colour)
			if (member.avatar_url == ''):
				embed.set_thumbnail(url=member.default_avatar_url)
			else:
				embed.set_thumbnail(url=member.avatar_url)
			await client.send_message(channel, content=None, embed=embed)
