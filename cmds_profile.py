# import
import discord
import time
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
		
# load profile
async def load_profile(member, conn, cur):
	t = (member.id,)
	cur.execute('SELECT * FROM profiles WHERE id=?', t)
	profile = cur.fetchone()
	data = list(profile)
	return data
	
# save profile
async def save_profile(member, data, conn, cur):
	t = (member.id,)
	profile = tuple(data)
	cur.execute('DELETE FROM profiles WHERE id=?', t)
	cur.execute('INSERT INTO profiles VALUES (?,?,?,?)', profile)
	conn.commit()
		
# load profile
async def load_ratelimit(member, conn, cur):
	t = (member.id,)
	cur.execute('SELECT * FROM ratelimits WHERE id=?', t)
	ratelimit = cur.fetchone()
	data = list(ratelimit)
	return data
	
# save profile
async def save_ratelimit(member, data, conn, cur):
	t = (member.id,)
	ratelimit = tuple(data)
	cur.execute('DELETE FROM ratelimits WHERE id=?', t)
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
		
			# load data
			await create_profile(message.mentions[0], conn, cur)
			data = await load_profile(message.mentions[0], conn, cur)
			
			# display data
			embed = discord.Embed(title=message.mentions[0].name + "'s profile", type='rich', description=data[2] + '\n\n**Credits**\n' + str(data[3]), colour=message.mentions[0].colour)
			if (message.mentions[0].avatar_url == ''):
				embed.set_thumbnail(url=message.mentions[0].default_avatar_url)
			else:
				embed.set_thumbnail(url=message.mentions[0].avatar_url)
			await client.send_message(channel, content=None, embed=embed)
				
		# profile commands
		elif (len(args) > 1):
			
			# load data
			data = await load_profile(member, conn, cur)
			
			# description set
			if (args[1] == 'desc'):
				if (len(args) > 2):
					data[2] = umsg[13:]
					await client.send_message(channel, 'Description set to `' + data[2] + '`!')
				else:
					await client.send_message(channel, 'You need to enter a description!')
		
			# save profile
			await save_profile(member, data, conn, cur)
		
		# show profile
		else:
			
			# load data
			data = await load_profile(member, conn, cur)
			
			# display data
			embed = discord.Embed(title=member.name + "'s profile", type='rich', description=data[2] + '\n\n**Credits**\n' + str(data[3]), colour=member.colour)
			if (member.avatar_url == ''):
				embed.set_thumbnail(url=member.default_avatar_url)
			else:
				embed.set_thumbnail(url=member.avatar_url)
			await client.send_message(channel, content=None, embed=embed)
			
	# daily
	if (args[0] == 'daily'):
		
		# check ratelimit
		rl = await load_ratelimit(member, conn, cur)
		t = int(time.time()) - rl[2]
		if (t > 86400):
		
			# add 100 credits to profile
			data = await load_profile(member, conn, cur)
			data[3] = data[3] + 100
			await save_profile(member, data, conn, cur)
			
			# update ratelimit
			rl[2] = int(time.time())
			await save_ratelimit(member, rl, conn, cur)
			await client.send_message('You have received your daily 100 credits!')
			
		# show time remaining
		else:
			msg = "Slow down! Your daily credits aren't ready yet!\nYou can get your next daily in "
			t = 86400 - t
			msg = msg + str(int(t/3600)) + ' hours, '
			t = t % 3600
			msg = msg + str(int(t/60)) + ' minutes, '
			t = t % 60
			msg = msg + str(t) + ' seconds'
			await client.send_message(channel, msg)
			
	# loot
	if (args[0] == 'loot'):
		
		# check ratelimit
		rl = await load_ratelimit(member, conn, cur)
		t = int(time.time()) - rl[3]
		if (t > 300):
		
			# get random credits and update profile
			loot = int(random.random() * 40) - 10
			if (loot > 0):
				data = await load_profile(member, conn, cur)
				data[3] = data[3] + loot
				await save_profile(member, data, conn, cur)
			
			# update ratelimit
			rl[3] = int(time.time())
			await save_ratelimit(member, rl, conn, cur)
			if (loot > 0):
				await client.send_message('You looted a whole ' + str(loot) + ' credits!')
			else:
				await client.send_message("You couldn't find anything to loot")
			
		# show time remaining
		else:
			msg = "Slow down! You just looted not that long ago!\nYou can loot again in "
			t = 300 - t
			msg = msg + str(int(t/60)) + ' minutes, '
			t = t % 60
			msg = msg + str(t) + ' seconds'
			await client.send_message(channel, msg)
