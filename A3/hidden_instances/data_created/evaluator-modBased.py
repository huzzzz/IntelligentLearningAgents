import os, sys
import numpy as np

### Implemented the Model Based Algorithm maintaining estimates of the Transitions and the Rewards and using Value Iteration ###

file_path = sys.argv[1]

lines = []
with open(file_path, 'r') as f:
	lines = f.readlines()

S = int(lines[0])
A = int(lines[1])
gamma = float(lines[2])
ind = 3

## The empirical estimates of the transitions and the rewards
T_est = {s : {a : {sPrime : 0 for sPrime in range(0,S)} for a in range(0,A)} for s in range(0,S)}
R_est = {s : {a  : {sPrime : 0 for sPrime in range(0,S)} for a in range(0,A)} for s in range(0,S)}

## the names are self explanatory
totalTransitions = {s : {a : {sPrime : 0 for sPrime in range(0,S)} for a in range(0,A)} for s in range(0,S)}
totalVisits = {s : {a :  0 for a in range(0,A)} for s in range(0,S)}
totalRewards = {s : {a : {sPrime : 0 for sPrime in range(0,S)} for a in range(0,A)} for s in range(0,S)}

## Maintains the probabilities i.e. the stochastic probability for each action for a given state  
totalProbs = {s : { a : 0 for a in range(0, A)} for s in range(0, S)}

while (ind < len(lines) - 1):

	try:
		[s, a, r] = lines[ind].rstrip().split("\t")
	except:
		print(lines[ind])
	s = int(s)
	a = int(a)
	r = float(r)
	sPrime = int(lines[ind+1].rstrip().split("\t")[0])
		
	totalRewards[s][a][sPrime] += r
	totalVisits[s][a] += 1
	totalTransitions[s][a][sPrime] += 1

	ind += 1

for s in range(0,S):
	totVisitsAllActions = sum(totalVisits[s].values())
	for a in range(0, A):
		for sPrime in range(0,S):
			if (totalVisits[s][a] > 0):
				T_est[s][a][sPrime] = totalTransitions[s][a][sPrime] * 1.0 / totalVisits[s][a]
			if (totalTransitions[s][a][sPrime] > 0):
				R_est[s][a][sPrime] = totalRewards[s][a][sPrime] * 1.0 / totalTransitions[s][a][sPrime]

		totalProbs[s][a] = totalVisits[s][a] * 1.0 / totVisitsAllActions

######################################### Value Iteration #############################################################################
## The value iteration method used here is using the Bellmans operators for stochastic policies, Here the policy is stochastic and the 
## probability of the actions are maintained empirically using the totalTransitions going to that action from a state normalised over
## all the actions. 

V = [0]*S

## Returns the | |_1 i.e. the 1 norm of the vectors V1, V2
def norm_fn(V1, V2):
	max_diff = 0
	absV = [abs(v1 - v2) for v1, v2 in zip(V1, V2)]	
	max_diff = max(absV)
	return max_diff

## Value Iteration applies the Bellmans operators for stochastic policies continually until the condition of 1 norm < 1e-6 is not obtained
while True:
	V_new = [0] * S

	for s in range(0,S):
		for a in range(0,A):	
			for sPrime in range(0,S):
				V_new[s] += totalProbs[s][a] * T_est[s][a][sPrime] * (R_est[s][a][sPrime] + gamma * V[sPrime])

	if (norm_fn(V_new, V) < 1e-6): 
		break	

	V = V_new[:]

Vals_est = V

####################################################################################################################################

for i in range(S):
	print(Vals_est[i])


### Code to test the rmsd errors of the estimated Values against the Actual Values

# soln_file_path  = sys.argv[3]
# lines2 = []
# with open(soln_file_path, 'r') as f:
# 	lines2 = f.readlines()

# Act_Values = [float(x.rstrip()) for x in lines2]

# def sd(a, b) : 
# 	return sum([(x-y)*(x-y) for x,y in zip(a,b)])

# print("The squared difference error is ", sd(Act_Values, Vals_est))