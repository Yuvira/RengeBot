# import
import discord
import random
import sqlite3
from renge_utils import load_profile
from renge_utils import save_profile
from renge_utils import is_int

# games
async def cmds_games(message, umsg, client, conn, cur):
	
	# args/variables
	args = umsg.split(' ')
	channel = message.channel
	member = message.author
	
	# roulette-----------------------------------------------------------------
	if (args[0] == 'roulette'):
		
		# variables
		bet_amount = 0
		bet_type = 'none'
		msg = ''
		
		# bet amount
		if (len(args) > 1):
			
			# check if integer
			if (is_int(args[1])):
				
				# check bet more than zero
				if (int(args[1]) > 0):
					
					# check bet within player's credits
					udata = await load_profile(member, conn, cur)
					if (int(args[1]) <= udata[3]):
						
						# bet type
						if (len(args) > 2):
							
							# red/black/odd/even/low/high
							if (args[2] == 'red' or args[2] == 'black' or args[2] == 'odd' or args[2] == 'even' or args[2] == 'low' or args[2] == 'high'):
								bet_amount = int(args[1])
								bet_type = args[2]
								msg = 'You bet $' + str(bet_amount) + ' on ' + bet_type + '!\n'
								
							# columns/dozens
							elif (args[2] == 'column' or args[2] == 'dozen'):
								if (len(args) > 3):
									if (args[3] == '1' or args[3] == '2' or args[3] == '3'):
										bet_amount = int(args[1])
										bet_type = args[2] + ' ' + args[3]
										msg = 'You bet $' + str(bet_amount) + ' on ' + bet_type + '!\n'
									else:
										await client.send_message(channel, 'Invalid ' + args[2] + ' number!')
								else:
									await client.send_message(channel, 'You need to specify a ' + args[2] + ' number!')
								
							# invalid bet type
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
				msg = msg + 'The ball landed on Red ' + str(roll) + '!\n'
			elif (roll in nums_blk):
				msg = msg + 'The ball landed on Black ' + str(roll) + '!\n'
			else:
				msg = msg + 'The ball landed on 0!\n'
					
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
	
	# slots--------------------------------------------------------------------
	# based somewhat heavily on Pokémon RBY slot mechanics
	elif (args[0] == 'slots'):
		
		# variables
		bet_amount = 0
		mode = 0
		mode_override = 0
		msg = ''
		
		# bet amount
		if (len(args) > 1):
			
			# check if integer
			if (is_int(args[1])):
				
				# check bet more than zero
				if (int(args[1]) > 0):
					
					# check bet within player's credits
					udata = await load_profile(member, conn, cur)
					if (int(args[1]) <= udata[3]):
						bet_amount = int(args[1])
						msg = 'You bet $' + str(bet_amount) + '\n'
						
						# get mode override if owner
						if (len(args) > 3 and member.id == '188663897279037440'):
							if (args[2] == 'mode'):
								if (args[3] == '0'):
									mode_override = 1
								elif (args[3] == '1'):
									mode_override = 2
								elif (args[3] == '2'):
									mode_override = 3
						
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
			
			# generate wheels
			s = [':cherries:', ':rice_ball:', ':butterfly:', ':cherry_blossom:', ':dollar:', ':gem:']
			wheel1 = [s[5], s[1], s[2], s[5], s[0], s[4], s[3], s[2], s[5], s[0], s[4], s[3], s[1], s[5], s[0], s[4], s[1], s[2], s[5]]
			wheel2 = [s[5], s[0], s[1], s[5], s[2], s[0], s[3], s[1], s[4], s[0], s[3], s[1], s[0], s[4], s[2], s[3], s[0], s[1], s[5]]
			wheel3 = [s[5], s[1], s[3], s[5], s[4], s[3], s[2], s[0], s[1], s[3], s[2], s[0], s[1], s[3], s[2], s[0], s[1], s[3], s[5]]
			wheel1 = wheel1 + wheel1[1:]
			wheel2 = wheel2 + wheel2[1:]
			wheel3 = wheel3 + wheel3[1:]
			
			# decide mode
			t = int(random.random() * 30)
			if (t == 0):
				mode = 2 # "super" mode, tries to guarantee high payout
			elif (t < 11):
				mode = 1 # "good" mode, tries to guarantee low payout
			else:
				mode = 0 # "bad" mode, guarantees no payout
			
			# override
			if (mode_override > 0):
				mode = mode_override-1
			
			# first spin (advance up to five times on "super" to get high payout)
			spin1 = int(random.random() * 18) + 1
			for a in range(0,5):
				if (mode == 2):
					if (wheel1[spin1] == s[4] or wheel1[spin1] == s[5]):
						break
					else:
						spin1 += 1
			
			# second spin (advance up to five times on "super" to match high payout, advance until any match on "good")
			spin2 = int(random.random() * 18) + 1
			for a in range(0,17):
				if (mode == 2 and a < 5):
					if (wheel1[spin1] == s[4] and wheel2[spin2] == s[4]):
						break
					elif (wheel1[spin1] == s[5] and wheel2[spin2] == s[5]):
						break
					else:
						spin2 += 1
				elif (mode == 1):
					if (wheel1[spin1] == s[0] and wheel2[spin2] == s[0]):
						break
					elif (wheel1[spin1] == s[1] and wheel2[spin2] == s[1]):
						break
					elif (wheel1[spin1] == s[2] and wheel2[spin2] == s[2]):
						break
					elif (wheel1[spin1] == s[3] and wheel2[spin2] == s[3]):
						break
					else:
						spin2 += 1
			
			# third spin (advance up to five times for any match on "good" or "super", advance past high payout on "good", avoid any match on "bad")
			spin3 = int(random.random() * 18) + 1
			for a in range(0,17):
				if (mode == 2 and a < 5):
					if (wheel2[spin2] == wheel3[spin3]):
						break
					else:
						spin3 += 1
				elif (mode == 1):
					if (wheel3[spin3] == s[4] or wheel3[spin3] == s[5]):
						spin3 += 1
					elif (a < 5):
						if (wheel2[spin2] == wheel3[spin3]):
							break
						else:
							spin3 += 1
				elif (mode == 0):
					if (wheel2[spin2] != wheel3[spin3]):
						break
					else:
						spin3 += 1
			
			# generate slot display
			msg = msg + wheel1[spin1+1] + ' | ' + wheel2[spin2+1] + ' | ' + wheel3[spin3+1] + '\n'
			msg = msg + wheel1[spin1] + ' | ' + wheel2[spin2] + ' | ' + wheel3[spin3] + '\n'
			msg = msg + wheel1[spin1-1] + ' | ' + wheel2[spin2-1] + ' | ' + wheel3[spin3-1] + '\n'
						
			# retrieve and display results
			winnings = 0
			if (wheel1[spin1] == wheel2[spin2] and wheel2[spin2] == wheel3[spin3]):
				if (wheel1[spin1] == s[0]):
					winnings = bet_amount * 2
				elif (wheel1[spin1] == s[1]):
					winnings = bet_amount * 3
				elif (wheel1[spin1] == s[2]):
					winnings = bet_amount * 5
				elif (wheel1[spin1] == s[3]):
					winnings = bet_amount * 10
				elif (wheel1[spin1] == s[4]):
					winnings = bet_amount * 25
				elif (wheel1[spin1] == s[5]):
					winnings = bet_amount * 50
			else:
				winnings = -bet_amount
			if (winnings > 0):
				if (wheel1[spin1] == s[4] or wheel1[spin1] == s[5]):
					msg = msg + 'Jackpot! You won $' + str(winnings) + '!'
				else:
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
