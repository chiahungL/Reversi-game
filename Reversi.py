#!usr/bin/python

import os.path
import string
INFINITE = float('inf') # define infinite
negaINFINITE = float('-inf') # define negative infinite

####################
# get file element
####################
filename = 'input.txt'

if not os.path.exists(filename):
	print "File doesn't exist."
	exit(0)

f = open('input.txt', 'r')
PlayerToMove = f.readline().rstrip() # get rid of \n
CutOffDepth =int(f.readline().rstrip()) # get rid of \n

### The map
matrix = []
for i in range(8):
	temp = f.readline().rstrip() # get rid of \n
	row = [c for c in temp]
	matrix.append(row)
f.close()
"""
# another style
matrix = []
for i in range(8):
	matrix_temp = []
	temp = f.readline().rstrip() # get rid of \n
	for j in range(8):
		matrix_temp.append(temp[j:j+1])
	matrix.append(matrix_temp)
"""

### Name of 64 grids
gridName = []
# print string.lowercase[:8] abcdefgh
for i in range(1, 9):
	temp = string.lowercase[:8]
	row = [(c + str(i)) for c in temp]
	gridName.append(row)

### Utility matrix
utility = []
utility.append([99, -8, 8, 6, 6, 8, -8, 99])
utility.append([-8, -24, -4, -3, -3, -4, -24, -8])
utility.append([8, -4, 7, 4, 4, 7, -4, 8])
utility.append([6, -3, 4, 0, 0, 4, -3, 6])
utility.append([6, -3, 4, 0, 0, 4, -3, 6])
utility.append([8, -4, 7, 4, 4, 7, -4, 8])
utility.append([-8, -24, -4, -3, -3, -4, -24, -8])
utility.append([99, -8, 8, 6, 6, 8, -8, 99])

### check matrix by print
def testMap(m):
	print "Here's the testMap:"
	for i in range(8):
		for j in range(8):
			print m[i][j],
		print ""
	print "-------------------"

####################
# function 
####################
class Tree (object):
	#def __init__ (self, name, parent, map, depth, InitialValue):
	def __init__ (self, name, parent, map, depth):
		self.name = name
		self.child = []
		self.parent = parent
		self.map = []
		self.depth = depth
		#self.value = InitialValue
		#self.alpha = negaINFINITE
		#self.beta = INFINITE
		self.value = None
		self.alpha = None
		self.beta = None
		
		for arr in map:
			self.map.append(list(arr))

