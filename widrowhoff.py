from random import randrange
import matplotlib.pyplot as plt
from math import sqrt
from copy import deepcopy

lrate = 0.7
bvec = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
theta = 0.01
class1 = [[1, 2, 7], [1, 8, 1], [1, 7, 5], [1, 6, 3], [1, 7, 8], [1, 5, 9], [1, 4, 5], [1, 4, 3.5], [1, 3.5, -3]]
class2 = [[1, 4, 2], [1, -1, -1], [1, 1, 3], [1, 3, -2], [1, 5, 3.25], [1, 2, 4], [1, 7, 1], [1, 6.5, 5], [1, 7.5, 3]]

weight = [0,0,0]
weight[0] = 1
weight[1] = 1
weight[2] = 1

# normalize class2
for i in class2:
	for j in range(len(i)):
		i[j] = -i[j]

# create dataset
dataset = []
for i in class1:
	dataset.append(i)
for i in class2:
	dataset.append(i)


print weight
# main loop
k = 0
count = 1
overallcnt = 0
while 1:
	value = 0
	for i in range(0,3):
		value += weight[i] * dataset[k][i]
	value = bvec[k] - value

	lr = lrate/count

	temp = deepcopy(dataset[k])
	for i in range(len(temp)):
		temp[i] = temp[i] * value * lr

	if sqrt((temp[0]*temp[0]) + (temp[1]*temp[1]) + (temp[2]*temp[2])) < theta:
		overallcnt += 1
		if overallcnt == 1:
			break
	else:
		overallcnt = 0
		for j in range(0,3):
			weight[j] = weight[j] + temp[j]

	k += 1
	if k == len(dataset):
		k %= len(dataset)
	count += 1

print weight

# denormalize
for i in class2:
	for j in range(len(i)):
		i[j] = -i[j]

class12Dx = []
class12Dy = []
class22Dx = []
class22Dy = []
for i in range(len(class1)):
	class12Dx.append(class1[i][1])
	class12Dy.append(class1[i][2])
for i in range(len(class2)):
	class22Dx.append(class2[i][1])
	class22Dy.append(class2[i][2])

plt.plot(class12Dx, class12Dy, 'bo')
plt.plot(class22Dx, class22Dy, 'ro')

# find points on x and y axes
y1 = -(weight[0]/weight[2]) 
x2 = -(weight[0]/weight[1])

lines, = plt.plot([0, y1], [x2, 0], label='widrowhoff')
plt.setp(lines, color='r', linewidth=1.0)

plt.axis([-10, 10, -10, 10])

plt.legend([lines], ['Widrow Hoff with linearly inseparable points'])

plt.show()


