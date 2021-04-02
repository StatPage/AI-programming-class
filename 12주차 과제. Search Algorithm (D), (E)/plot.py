import numpy as np
import matplotlib.pyplot as plt

# First-choice hill climbing
y1 = []
infile = open("FirstChoice.txt", 'r')
for line in infile:
    y1.append(float(line))
x1 = np.arange(len(y1))
infile.close()

# Simulated annealing
y2 =[]
infile = open('Simulated.txt', 'r')
for line in infile:
    y2.append(float(line))
x2 = np.arange(len(y2))
infile.close()

plt.plot(x1, y1)
plt.plot(x2, y2)
plt.xlabel('Number of Evaluations')
plt.ylabel('Tour Cost')
plt.title('Search Performance (TSP-100)')

plt.legend(['First-Choice HC', 'Simulated Annealing'])
plt.show()