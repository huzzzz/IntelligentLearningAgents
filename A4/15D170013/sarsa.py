from windyGrid import *
import random
import matplotlib.pyplot as plt
import sys
	

## User input defined
A = int(sys.argv[1])
isStoch = int(sys.argv[2])
graph_name = sys.argv[3]	

## Predefined Variables
alpha = 0.5
gamma = 1
epsilon = 0.1
S = n*m

def getGreedyAct(s, epsilon):
	maxAct = 0
	if (random.uniform(0,1) < epsilon):
		maxAct = random.choice(list(range(0, A)))		
	else:
		for act in range(0, A):
			if (Q[s][act] > Q[s][maxAct]):
				maxAct = act
	return maxAct

numruns = 10
numEpisodes = 170
epsisode_end_cum = [0]*numEpisodes

for run in range(numruns):
	time_step = 0
	Q = {s : {a : 0 for a in range(A)} for s in range(S)}	
	numEpisodes = 170
	epsisode_end = [0]*numEpisodes
		
	for ep in range(numEpisodes):
		s = start_state
		a = getGreedyAct(s, epsilon)

		while (s != goal_state):
			(sPrime, reward) = takeAction(s, a, isStoch)
			aPrime = getGreedyAct(sPrime, epsilon)
			Q[s][a] += alpha*(reward + gamma*Q[sPrime][aPrime] - Q[s][a])
			s = sPrime
			a = aPrime
			time_step += 1

		epsisode_end[ep] = time_step

	epsisode_end_cum = [x + y for x, y in zip(epsisode_end_cum, epsisode_end)]

epsisode_end_cum = [int(x / numruns) for x in epsisode_end_cum]

print(', '.join(map(str, epsisode_end_cum)))
plt.plot(epsisode_end_cum, list(range(1, len(epsisode_end_cum) + 1)))
plt.title('Plot Performance '+ graph_name)
plt.xlabel("Time Steps")
plt.ylabel("Episodes")
plt.savefig("plots/"+graph_name+".png")
plt.show()