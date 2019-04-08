import random as r
import math as m
import numpy as np
import xlsxwriter

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
		if(i >= equilibrium and (i - equilibrium) % int((numTrials - equilibrium)/20) == 0):
			energyVals.append(calculateEnergy(spins, magField))
			magnetizationVals.append(calculateMagnetization(spins))
		energyChange = -J*((2*spins[(index-1) % len(spins)] + 2*spins[(index + 1) % len(spins)]) * spins[index]) - magField*2*spins[index]
		if(energyChange <= 0):
			spins[index] = -spins[index]
		else:
			spins[index] = -spins[index] if (r.uniform(0,1) <= m.pow(m.e, (-beta*J*2*energyChange))) else spins[index]
	return energyVals, magnetizationVals

def writeToSheet(sheet, list, startRow, column):
	for x in list:
		sheet.write(startRow, column, x)
		startRow += 1


def calculateEnergy(spins, magField):
	N = len(spins)
	energy = 0
	for x in range(0, N-1):
		energy += -spins[x]*spins[x+1] - magField*spins[x]
	return energy/len(spins)

def calculateMagnetization(spins):
	return sum(spins)/len(spins)


energyVals = []
magnetizationVals = []
tempList = np.linspace(0.001, 0.1, 100)
for temp in tempList:
	energy, magnetization = flipSpins(createSpins(20, False), 10000, 2000, 1/temp, 0, 1)
	energyVals.append(energy)
	magnetizationVals.append(magnetization)

heatCapacities = []

for e in range(len(tempList)):
	mu2 = calculateMagnetization(energyVals[e])
	mu2 = mu2*mu2
	temp = [x*x for x in energyVals[e]]
	mu = calculateMagnetization(temp)
	heatCapacities.append(1/(tempList[e]*tempList[e])*(mu-mu2))

print(heatCapacities)








workbook = xlsxwriter.Workbook('Test.xlsx')
worksheet = workbook.add_worksheet()

writeToSheet(worksheet, tempList, 0, 0)
writeToSheet(worksheet, energyVals, 0, 1)
writeToSheet(worksheet, magnetizationVals, 0, 2)

workbook.close()