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
algorithm="epsilon-greedy"
# algorithm="UCB"
# algorithm="KL-UCB"
# algorithm="Thompson-Sampling"
horizon=1000
epsilon=1
numArms=5
randomSeed=$RANDOM

banditFile="$PWD/data/instance-histogram-5.txt"



SERVERDIR=./server
CLIENTDIR=./client

OUTPUTFILE=$PWD/serverlog.txt

pushd $SERVERDIR > /dev/null
cmd="./startserver.sh $numArms $horizon $port $banditFile $randomSeed $OUTPUTFILE &"
# echo $cmd
$cmd 
popd > /dev/null

sleep 1

pushd $CLIENTDIR > /dev/null
cmd="./startclient.sh $numArms $horizon $hostname $port $randomSeed $algorithm $epsilon&"
#echo $cmd
# $cmd > /dev/null
$cmd	
popd > /dev/null

