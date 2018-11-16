SERVERDIR=./server
CLIENTDIR=./client

PWD=`pwd`

port=5000
hostname="localhost"

for instance in $(ls ./data); do
	if [[ $instance == *25.txt ]]; then
		numArms=25
	else
		numArms=5
	fi
	# for algo_eps in {"epsilon-greedy 0.001","epsilon-greedy 0.01","epsilon-greedy 0.1","epsilon-greedy 0.25","epsilon-greedy 0.5","KL-UCB 0"}; do
	for algo_eps in {"epsilon-greedy 0.01","epsilon-greedy 0.1","epsilon-greedy 0.25","epsilon-greedy 0.5", "epsilon-greedy 0.8","UCB 0","KL-UCB 0","Thompson-Sampling 0","rr 0"}; do
		arr=($algo_eps)
		algo=${arr[0]}
		eps=${arr[1]}
		for horizon in {1000,10000}; do
			for seed in {1..100}; do
				randomSeed=$RANDOM
				# port=$((port+1))

				echo "i=${instance}_a=${algo}_e=${eps}_h=${horizon}_s=${seed}_n=${numArms}_p=${port}"

				serverfile="../results/${instance}_${algo}_${eps}_${horizon}_${randomSeed}_${numArms}_server.txt"
				clientfile="../results/${instance}_${algo}_${eps}_${horizon}_${randomSeed}_${numArms}_client.txt"
				# echo $clientfile
				# echo $serverfile

				cmd1="./startserver.sh $numArms $horizon $((port+seed)) ../data/$instance $randomSeed $serverfile"
				cmd2="./startclient.sh $numArms $horizon $hostname $((port+seed)) $((randomSeed+1)) $algo $eps"
				# echo $cmd
				(pushd $SERVERDIR > /dev/null; $cmd1; popd > /dev/null; sleep 0.4; pushd $CLIENTDIR > /dev/null; $cmd2 > $clientfile; popd > /dev/null) &

			done
			wait
		done
	done
done