####################
# function. Find legal moves. Expand the children under parent.
####################
def findValid(current, goal, initialI, initialJ): # Find valid moves for player X.
	flagFlip = False # if flagFlip == True, it means we need to call function flip after searching 8 directions
	timesFlip = 0 # how many times we need to flip (one direction: timesFlip == 1, two: timesFlip == 2)
	arrFlip = [] # store the directions that needs to flip
	if goal == "X":
		for i in range(initialI, 8):
			startJ = initialJ + 1 if i == initialI else 0
			for j in range(startJ, 8):
				if current.map[i][j] == '*':
					if i-1 >= 0 and j-1 >= 0 and current.map[i-1][j-1] == "O": #left-up
						if checkValid(current, -1, -1, i-1, j-1, goal) == True: #Valid!!!!!!!!!!!!! generate node
							#newChild = Tree(gridName[i][j], current, current.map, current.depth + 1) #new map isn't ready
							#newChild.map = flip(newChild.map, -1, -1, i, j, goal) #new map is ready
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([-1, -1]) ###start from here
							#return (i, j, newChild)
					if i-1 >= 0 and current.map[i-1][j] == "O": #up
						if checkValid(current, -1, 0, i-1, j, goal) == True:
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([-1, 0])
					if i-1 >= 0 and j+1 <= 7 and current.map[i-1][j+1] == "O": #right-up
						if checkValid(current, -1, 1, i-1, j+1, goal) == True:
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([-1, 1])
					if j-1 >= 0 and current.map[i][j-1] == "O": #left
						if checkValid(current, 0, -1, i, j-1, goal) == True:
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([0, -1])
					if j+1 <= 7 and current.map[i][j+1] == "O": #right
						if checkValid(current, 0, 1, i, j+1, goal) == True:
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([0, 1])
					if i+1 <= 7 and j-1 >= 0 and current.map[i+1][j-1] == "O": #left-down
						if checkValid(current, 1, -1, i+1, j-1, goal) == True:
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([1, -1])
					if i+1 <= 7 and current.map[i+1][j] == "O": #down
						if checkValid(current, 1, 0, i+1, j, goal) == True: #Valid!!!!!!!!!!!!! generate node
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([1, 0])
					if i+1 <= 7 and j+1 <= 7 and current.map[i+1][j+1] == "O": #right-down
						if checkValid(current, 1, 1, i+1, j+1, goal) == True: #Valid!!!!!!!!!!!!! generate node
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([1, 1])
					if flagFlip == True:
						newChild = Tree(gridName[i][j], current, current.map, current.depth + 1) #new map isn't ready
						newChild.map = flip(newChild.map, arrFlip, timesFlip, i, j, goal)
						return (i, j, newChild, True)
					else:
						pass
				else: #current.map[i][j] == 'O' or 'X', pass and search next grid
					pass
		return (initialI, initialJ, None, False) # done the double for loop, and didn't find valid
	else: # goal == "O"
		for i in range(initialI, 8):
			startJ = initialJ + 1 if i == initialI else 0
			for j in range(startJ, 8):
				#print "(%d, %d) = " % (i, j)
				if current.map[i][j] == '*':
					if i-1 >= 0 and j-1 >= 0 and current.map[i-1][j-1] == "X": #left-up
						if checkValid(current, -1, -1, i-1, j-1, goal) == True: #Valid!!!!!!!!!!!!! generate node
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([-1, -1])
							#return (i, j, newChild)
					if i-1 >= 0 and current.map[i-1][j] == "X": #up
						if checkValid(current, -1, 0, i-1, j, goal) == True:
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([-1, 0])
					if i-1 >= 0 and j+1 <= 7 and current.map[i-1][j+1] == "X": #right-up
						if checkValid(current, -1, 1, i-1, j+1, goal) == True:
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([-1, 1])
					if j-1 >= 0 and current.map[i][j-1] == "X": #left
						if checkValid(current, 0, -1, i, j-1, goal) == True:
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([0, -1])
					if j+1 <= 7 and current.map[i][j+1] == "X": #right
						if checkValid(current, 0, 1, i, j+1, goal) == True:
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([0, 1])
					if i+1 <= 7 and j-1 >= 0 and current.map[i+1][j-1] == "X": #left-down
						if checkValid(current, 1, -1, i+1, j-1, goal) == True:
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([1, -1])
					if i+1 <= 7 and current.map[i+1][j] == "X": #down
						if checkValid(current, 1, 0, i+1, j, goal) == True: #Valid!!!!!!!!!!!!! generate node
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([1, 0])
					if i+1 <= 7 and j+1 <= 7 and current.map[i+1][j+1] == "X": #right-down
						if checkValid(current, 1, 1, i+1, j+1, goal) == True: #Valid!!!!!!!!!!!!! generate node
							flagFlip = True
							timesFlip = timesFlip + 1
							arrFlip.append([1, 1])
					if flagFlip == True:
						newChild = Tree(gridName[i][j], current, current.map, current.depth + 1) #new map isn't ready
						newChild.map = flip(newChild.map, arrFlip, timesFlip, i, j, goal)
						return (i, j, newChild, True)
					else:
						pass
				else: #current.map[i][j] == 'O' or 'X', pass and search next grid
					pass
		return (initialI, initialJ, None, False) # done the double for loop, and didn't find valid

def checkValid(current, directionI, directionJ, newI, newJ, goal): # check if there is a X after O (e.g. *OOOX)
	if newI < 0 or newI > 7 or newJ < 0 or newJ > 7:
		return False
	while (True):
		if current.map[newI][newJ] == "*":
			return False
		elif current.map[newI][newJ] == goal:
			return True
		else:
			return checkValid(current, directionI, directionJ, newI+directionI, newJ+directionJ, goal)
			
