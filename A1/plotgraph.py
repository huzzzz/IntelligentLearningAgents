import os
import matplotlib.pyplot as plt

data = {}

algos = ["epsilon-greedy 0.0001","epsilon-greedy 0.001","epsilon-greedy 0.01","epsilon-greedy 0.25","epsilon-greedy 0.5","UCB 0","KL-UCB 0","Thompson-Sampling 0","rr 0"]

resultsfiles = set(os.listdir('results'))

count = 0

for datafile in os.listdir('data'):
	data[datafile] = {}
	if '25' in datafile:
		arms = 25
	else:
		arms = 5
	for horizon in [1000, 10000]:
		for algo in algos:
			c2 = 0
			regret = [0 for i in range(horizon)]
			for t in range(1, 101):

				fileprefix = datafile+'_'+algo.replace(' ','_')+'_'+str(horizon)+'_'+str(t)+'_'+str(arms)
				clientfile = fileprefix+'_client.txt'
				serverfile = fileprefix+'_server.txt'
				if serverfile in resultsfiles:
					maxProb = float(open('results/'+serverfile).readlines()[-3].split()[0][7:])
				if serverfile in resultsfiles:
					lines = open('results/'+serverfile).readlines()
					for line in lines[3:-3:2]:
						regret[int(line.split()[5].split('.')[0])-1] += float(line.split()[2][:-1])
					count += 1
					c2 += 1
			for i in range(1, horizon):
				regret[i] += regret[i-1]
			# print(maxProb)
			for i in range(0, horizon):
				regret[i] = (i+1)*maxProb - regret[i]/100

			print(*(regret[:10]))
			plt.plot(range(1, horizon+1), regret, label=algo)
			if 0 < c2 < 100:
				print(datafile+'_'+algo.replace(' ','_')+'_'+str(horizon), c2)
		plt.legend(loc='upper left')
		plt.title('Instance: '+datafile+'\nHorizon: '+str(horizon))
		plotfile = datafile+'-'+str(horizon)
		plt.savefig('plots/'+plotfile+'.png')
		plt.savefig('plots/'+plotfile+'.pdf')
		plt.clf()
		print(plotfile)
print(count)