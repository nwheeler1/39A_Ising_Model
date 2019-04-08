import random as r
import math as m
import numpy as np
import xlsxwriter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
from matplotlib import cm

#Initializes spins to either all parallel or randomly +-1
def createSpins(numSpins, parallel):
	if(parallel):
		spins = [1]*numSpins
	else:
		spins = [r.randint(0, 1)*2 - 1 for x in range(0,numSpins)]
	return spins

def flipSpins(spins, numTrials, equilibrium, beta, magField, J):
	energyVals = []
	magnetizationVals = []
	for i in range(0, numTrials):
		index = r.randint(0, len(spins) - 1)
		if(i >= equilibrium):
			energyVals.append(calculateEnergy(spins, magField))
			magnetizationVals.append(calculateMagnetization(spins))
		energyChange = J*((2*spins[(index-1) % len(spins)] + 2*spins[(index + 1) % len(spins)]) * spins[index]) - magField*2*spins[index]
		if(energyChange <= 0):
			spins[index] = -spins[index]
		else:
			spins[index] = -spins[index] if (r.uniform(0,1) <= m.pow(m.e, (-beta*energyChange))) else spins[index]
	return energyVals, magnetizationVals

def writeToSheet(sheet, list, startRow, column):
	for x in list:
		sheet.write(startRow, column, x)
		startRow += 1


def calculateEnergy(spins, magField):
	N = len(spins)
	energy = 0
	for x in range(0, N):
		energy += -spins[x]*spins[(x+1)%N] - magField*spins[x]
	return energy/N

def calculateMagnetization(spins):
	return sum(spins)/len(spins)


energyVals = [[0]*20]*20
magnetizationVals = []
tempList = np.linspace(0.5, 10, 20)
temptempList = np.linspace(-4, 4, 20)
for x in range(len(tempList)):
	for y in range(len(temptempList)):
		energy, magnetization = flipSpins(createSpins(64, False), 2000, 1000, 1/(tempList[x]), temptempList[y], 1)
		energyVals[y][x] = energy
		magnetizationVals.append(magnetization)

heatCapacities = []

# for e in range(len(tempList)):
# 	mu2 = calculateMagnetization(energyVals[e])
# 	mu2 = mu2*mu2
# 	temp = [x*x for x in energyVals[e]]
# 	mu = calculateMagnetization(temp)
# 	heatCapacities.append(1/(tempList[e]*tempList[e])*(mu-mu2))


# susceptibilities = []

# for e in range(len(tempList)):
# 	mu2 = calculateMagnetization(magnetizationVals[e])
# 	mu2 = mu2*mu2
# 	temp = [x*x for x in magnetizationVals[e]]
# 	mu = calculateMagnetization(temp)
# 	susceptibilities.append(1/(tempList[e])*(mu-mu2))
Z = [[0]*20]*20
for x in range(20):
	for y in range(20):
		Z[x][y] = calculateMagnetization(energyVals[x][y])


fig = plt.figure()
ax = fig.gca(projection='3d')
X,Y = np.meshgrid(tempList, temptempList)
urf = ax.plot_surface(X, Y, np.array(Z), cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

plt.show()
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# z = energyAve
# y = temptempList
# x = tempList
# ax.plot(x,y,z)

# plt.show()





# workbook = xlsxwriter.Workbook('Test.xlsx')
# worksheet = workbook.add_worksheet()

# writeToSheet(worksheet, tempList, 0, 0)
# writeToSheet(worksheet, energyVals, 0, 1)
# writeToSheet(worksheet, magnetizationVals, 0, 2)

# workbook.close()