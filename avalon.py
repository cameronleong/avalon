# The Resistance: Avalon - github.com/cameronleong - 16/07/16 #
import discord
import random
import linecache
import re
import shelve
import copy
from random import shuffle, randint
from text import *
from datetime import datetime


async def avalon(client, message):			#main loop
	#Declarations
	playerlist = [] 				#list of players in the game
	rules = [] 					#number of players for each quest.
	roles = {} 					#active roles based on the # of players. it can be changed.
	canreject = []
	cantreject = []
	gamestate = [0,0,1,5,0,0,1] 
	gamestate[0] = 0
	boardstate = [":red_circle:",":red_circle:",":red_circle:",":red_circle:",":red_circle:"]
	
	if gamestate[0] == 0: await login(client,message,playerlist,gamestate,rules,roles)
	if gamestate[0] == 2: await night(client,message,playerlist,gamestate,rules,roles,canreject,cantreject)
	#gamestate[1] = randint(0,len(playerlist)-1)	#leadercounter
	#gamestate[2] = 1				#questcounter
	#gamestate[3] = 5				#passcounter
	#gamestate[4] = 0 				#successcount
	#gamestate[5] = 0 				#failcount #failcounter is 6
	names = []
	while gamestate[0] == 3 or gamestate[0] == 4 or gamestate[0] == 5:
		if gamestate[0] == 3: await quest(client,message,playerlist,gamestate,rules,roles,boardstate,names)
		if gamestate[0] == 4: await teamvote(client,message,playerlist,gamestate,rules,roles,boardstate,names)
		if gamestate[0] == 5: await privatevote(client,message,playerlist,gamestate,rules,roles,boardstate,names,canreject)
	if gamestate[0] == 6: await gameover(client,message,playerlist,gamestate,rules,roles,boardstate,names,canreject,cantreject)
	
async def login(client,message,playerlist,gamestate,rules,roles):	
	#Login Phase
	gamestate[0] = 1
	await client.send_message(message.channel, loginStr)
	while gamestate[0] == 1:
		reply = await client.wait_for_message(channel=message.channel)
		if reply.content == "!join" and len(playerlist) <= 10:
			if reply.author not in playerlist:
				await client.send_message(message.channel, joinStr.format(reply.author.mention))
				playerlist.append(reply.author)
				if len(playerlist) == 5:
					await client.send_message(message.channel, fiveStr.format(reply.author.mention))
				"""
				## TEST DATA ##
				bot1 = copy.deepcopy(reply.author)
				bot1.name = "Bot 1"
				playerlist.append(bot1)
				
				bot2 = copy.deepcopy(reply.author)
				bot2.name = "Bot 2"
				playerlist.append(bot2)
				
				bot3 = copy.deepcopy(reply.author)
				bot3.name = "Bot 3"
				playerlist.append(bot3)
				
				bot4 = copy.deepcopy(reply.author)
				bot4.name = "Bot 4"
				playerlist.append(bot4)
				
				bot5 = copy.deepcopy(reply.author)
				bot5.name = "Bot 5"
				playerlist.append(bot5)
				
				bot6 = copy.deepcopy(reply.author)
				bot6.name = "Bot 6"
				playerlist.append(bot6)
				
				bot7 = copy.deepcopy(reply.author)
				bot7.name = "Bot 7"
				playerlist.append(bot7)
				
				bot8 = copy.deepcopy(reply.author)
				bot8.name = "Bot 8"
				playerlist.append(bot8)
				
				bot9 = copy.deepcopy(reply.author)
				bot9.name = "Bot 9"
				playerlist.append(bot9)"""
				
			else:
				await client.send_message(message.channel, alreadyJoinedStr.format(reply.author.mention))
		if reply.content == "!join" and len(playerlist) > 10:
			await client.send_message(message.channel, gameFullStr)
		if reply.content == "!start" and len(playerlist) < 5:
			## TEST DATA ##
			#bot1 = copy.deepcopy(reply.author)
			#bot1.name = "Bot 1"
			#playerlist.append(bot1)
			await client.send_message(message.channel, notEnoughPlayers)
		if reply.content == "!start" and len(playerlist) >= 5:
			await loadrules(client,message,rules,roles,playerlist,len(playerlist))
			random.seed(datetime.now())
			gamestate[1] = randint(0,len(playerlist)-1)	#leadercounter
			gamestate[0] = 2
		if reply.content == "!stop":
			await client.send_message(message.channel, stopStr)
			gamestate[0] = 0

