#import modules
from random import randint
from playsound import playsound
from pathlib import Path
import threading

#Initial game parameters
max_rounds = 10
low_bound = 2
high_bound = 12
sudden_death = False
score_multiplier = 0
score_file_name = "scores.scs"
sound_dir = Path(__file__).parent
coin_sound = sound_dir / 'CoinFalling.mp3'

#String variables
ScoreMultiplier = lambda x : f"Current Score Multiplier: ({x})"#{}score_multiplier
menu_item1 = "1) Start Game"
menu_item2 = lambda x : f"2) Max Rounds ({x})" #{}max_rounds
menu_item3 = lambda x : f"3) Lowest Multiplier ({x})" #{}low_bound
menu_item4 = lambda x : f"4) Highest Multiplier ({x})" #{}high_bound
menu_item5 = lambda x : f"5) Sudden Death Mode ({x})" #{}sudden_death
menu_item6 = "6) Show High Scores"
menu_item7 = "7) Quit"
msg_welcome = "WELCOME TO THE MULTIPLYING GAME!"
msg_quit = 'Type \'q\' or "quit" to the exit game.\n'
end_game_keywords = ["q","quit"]
input_msg_rounds = "How many rounds do you want to play?: "
blank_line = ""
msg_score = "Round {0} ---- Score: {1}" #{0}round count , {1}score
msg_multiply = "What is {0}x{1}?" #{0}random number, {1}random number
input_msg_answer = "Answer: "
msg_correct = "Correct! +{0} point!\n" #{0}score multiplier
msg_wrong = "Wrong! It is {0}!\n" #{0}correct answer
msg_game_over = "Game over!"
msg_final_score = "{0} of {1} round(s) completed final score: {2}" #{0}round count, {1}max_rounds, {2}score
msg_perfect_score = "Perfect Score!"
input_msg_enter_int = "Enter a positive integer or 'q' to quit: "
input_msg_select_option = "Select an option: "
msg_invalid_menu = "Invalid menu selection!"
input_msg_rounds = "Enter the number of rounds to play: "
input_msg_lowbound = "Enter the lowest random multiplier: "
input_msg_highbound = "Enter the highest random multiplier: "
input_msg_again = "Enter 'y' to play again with the same settings: "
error_msg_low_bound = "ERROR: Low bound must be less than high bound!"
error_msg_high_bound = "ERROR: High bound must be greater than low bound!"
msg_sudden_death = "SUDDEN DEATH!"
msg_high_score_header = "Top Five Scores\nNAME --- SCORE"
input_msg_get_name = "New high score!\nEnter your name: "
error_msg_save_score = "ERROR: Something went wrong with saving the scores"
error_msg_corrupt_score = "ERROR: {0}'s score is corrupt. Removing it from the list." #{0}player_score[0]
error_msg_score_read = "Something went wrong reading scores."
error_msg_max_rounds = "ERROR: Max rounds cannot be less than 1 or greater than {0}. This is the maximum number of unique problems" #{0}max_rounds_limit
msg_max_rounds_reduced = "Max rounds cannot be greater than the number of unique problems possible"

#Try to save the score_list to the score file. Returns False if there is an error.
def savescore(file_name,score_list):
	try:
		with open(file_name,"w") as score_file:
			for x in score_list:
				score_file.write(str(x[0])+","+str(x[1])+"\n")
		score_saved = True
	except: 
		score_saved = False
		print(error_msg_save_score)

	return score_saved

#Try to read the score list and return a list of player scores. Returns an empty list if there is an error.
def readscore(file_name):
	new_list=[]
	try:
	with open(file_name,"r") as score_file:
			for line in score_file:
				line=line.strip()
				player_score=line.split(",")

				try:
					player_score[1] = int(player_score[1])
					new_list.append(player_score)
				except:
					print(error_msg_corrupt_score.format(player_score[0]))
	except:
		print(error_msg_score_read)
	
	return new_list

#Key for sorting high scores by score
def ScoreSortKey(x):
	return x[1]

#Checksthe score list to see if the score list has 5 or less items or the player has a new high score
def CheckScoreList(score_list,score):
	new_score = False
	if len(score_list) < 5:
		new_score = True
	else:
		for i in score_list:
			if score > i[1]:
				new_score = True
	return new_score

#Get the player's name, pop() the lowest score, add the new score to the list, sort the list, and return the sorted list
def UpdateScoreList(score_list,score):
	player_name = ""
	while player_name == "" or not(player_name.isalnum):
		player_name = input(input_msg_get_name)
	score_list.append([player_name,score])
	new_score_list = sorted(score_list,reverse = True,key = ScoreSortKey)
	while len(new_score_list) > 5:
		new_score_list.pop()
	return new_score_list

#Displays the high score list
def ShowScoreList(score_list):
	#sorted_score_list=sorted(score_list,reverse=True,key=ScoreSortKey)
	print(msg_high_score_header)
	for i in score_list:
		print(i[0],"---",i[1])