def flip(newMap, arrFlip, timesFlip, inI, inJ, goal): # generate a new map after flipping at the current grid	
	for m in range(timesFlip): # There are "timesFlip" directions that need to do flip.
		i = inI + arrFlip[m][0]
		j = inJ + arrFlip[m][1]
		while (True):
			if newMap[i][j] == goal:
				break
			else:
				newMap[i][j] = goal
			# newMap[i][j] won't be *, since we already checked in function "checkValid"
			i = i + arrFlip[m][0]
			j = j + arrFlip[m][1]
	newMap[inI][inJ] = goal
	return newMap
	
def calculate(node, goal, utility):
	sum = 0
	if goal == "X":
		for i in range(8):
			for j in range(8):
				if node.map[i][j] == "X":
					sum = sum + utility[i][j]
				elif node.map[i][j] == "O":
					sum = sum - utility[i][j]
				else: # node.map[i][j] == "*"
					pass
	else: # goal == "O"
		for i in range(8):
			for j in range(8):
				if node.map[i][j] == "X":
					sum = sum - utility[i][j]
				elif node.map[i][j] == "O":
					sum = sum + utility[i][j]
				else: # node.map[i][j] == "*"
					pass
	return sum
	
def printOutput(node, v, alpha, beta):
	tempPrint = ""
	tempPrint += node.name
	tempPrint += ','
	tempPrint += str(node.depth)
	tempPrint += ','
	
	if v == INFINITE:
		tempPrint += "Infinity"
	elif v == negaINFINITE:
		tempPrint += "-Infinity"
	else:
		tempPrint += str(v)
	tempPrint += ','
	
	if alpha == negaINFINITE:
		tempPrint += "-Infinity"
	else:
		tempPrint += str(alpha)
	tempPrint += ','
	
	if beta == INFINITE:
		tempPrint += "Infinity"
	else:
		tempPrint += str(beta)
	#print tempPrint
	return tempPrint
	