async def night(client,message,playerlist,gamestate,rules,roles,canreject,cantreject):
	await client.send_message(message.channel, nightStr)
	shuffledlist = copy.deepcopy(playerlist)		#these are the things we need
	shuffle(shuffledlist)
	evillist = []
	merlinlist = []
	percivallist = []
	for key in roles:					#populate the lists
		roles[key] = shuffledlist.pop()
	for key in roles:
		if key == "Agravain, Minion of Mordred" or key == "The Assassin" or key == "Mordred" or key == "Morgana":
			evillist.append(roles[key])	
	for key in roles:
		if key == "Agravain, Minion of Mordred" or key == "The Assassin" or key == "Morgana":
			merlinlist.append(roles[key])			
	for key in roles:
		if key == "Merlin" or key == "Morgana":
			percivallist.append(roles[key])
	
	shuffle(evillist)
	shuffle(merlinlist)
	shuffle(percivallist)
	
	def toString(list1):
		string1 = ""
		for x in list1:
			string1 += ":black_small_square: "+x.name+"\n"
		return string1

	for key in roles:
		#print(str(roles[key].name)+" is "+str(key))	#Cheat code to reveal all roles for debugging purposes
		if key == "Galahad, Loyal Servant of Arthur" or key == "Tristan, Loyal Servant of Arthur" or key == "Guinevere, Loyal Servant of Arthur" or key == "Lamorak, Loyal Servant of Arthur":
			cantreject.append(roles[key])
			await client.send_message(roles[key],loyalDM.format(roles[key].name,key))	
		if key == "Agravain, Minion of Mordred":
			canreject.append(roles[key])
			await client.send_message(roles[key],minionDM.format(roles[key].name,key,toString(evillist)))
		if key == "Merlin":
			cantreject.append(roles[key])
			await client.send_message(roles[key],merlinDM.format(roles[key].name,key,toString(merlinlist)))
		if key == "The Assassin":
			canreject.append(roles[key])
			await client.send_message(roles[key],assassinDM.format(roles[key].name,key,toString(evillist)))
		if key == "Mordred":
			canreject.append(roles[key])
			await client.send_message(roles[key],mordredDM.format(roles[key].name,key,toString(evillist)))
		if key == "Morgana":
			canreject.append(roles[key])
			await client.send_message(roles[key],morganaDM.format(roles[key].name,key,toString(evillist)))
		if key == "Percival":
			cantreject.append(roles[key])
			await client.send_message(roles[key],percivalDM.format(roles[key].name,key,toString(percivallist)))
	await client.send_message(message.channel, night2Str)
	gamestate[0] = 3

async def quest(client,message,playerlist,gamestate,rules,roles,boardstate,names):
				
	if len(playerlist) >= 7 and gamestate[2] == 4:
		gamestate[6] = 2
	else:
		gamestate[6] = 1
		
	playersnamestring = "|"
	for x in playerlist:
		playersnamestring += "` "+x.name+" `|"
	boardstatestring = ""
	for x in boardstate:
		boardstatestring += x+" "
		
	await client.send_message(message.channel, teamStr.format(playersnamestring,playerlist[gamestate[1]].mention,gamestate[2],rules[gamestate[2]-1],gamestate[6],boardstatestring,rules[gamestate[2]-1]))
	mentionstring = ""
	for x in playerlist:
		mentionstring += x.mention+" "
	while gamestate[0] == 3:
		votetrigger = await client.wait_for_message(channel=message.channel)
		if votetrigger.content.startswith("!party") and votetrigger.author == playerlist[gamestate[1]]:
			await client.send_message(message.channel, partyStr)
			templist = votetrigger.content.split()
			#print(templist)
			names.clear()
			k = len(templist)
			for j in range(0,k):
				names.append(templist.pop())
			valid = 1
			for name in names:
				if name not in mentionstring and name != "!party":
					await client.send_message(message.channel,playernotingame.format(name))
					valid = 0
					break
			#print(names)
			
			if valid == 1:
				if len(names) == len(set(names)):
					if len(names)-1 == rules[(gamestate[2]-1)]:
						await client.send_message(message.channel,"Valid request submitted.")
						gamestate[0] = 4
					else:
						await client.send_message(message.channel,malformedStr.format(rules[gamestate[2]-1]))
				else:
					await client.send_message(message.channel,duplicateStr.format(rules[gamestate[2]-1]))
				#gamestate[0] = 4 #cheatcode
		if votetrigger.content.startswith("!stop"):
			await client.send_message(message.channel,stopStr)
			gamestate[0] = 0
		
