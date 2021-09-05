# used to plot runtime graph
# pip install matplotlib
import matplotlib.pyplot as plot
import random
import time
import numpy as np
from driver import Aquarium, Skyscraper


def timer(f, file):
	start = time.time()
	f(file)
	return time.time() - start


x = [6, 15, 20, 25, 30]
y = [0, 0, 0, 0, 0]

# x = [4, 5, 6, 7]
# y = [0, 0, 0, 0]


for j in range(100):
	y[0] += timer(Aquarium, "ExtraTests/A3.txt")

for j in range(100):
	y[1] += timer(Aquarium, "ExtraTests/ICLP2.txt")

for j in range(100):
	y[2] += timer(Aquarium, "ExtraTests/ICLP3.txt")

for j in range(100):
	y[3] += timer(Aquarium, "ExtraTests/ICLP4.txt")

for j in range(100):
	y[4] += timer(Aquarium, "ExtraTests/ICLP5.txt")

y = [j/100 for j in y]

print(x)
print(y)

plot.plot(x, y, label = "Aquarium")
plot.legend()
plot.show()
