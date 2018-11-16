#!/bin/sh

for i in 0.2 0.4 0.6 0.8
	do
		mdp_file_path=gamblermdp$i.txt

		python3 encodeGambler.py $i > $mdp_file_path;

	done;

for algorithm in lp hpi
	do
	for i in 0.2 0.4 0.6 0.8
		do

			mdp_file_path=gamblermdp$i.txt
			sol_file_path=sol_$algorithm$i.txt

			python3 planner.py $mdp_file_path $algorithm > $sol_file_path;

		done;
	done;

for algorithm in lp hpi
	do
		python3 plotting_script.py . lp
		python3 plotting_script.py . hpi		
	done;