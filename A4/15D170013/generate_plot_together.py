import matplotlib.pyplot as plt
import sys
 
out_file = sys.argv[1]
with open(out_file, 'r') as f:
	lines = f.readlines()

lines = [x.rstrip().split(',') for x in lines]
linesInt = [[int(x) for x in y] for y in lines]

plt.plot(linesInt[0], list(range(1, len(linesInt[0]) + 1)), label ='windyGrid')
plt.plot(linesInt[1], list(range(1, len(linesInt[1]) + 1)), label ='kingMovesWindyGrid')
plt.plot(linesInt[2], list(range(1, len(linesInt[2]) + 1)), label ='stochWindyGrid')
plt.title('Performance Plot')
plt.legend()
plt.xlabel("Time Steps")
plt.ylabel("Episodes")
plt.savefig("plots/Comparative.png")
plt.show()
