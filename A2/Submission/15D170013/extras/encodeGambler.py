import sys

## Construct the MDP in terms of python variables
ph = float(sys.argv[1])

S = 101
A = 51

T = {s : {a : {s_prime : 0 for s_prime in range(0, S)} for a in range(0, A)} for s in range(0,S)}   
R = {s : {a : {s_prime : 0 for s_prime in range(0, S)} for a in range(0, A)} for s in range(0,S)}

for s in range(0,S):
	for a in range(1, A):
		if a > min(s, S-s-1):
			break
		T[s][a][s+a] = ph
		T[s][a][s-a] = 1 - ph
		
		if (s + a >= S - 1):
			R[s][a][s+a] = 1

gamma = 1
mdp_type = 'episodic'

## Print in the format specified
print(S)
print(A)

for s in range(0, S):
	for a in range(0, A):
		for sPrime in range(0, S):
			print(str(R[s][a][sPrime]) + "\t", end='')

		print("\n", end='')

for s in range(0, S):
	for a in range(0, A):
		for sPrime in range(0, S):
			print(str(T[s][a][sPrime]) + "\t", end='')

		print("\n", end='' )

print(gamma)
print(mdp_type)