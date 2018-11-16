#!/bin/bash

PWD=`pwd`

port=5001
nRuns=100
hostname="localhost"

# Allowed values for algorithm parameter(case-sensitive)
# 1. epsilon-greedy 
# 2. UCB 
# 3. KL-UCB 
# 4. Thompson-Sampling
# 5. rr

# algorithm="rr"
algorithms="epsilon-greedy Thompson-Sampling KL-UCB UCB"
# algorithm="epsilon-greedy"
# algorithm="Thompson-Sampling"
horizon=1000
epsilon=0.25
numArms=5
randomSeed=3

bandInstanceChoices="instance-bernoulli-"

banditFile="$PWD/data/instance-histogram-5.txt"

OUTPUTDIR=./output
SERVERDIR=./server
CLIENTDIR=./client

numArmsChoices="5 25"
# bandInstanceChoices="betaDist_ instance-bernoulli- instance-histogram-"
horizonChoices="1000 10000"
epsilonChoices="0.05 0.2 0.5 0.75 0.95"
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
						mkdir -p $OUTPUTFILEDIR
							
						port=5001
						for ((i =0; i < 100; i++))
						do 
							# echo $banditFile
							# echo "AHSKJKKKKJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ"

							randomSeed=$RANDOMn
							
							# echo $randomSeed

							OUTPUTFILE="../$OUTPUTFILEDIR/serverlog$i.txt"
							
							pushd $SERVERDIR > /dev/null
							cmd="./startserver.sh $numArmsChoice $horizonChoice $port $banditFile $randomSeed $OUTPUTFILE &"
							
							$cmd 
							popd > /dev/null

							sleep 0.1

							pushd $CLIENTDIR > /dev/null
							cmd="./startclient.sh $numArms $horizon $hostname $port $randomSeed $algorithm $epsilon&"
							
							$cmd > /dev/null
							popd > /dev/null

							((port++)) 
						done

						wait
						echo "$counter Done"
						((counter++))						
					done
				done		
			else
				for horizonChoice in $horizonChoices
				do
					OUTPUTFILEDIR="$OUTPUTSUBDIR/$horizonChoice/$algorithm/$epsilon"
					mkdir -p $OUTPUTFILEDIR
						
					port=5001
					for ((i =0; i < 100; i++))
					do 
						randomSeed=$RANDOM
					
						OUTPUTFILE="../$OUTPUTFILEDIR/serverlog$i.txt"
						
						pushd $SERVERDIR > /dev/null
						cmd="./startserver.sh $numArmsChoice $horizonChoice $port $banditFile $randomSeed $OUTPUTFILE &"
						
						$cmd 
						popd > /dev/null

						sleep 0.1

						pushd $CLIENTDIR > /dev/null
						cmd="./startclient.sh $numArms $horizon $hostname $port $randomSeed $algorithm $epsilon&"
						
						$cmd > /dev/null
						popd > /dev/null

						((port++)) 
					done

					wait
					echo "$counter Done"
					((counter++))						
				done
			fi
		done
	done
done
