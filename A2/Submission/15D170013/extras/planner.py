import sys
import pulp as lp
import numpy as np
import argparse


gridfile = sys.argv[1]
algorithm = sys.argv[2]

with open(gridfile, 'r') as f:
	lines = f.readlines()

lines = [l.rstrip().split("\t") for l in lines]

S = int(lines[0][0])
A = int(lines[1][0])

i = 2

T = {s : {a : {s_prime : 0 for s_prime in range(0, S)} for a in range(0, A)} for s in range(0,S)}	
R = {s : {a : {s_prime : 0 for s_prime in range(0, S)} for a in range(0, A)} for s in range(0,S)}

for s in range(0, S):
	for a in range(0, A):
		for sPrime in range(0, S):
			R[s][a][sPrime] = float(lines[i][sPrime])
		i+=1

for s in range(0, S):
	for a in range(0, A):
		for sPrime in range(0, S):
			T[s][a][sPrime] = float(lines[i][sPrime])
		i+=1

gamma = float(lines[-2][0])
mdp_type = lines[-1][0]
i += 2
	
Opt_Vals = []
Opt_Pols = []

if(algorithm == 'lp'):
	
	prob = lp.LpProblem("MDP Values Solve Problem", lp.LpMinimize)
	V_s = []

	for s in range(0, S):
		V_s.append(lp.LpVariable("V_" + str(s), cat= 'Continuous'))
	
	if mdp_type == "episodic":
		V_s[S-1] = lp.LpVariable("V_" + str(S-1), cat= 'Continuous',  lowBound=0, upBound=0)

	prob += lp.lpSum(V_s), "Sum of Values"

	for s in range(0, S):
		for a in range(0, A):
			temp = []
			for sPrime in range(0, S):
				temp.append(T[s][a][sPrime] * (R[s][a][sPrime] + gamma * V_s[sPrime]))
			prob += V_s[s] >= lp.lpSum(temp)
		
	prob.solve()

	# print(lp.LpStatus[prob.status])
	
	# if (lp.LpStatus[prob.status] != 'Optimal'):
	# 	print("Non Optimal Solution")
	# 	print(lp.LpStatus[prob.status])

	for variable in V_s:
		Opt_Vals.append(variable.varValue)

	for s in range(0,S):
		best_val = -float("INF")
		best_val_act = 0 
		for a in range(0,A):
			temp = []
			for sPrime in range(0, S):
				temp.append(T[s][a][sPrime] * (R[s][a][sPrime] + gamma * Opt_Vals[sPrime]))
			if (sum(temp) > best_val):
				best_val = sum(temp)
				best_val_act = a

		Opt_Pols.append(best_val_act)

elif(algorithm == 'hpi'):

	Opt_Pols = []
	Opt_Pols_New = [0] * S

	def Q_func(s, a, Curr_Vs):
		return sum([T[s][a][sPrime]*(R[s][a][sPrime] + gamma * Curr_Vs[sPrime]) for sPrime in range(0,S)])
	
	Curr_Vs = []

	while(Opt_Pols_New != Opt_Pols):
		
		Opt_Pols = Opt_Pols_New.copy()

		A_arr = [[T[s][Opt_Pols[s]][sPrime]*gamma for sPrime in range(0,S)] for s in range(0,S)]
		I = np.identity(S)
		A_arr = I - np.array(A_arr)
		B_arr = np.array([sum([T[s][Opt_Pols[s]][sPrime] * R[s][Opt_Pols[s]][sPrime] for sPrime in range(0,S)]) for s in range(0, S)])	
		
		if mdp_type == 'episodic':
			A_arr[S-1] = I[S-1]
			B_arr[S-1] = 0

		for s in range(0, S):
			if not np.any(A_arr[s]):
				A_arr[s] = I[s]
				B_arr[s] = 0

		Curr_Vs = np.linalg.solve(A_arr, B_arr);
		
		threshold = 1e-6
		for s in range(0,S):
			for a in range(0,A):
				if (Q_func(s, a, Curr_Vs) - Curr_Vs[s] > threshold) and (Opt_Pols_New[s] != a): 
					Opt_Pols_New[s] = a
					break

	Opt_Vals = Curr_Vs.tolist()

for s in range(0, S):
	print(str(Opt_Vals[s]) + "\t" + str(Opt_Pols[s]))
