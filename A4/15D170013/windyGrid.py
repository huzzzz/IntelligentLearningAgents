import random

actions = {'L' : 0, 'R' : 1, 'U' : 2, 'D' : 3}
kmactions = {'L' : 0, 'R' : 1, 'U' : 2, 'D' : 3, 'LU' : 4, 'LD' : 5, 'RU' : 6, 'RD' : 7}

n = 7
m = 10

def getWind(s):
	wind  = 0
	if (s[1] < 9 and s[1] > 2):
		wind += 1
	if (s[1] < 8 and s[1] > 5):
		wind += 1
	return wind

def getFromTuple(s):
	return s[0]*m + s[1]

def makeTuple(s):
	return (s//m, s%m)

start_state_tup = (3, 0)
goal_state_tup = (3, 7)

start_state = getFromTuple(start_state_tup)
goal_state = getFromTuple(goal_state_tup)

def takeAction(s, a, stoch=False):
	s_tup = makeTuple(s)

	c = s_tup[1]
	r = s_tup[0]
	reward = -1
	
	# print(s_tup, s, a)

	if (a == 0):
		c = min(s_tup[1] + 1, m-1)
	elif (a == 1):
		c = max(s_tup[1] - 1, 0) 
	elif (a == 2):
		r = max(s_tup[0] - 1, 0)
	elif(a == 3):
		r = min(s_tup[0] + 1, n-1)
	
	
	# Kings Moves
	elif(a == 4):
		c = min(s_tup[1] + 1, m-1)
		r = max(s_tup[0] - 1, 0)		
	elif(a == 5):
		c = min(s_tup[1] + 1, m-1)
		r = min(s_tup[0] + 1, n-1)
	elif(a == 6):
		c = max(s_tup[1] - 1, 0) 
		r = max(s_tup[0] - 1, 0)		
	elif(a == 7):
		c = max(s_tup[1] - 1, 0) 
		r = min(s_tup[0] + 1, n-1)

	# print(r,c)
	if (not stoch):
		r = min(max(0, r - getWind(s_tup)),  n - 1)

	else:
		myCh = random.choice([-1, 0, 1])
		r = min(max(0, r - getWind(s_tup) + myCh),  n - 1)
		
	# print(r,c, getWind(s_tup))
	sNew_tup = (r,c)
	sNew = getFromTuple(sNew_tup)

	if (sNew == goal_state):
		reward = 0 	

	return [sNew, reward]

# print(makeTuple(takeAction(getFromTuple((0, 9)), 3)[0]))
# print(makeTuple(takeAction(getFromTuple((2, 4)), 1)[0]))
# print(makeTuple(takeAction(getFromTuple((3, 9)), 1)[0]))
# print(makeTuple(takeAction(getFromTuple((1, 1)), 1)[0]))
# print(makeTuple(takeAction(getFromTuple((0, 0)), 1)[0]))
# print(makeTuple(takeAction(getFromTuple((7, 7)), )[0]))
