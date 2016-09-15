import numpy as np
import matplotlib.pyplot as plt
from random import randint, seed, random
from sys import exit
from math import sqrt

numbers = [3, 5, 7]
d = 64
nH = 20
o = 2
eta = 0.7
theta = 0.001

def outputmap(num):
	if num == numbers[0]:
		return ([0, 0])
	elif num == numbers[1]:
		return ([0, 1])
	else:
		return ([1, 0])

def parseandprocess(filename):
	dataarray = []
	numarray = []
	numberofones = [0] * 8
	tempdata = [1] # To account for the bias term
	with open(filename) as f:
		content = f.read().splitlines()
		content = content[21:]
		while 1:
			for i in range(0,33):
				if i == 32:
					if int(content[i]) in numbers:					
						dataarray.append(tempdata)
						numarray.append(int(content[i]))
				if i != 32:
					for j in range(len(content[i])):
						if int(content[i][j]) == 1:
							numberofones[j/4] += 1
				if ((i + 1) % 4) == 0:
					for k in numberofones:
						if k/8 > 0.5:
							tempdata.append(1)
						elif k/8 == 0.5:
							tempdata.append(randint(0,1))
						else:
							tempdata.append(0)
					numberofones = [0] * 8
			tempdata = [1]
			content = content[33:]
			if not content:
				break

	return numarray, dataarray

def sigmoidfunc(x, derivativeflag = False):
	sigma = 1/(1 + np.exp(-x))
	if not derivativeflag:
		return sigma
	else:
		return (sigma * (1 - sigma))

def nn(num, data):
	#initialize wji and wkj
	wji = np.empty([d + 1, nH])
	wkj = np.empty([nH + 1, o])
	for i in range(len(wji)):
		for j in range(len(wji[i])):
			if 	randint(0,1):
				wji[i][j] = random() * (1/sqrt(d))
			else:
				wji[i][j] = -(random() * (1/sqrt(d)))
	for i in range(len(wkj)):
		for j in range(len(wkj[i])):
			if randint(0,1):
				wkj[i][j] = random() * (1/sqrt(nH))
			else:
				wkj[i][j] = -(random() * (1/sqrt(nH)))

	while 1:
		randIndex = randint(0,len(num) - 1)
		xi = np.array(data[randIndex])
		netj = np.dot(xi, wji)
		yj = np.array([1])
		yj = np.append(yj, sigmoidfunc(netj))

		netk = np.dot(yj, wkj)
		zk = sigmoidfunc(netk)

		tk = outputmap(num[randIndex])
		
		copywkj = wkj[:]
		deltak = []
		for k in range(o):
			diff = (tk[k] - zk[k])
			deltak.append(diff*sigmoidfunc(netk[k], True))
			for j in range(nH + 1):
				wkj[j][k] += eta * deltak[k] * yj[j]

		for j in range(nH):
			sums = 0
			for k in range(o):
				sums += deltak[k] * copywkj[j][k]
			for i in range(d + 1):
				wji[i][j] += eta * xi[i] * sigmoidfunc(netj[j], True) * sums

		delJ = tk - zk
		if np.linalg.norm(delJ) < theta:
			break
		
	return wji, wkj

def testing(wji, wkj, testnum, testdata):
	count = 0
	for i in range(len(testdata)):
		number = testnum[i]
		tdata = np.array(testdata[i])
		netj = np.dot(tdata, wji)
		yj = np.array([1])
		yj = np.append(yj, sigmoidfunc(netj))

		netk = np.dot(yj, wkj)
		zk = sigmoidfunc(netk)

		for j in range(len(zk)):
			if zk[j] > 0.5:
				zk[j] = 1
			elif zk[j] == 0.5:
				zk[j] = randint(0,1)
			else:
				zk[j] = 0

		tk = outputmap(number)

		if zk[0] == tk[0] and zk[1] == tk[1]:
			count += 1

	print (float(count)/float(len(testdata))) * 100, "percent"

def main():
	seed()
	np.random.seed()
	num, data = parseandprocess("optdigits-orig.tra")
	testnum, testdata = parseandprocess("optdigits-orig.cv")

	wji, wkj = nn(num, data)
	testing(wji, wkj, testnum, testdata)

if __name__ == '__main__':
	main()

