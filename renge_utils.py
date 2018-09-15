# import
import discord
import sqlite3

# servers----------------------------------------------------------------------

# create blank server profile
async def create_server(server, conn, cur):
	
	# retrieve server
	t = (server.id,)
	cur.execute('SELECT * FROM servers WHERE id=?', t)
	t = cur.fetchone()
	
	# return if server found
	if (t != None):
		return
	
	# create server
	server = (server.id, None, None, None, None, None, None)
	cur.execute('INSERT INTO servers VALUES (?,?,?,?,?,?,?)', server)
	conn.commit()
		
# load server
async def load_server(server, conn, cur):
	await create_server(server, conn, cur)
	t = (server.id,)
	cur.execute('SELECT * FROM servers WHERE id=?', t)
	serverdata = cur.fetchone()
	data = list(serverdata)
	return data
	
# save server
async def save_server(data, conn, cur):
	t = (data[0],)
	server = tuple(data)
	cur.execute('DELETE FROM servers WHERE id=?', t)
	cur.execute('INSERT INTO servers VALUES (?,?,?,?,?,?,?)', server)
	conn.commit()

# profiles---------------------------------------------------------------------

# create blank profile
async def create_profile(member, conn, cur):
	
	# retrieve user
	t = (member.id,)
	cur.execute('SELECT * FROM profiles WHERE id=?', t)
	t = cur.fetchone()
	
	# return if user found
	if (t != None):
		return
		
	# create profile
	profile = (member.id, member.name + '#' + member.discriminator, 'Nothing to see here', 0, 0, None, None, None, None, None)
	cur.execute('INSERT INTO profiles VALUES (?,?,?,?,?,?,?,?,?,?)', profile)
	conn.commit()
	
	# retrieve ratelimit
	t = (member.id,)
	cur.execute('SELECT * FROM ratelimits WHERE id=?', t)
	t = cur.fetchone()
	
	# return if found
	if (t != None):
		return
	
	# create ratelimits
	ratelimit = (member.id, 0, 0, 0)
	cur.execute('INSERT INTO ratelimits VALUES (?,?,?,?)', ratelimit)
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
	cur.execute('INSERT INTO profiles VALUES (?,?,?,?,?,?,?,?,?,?)', profile)
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
	cur.execute('INSERT INTO ratelimits VALUES (?,?,?,?)', ratelimit)
	conn.commit()
	
# misc-------------------------------------------------------------------------
	
# check integer
def is_int(s):
	try:
		int(s)
		return True
	except:
		return False
		
# set size of string by adding spaces
def set_string_size(string, len1):
	len0 = len(string)
	if (len0 > len1):
		return string
	for a in range(len0, len1):
		string = string + " "
	return string
