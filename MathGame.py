#import modules
from random import randint
from sys import exit

#String variables
ScoreMultiplier = lambda x : f"Current Score Multiplier: ({x})"#{}score_multiplier
menu_item1 = "1) Start Game"
menu_item2 = lambda x : f"2) Game Type: {x}" #{}game_type
menu_item3 = lambda x : f"3) Max Rounds ({x})" #{}max_rounds
menu_item4 = lambda x : f"4) Lowest Multiplier ({x})" #{}low_bound
menu_item5 = lambda x : f"5) Highest Multiplier ({x})" #{}high_bound
menu_item6 = lambda x : f"6) Sudden Death Mode ({x})" #{}sudden_death
menu_item7 = "7) Show High Scores"
menu_item8 = "8) Quit"
msg_welcome = "WELCOME TO THE MATH GAME!"
msg_quit = 'Type \'q\' or "quit" to the exit game.\n'
input_msg_rounds = "How many rounds do you want to play?: "
blank_line = ""
msg_score = "Round {0} ---- Score: {1}" #{0}round count , {1}score
msg_multiply = "What is {0} x {1}?" #{0}random integer, {1}random integer
msg_add = "What is {0} + {1}?" #{0}random integer, {1}random integer
msg_subtract = "What is {0} - {1}?" #{0}random integer, {1}random integer
input_msg_answer = "Answer: "
msg_correct = "Correct! +{0} point!\n" #{0}score multiplier
msg_wrong = "Wrong! It is {0}!\n" #{0}correct answer
msg_game_over = "Game over!"
msg_final_score = "{0} of {1} round(s) completed final score: {2}" #{0}round count, {1}max_rounds, {2}score
msg_perfect_score = "Perfect Score!"
input_msg_enter_int = "Enter an integer or 'q' to quit: "
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
error_msg_integer = "ERROR: Input is not an integer"
input_msg_gameoption = "Enter number of the game type you wish to play: "
error_msg_game_option = "Invalid game type"

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
	new_list = []
	try:
		with open(file_name,"r") as score_file:
			for line in score_file:
				line = line.strip()
				player_score = line.split(",")

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
	#sorted_score_list = sorted(score_list,reverse = True,key = ScoreSortKey)
	print(msg_high_score_header)
	for i in score_list:
		print(i[0],"---",i[1])

#Function for ending the game.
def QuitGame():
	print(msg_game_over)
	savescore(score_file_name,score_list)
	exit(1)

#Function for getting user input as an integer. Quits the game if 'q' or 'quit' is entered.
def EnterInt(msg):
	correct_input = False

	while correct_input == False:
		x = input(msg)
		if x.lower() in end_game_keywords:
			QuitGame()
		try:
			y = int(x)
			correct_input = True
		except:
			print(error_msg_integer)

	return y
	
#Function that generates a unique set of tuples with two integers each within low_bound and high_bound values
def GenerateOperands(low_bound,high_bound):
	problem = ()
	problem_list = set()
	
	while len(problem_list) < max_rounds:
		y = randint(low_bound,high_bound)
		x = randint(low_bound,high_bound)
		problem = (y,x)
		problem_list.add(problem)
	return problem_list