def alphaBeta(node, CutOffDepth, alpha, beta, maximizingPlayer, goal, antiGoal, utility, logOutput, ansMap, passMove):
	retI = 0
	retJ = 0
	noAnyMove = True
	if node.depth == CutOffDepth or passMove == 2:
		v = calculate(node, goal, utility)
		if CutOffDepth == 0:
			for arr in node.map:
				ansMap.append(list(arr))
		logOutput.append(printOutput(node, v, alpha, beta))
		#printOutput(node, v, alpha, beta)
		return v # return weight (utility)
	if maximizingPlayer == True:
		v = negaINFINITE
		for i in range(8):
			for j in range(8):
				find = False
				(testI, testJ, newChild, find) = findValid(node, goal, retI, retJ)
				
				if find == True:
					retI = testI
					retJ = testJ
					logOutput.append(printOutput(node, v, alpha, beta))
					#printOutput(node, v, alpha, beta)
					noAnyMove = False
					passMove = 0
					#Here~~~~~~~~~~~~~~~~~~~~~~~~
					#v = max(v, alphaBeta(newChild, CutOffDepth, alpha, beta, False, goal, antiGoal, utility, logOutput, ansMap, passMove))
					tempV = alphaBeta(newChild, CutOffDepth, alpha, beta, False, goal, antiGoal, utility, logOutput, ansMap, passMove)
					if tempV > v: #######
						v = tempV
						if newChild.depth == 1:
							for arr in newChild.map:
								ansMap.append(list(arr))
					if beta <= v:
						logOutput.append(printOutput(node, v, alpha, beta))
						#printOutput(node, v, alpha, beta)
						return v # CUT OFF
					alpha = max(alpha, v)
				
				elif find == False and noAnyMove == True: # check antiGoal
					passMove = passMove + 1
					if passMove == 2:
						newChild = Tree("pass", node, node.map, node.depth + 1)
						logOutput.append(printOutput(node, v, alpha, beta))
						#printOutput(node, v, alpha, beta)
						v = max(v, calculate(node, goal, utility))
						logOutput.append(printOutput(newChild, v, alpha, beta))
						#printOutput(newChild, v, alpha, beta)
						alpha = max(alpha, v)
						logOutput.append(printOutput(node, v, alpha, beta))
						#printOutput(node, v, alpha, beta)
						return v
					else:
						newChild = Tree("pass", node, node.map, node.depth + 1)
						logOutput.append(printOutput(node, v, alpha, beta))
						#printOutput(node, v, alpha, beta)
						noAnyMove = False
						#v = max(v, alphaBeta(newChild, CutOffDepth, alpha, beta, False, goal, antiGoal, utility, logOutput, ansMap, passMove))
						tempV = alphaBeta(newChild, CutOffDepth, alpha, beta, False, goal, antiGoal, utility, logOutput, ansMap, passMove)
						if tempV > v:
							v = tempV
							if newChild.depth == 1:
								for arr in newChild.map:
									ansMap.append(list(arr))
						if beta <= v:
							logOutput.append(printOutput(node, v, alpha, beta))
							#printOutput(node, v, alpha, beta)
							return v
						alpha = max(alpha, v)
				elif find == False and noAnyMove == False:
					logOutput.append(printOutput(node, v, alpha, beta))
					#printOutput(node, v, alpha, beta)
					return v
				else:
					pass
				
	else: # maximizingPlayer == False
		v = INFINITE
		for i in range(8):
			for j in range(8):
				find = False
				(testI, testJ, newChild, find) = findValid(node, antiGoal, retI, retJ)
				
				if find == True:
					retI = testI
					retJ = testJ
					logOutput.append(printOutput(node, v, alpha, beta))
					#printOutput(node, v, alpha, beta)
					noAnyMove = False
					passMove = 0
					v = min(v, alphaBeta(newChild, CutOffDepth, alpha, beta, True, goal, antiGoal, utility, logOutput, ansMap, passMove))
					if v <= alpha:
						logOutput.append(printOutput(node, v, alpha, beta))
						#printOutput(node, v, alpha, beta)
						return v # CUT OFF
					beta = min(beta, v)
				elif find == False and noAnyMove == True: #check antiGoal
					passMove = passMove + 1
					if passMove == 2:#############################
						newChild = Tree("pass", node, node.map, node.depth + 1)
						logOutput.append(printOutput(node, v, alpha, beta))
						#printOutput(node, v, alpha, beta)
						v = min(v, calculate(node, goal, utility))
						logOutput.append(printOutput(newChild, v, alpha, beta))
						#printOutput(newChild, v, alpha, beta)
						beta = min(beta, v)
						logOutput.append(printOutput(node, v, alpha, beta))
						#printOutput(node, v, alpha, beta)
						return v
					else:
						newChild = Tree("pass", node, node.map, node.depth + 1)
						logOutput.append(printOutput(node, v, alpha, beta))
						#printOutput(node, v, alpha, beta)
						noAnyMove = False
						v = min(v, alphaBeta(newChild, CutOffDepth, alpha, beta, True, goal, antiGoal, utility, logOutput, ansMap, passMove))
						if v <= alpha:
							logOutput.append(printOutput(node, v, alpha, beta))
							#printOutput(node, v, alpha, beta)
							return v # CUT OFF
						beta = min(beta, v)
				elif find == False and noAnyMove == False:
					logOutput.append(printOutput(node, v, alpha, beta))
					#printOutput(node, v, alpha, beta)
					return v
				else:
					pass
				
####################
# main
####################
if PlayerToMove == "X":
	goal = "X"
	antiGoal = "O"
else:
	goal = "O"
	antiGoal = "X"
root = Tree("root", [], matrix, 0)

logOutput = []
ansMap = []
ansMap.append([999999999999])
passMove = 0
#print "Node,Depth,Value,Alpha,Beta"
alphaBeta(root, CutOffDepth, negaINFINITE, INFINITE, True, goal, antiGoal, utility, logOutput, ansMap, passMove)
"""
for i in range(len(ansMap)-8, len(ansMap)):
	for j in range(8):
		print ansMap[i][j],
	print ""
"""

"""
print "Node,Depth,Value,Alpha,Beta"
for k in range(len(logOutput)):
	if logOutput[k] == None:
		pass
	else:
		print logOutput[k]
"""
###################
# print at output.txt
###################

f = open("output.txt", "w")

for i in range(len(ansMap)-8, len(ansMap)):
	for j in range(8):
		f.write(ansMap[i][j])
	f.write("\n")

f.write("Node,Depth,Value,Alpha,Beta\n")
for k in range(len(logOutput)):
	if logOutput[k] == None:
		pass
	else:
		f.write(logOutput[k])
	if k != len(logOutput) - 1:
		f.write("\n")
