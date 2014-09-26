# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  fringe=util.Stack() # using stack for DFS
  fringe.push((problem.getStartState(),[],0)) #state, total actions, total cost (cost not needed for DFS)
  state,fullactions,fullcost=fringe.pop()
  explored_states=[state] # keep a track of visited states
  while (not problem.isGoalState(state)):
    successors=problem.getSuccessors(state)
    for next_state,action,cost in successors:
        #print "next state:",next_state, action
        if (not next_state in explored_states):
          fringe.push((next_state,fullactions+[action],fullcost+cost))
          explored_states.append(next_state)
          #print "explored_states: ",explored_states
    #print "All actions: ",fullactions
    state,fullactions,fullcost=fringe.pop()
    
  return  fullactions
#frontier.push(problem.getSuccessors(problem.getStartState()))
#return None
#return tree_search(problem, Stack())
#util.raiseNotDefined()

def breadthFirstSearch(problem):
  '''"Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  #util.raiseNotDefined()'''
  fringe=util.Queue() # Using a Queue for BFS
  fringe.push((problem.getStartState(),[],0))# #state, total actions, total cost (cost not needed for BFS)
  state,fullactions,fullcost=fringe.pop()
  explored_states=[state]
  while (not problem.isGoalState(state)):
      successors=problem.getSuccessors(state)
      #print (successors)
      for next_state,action,cost in successors:
          #print "next state:",next_state, action
          if(not next_state in explored_states):
              #if(action=='North'):action =
              fringe.push((next_state,fullactions+[action],fullcost+cost))
              explored_states.append(next_state)
      #print "explored_states: ",explored_states
      #print "All actions: ",fullactions
      state,fullactions,fullcost=fringe.pop()
  #if problem.isGoalState(problem.getStartState()):
  #return node
  return fullactions

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
#util.raiseNotDefined()
  fringe=util.PriorityQueue() # Priority Queue, to prioritize according to cost
  fringe.push((problem.getStartState(),[],0),0) #state, total actions, total cost
  state,fullactions,fullcost=fringe.pop()
  explored_states=[(state,0)]
    #print "pop ",fullcost
  while (not problem.isGoalState(state)):
   successors=problem.getSuccessors(state)
   for next_state,action,cost in successors:
        #print "next state:",next_state, action
    explored=False
    total_cost=problem.getCostOfActions(fullactions+[action])
    for i in range(len(explored_states)):
     state_tmp,cost_tmp=explored_states[i]
     if (next_state==state_tmp) and (total_cost>=cost_tmp): # if the cost of this way is lesser even though this state is already seen, take this way
      explored=True
    if (not explored):
      fringe.push((next_state,fullactions+[action],total_cost),total_cost)
      explored_states.append((next_state,total_cost))
          #print "create cost ",total_cost+cost
          #print "explored_states: ",explored_states
      #print "All actions: ",fullactions
   state,fullactions,fullcost=fringe.pop()
      #print "pop ",fullcost
    
  return  fullactions

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0
def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    #print "Enter aStarSearch..."
    # A* is basically UCS with a heuristic, since heuristic is given in this case, just use what is given.
    fringe=util.PriorityQueue() # 
    fringe.push((problem.getStartState(),[],0),0) #state, total actions, total cost
    
    state,fullactions,fullcost=fringe.pop()
    explored_states=[(state,0)]
    while (not problem.isGoalState(state)):
      
      successors=problem.getSuccessors(state)
      for next_state,action,cost in successors:
        total_cost=problem.getCostOfActions(fullactions+[action])
        explored=False
        #print "next state:",next_state, action
        for i in range(len(explored_states)):
          state_tmp,cost_tmp=explored_states[i]
          if (next_state==state_tmp) and (total_cost>=cost_tmp):
            explored=True
        if (not explored):
          total_cost=problem.getCostOfActions(fullactions+[action])
          fringe.push((next_state,fullactions+[action],total_cost),total_cost+heuristic(next_state,problem))
          explored_states.append((next_state,total_cost))
          #print "explored_states: ",explored_states
      #print "All actions: ",fullactions
      state,fullactions,fullcost=fringe.pop()
    
    return  fullactions
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
