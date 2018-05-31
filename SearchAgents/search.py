# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
	"""
	This class outlines the structure of a search problem, but doesn't implement
	any of the methods (in object-oriented terminology: an abstract class).

	You do not need to change anything in this class, ever.
	"""

	def getStartState(self):
		"""
		Returns the start state for the search problem
		"""
		util.raiseNotDefined()

	def isGoalState(self, state):
		"""
		  state: Search state

		Returns True if and only if the state is a valid goal state
		"""
		util.raiseNotDefined()

	def getSuccessors(self, state):
		"""
		  state: Search state

		For a given state, this should return a list of triples,
		(successor, action, stepCost), where 'successor' is a
		successor to the current state, 'action' is the action
		required to get there, and 'stepCost' is the incremental
		cost of expanding to that successor
		"""
		util.raiseNotDefined()

	def getCostOfActions(self, actions):
		"""
		 actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.  The sequence must
		be composed of legal moves
		"""
		util.raiseNotDefined()


def tinyMazeSearch(problem):
	"""
	Returns a sequence of moves that solves tinyMaze.  For any other
	maze, the sequence of moves will be incorrect, so only use this for tinyMaze
	"""
	from game import Directions
	s = Directions.SOUTH
	w = Directions.WEST
	return  [s,s,w,s,w,w,s,w]

# Helper function, merge the fringe with successors (Used for BFS and DFS)
def fringe_merge(search_type, fringe, list_nodes, source_path, visited):
	for loc, action, cost in list_nodes:
		# if we visited the location before, dont add to fringe
		if loc in visited:
			continue

		# BFS/DFS: Cost is not factored in
		fringe.push((loc, source_path + [action]))

		if search_type == "BFS":
			# Add location of newly added node to the visited set
			visited.add(loc)


	

def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first

	Your search algorithm needs to return a list of actions that reaches
	the goal.  Make sure to implement a graph search algorithm

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:
	"""

	# Initialize Fringe (Stack)
	start = problem.getStartState()

	fringe = util.Stack()
	fringe.push((start, []))

	# Initialize visited set
	visited = set()

	while True:
		# If the fringe is empty then report the error and terminate
		if fringe.isEmpty():
			print "ERROR: No solution found. [Fringe is empty]"
			return None

		# Pop off the top of the stack
		loc, path = fringe.pop()


		
		# If we reached the goal state, we are done and can return the solution path
		if problem.isGoalState(loc):
			return path

		# Add expanded node to the visited set
		visited.add(loc)

		
		# Perform fringe merging with child nodes
		fringe_merge("DFS", fringe, problem.getSuccessors(loc), path, visited)
		
	return [] # No solution found (this shouldn't be called given the while loops error checking on the fringe)


def breadthFirstSearch(problem):
	"""
	Search the shallowest nodes in the search tree first.
	"""
	# Initialize Fringe (Queue)
	start = problem.getStartState()

	fringe = util.Queue()
	fringe.push((start, []))

	# Initialize visited set
	visited = set()

	while True:
		# If the fringe is empty then report the error and terminate
		if fringe.isEmpty():
			print "ERROR: No solution found. [Fringe is empty]"
			return None

		# Pop off the top of the stack
		loc, path = fringe.pop()
		
		# If we reached the goal state, we are done and can return the solution path
		if problem.isGoalState(loc):
			return path

		# Add expanded node to the visited set
		visited.add(loc)
		
		# Perform fringe merging with child nodes
		fringe_merge("BFS", fringe, problem.getSuccessors(loc), path, visited)

	return [] # No solution found (this shouldn't be called given the while loops error checking on the fringe)

def uniformCostSearch(problem):
	"Search the node of least total cost first. "
	# Initialize Fringe (Priority Queue)
	start = problem.getStartState()

	fringe = util.PriorityQueue()
	fringe.push((start, []), 0) # start has no cost

	# Initialize visited set
	visited = set()

	while True:
		# If the fringe is empty then report the error and terminate
		if fringe.isEmpty():
			print "ERROR: No solution found. [Fringe is empty]"
			return None

		# Pop off the top of the PriorityQueue
		current_loc, path = fringe.pop()
		
		# If we reached the goal state, we are done and can return the solution path
		if problem.isGoalState(current_loc):
			return path

		# Get successors of current state
		successors = problem.getSuccessors(current_loc)
		
		# Loop over successors
		for loc, action, cost in successors:
			# Reset step cost
			stepcost = 0

			# Determine step cost
			for node in fringe.heap:
				if loc == node[2][0]:
					stepcost = node[0] - problem.getCostOfActions(path)
			
			# If the successor is unvisited and the cost is less than the stepcost, add it to the queue
			if loc not in visited:
				if (cost < stepcost) or sum([1 for node in fringe.heap if loc == node[2][0]]) == 0:
					# Push successors' state, actions and cost to the fringe if not visited
					fringe.push([loc, path + [action]], problem.getCostOfActions(path) + cost)
					
		# Current node is visited	  
		visited.add(current_loc)
		

	return [] # No solution found (this shouldn't be called given the while loops error checking on the fringe)

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0
	
def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	"*** YOUR CODE HERE ***"
	start = problem.getStartState()
	
	# Initialize Fringe (Priority Queue)
	fringe = util.PriorityQueue()
	# Start has no initial path cost but it does have a heuristic value
	fringe.push((start, [], 0), heuristic(start, problem))
	
	# Initialize visited set
	visited = set()

	while True:
		# If the fringe is empty then report the error and terminate
		if fringe.isEmpty():
			print "ERROR: No solution found. [Fringe is empty]"
			return []
			
		# Pop off the top of the PriorityQueue
		current_loc, path, current_cost = fringe.pop();
		
		# If we have visited this node, skip it
		if current_loc in visited:
			continue
		
		# If we reached the goal state, we are done and can return the solution path
		if problem.isGoalState(current_loc):
			return path
		
		# Current node is visited	
		visited.add(current_loc)

		# Get successors of current state
		successors = problem.getSuccessors(current_loc)
		
		# Loop over successors
		for loc, action, cost in successors:
			# Do not add nodes to the fringe which have been visited
			if(loc in visited):
				continue
				
			# Add successor to the fringe
			fringe.push((loc, path + [action], current_cost+cost),current_cost + cost + heuristic(loc, problem))
			
	return [] # No solution found (this shouldn't be called given the while loops error checking on the fringe)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
