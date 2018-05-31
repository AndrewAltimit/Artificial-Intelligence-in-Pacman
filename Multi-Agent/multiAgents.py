# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
	"""
	  A reflex agent chooses an action at each choice point by examining
	  its alternatives via a state evaluation function.

	  The code below is provided as a guide.  You are welcome to change
	  it in any way you see fit, so long as you don't touch our method
	  headers.
	"""


	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"

		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
		
		### Base Cases - Successor is a win or lose state ###
		if successorGameState.isWin():
			return float("inf") # infinite score
			
		if successorGameState.isLose(): 
			return float("-inf") # infinite cost
			
		### Extract more useful information ###
		# List of (x, y) active food co-ordinates
		newFood = newFood.asList()
		# Active ghosts (not scared)
		attack_ghosts = [g for g in newGhostStates if g.scaredTimer == 0]

		### Base Case - Ghost is too close to pacman (4 blocks away) ###
		# get the total distance (manhattan distance) of all the active ghosts to pacman
		distances = [util.manhattanDistance(g.getPosition(), newPos) for g in attack_ghosts]
		
		# If there is a ghost within a 4 for manhattanDistance then return (too close to a ghost)
		run_flag = (len(distances) > 0) and (min(distances) < 4)
		if run_flag:
			return  float("-inf")
			
		# Add score for closest food and number of remaining foods
		# smaller sizes should yield larger rewards so score is equal to weight / score_metric
		# Weights determined by empirical evidence
		weight_min_food = 10
		weight_len_food = 1
		distances = [util.manhattanDistance(f, newPos) for f in newFood]
		if len(distances) > 0:
			return successorGameState.getScore() + weight_min_food / min(distances) + weight_len_food / len(newFood)

		# No food nearby, just return the score
		return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
	"""
	  This default evaluation function just returns the score of the state.
	  The score is the same one displayed in the Pacman GUI.

	  This evaluation function is meant for use with adversarial search agents
	  (not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	  This class provides some common elements to all of your
	  multi-agent searchers.  Any methods defined here will be available
	  to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	  You *do not* need to make any changes here, but you can if you want to
	  add functionality to all your adversarial search agents.  Please do not
	  remove anything, however.

	  Note: this is an abstract class: one that should not be instantiated.  It's
	  only partially specified, and designed to be extended.  Agent (game.py)
	  is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.

		  Here are some method calls that might be useful when implementing minimax.

		  gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1

		  gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action

		  gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		# Begin mini-max algorithm using depth 0,  player 0 (pacman)
		return self.value(gameState, 0, 0)
		
	def value(self, gameState, current_depth, player_id):
		'''
		Procedure from class notes:
		If the state is a terminal state: return the state's utility
		If the agent at the state is MAX: return max-value(state)
		If the agent at the state is MIN: return min-value(state)
		'''
		
		# If the state is a terminal state: return the state's utility
		if gameState.isWin() or gameState.isLose() or current_depth == self.depth:
			return self.evaluationFunction(gameState)
			

		# Determine next player / depth / valid successors (move isn't stop)
		next_player = (player_id + 1) % gameState.getNumAgents()
		next_depth = current_depth + (1 * next_player == 0)
		possible_moves = self.filter_actions(gameState, player_id)
		
		### Recursive Call ###
		values = []
		for a in possible_moves:
			v = self.value(gameState.generateSuccessor(player_id, a) , next_depth, next_player)
			values.append(v)
		######################

		# Max Player #
		if player_id == 0:
			values.append(float("-inf")) # Initialize max = -infinity
			if current_depth == 0:
				return possible_moves[values.index(max(values))]
			return max(values)
		
		# Min Player #
		values.append(float("inf")) # Initialize min = infinity
		return min(values)
		
	# Given a gameState and player ID, determine all possible moves that are valid (not resulting in a stop)
	def filter_actions(self, gameState, player_id):
		return [a for a in gameState.getLegalActions(player_id) if a.upper() != 'STOP']
		

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent with alpha-beta pruning (question 3)
	"""
	def getAction(self, gameState):
		# Return the 0th index because we want the action, not the score
		# Initialize alpha to -infinity and beta to infinity
		return self.value(gameState, 0, 0, float("-inf"), float("inf"))[0]
			
	def value(self, gameState, player_id, current_depth, alpha, beta): 
		# Determine next depth and player
		next_depth = current_depth + (player_id >= gameState.getNumAgents())
		player_id = player_id % gameState.getNumAgents()

		# If the state is a terminal state: return the state's utility
		if next_depth == self.depth or gameState.isWin() or gameState.isLose():
			return ("", self.evaluationFunction(gameState))
			
		# Max Player #
		if player_id == 0:
			action, score = "", float("-inf")

			# For each possible action you can perform, get the successor values and evaluate
			for a in self.filter_actions(gameState, player_id):
				successor_value = self.value(gameState.generateSuccessor(player_id, a), player_id + 1, next_depth, alpha, beta)[-1] 

				# Update action and score
				if successor_value > score:
					action, score = a, successor_value
				
				# Perform prunning if score > beta
				if score > beta:
					return action, score

				# alpha is the max of the two
				alpha = max(alpha, score)
			
		# Min Player #
		else:
			action, score = "", float("inf")
			
			# For each possible action you can perform, get the successor values and evaluate
			for a in self.filter_actions(gameState, player_id):
				successor_value = self.value(gameState.generateSuccessor(player_id, a), player_id + 1, next_depth, alpha, beta)[-1] 

				# Update action and score
				if successor_value < score:
					action, score = a, successor_value
				
				# Perform prunning if score < alpha
				if score < alpha:
					return action, score
				
				# Beta is the min of the two
				beta = min(beta, score)

		# Return the action and the score
		return action, score


		
	# Given a gameState and player ID, determine all possible moves that are valid (not resulting in a stop)
	def filter_actions(self, gameState, player_id):
		return [a for a in gameState.getLegalActions(player_id) if a.upper() != 'STOP']

