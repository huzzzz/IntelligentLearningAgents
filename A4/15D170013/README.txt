To generate the plots : 

1) Create a directory called plots in the current directory
2) Run the bash script 'generate_results.sh'
 
Note : 
This code generates a temporary out.txt file, for internal use.
Also the code generates the 4 plots in an iterative manner and we can only move to the next graph after the user closes the first graph.

The plots for the 3 experiments and the cumulative plots plotted together are generated in the plots folder.

------------------------------------------------------------------------------------------------------------------------------------------

Files :
1) windyGrid.py : python file for the environment
2) sarsa.py : python file with the code of training the sarsa agent and plotting the time step vs episode graphs
3) generate_results.sh :  Bash script used to generate all the data and plots
4) generate_plot_together.py : python script that takes in the outputs generated in the out.txt file and generates the graph
5) plots/ : folder containing the plots
6) report.pdf : Report

------------------------------------------------------------------------------------------------------------------------------------------

Usage : 
sarsa.py :  python3 sarsa.py num_actions is_stochastic file_name_plot
generate_plot_together.py : python3 generate_plot_together.py file_name 

------------------------------------------------------------------------------------------------------------------------------------------