async def teamvote(client,message,playerlist,gamestate,rules,roles,boardstate,names):
	await client.send_message(message.channel, teamvoteStr.format(gamestate[3]))
	def votecheck(msg):
		if msg.channel.is_private:
			if msg.author in templist:
				if msg.content == "!approve" or msg.content == "!reject":
					templist.remove(msg.author)
					return True
		elif msg.content.startswith('!stop'):
			return True
		return False
		
	while gamestate[0] == 4:
		#wait for votes
		stop = False
		vc=0
		rejectcounter=0
		voteStr="\n**Team Vote Results**:\n"
		templist = copy.deepcopy(playerlist)
		for player in templist:
			if player == playerlist[gamestate[1]]:
				templist.remove(player)
		for j in range(0,len(playerlist)-1):
			vc += 1
			pmtrigger = await client.wait_for_message(check=votecheck)
			if pmtrigger.content == "!approve":
				voteStr += ":black_small_square: "+pmtrigger.author.name+" voted **approve**.\n"
			elif pmtrigger.content == "!reject":
				voteStr += ":black_small_square: "+pmtrigger.author.name+" voted **reject**.\n"
				rejectcounter += 1
			if pmtrigger.content == "!stop":
				stop = True
				break
			await client.send_message(message.channel,pmtrigger.author.mention+" has submitted their vote ("+str(vc)+"/"+str(len(playerlist)-1)+")")
		
		if stop == True:
			await client.send_message(message.channel, stopStr)
			gamestate[0] = 0
			break
		
		#votes have been submitted	
		if gamestate[1] == (len(playerlist)-1):
			gamestate[1] = 0
		else:
			gamestate[1] += 1
		
		if rejectcounter >= (len(playerlist) / 2):			
			gamestate[3] -= 1
			if gamestate[3] == 0:
				voteStr += "\nThe team has been **rejected**. **Evil has won!**"
				await client.send_message(message.channel,voteStr)
				gamestate[0] = 6 #evil win state
			else:
				voteStr += "\nThe team has been **rejected**. Moving leader to the next player..."
				await client.send_message(message.channel,voteStr)
				gamestate[0] = 3
		else:
			gamestate[3] = 5 #reset passcount
			voteStr += "\nThe team has been **approved**. Entering private vote phase."
			await client.send_message(message.channel,voteStr)
			gamestate[0] = 5

async def privatevote(client,message,playerlist,gamestate,rules,roles,boardstate,names,canreject):
	while gamestate[0] == 5:
		def privatevotecheck(msg):
			if msg.channel.is_private:
				if msg.author in activeplayers and msg.author in canreject:
					if msg.content == "!success" or msg.content == "!fail":
						activeplayers.remove(msg.author)
						return True
				elif msg.author in activeplayers:
					if msg.content == "!success":
						activeplayers.remove(msg.author)
						return True
			elif msg.content.startswith('!stop'):
				return True
			return False
		stop = False
		fails = 0
		activeplayers = []
		namestring = ""
		
		for x in names:
			namestring += x+" "
		for player in playerlist:
			if player.mention in namestring:
				activeplayers.append(player)
		
		await client.send_message(message.channel,privatevoteStr.format(namestring))

		votecount = len(activeplayers)
		for j in range(0,votecount):
			pmtrigger = await client.wait_for_message(check=privatevotecheck)
			if pmtrigger.content == "!success":		
				pass
			elif pmtrigger.content == "!fail":
				fails += 1
			if pmtrigger.content == "!stop":
				stop = True
				break
			await client.send_message(message.channel,str(pmtrigger.author.name)+" has completed their task.")
		if stop == True:
			await client.send_message(message.channel, stopStr)
			gamestate[0] = 0
			break
		
		if fails >= (gamestate[6]):
			gamestate[5] += 1
			boardstate[gamestate[2]-1] = ":no_entry_sign:"
			await client.send_message(message.channel,"\nQuest **failed**. `"+str(fails)+"` adventurer(s) failed to complete their task.\n")
		else:
			gamestate[4] += 1
			boardstate[gamestate[2]-1] = ":o:"
			await client.send_message(message.channel,"\nQuest **succeeded**. `"+str(fails)+"` adventurer(s) failed to complete their task.\n")

		gamestate[2] += 1
		
		if gamestate[4] == 3 or gamestate[5] == 3:
			gamestate[0] = 6
		else:
			gamestate[0] = 3

