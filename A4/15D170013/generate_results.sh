python3 sarsa.py 4 0 windyGridWorld > out.txt
python3 sarsa.py 8 0 kingsMovesWindyGridWorld >> out.txt 
python3 sarsa.py 8 1 stochWindyGridWorld >> out.txt

python3 generate_plot_together.py out.txt
rm out.txt 