from random import randrange
import matplotlib.pyplot as plt
from copy import deepcopy
from math import sqrt
from time import time

class1 = [[1, 2, 7], [1, 8, 1], [1, 7, 5], [1, 6, 3], [1, 7, 8], [1, 5, 9], [1, 4, 5]]
class2 = [[1, 4, 2], [1, -1, -1], [1, 1, 3], [1, 3, -2], [1, 5, 3.25], [1, 2, 4], [1, 7, 1]]

global line1
global line2
global line3
global line4

def singlesampleperceptron(weight):
	start = time()

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

	# main loop
	k = 0
	count = 0
	while 1:
		value = 0
		for i in range(0,3):
			value += weight[i] * dataset[k][i]

		if value > 0:
			count += 1
			if count == len(dataset):
				break
		else:
			count = 0
			for i in range(0,3):
				weight[i] += dataset[k][i]

		k += 1
		if k == len(dataset):
			k %= len(dataset)

	print weight
	end = time()
	print end - start, "Time"
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

	plt.plot(class12Dx, class12Dy, 'ro')
	plt.plot(class22Dx, class22Dy, 'bo')

	# find points on x and y axes
	y1 = -(weight[0]/weight[2]) 
	x2 = -(weight[0]/weight[1])

	line1, = plt.plot([0, y1], [x2, 0], label = "ssp")
	plt.setp(line1, color='r', linewidth=1.0)

	return line1, weight

def singlesampleperceptronmargin(margin, weight):
	start = time()

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

	# main loop
	k = 0
	count = 0
	while 1:
		value = 0
		for i in range(0,3):
			value += weight[i] * dataset[k][i]

		if value > margin:
			count += 1
			if count == len(dataset):
				break
		else:
			count = 0
			for i in range(0,3):
				weight[i] += dataset[k][i]

		k += 1
		if k == len(dataset):
			k %= len(dataset)

	print weight
	end = time()
	print end - start, "Time"

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

	plt.plot(class12Dx, class12Dy, 'ro')
	plt.plot(class22Dx, class22Dy, 'bo')

	# find points on x and y axes
	y1 = -(weight[0]/weight[2]) 
	x2 = -(weight[0]/weight[1])

	line2, = plt.plot([0, y1], [x2, 0], label='sspm')
	plt.setp(line2, color='b', linewidth=1.0)

	return line2, weight

def relaxationalgo(lrate, margin, weight):
	start = time()

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

	# main loop
	k = 0
	count = 0
	overallcount = 0
	while 1:
		overallcount += 1
		value = 0
		for i in range(0,3):
			value += weight[i] * dataset[k][i]
		if value > margin:
			count += 1
			if count == len(dataset):
				break
		else:
			count = 0

			value = 0
			for i in range(0,3):
				value += (weight[i] * dataset[k][i])
			value = (-(value) + margin)/((dataset[k][0]*dataset[k][0]) + (dataset[k][1]*dataset[k][1]) + (dataset[k][2]*dataset[k][2]))

			for j in range(0,3):
				weight[j] = weight[j] + (lrate * value * dataset[k][j])
		
		k += 1
		if k == len(dataset):
			k %= len(dataset)

	print weight
	end = time()
	print end - start, "Time"

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

	plt.plot(class12Dx, class12Dy, 'ro')
	plt.plot(class22Dx, class22Dy, 'bo')

	# find points on x and y axes
	y1 = -(weight[0]/weight[2]) 
	x2 = -(weight[0]/weight[1])

	line3, = plt.plot([0, y1], [x2, 0], label='relaxationalgo')
	plt.setp(line3, color='g', linewidth=1.0)

	return line3, weight

def widrowhoff(lrate, theta, weight):
	start = time()
	bvec = [1,1,1,1,1,1,1,1,1,1,1,1,1,1]

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
	end = time()
	print end - start, "Time"

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

	plt.plot(class12Dx, class12Dy, 'ro')
	plt.plot(class22Dx, class22Dy, 'bo')

	# find points on x and y axes
	y1 = -(weight[0]/weight[2]) 
	x2 = -(weight[0]/weight[1])

	line4, = plt.plot([0, y1], [x2, 0], label='widrowhoff')
	plt.setp(line4, color='y', linewidth=1.0)

	return line4, weight

def main():
	weight = [1,1,1]

	weight1 = deepcopy(weight)
	line1, weight1 = singlesampleperceptron(weight1)
	
	weight2 = deepcopy(weight)
	margin = 0.5
	line2, weight2 = singlesampleperceptronmargin(margin, weight2)

	weight3 = deepcopy(weight)
	lrate = 2
	margin = 0.5
	line3, weight3 = relaxationalgo(lrate, margin, weight3)

	weight4 = deepcopy(weight)
	lrate = 0.7
	theta = 0.01
	line4, weight4 = widrowhoff(lrate, theta, weight4)

	plt.axis([-5, 15, -5, 15])
	plt.legend([line1, line2, line3, line4], ['Single Sample Perceptron' + str(weight1), 'Perceptron with margin' + str(weight2), 'Perceptron with Margin and Relaxation' + str(weight3), 'Widrow Hoff' + str(weight4)])
	plt.show()

if __name__ == '__main__':
	main()