# import
import discord
import sqlite3

# profiles---------------------------------------------------------------------

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
		
# load ratelimit
async def load_ratelimit(member, conn, cur):
	t = (member.id,)
	cur.execute('SELECT * FROM ratelimits WHERE id=?', t)
	ratelimit = cur.fetchone()
	data = list(ratelimit)
	return data
	
# save ratelimit
async def save_ratelimit(member, data, conn, cur):
	t = (member.id,)
	ratelimit = tuple(data)
	cur.execute('DELETE FROM ratelimits WHERE id=?', t)
	cur.execute('INSERT INTO ratelimits VALUES (?,?,?,?)', ratelimit)
	conn.commit()
	
# games------------------------------------------------------------------------

# create blank game profile
async def create_game(channel, conn, cur):
	t = (channel.id,)
	cur.execute('SELECT * FROM games WHERE channel=?', t)
	t = cur.fetchone()
	if (t == None):
		game = (channel.id, 'None', None, 0, None, None, 0, None, None, 0, None, None, 0, None)
		cur.execute('INSERT INTO games VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', game)
		conn.commit()
	
# load game
async def load_game(channel, conn, cur):
	t = (channel.id,)
	cur.execute('SELECT * FROM games WHERE channel=?', t)
	game = cur.fetchone()
	data = list(game)
	return data
	
# save game
async def save_game(channel, data, conn, cur):
	t = (channel.id,)
	game = tuple(data)
	cur.execute('DELETE FROM games WHERE channel=?', t)
	cur.execute('INSERT INTO games VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', game)
	conn.commit()
	
# misc-------------------------------------------------------------------------
	
# check integer
def is_int(s):
	try:
		int(s)
		return True
	except:
		return False