#Displays the main game menu with options to change the game parameters, start, and quit the game.
def MainMenu(game_type_options,game_type,max_rounds,low_bound,high_bound,sudden_death):
	start_game = False
	ms = ""

	while start_game == False:
		max_rounds_limit = (high_bound-low_bound+1)**2
		if max_rounds > max_rounds_limit:
			max_rounds = max_rounds_limit
			print(msg_max_rounds_reduced)
		score_multiplier = high_bound-low_bound
		if sudden_death == True: score_multiplier += 3
		print(blank_line)
		print(ScoreMultiplier(score_multiplier))
		print(blank_line)
		print(menu_item1)
		print(menu_item2(game_type))
		print(menu_item3(max_rounds))
		print(menu_item4(low_bound))
		print(menu_item5(high_bound))
		print(menu_item6(sudden_death))
		print(menu_item7)
		print(menu_item8)
		
		ms = EnterInt(input_msg_select_option)
		
		if ms == 1:
			print(blank_line)
			start_game = True

		elif ms == 2:
			for opt in game_type_options:
				print(str(game_type_options.index(opt))+") "+opt)
			g=EnterInt(input_msg_gameoption)
			try:
				game_type=game_type_options[g]
			except:
				print(error_msg_game_option)

		elif ms == 3:
			max_rounds_error = True
			while max_rounds_error == True:
				max_rounds = EnterInt(input_msg_rounds)
				if max_rounds > max_rounds_limit or max_rounds < 1:
					print(error_msg_max_rounds.format(max_rounds_limit))
				else:
					max_rounds_error = False

		elif ms == 4:
			low_bound_error = True
			while low_bound_error == True:
				low_bound = EnterInt(input_msg_lowbound)
				if high_bound <= low_bound:
					print(error_msg_low_bound)
				else:
					low_bound_error = False
		
		elif ms == 5:
			high_bound_error = True
			while high_bound_error == True:
				high_bound = EnterInt(input_msg_highbound)
				if high_bound <= low_bound:
					print(error_msg_high_bound)
				else:
					high_bound_error = False
		
		elif ms == 6:
			if sudden_death == False:
				sudden_death = True
			else:
				sudden_death = False

		elif ms == 7:
			print(blank_line)
			ShowScoreList(score_list)

		elif ms == 8:
			QuitGame()

		else:
			print(msg_invalid_menu)

	return (game_type,max_rounds,low_bound,high_bound,sudden_death,score_multiplier)

#Plays the game. Quits the game if 'q' or 'quit' is entered.
def PlayGame(start_round,game_type_options,game_type,max_rounds,low_bound,high_bound,sudden_death,score_multiplier):
	print(msg_quit)
	score = 0
	current_round = 0
	
	#Prevent duplicates by storing a tuples with 2 operators each in a set. Max rounds is limited to (high_bound-lowbound)**2 to prevent infintite looping.
	problem_list = GenerateOperands(low_bound,high_bound)

	for problem in problem_list:
		if game_type == "Mixed Math":
			problem_type = randint(1,len(game_type_options)-1)
		
		elif game_type == "Addition":
			problem_type = 1
		
		elif game_type == "Subtraction":
			problem_type = 2
		
		elif game_type == "Multiplication":
			problem_type = 3

		current_round += 1
		print(msg_score.format(current_round,score))
		
		if problem_type == 1:
			print(msg_add.format(problem[0],problem[1]))
			solution = problem[0]+problem[1]
		elif problem_type == 2:
			print(msg_subtract.format(problem[0],problem[1]))
			solution = problem[0]-problem[1]
		elif problem_type == 3:
			print(msg_multiply.format(problem[0],problem[1]))
			solution = problem[0]*problem[1]

		input_answer = EnterInt(input_msg_answer)

		if int(input_answer) == solution:
			score += score_multiplier
			print(msg_correct.format(score_multiplier))
		else:
			print(msg_wrong.format(solution))
			if sudden_death == True:
				current_round -= 1
				print(msg_sudden_death)
				break

	print(msg_final_score.format(current_round,max_rounds,score))

	print(blank_line)
	return score

#Displys the final score and repeats the game if the player enters 'y'.
def RepeatGame():
	if input(input_msg_again).lower() == "y":
		play_again = True
	else:
		play_again = False	
	return play_again


#Initial game parameters
max_rounds = 10
low_bound = 2
high_bound = 12
game_type_options = ("Mixed Math","Addition","Subtraction","Multiplication")
game_type = game_type_options[0]
end_game_keywords = ["q","quit"]
sudden_death = False
score_multiplier = 0
score_file_name = "scores.scs"

#Main game loop
print(msg_welcome)

score_list = readscore(score_file_name)

while 1 == 1:
	#Reset variables
	score = 0
	start_round = 1
	current_round = start_round
	play_again = True

	#Load main menu, display options, and get user input
	game_type,max_rounds,low_bound,high_bound,sudden_death,score_multiplier = MainMenu(game_type_options,game_type,max_rounds,low_bound,high_bound,sudden_death)

	while play_again == True:
		#Play the game
		score = PlayGame(start_round,game_type_options,game_type,max_rounds,low_bound,high_bound,sudden_death,score_multiplier)

		#Check for new score and if true update the score list and then shows it
		if (CheckScoreList(score_list,score)):
			score_list = UpdateScoreList(score_list,score)
			print(blank_line)
			ShowScoreList(score_list)
			print(blank_line)

		#Prompt for repeat game
		play_again = RepeatGame()