async def gameover(client,message,playerlist,gamestate,rules,roles,boardstate,names,canreject,cantreject):
	def assassincheck(msg):
			if msg.content.startswith('!assassinate') and msg.author == roles["The Assassin"]:
				return True
			elif msg.content.startswith('!stop'):
				return True
			return False
	await client.send_message(message.channel,gameoverStr)
	if gamestate[4] == 3:
		await client.send_message(message.channel,"Three quests have been completed successfully.\n\nThe assassin may now `!assassinate` someone. You only have ONE chance to get the name and formatting correct. Make sure you tag the correct target with @!")
		ass = await client.wait_for_message(channel=message.channel,check=assassincheck)
		if ass.content.startswith('!assassinate'):
			asslist = ass.content.split()
			if roles["Merlin"].mention == asslist[-1]:
				await client.send_message(message.channel,"Merlin has been assassinated!\n\n")
				await client.send_message(message.channel,":smiling_imp: **Evil** Wins :smiling_imp:")
				for player in canreject:
					await addscore(client,message,player)
			else:
				await client.send_message(message.channel,"GOT THE WRONG GUY SON\n\n")
				await client.send_message(message.channel,":angel: **Good** Wins :angel: ")
				for player in cantreject:
					await addscore(client,message,player)
			
	elif gamestate[5] == 3:
		await client.send_message(message.channel,":smiling_imp: **Evil** Wins :smiling_imp: ")
		for player in canreject:
			await addscore(client,message,player)
	elif gamestate[4] != 3 and gamestate[5] != 3:
		await client.send_message(message.channel,":smiling_imp: **Evil** Wins by failure :smiling_imp: ")
		for player in canreject:
			await addscore(client,message,player)
	roleStr = "\n"
	for key in roles:
		#await client.send_message(message.channel,str(roles[key])+" is "+str(key))
		roleStr += str(roles[key])+" is **"+str(key)+"**\n"
	roleStr += "\n**30 frickin' dollarydoos** have been credited to members of the winning team.\n\n"
	await client.send_message(message.channel, roleStr)
	await client.send_message(message.channel, stopStr)
	gamestate[0] = 0

async def addscore(client, message, user):
	score = shelve.open('leaderboard', writeback=True)
	if user.id in score:
		current = score[user.id]
		score[user.id] = current + 30
	else:
		score[user.id] = 30
	#await client.send_message(message.channel, str(user.name)+" now has "+str(score[user.id])+" dollarydoos")
	score.sync()
	score.close()

async def scoreboard(client,message):
	counter = 0
	scoreStr= "\n         :star: Top 10 Players :star: \n\n"
	score = shelve.open('leaderboard')
	klist = score.keys()
	scoreboard = {}
	for key in klist:
		m = discord.utils.get(message.server.members, id=key)
		scoreboard[m.name] = score[key]
	
	for item in sorted(scoreboard, key=scoreboard.get, reverse=True):
		if counter < 10:
			scoreStr += ':military_medal: `{:20}{:>4}`\n'.format(str(item),str(scoreboard[item]))
			counter = counter + 1
	await client.send_message(message.channel,scoreStr)
	score.close()	
	
