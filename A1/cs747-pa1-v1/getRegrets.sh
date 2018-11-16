#!/bin/bash

algorithms="epsilon-greedy Thompson-Sampling KL-UCB UCB"
horizon=1000
epsilon=0.25
numArms=5
randomSeed=3

banditFile="$PWD/data/instance-histogram-5.txt"

OUTPUTDIR=./output
SERVERDIR=./server
CLIENTDIR=./client

numArmsChoices="5 25"
bandInstanceChoices="betaDist_ instance-bernoulli- instance-histogram-"
epsilonChoices="0.05 0.2 0.5 0.75 0.95"
horizonChoices="1000 2000"
counter=1
for numArmsChoice in $numArmsChoices
do
	for bandInstanceChoice in $bandInstanceChoices
	do
		# echo $bandInstanceChoice
		# echo $numArmsChoice
		banditFile="$PWD/data/$bandInstanceChoice$numArmsChoice.txt"
		OUTPUTSUBDIR="$OUTPUTDIR/$bandInstanceChoice$numArmsChoice"
		for algorithm in $algorithms
		do
			if [ $algorithm == 'epsilon-greedy' ] 
			then 
				for epsilonChoice in $epsilonChoices
				do
					for horizonChoice in $horizonChoices
					do
						OUTPUTFILEDIR="$OUTPUTSUBDIR/$horizonChoice/$algorithm/$epsilonChoice"
						OUTPUTFILE="$OUTPUTFILEDIR/Regrets.txt"
						touch OUTPUTFILE
						echo $OUTPUTFILEDIR > $OUTPUTFILE
						for file  in $OUTPUTFILEDIR/*.txt
						do		
							grep "Regret" $file >> $OUTPUTFILE 
						done
						echo "$counter Done"
						((counter++))						
					done
				done		
			else
				for horizonChoice in $horizonChoices
				do
					OUTPUTFILEDIR="$OUTPUTSUBDIR/$horizonChoice/$algorithm/$epsilon"
					OUTPUTFILE="$OUTPUTFILEDIR/Regrets.txt"
					touch OUTPUTFILE
					echo $OUTPUTFILEDIR > $OUTPUTFILE
					for file  in $OUTPUTFILEDIR/*.txt
					do	
						grep "Reward" $file >> $OUTPUTFILE 
					done
					echo "$counter Done"
					((counter++))						
				done
			fi
		done
	done
done
