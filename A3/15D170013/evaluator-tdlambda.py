import os, sys

file_path = sys.argv[1]
lambda_val = float(sys.argv[2])

lines = []
with open(file_path, 'r') as f:
	lines = f.readlines()

S = int(lines[0])
A = int(lines[1])
gamma = float(lines[2])
ind = 3

Values = [0]*S
etrace = [0]*S

while (ind < len(lines) - 1):
	alpha_t = float(9) / (ind - 2)

	[s, a, r] = lines[ind].rstrip().split("\t")
	s = int(s)
	r = float(r)
	sPrime = int(lines[ind+1].rstrip().split("\t")[0])
	
	delta = r + gamma * Values[sPrime] - Values[s]
	etrace[s] = etrace[s] + 1
	
	for state in range(S):
		Values[state] += alpha_t * delta * etrace[state]
		etrace[state] *= gamma * lambda_val

	ind += 1

for i in range(S):
	print(Values[i])

Vals_est = Values

### Code to test the rmsd errors of the estimated Values against the Actual Values

# soln_file_path  = sys.argv[3]
# lines2 = []
# with open(soln_file_path, 'r') as f:
# 	lines2 = f.readlines()

# Act_Values = [float(x.rstrip()) for x in lines2]

# def sd(a, b) : 
# 	return sum([(x-y)*(x-y) for x,y in zip(a,b)])

# print("The squared difference error is ", sd(Act_Values, Vals_est))