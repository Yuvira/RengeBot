# import
import discord
import sqlite3
from games_roulette import games_roulette

# create blank game profile
async def create_game(channel, conn, cur):
	t = (channel.id,)
	cur.execute('SELECT * FROM profiles WHERE channel=?', t)
	t = cur.fetchone()
	if (t == None):
		game = (channel.id, 'None', None, 0, None, None, 0, None, None, 0, None, None, 0, None)
		cur.execute('INSERT INTO profiles VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', game)
		conn.commit()

# game redirects
async def cmds_games(message, umsg, client, conn, cur):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	
	# create profile if not exist
	await create_game(channel, conn, cur)
	
	# roulette
	if (args[0] == 'roulette'):
		await games_roulette(message, umsg, client, conn, cur)
