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
        #print(legalMoves[chosenIndex])
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
        newFoodCount = newFood.count() # get number of food items
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newGhostPositions = [ghostState.getPosition() for ghostState in newGhostStates] # the positions of the ghost(s)
        "*** YOUR CODE HERE ***"
        #Calculate Distance to each Ghost
        distanceToGhosts = [manhattanDistance(ghostPosition, newPos) for ghostPosition in newGhostPositions]
        #find out the nearest Ghost
        distanceToNearestGhost =0
        if distanceToGhosts : distanceToNearestGhost = min(distanceToGhosts)
        #Calculate Distance to each Food
        newFoodsList = newFood.asList()
        AvgDistanceToFoods =1 #unused for now, keeping in case it's needed later
        distanceToNearestFood=0
        distanceToFarthestFood=1
        #find distance to each food from current position
        distanceToFoods = [manhattanDistance(aFood, newPos) for aFood in newFoodsList]
        if distanceToFoods: distanceToNearestFood = min(distanceToFoods) #nearest food
        if distanceToFoods: distanceToFarthestFood = max(distanceToFoods) # farthest food
        if distanceToFoods: AvgDistanceToFoods = sum(distanceToFoods)/len(distanceToFoods) # avg distance to all foods
        #calculation each feature value and its weight.
        featureGhost = distanceToNearestGhost
        if not newFoodCount==0 : featureFoodCount = float(1.0/float(newFoodCount))
        else :
            featureFoodCount =0
        if distanceToNearestFood ==0: featureNearFood=0 # boundary case
        else : featureNearFood = float(1.0/float(distanceToNearestFood+distanceToFarthestFood))
        # just have any food if it is so close by, don't get confused to not have it keep for later
        if(featureNearFood==1):weightNearFood = 0
        else: weightNearFood=25 # otherwise distance to food it very important
        if(distanceToNearestGhost<3): weightGhost = -200 # The ghost is near by, run away now !
        else : weightGhost=0 # The ghost is not near, so don't worry, just concentrate on the food
        weightFoodCount=20 # even count of remaining food is important, in-case another nearby position does not have food
        weightScore=2 # giving a little weight to score as well
        result = weightNearFood*featureNearFood+weightFoodCount*featureFoodCount+weightGhost*featureGhost+weightScore*successorGameState.getScore()
        return result

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
        "*** YOUR CODE HERE ***"
	"""
        The first layer will contain the maximizer node which is the root.
        The second layer onwards it will contain the minimizer nodes.

        """
        """
        The variable value will start of with minus infinity and increment it for the max root node
        """
        bestScore = -float('Inf')
        bestAction = Directions.STOP

        """
        MAX function to calculate the value for the maximizer node.
        The root will be the only maximizer node here in our case.
        According to this algorithm, this function will evaluate the max value that is available from the minimum values
        available from the child nodes.
        That is, it will evaluate the MAX best option available from the MIN's best option to root.
        """
        def max_value(gameState, depth, numAgents):
                """
                Terminating condition
                """
                if depth == 0 or gameState.isWin() or gameState.isLose():
                        return self.evaluationFunction(gameState)
                """
                Starting off with minus infinity and incrementing it till we find the best MAX score
                """
                v = -float('Inf')
                agentIndex = 0
                actionList = gameState.getLegalActions(agentIndex)
                if(len(actionList)==0) : return self.evaluationFunction(gameState)
                if(actionList.__contains__(Directions.STOP)) : actionList.remove(Directions.STOP)
                for eachAction in actionList:
                        """
                        Traversing out through the child minimizer nodes and retrieving the max value from them
                        """
                        v = max(v, min_value(gameState.generateSuccessor(agentIndex, eachAction), depth, 1, numAgents))
                return v

	"""
        MIN function to calculate the value for the minimizer nodes.
        According to this algorithm, this function will evaluate the best minimum value available in the child nodes.

        """

        def min_value(gameState, depth, agentIndex, numAgents):
                """
                Terminating condition
                """
                if depth == 0 or gameState.isWin() or gameState.isLose():
                        return self.evaluationFunction(gameState)
                """
		Starting off with plus infinity and decrementing it till we find the best MIN score
                """
                v = float('Inf')
                for eachAction in gameState.getLegalActions(agentIndex):
                        """
                        Checking if the node is the root node or not.
                        If root node, run the maximizer function.
                        Else, for child nodes in layer, run the minimizer function for evaluation.
                        """
                        if numAgents == agentIndex:
                                v = min(v, max_value(gameState.generateSuccessor(agentIndex, eachAction), depth - 1, numAgents))
                        else:
                                v = min(v, min_value(gameState.generateSuccessor(agentIndex, eachAction), depth, agentIndex + 1, numAgents))
                return v

        """
        Traversing through the actions to get the best action by using Minimax algorithm
        """
        actionList = gameState.getLegalActions(0)
        if(len(actionList)==0) : return self.evaluationFunction(gameState)
        if(actionList.__contains__(Directions.STOP)) : actionList.remove(Directions.STOP)
        numAgents = gameState.getNumAgents()-1
        for eachAction in actionList:
                previousScore = bestScore
                bestScore = max(bestScore, min_value(gameState.generateSuccessor(0, eachAction), self.depth, 1, numAgents))
                if bestScore > previousScore:
                        bestAction = eachAction
        return bestAction



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
	"""
	The first layer will contain the maximizer node which is the root.
	The second layer onwards it will contain the minimizer nodes.
		
	"""
	"""
	The variable value will start of with minus infinity and increment it for the max root node
	"""
	bestScore = -float('Inf')
	"""
	alpha: MAX's best option on path to root
	"""
        alpha = -float('Inf')
	"""
	beta: MIN's best option on path to root
	"""
        beta = float('Inf')
        bestAction = Directions.STOP

        """
	MAX function to calculate the value for the maximizer node. 
	The root will be the only maximizer node here in our case.
	According to this algorithm, this function will evaluate the max value that is available from the minimum values available from the child nodes. 
	That is, it will evaluate the MAX best option available from the MIN's best option to root. It will also keep a track of whether or not to traverse any further nodes for better values.
	
	"""
	def max_value(gameState, alpha, beta, depth):
                """
		Terminating condition
		"""
		if depth == 0 or gameState.isWin() or gameState.isLose():
                        return self.evaluationFunction(gameState)
                """
		Starting off with minus infinity and incrementing it till we find the best MAX score
		"""
		v = -float('Inf')
                numAgents = gameState.getNumAgents() - 1
		agentIndex = 0
                for eachAction in gameState.getLegalActions(agentIndex):
                        """
			Traversing out through the child minimizer nodes and retrieving the max value from them		
			"""
			v = max(v, min_value(gameState.generateSuccessor(agentIndex, eachAction), alpha, beta, depth, numAgents))
                        """
			If the maximizer value at the parent node (beta) is less than the min values retrieved from the child nodes(v), return the max value and thus prune any further child nodes computation
			"""

			if v >= beta:
                                return v
                        alpha = max(alpha, v)
                return v

	"""
	MIN function to calculate the value for the minimizer nodes. 
	According to this algorithm, this function will evaluate the best minimum value available in the child nodes.
	Also, it will keep a track of whether or not to traverse any further nodes for better values.
	
	"""

        def min_value(gameState, alpha, beta, depth, agentIndex):
                """
		Terminating condition
		"""
		if depth == 0 or gameState.isWin() or gameState.isLose():
                        return self.evaluationFunction(gameState)
                """
		Starting off with plus infinity and decrementing it till we find the best MIN score
		"""
		v = float('Inf')
                numAgents = gameState.getNumAgents() - 1
                for eachAction in gameState.getLegalActions(agentIndex):
			"""
			Checking if the node is the root node or not.
			If root node, run the maximizer function.
			Else, for child nodes in layer, run the minimizer function for evaluation.	
			"""
                        if numAgents == agentIndex:
                                v = min(v, max_value(gameState.generateSuccessor(agentIndex, eachAction), alpha, beta, depth - 1))
                        else:
                                v = min(v, min_value(gameState.generateSuccessor(agentIndex, eachAction), alpha, beta, depth, agentIndex + 1))
                        """
			If the max value at parent node (alpha) computed is less than the value for child nodes under it(v), return the min value and thus prune any further child nodes for computation 
			"""
			if v <= alpha:
                                return v
                        beta = min(beta, v)
                return v

	"""
	Traversing through the actions to get the best action by using Alpha Beta pruning
	"""

        for eachAction in gameState.getLegalActions(0):
                previousScore = bestScore
                alpha = max(alpha, bestScore)
                bestScore = max(bestScore, min_value(gameState.generateSuccessor(0, eachAction), alpha, beta, self.depth, 1))
                if bestScore > previousScore:
                        bestAction = eachAction
                if beta <= bestScore:
                        return bestAction
        return bestAction

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
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

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