async def loadrules(client,message,rules,roles,playerlist,playerno):
	playersnamestring = "|"
	for x in playerlist:
		playersnamestring += "` "+x.name+" `|"
	if playerno == 5:
		rules.append(2) #quest 1
		rules.append(3)
		rules.append(2)
		rules.append(3)
		rules.append(3)
		roles["Merlin"] = ""
		roles["The Assassin"] = ""
		roles["Galahad, Loyal Servant of Arthur"] = ""
		roles["Tristan, Loyal Servant of Arthur"] = ""
		roles["Agravain, Minion of Mordred"] = ""
		rolesStr = ""
		for key in roles:
			rolesStr += ":black_small_square: "+key+"\n"
		await client.send_message(message.channel, startStr.format(playersnamestring,len(playerlist),"3","2",rolesStr))
	elif playerno == 6:
		rules.append(2) #quest 1
		rules.append(3)
		rules.append(4)
		rules.append(3)
		rules.append(4)
		roles["Merlin"] = ""
		roles["The Assassin"] = ""
		roles["Galahad, Loyal Servant of Arthur"] = ""
		roles["Tristan, Loyal Servant of Arthur"] = ""
		roles["Agravain, Minion of Mordred"] = ""
		roles["Guinevere, Loyal Servant of Arthur"] = ""
		rolesStr = ""
		for key in roles:
			rolesStr += ":black_small_square: "+key+"\n"
		await client.send_message(message.channel, startStr.format(playersnamestring,len(playerlist),"4","2",rolesStr))
	elif playerno == 7:
		rules.append(2) #quest 1
		rules.append(3)
		rules.append(3)
		rules.append(4)
		rules.append(4)
		roles["Merlin"] = ""
		roles["The Assassin"] = ""
		roles["Galahad, Loyal Servant of Arthur"] = ""
		roles["Tristan, Loyal Servant of Arthur"] = ""
		roles["Agravain, Minion of Mordred"] = ""
		roles["Percival"] = ""
		roles["Morgana"] = ""
		rolesStr = ""
		for key in roles:
			rolesStr += ":black_small_square: "+key+"\n"
		await client.send_message(message.channel, startStr.format(playersnamestring,len(playerlist),"4","3",rolesStr))
	elif playerno == 8:
		rules.append(3) #quest 1
		rules.append(4)
		rules.append(4)
		rules.append(5)
		rules.append(5)
		roles["Merlin"] = ""
		roles["The Assassin"] = ""
		roles["Galahad, Loyal Servant of Arthur"] = ""
		roles["Tristan, Loyal Servant of Arthur"] = ""
		roles["Agravain, Minion of Mordred"] = ""
		roles["Percival"] = ""
		roles["Morgana"] = ""
		roles["Guinevere, Loyal Servant of Arthur"] = ""
		rolesStr = ""
		for key in roles:
			rolesStr += ":black_small_square: "+key+"\n"
		await client.send_message(message.channel, startStr.format(playersnamestring,len(playerlist),"5","3",rolesStr))
	elif playerno == 9:
		rules.append(3) #quest 1
		rules.append(4)
		rules.append(4)
		rules.append(5)
		rules.append(5)
		roles["Merlin"] = ""
		roles["The Assassin"] = ""
		roles["Galahad, Loyal Servant of Arthur"] = ""
		roles["Tristan, Loyal Servant of Arthur"] = ""
		roles["Mordred"] = ""
		roles["Percival"] = ""
		roles["Morgana"] = ""
		roles["Guinevere, Loyal Servant of Arthur"] = ""
		roles["Lamorak, Loyal Servant of Arthur"] = ""
		rolesStr = ""
		for key in roles:
			rolesStr += ":black_small_square: "+key+"\n"
		await client.send_message(message.channel, startStr.format(playersnamestring,len(playerlist),"6","3",rolesStr))
	elif playerno == 10:
		rules.append(3) #quest 1
		rules.append(4)
		rules.append(4)
		rules.append(5)
		rules.append(5)
		roles["Merlin"] = ""
		roles["The Assassin"] = ""
		roles["Galahad, Loyal Servant of Arthur"] = ""
		roles["Tristan, Loyal Servant of Arthur"] = ""
		roles["Mordred"] = ""
		roles["Percival"] = ""
		roles["Morgana"] = ""
		roles["Guinevere, Loyal Servant of Arthur"] = ""
		roles["Lamorak, Loyal Servant of Arthur"] = ""
		roles["Agravain, Minion of Mordred"] = ""
		rolesStr = ""
		for key in roles:
			rolesStr += ":black_small_square: "+key+"\n"
		await client.send_message(message.channel, startStr.format(playersnamestring,len(playerlist),"6","4",rolesStr))
	else:
		await client.send_message(message.channel,"Rule Loading Error!")
