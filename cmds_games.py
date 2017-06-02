# import
import discord
import random
import sqlite3
from cmds_profile import load_profile
from cmds_profile import save_profile

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
	
# check integer
def is_int(s):
	try:
		int(s)
		return True
	except:
		return False

# games
async def cmds_games(message, umsg, client, conn, cur):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	
	# create game if not exist
	await create_game(channel, conn, cur)
	
	# roulette
	if (args[0] == 'roulette'):
		
		# roulette commands
		if (len(args) > 1):
			
			# bet
			if (args[1] == 'bet'):
				
				# load game
				data = await load_game(channel, conn, cur)
				
				# check for full game/get position
				pos = 0
				for a in range(2, 14, 3):
					if (data[a] == None):
						pos = a
						
				# check already in game
				if (data[2] == member.id or data[5] == member.id or data[8] == member.id or data[11] == member.id):
					pos = -1
					
				# start bet
				if (pos > 0):
					
					# bet amount
					if (len(args) > 2):
						
						# check if integer
						if (is_int(args[2])):
							
							# check bet more than zero
							if (int(args[2]) > 0):
								
								#check bet within player's credits
								udata = await load_profile(member, conn, cur)
								if (int(args[2]) < udata[3]):
							
									# bet type
									if (len(args) > 3):
										
										# red/black/odd/even/low/high
										if (args[3] == 'red' or args[3] == 'black' or args[3] == 'odd' or args[3] == 'even' or args[3] == 'low' or args[3] == 'high'):
											data[pos] = member.id
											data[pos+1] = args[2]
											data[pos+2] = args[3]
											if (data[1] == 'None'):
												data[1] = 'Roulette'
												await client.send_message(channel, 'Started a new game of roulette!')
											await save_game(channel, data, conn, cur)
											await client.send_message(channel, member.name + ' has bet $' + data[pos+1] + ' on ' + data[pos+2] + '!')
											
										# columns/dozens
										elif (args[3] == 'column' or args[3] == 'dozen'):
											if (len(args) > 4):
												if (args[4] == '1' or args[4] == '2' or args[4] == '3'):
													data[pos] = member.id
													data[pos+1] = args[2]
													data[pos+2] = args[3] + ' ' + args[4]
													if (data[1] == 'None'):
														data[1] = 'Roulette'
														await client.send_message(channel, 'Started a new game of roulette!')
													await save_game(channel, data, conn, cur)
													await client.send_message(channel, member.name + ' has bet $' + data[pos+1] + ' on ' + data[pos+2] + '!')
												else:
													await client.send_message(channel, 'Invalid ' + args[3] + ' number!')
											else:
												await client.send_message(channel, 'You need to specify a ' + args[3] + ' number!')
											
										#invalid bet type
										else:
											await client.send_message(channel, 'Invalid bet type!')
									
									# no bet type
									else:
										await client.send_message(channel, 'You need to specify what to bet on!')
									
								# not enough credits
								else:
									await client.send_message(channel, 'You do not have enough credits to place this bet!')
									
							# bet less than 1
							else:
								await client.send_message(channel, 'You must bet more than zero!')
						
						# not integer bet
						else:
							await client.send_message(channel, 'Invalid bet amount!')
							
					#insufficient arguments
					else:
						await client.send_message(channel, 'You must specify an amount to bet!')
						
				# in game already
				elif (pos == -1):
					await client.send_message(channel, 'You are already in the game!')
						
				# game full
				else:
					await client.send_message(channel, 'The current game is already full!')
						
			# cancel bet
			elif (args[1] == 'cancel'):
				
				# load game
				data = await load_game(channel, conn, cur)
				
				# check active game
				if (data[1] == 'Roulette'):
					
					# check if user is in game
					t = False
					for a in range(2, 14, 3):
						if (member.id == data[a]):
							data[a] = None
							data[a+1] = 0
							data[a+2] = None
							t = True
							await client.send_message(channel, 'Successfully removed bet from the game!')
							if (data[2] == None and data[5] == None and data[8] == None and data[11] == None):
								data[1] = 'None'
								await client.send_message(channel, 'All players quit! Closing game...')
							await save_game(channel, data, conn, cur)
						
					# not in game
					if (t == False):
						await client.send_message(channel, 'You are not in the current game!')
					
				# no game active
				else:
					await client.send_message(channel, 'There are no roulette games currently active!')
					
			# spin it baby
			elif (args[1] == 'spin'):
				
				# load game
				data = await load_game(channel, conn, cur)
				
				# values
				nums_red = [2,  4,  6,  8,  10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
				nums_blk = [1,  3,  5,  7,  9,  12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
				nums_odd = [1,  3,  5,  7,  9,  11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
				nums_evn = [2,  4,  6,  8,  10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
				nums_low = [1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12, 13, 14, 15, 16, 17, 18]
				nums_hgh = [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
				nums_col1 = [1,  4,  7,  10, 13, 16, 19, 22, 25, 28, 31, 34]
				nums_col2 = [2,  5,  8,  11, 14, 17, 20, 23, 26, 29, 32, 35]
				nums_col3 = [3,  6,  9,  12, 15, 18, 21, 24, 27, 30, 33, 36]
				nums_doz1 = [1,  2,  3,  4,  5,  6,  7,  8,  9,  10, 11, 12]
				nums_doz2 = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
				nums_doz3 = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
				
				# check active game
				if (data[1] == 'Roulette'):
				
					# start message
					msg = ''
					
					# roll number
					roll = int(random.random() * 37)
					if (roll in nums_red):
						msg = msg + 'The ball has landed on Red ' + str(roll) + '!\n'
					elif (roll in nums_grn):
						msg = msg + 'The ball has landed on Black ' + str(roll) + '!\n'
					else:
						msg = msg + 'The ball has landed on 0!\n'
						
					# results
					for a in range(2, 14, 3):
						if (data[a] != None):
							
							# retrieve and display results
							user = await client.get_user_info(data[a])
							winnings = 0
							msg = msg + user.mention
							if (data[a+2] == 'red' and roll in nums_red):
								winnings = data[a+1]
							elif (data[a+2] == 'black' and roll in nums_blk):
								winnings = data[a+1]
							elif (data[a+2] == 'odd' and roll in nums_odd):
								winnings = data[a+1]
							elif (data[a+2] == 'even' and roll in nums_evn):
								winnings = data[a+1]
							elif (data[a+2] == 'low' and roll in nums_low):
								winnings = data[a+1]
							elif (data[a+2] == 'high' and roll in nums_hgh):
								winnings = data[a+1]
							elif (data[a+2] == 'column 1' and roll in nums_col1):
								winnings = data[a+1] * 2
							elif (data[a+2] == 'column 2' and roll in nums_col2):
								winnings = data[a+1] * 2
							elif (data[a+2] == 'column 3' and roll in nums_col3):
								winnings = data[a+1] * 2
							elif (data[a+2] == 'dozen 1' and roll in nums_doz1):
								winnings = data[a+1] * 2
							elif (data[a+2] == 'dozen 2' and roll in nums_doz2):
								winnings = data[a+1] * 2
							elif (data[a+2] == 'dozen 3' and roll in nums_doz3):
								winnings = data[a+1] * 2
							else:
								winnings = -data[a+1]
							if (winnings > 0):
								msg = msg + ' won $' + str(winnings) + '!\n'
							else:
								msg = msg + ' lost $' + str(data[a+1]) + '!\n'
								
							# update user
							udata = await load_profile(user, conn, cur)
							udata[3] = udata[3] + int(winnings)
							await save_profile(user, udata, conn, cur)
							
					# clear game & final results
					data = [channel.id, 'None', None, 0, None, None, 0, None, None, 0, None, None, 0, None]
					await save_game(channel, data, conn, cur)
					msg = msg + 'End of roulette game!'
					await client.send_message(channel, msg)
					
				# no game active
				else:
					await client.send_message(channel, 'There are no roulette games currently active!')
			
			# invalid input
			else:
				await client.send_message(channel, 'Invalid action!')
			
		# insufficient arguments
		else:
			await client.send_message(channel, 'You need to specify what you want to do!')