#Function for ending the game.
def QuitGame():
	print(msg_game_over)
	savescore(score_file_name,score_list)
	quit()

#Function for getting use input. Quits the game if 'q' or 'quit' is entered.
def EnterInt(msg):
	x=""
	x=input(msg)
	if x.lower() in end_game_keywords:
		QuitGame()
	while x.isdigit()==False:
		x=input(input_msg_enter_int)
		if x.lower() in end_game_keywords:
			QuitGame()
	return int(x)

#Displays the main game menu with options to change the game parameters, start, and quit the game.
def MainMenu(max_rounds,low_bound,high_bound,sudden_death):
	start_game=False
	ms=""

	while start_game==False:
		max_rounds_limit=(high_bound-low_bound+1)**2
		if max_rounds > max_rounds_limit:
			max_rounds = max_rounds_limit
			print(msg_max_rounds_reduced)
		score_multiplier = high_bound-low_bound
		if sudden_death == True: score_multiplier += 3
		print(blank_line)
		print(ScoreMultiplier(score_multiplier))
		print(blank_line)
		print(menu_item1)
		print(menu_item2(max_rounds))
		print(menu_item3(low_bound))
		print(menu_item4(high_bound))
		print(menu_item5(sudden_death))
		print(menu_item6)
		print(menu_item7)
		ms=EnterInt(input_msg_select_option)
		if ms==1:
			print(blank_line)
			start_game=True
		elif ms==2:
			max_rounds_error=True
			while max_rounds_error == True:
				max_rounds=EnterInt(input_msg_rounds)
				if max_rounds > max_rounds_limit or max_rounds < 1:
					print(error_msg_max_rounds.format(max_rounds_limit))
				else:
					max_rounds_error = False
		elif ms==3:
			low_bound_error=True
			while low_bound_error==True:
				low_bound=EnterInt(input_msg_lowbound)
				if high_bound<=low_bound:
					print(error_msg_low_bound)
				else:
					low_bound_error=False
		elif ms==4:
			high_bound_error=True
			while high_bound_error==True:
				high_bound=EnterInt(input_msg_highbound)
				if high_bound<=low_bound:
					print(error_msg_high_bound)
				else:
					high_bound_error=False
		elif ms==5:
			if sudden_death==False:
				sudden_death=True
			else:
				sudden_death=False
		elif ms==6:
			print(blank_line)
			ShowScoreList(score_list)
		elif ms==7:
			QuitGame()
		else:
			print(msg_invalid_menu)
	return (max_rounds,low_bound,high_bound,sudden_death,score_multiplier)

#Plays the game. Quits the game if 'q' or 'quit' is entered.
def PlayGame(start_round,max_rounds,low_bound,high_bound,sudden_death,score_multiplier):
	print(msg_quit)
	score=0
	current_round=0
	problem_list=set()
	problem=""
	
	#Prevent duplicates by storing a tuples with 2 operators each in a set. Max rounds is limited to (high_bound-lowbound)**2 to prevent infintite looping.
	while len(problem_list) < max_rounds:
		y=randint(low_bound,high_bound)
		x=randint(low_bound,high_bound)
		problem=(y,x)
		problem_list.add(problem)

	for problem in problem_list:
		#playsound(coin_sound,True)
		threading.Thread(target=playsound, args=(coin_sound,), daemon=True).start()
		current_round+=1
		print(msg_score.format(current_round,score))
		print(msg_multiply.format(problem[0],problem[1]))
		solution=problem[0]*problem[1]
		input_answer=EnterInt(input_msg_answer)
		if int(input_answer)==solution:
			score+=score_multiplier
			print(msg_correct.format(score_multiplier))
		else:
			print(msg_wrong.format(solution))
			if sudden_death==True:
				current_round-=1
				print(msg_sudden_death)
				break
	print(msg_final_score.format(current_round,max_rounds,score))
	#Removed perfect score for now -BP 2022-08-08
	#if score>0 and start_round==max_rounds and max_rounds==score:
		#print(msg_perfect_score)
	print(blank_line)
	return score

#Displys the final score and repeats the game if the player enters 'y'.
def RepeatGame():
	if input(input_msg_again).lower()=="y":
		play_again=True
	else:
		play_again=False	
	return play_again


#Main game loop
print(msg_welcome)

score_list=readscore(score_file_name)

while 1==1:
	#Reset variables
	score=0
	start_round=1
	current_round=start_round
	play_again=True

	#Load main menu, display options, and get user input
	max_rounds,low_bound,high_bound,sudden_death,score_multiplier=MainMenu(max_rounds,low_bound,high_bound,sudden_death)

	while play_again==True:
		#Play the game
		score=PlayGame(start_round,max_rounds,low_bound,high_bound,sudden_death,score_multiplier)

		#Check for new score and if true update the score list and then shows it
		if (CheckScoreList(score_list,score)):
			score_list=UpdateScoreList(score_list,score)
			print(blank_line)
			ShowScoreList(score_list)
			print(blank_line)

		#Prompt for repeat game
		play_again=RepeatGame()