class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""

	def getAction(self, gameState):
		"""
		  Returns the expectimax action using self.depth and self.evaluationFunction

		  All ghosts should be modeled as choosing uniformly at random from their
		  legal moves.
		"""
		return self.value(gameState, 0, 1)
			
	def value(self, gameState, player_id, current_depth):
		# If the state is a terminal state: return the state's utility
		if current_depth > self.depth or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
	
		# Determine next depth and player
		next_player = (player_id + 1) % gameState.getNumAgents()
		next_depth = current_depth + ((player_id + 1) == gameState.getNumAgents())
		possible_moves = self.filter_actions(gameState, player_id)

		### Recursive Call ###
		values = []
		for a in possible_moves:
			v = self.value(gameState.generateSuccessor(player_id, a) , next_player, next_depth)
			values.append(v)
		######################

		# Max Player #
		if player_id == 0:
			if current_depth == 1:
				return possible_moves[values.index(max(values))]
			return max(values)
			
		# Min Player #
		else:
			average_score = sum(values)/len(values)
			return average_score

			
	# Given a gameState and player ID, determine all possible moves that are valid (not resulting in a stop)
	def filter_actions(self, gameState, player_id):
		return [a for a in gameState.getLegalActions(player_id) if a.upper() != 'STOP']
		
		

def betterEvaluationFunction(currentGameState):
	"""
	Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	evaluation function.

	DESCRIPTION: If this state is a win or lose state, use inf and -inf. Otherwise determine the score.
	
	Score is based on:
	1. The manhattan distances of enemy ghosts to pacman
	2. The manhattan distances of scared ghosts to pacman
	3. The manhattan distances of the closest food to pacman
	"""
	
	### Base Cases - currentGameState is a win or lose state ###
	if currentGameState.isWin():
		return float("inf") # infinite score
		
	if currentGameState.isLose(): 
		return float("-inf") # infinite cost
		
	### Extract more useful information ###
	# List of (x, y) active food co-ordinates
	current_pos = currentGameState.getPacmanPosition()
	new_food = currentGameState.getFood().asList()
	food_distances = [(util.manhattanDistance(current_pos, f) ) for f in new_food]
	
	# Extract scared vs enemy ghost distances
	scared_ghost_distances = []
	enemy_ghost_distances  = []
	for g in currentGameState.getGhostStates():
		# We should value being close to scared ghosts since we can eat them
		if g.scaredTimer == 0:
			scared_ghost_distances.append(util.manhattanDistance(current_pos, g.getPosition()))
		else:
			enemy_ghost_distances.append(util.manhattanDistance(current_pos, g.getPosition()))
	
	### Weights ###
	food_dist_weight     = 10
	scared_ghost_weight  = 1
	enemy_ghost_weight   = 3

	# Standard score for this state
	score = scoreEvaluationFunction(currentGameState)

	# Higher score if a piece of food is closer (the large pieces, not the small ones)
	score += food_dist_weight / min(food_distances)
	
	# Higher score for closer scared ghosts
	if ( len(scared_ghost_distances) > 0 ): 
		score += scared_ghost_weight / min(scared_ghost_distances)

	# Higher score for further enemy ghosts
	if ( len(enemy_ghost_distances) > 0 ): 
		score += enemy_ghost_weight / min(enemy_ghost_distances)

	return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
	"""
	  Your agent for the mini-contest
	"""

	def getAction(self, gameState):
		"""
		  Returns an action.  You can use any method you want and search to any depth you want.
		  Just remember that the mini-contest is timed, so you have to trade off speed and computation.

		  Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
		  just make a beeline straight towards Pacman (or away from him if they're scared!)
		"""
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()

