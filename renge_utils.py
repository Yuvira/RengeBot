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
		ratelimit = (member.id, 0, 0)
		cur.execute('INSERT INTO ratelimits VALUES (?,?,?)', ratelimit)
		conn.commit()
		
# load profile
async def load_profile(member, conn, cur):

	# given member
	try:
		t = (member.id,)
		await create_profile(member, conn, cur)
		cur.execute('SELECT * FROM profiles WHERE id=?', t)
		profile = cur.fetchone()
		data = list(profile)
		data[1] = member.name + '#' + member.discriminator
		return data
		
	# given id
	except:
		t = (member,)
		cur.execute('SELECT * FROM profiles WHERE id=?', t)
		profile = cur.fetchone()
		data = list(profile)
		return data
	
# save profile
async def save_profile(data, conn, cur):
	t = (data[0],)
	profile = tuple(data)
	cur.execute('DELETE FROM profiles WHERE id=?', t)
	cur.execute('INSERT INTO profiles VALUES (?,?,?,?)', profile)
	conn.commit()
		
# load ratelimit
async def load_ratelimit(member, conn, cur):
	await create_profile(member, conn, cur)
	t = (member.id,)
	cur.execute('SELECT * FROM ratelimits WHERE id=?', t)
	ratelimit = cur.fetchone()
	data = list(ratelimit)
	return data
	
# save ratelimit
async def save_ratelimit(data, conn, cur):
	t = (data[0],)
	ratelimit = tuple(data)
	cur.execute('DELETE FROM ratelimits WHERE id=?', t)
	cur.execute('INSERT INTO ratelimits VALUES (?,?,?)', ratelimit)
	conn.commit()
	
# games------------------------------------------------------------------------

# create blank game profile
async def create_game(id, conn, cur):
	t = (id,)
	cur.execute('SELECT * FROM games WHERE channel=?', t)
	t = cur.fetchone()
	if (t == None):
		game = (id, 'None', None, 0, None, None, 0, None, None, 0, None, None, 0, None)
		cur.execute('INSERT INTO games VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', game)
		conn.commit()
	
# load game
async def load_game(id, conn, cur):
	await create_game(id, conn, cur)
	t = (id,)
	cur.execute('SELECT * FROM games WHERE channel=?', t)
	game = cur.fetchone()
	data = list(game)
	return data
	
# save game
async def save_game(data, conn, cur):
	t = (data[0],)
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
