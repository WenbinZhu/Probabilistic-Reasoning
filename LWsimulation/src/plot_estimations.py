import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

def plot_estimation(path):
	with open(path) as file:
		for line in file.readlines():
			line = line[0 : -1].split(" ")
			label = line[0]
			y = line[1 : -1]
			x = [10 ** (i + 3) for i in range(min(4, len(y)))]
			x.extend([1000000 + (i + 1) * 1000000 for i in range(len(y) - len(x))])
			
			# red_patch = mpatches.Patch(color='green', label=label)
			# plt.legend(handles=[red_patch])
			points,  = plt.plot(x, y, "--go", label=label)
			plt.legend(handler_map={points: HandlerLine2D(numpoints=3)})
			plt.xlabel('Number of Samples')
			plt.ylabel('Probability Estimation')
			plt.show()
			

	# plt.yscale('log')
	

if __name__ == "__main__":
	path = "../estimation_history.txt"
	plot_estimation(path);