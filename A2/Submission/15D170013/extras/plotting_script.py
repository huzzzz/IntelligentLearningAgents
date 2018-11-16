import matplotlib.pyplot as plt
import sys
import numpy as np
import os

dir_name = sys.argv[1]
alg = sys.argv[2]

fig, ax = plt.subplots(1, 1)
fig2, ax2 = plt.subplots(1, 1)

Vals = {}
Pols = {}

p_h_vals = [0.2, 0.4, 0.6, 0.8]

for p_h in p_h_vals:

	file_name = os.path.join(dir_name, 'sol_' + alg + str(p_h) + ".txt")
	lines = open(file_name, 'r').readlines()
	formatted_lines = [x.rstrip().split("\t") for x in lines]

	Vals[p_h] = [float(x[0]) for x in formatted_lines]
	Pols[p_h] = [float(x[1]) for x in formatted_lines]

	# p_h = float(sys.argv[2])

	# lines = open(file_name, 'r').readlines()
	# formatted_lines = [x.rstrip().split("\t") for x in lines]

	# Vals[p_h] = [float(x[0]) for x in formatted_lines]
	# Pols[p_h] = [float(x[1]) for x in formatted_lines]

	ax.plot(Vals[p_h][:-1], label='p_h = ' + str(p_h))	
	ax2.plot(Pols[p_h][:-1], label='p_h = ' + str(p_h))

ax.set_xlabel('Capital / States')
ax.set_ylabel('Values')
ax.legend()

ax2.set_xlabel('Capital / States')
ax2.set_ylabel('Policies')
ax2.legend()

fig.savefig('Values Plot-'+alg+'.png')
plt.close(fig)

fig2.savefig('Policies Plot-'+alg+'.png')
plt.close(fig2)