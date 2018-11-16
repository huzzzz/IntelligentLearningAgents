import matplotlib.pyplot as plt
import os, sys
import numpy as np
import matplotlib.cm as cm


avg_regrets_dict_per_instance = {}
algorithms = ["epsilon-greedy", "Thompson-Sampling", "KL-UCB", "UCB"]
numArmsChoices=["5","25"]
epsilons = ["0.05", "0.2", "0.5" ,"0.75", "0.95"]
horizonChoices=["1000","10000"]
# bandInstanceChoices=["betaDist_","instance-bernoulli-","instance-histogram-"]
bandInstanceChoices=["instance-bernoulli-"]

OUTPUTDIR = os.getcwd() + "/output"
fig_num = 0

for numArmsChoice in numArmsChoices:
	for bandInstanceChoice in bandInstanceChoices:
		
		banditFile="data/"+bandInstanceChoice+numArmsChoice+".txt"
		OUTPUTSUBDIR=OUTPUTDIR+"/"+bandInstanceChoice+numArmsChoice

		for horizonChoice in horizonChoices:

			plt.figure(fig_num)
			fig_num+=1
			cols = cm.rainbow(np.linspace(0, 1, 8))
			col_index = 0
			for algorithm in algorithms:
				if algorithm == 'epsilon-greedy' : 
					for epsilonChoice in epsilons:						
						OUTPUTFILEDIR = OUTPUTSUBDIR+"/" + horizonChoice+"/"+algorithm+"/"+epsilonChoice
						regrets_array = [0] * int(horizonChoice)
						for file in os.listdir(OUTPUTFILEDIR):
							curr_regret = ''
							with open(os.path.join(OUTPUTFILEDIR,file), 'r') as f:
								curr_regret = f.readlines()
							curr_regret = list(map(lambda x : float(x.rstrip()), curr_regret))
							regrets_array = [x+y for x, y in zip(regrets_array, curr_regret)]
						regrets_array_final = [(x/100) for x in regrets_array]
						regrets_array_str = [str(x/100) for x in regrets_array] 

						with open(os.path.join(OUTPUTFILEDIR,"avgRegrets.txt"), 'w') as f:
							f.write("\n".join(regrets_array_str))
						plt.plot(regrets_array_final, color=cols[col_index], label=algorithm+" epsilon : "+epsilonChoice)
						col_index+=1
				else:
					epsilonChoice = "0.25"
					OUTPUTFILEDIR = OUTPUTSUBDIR+"/" + horizonChoice+"/"+algorithm+"/"+epsilonChoice
					regrets_array = [0] * int(horizonChoice)
					for file in os.listdir(OUTPUTFILEDIR):
						curr_regret = ''
						with open(os.path.join(OUTPUTFILEDIR,file), 'r') as f:
							curr_regret = f.readlines()
						curr_regret = list(map(lambda x : float(x.rstrip()), curr_regret))
						regrets_array = [x+y for x, y in zip(regrets_array, curr_regret)]
					regrets_array_str = [str(x/100) for x in  regrets_array] 
					regrets_array_final = [x/100 for x in regrets_array]

					with open(os.path.join(OUTPUTFILEDIR,"avgRegrets.txt"), 'w') as f:
						f.write("\n".join(regrets_array_str))
					plt.plot(regrets_array_final,color= cols[col_index], label=algorithm)
					col_index+=1

			plt.title('Bandit Instance: '+bandInstanceChoice+numArmsChoice +"  horizonChoice: "+ horizonChoice)
			plt.legend()
			plt.xlabel("Time")
			plt.ylabel("Regret")
			plt.savefig("client/report/plots/"+bandInstanceChoice+numArmsChoice+"_"+horizonChoice+".png")