# import
import discord
import random
import sqlite3
from renge_utils import load_profile
from renge_utils import save_profile
from renge_utils import create_game
from renge_utils import load_game
from renge_utils import save_game
from renge_utils import is_int

# games
async def cmds_games(message, umsg, client, conn, cur):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	
	# roulette
	if (args[0] == 'roulette'):
		
		# roulette commands
		if (len(args) > 1):
			
			# bet
			if (args[1] == 'bet'):
				
				# load game
				data = await load_game(channel.id, conn, cur)
				
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
								if (int(args[2]) <= udata[3]):
							
									# bet type
									if (len(args) > 3):
										
										# red/black/odd/even/low/high
										if (args[3] == 'red' or args[3] == 'black' or args[3] == 'odd' or args[3] == 'even' or args[3] == 'low' or args[3] == 'high'):
											data[pos] = member.id
											data[pos+1] = args[2]
											data[pos+2] = args[3]
											udata[3] -= int(args[2])
											await save_profile(udata, conn, cur)
											if (data[1] == 'None'):
												data[1] = 'Roulette'
												await client.send_message(channel, 'Started a new game of roulette!')
											await save_game(data, conn, cur)
											await client.send_message(channel, member.name + ' has bet $' + data[pos+1] + ' on ' + data[pos+2] + '!')
											
										# columns/dozens
										elif (args[3] == 'column' or args[3] == 'dozen'):
											if (len(args) > 4):
												if (args[4] == '1' or args[4] == '2' or args[4] == '3'):
													data[pos] = member.id
													data[pos+1] = args[2]
													data[pos+2] = args[3] + ' ' + args[4]
													udata[3] -= int(args[2])
													await save_profile(udata, conn, cur)
													if (data[1] == 'None'):
														data[1] = 'Roulette'
														await client.send_message(channel, 'Started a new game of roulette!')
													await save_game(data, conn, cur)
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
				data = await load_game(channel.id, conn, cur)
				
				# check active game
				if (data[1] == 'Roulette'):
					
					# check if user is in game
					t = False
					for a in range(2, 14, 3):
						if (member.id == data[a]):
							udata = await load_profile(member, conn, cur)
							udata[3] += data[a+1]
							await save_profile(udata, conn, cur)
							data[a] = None
							data[a+1] = 0
							data[a+2] = None
							t = True
							await client.send_message(channel, 'Successfully removed bet from the game!')
							if (data[2] == None and data[5] == None and data[8] == None and data[11] == None):
								data[1] = 'None'
								await client.send_message(channel, 'All players quit! Closing game...')
							await save_game(data, conn, cur)
						
					# not in game
					if (t == False):
						await client.send_message(channel, 'You are not in the current game!')
					
				# no game active
				else:
					await client.send_message(channel, 'There are no roulette games currently active!')
					
			# spin it baby
			elif (args[1] == 'spin'):
				
				# load game
				data = await load_game(channel.id, conn, cur)
				
				# clear game to prevent double-spin
				clear = [channel.id, 'None', None, 0, None, None, 0, None, None, 0, None, None, 0, None]
				await save_game(clear, conn, cur)
				
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
					elif (roll in nums_blk):
						msg = msg + 'The ball has landed on Black ' + str(roll) + '!\n'
					else:
						msg = msg + 'The ball has landed on 0!\n'
						
					# results
					for a in range(2, 14, 3):
						if (data[a] != None):
							
							# retrieve and display results
							winnings = 0
							msg = msg + '<@' + data[a] + '>'
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
							udata = await load_profile(data[a], conn, cur)
							udata[3] += data[a+1]
							udata[3] += int(winnings)
							if (udata[3] > 9200000000000000000):
								udata[3] = 9200000000000000000
								await client.send_message(channel, ":tada: Good job, somebody reached the credit limit. Hope you're proud of yourself")
							await save_profile(udata, conn, cur)
							
					# final results
					msg = msg + 'End of roulette game!'
					await client.send_message(channel, msg)
					
				# no game active
				else:
					await client.send_message(channel, 'There are no roulette games currently active!')
			
			# quick roulette
			elif (args[1] == 'quick'):
			
				# variables
				bet_amount = 0
				bet_type = 'none'
				msg = ''
				
				# bet amount
				if (len(args) > 2):
					
					# check if integer
					if (is_int(args[2])):
						
						# check bet more than zero
						if (int(args[2]) > 0):
							
							#check bet within player's credits
							udata = await load_profile(member, conn, cur)
							if (int(args[2]) <= udata[3]):
						
								# bet type
								if (len(args) > 3):
									
									# red/black/odd/even/low/high
									if (args[3] == 'red' or args[3] == 'black' or args[3] == 'odd' or args[3] == 'even' or args[3] == 'low' or args[3] == 'high'):
										bet_amount = int(args[2])
										bet_type = args[3]
										msg = 'You bet $' + str(bet_amount) + ' on ' + bet_type + '!\n'
										
									# columns/dozens
									elif (args[3] == 'column' or args[3] == 'dozen'):
										if (len(args) > 4):
											if (args[4] == '1' or args[4] == '2' or args[4] == '3'):
												bet_amount = int(args[2])
												bet_type = args[3] + ' ' + args[4]
												msg = 'You bet $' + str(bet_amount) + ' on ' + bet_type + '!\n'
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
						
				# insufficient arguments
				else:
					await client.send_message(channel, 'You must specify an amount to bet!')
					
				# check message exists
				if not (msg == ''):
				
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
					
					# roll number
					roll = int(random.random() * 37)
					if (roll in nums_red):
						msg = msg + 'The ball has landed on Red ' + str(roll) + '!\n'
					elif (roll in nums_blk):
						msg = msg + 'The ball has landed on Black ' + str(roll) + '!\n'
					else:
						msg = msg + 'The ball has landed on 0!\n'
							
					# retrieve and display results
					winnings = 0
					if (bet_type == 'red' and roll in nums_red):
						winnings = bet_amount
					elif (bet_type == 'black' and roll in nums_blk):
						winnings = bet_amount
					elif (bet_type == 'odd' and roll in nums_odd):
						winnings = bet_amount
					elif (bet_type == 'even' and roll in nums_evn):
						winnings = bet_amount
					elif (bet_type == 'low' and roll in nums_low):
						winnings = bet_amount
					elif (bet_type == 'high' and roll in nums_hgh):
						winnings = bet_amount
					elif (bet_type == 'column 1' and roll in nums_col1):
						winnings = bet_amount * 2
					elif (bet_type == 'column 2' and roll in nums_col2):
						winnings = bet_amount * 2
					elif (bet_type == 'column 3' and roll in nums_col3):
						winnings = bet_amount * 2
					elif (bet_type == 'dozen 1' and roll in nums_doz1):
						winnings = bet_amount * 2
					elif (bet_type == 'dozen 2' and roll in nums_doz2):
						winnings = bet_amount * 2
					elif (bet_type == 'dozen 3' and roll in nums_doz3):
						winnings = bet_amount * 2
					else:
						winnings = -bet_amount
					if (winnings > 0):
						msg = msg + 'You won $' + str(winnings) + '!'
					else:
						msg = msg + 'You lost $' + str(bet_amount) + '!'
						
					# update user
					udata = await load_profile(member.id, conn, cur)
					udata[3] += int(winnings)
					if (udata[3] > 9200000000000000000):
						udata[3] = 9200000000000000000
						await client.send_message(channel, ":tada: Good job, you reached the credit limit. Hope you're proud of yourself")
					await save_profile(udata, conn, cur)
							
					# send results
					await client.send_message(channel, msg)
			
			# invalid input
			else:
				await client.send_message(channel, 'Invalid action!')
			
		# insufficient arguments
		else:
			await client.send_message(channel, 'You need to specify what you want to do!')
	
	# slots (thanks Desii)
	elif (args[0] == 'slots'):
		
		# credits
		data = await load_profile(member, conn, cur)
		if (data[3] >= 50):
		
			# vars for slot values
			var1 = int(random.random() * 5)
			var2 = int(random.random() * 5)
			var3 = int(random.random() * 5)
			var4 = int(random.random() * 5)
			var5 = int(random.random() * 5)
			var6 = int(random.random() * 5)
			var7 = int(random.random() * 5)
			var8 = int(random.random() * 5)
			var9 = int(random.random() * 5)
			
			# emotes
			col = [":moneybag:", ":cherries:", ":carrot:", ":popcorn:", ":seven:"]
			
			# win
			if var6 == var5 and var5 == var4 and var4 == var6:
				msg = "**You won 150 credits!**"
				data[3] = data[3] + 150
				if (data[3] > 9200000000000000000):
					data[3] = 9200000000000000000
					await client.send_message(channel, ':tada: Good job, ' + member.name + ", you reached the credit limit. Hope you're proud of yourself")
				await save_profile(data, conn, cur)
			
			# lose
			else:
				msg = "**You lost 50 credits!**"
				data = await load_profile(member, conn, cur)
				data[3] = data[3] - 50
				await save_profile(data, conn, cur)
			
			# show result and board
			await client.send_message(channel, msg + "\n" + str(col[var1]) + str(col[var2]) + str(col[var3]) + "\n" + str(col[var4]) + str(col[var5]) + str(col[var6]) + "\n" + str(col[var7]) + str(col[var8]) + str(col[var9]))
		
		# insufficient credits
		else:
			await client.send_message(channel, "You don't have enough credits!")
