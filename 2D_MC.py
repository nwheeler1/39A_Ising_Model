import random as r
import math as m
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from astropy.stats import jackknife_resampling
from astropy.stats import jackknife_stats

#Stores energy and magnetization lists
eVals = []
mVals = []

#Input parameters. Stores start/end temps and external mag fields, 
#parallel spins, number of spins, number of trials, and number of simulations
#of both the temps and the external magnetic fields (so the total number of
#trials will be that number squared)
parallel = False
numSims = 10
numSpins = 16
trials = 60000
startTemp = 1.5
endTemp = 3.5

#Initializes time and external mag field arrays
temps = np.linspace(startTemp, endTemp, numSims)





#Function definitions

#Simulates the flips with the given inputs, the spin list, the number of trials,
#the value of beta, and the strength of the external magnetic field.
#Equilibrium is assumed to be achieved once half of the trials have completed.
def simulate(spins, trials, beta):
	energies = []
	magnetizations = []

	#Tries to flips the specified number of times
	for x in range(trials):

		#Finds a random index in the list
		i = r.randint(0, len(spins) - 1)
		j = r.randint(0, len(spins) - 1)

		#Finds the change in energy due to a flip
		eChange = 2*(spins[(i-1)%numSpins][j] + spins[(i+1)%numSpins][j] + spins[i][(j-1)%numSpins] + spins[i][(j+1)%numSpins])*spins[i][j]

		#Flips if energy change is negative, checks random value if positive
		if(eChange <= 0):
			spins[i][j] = -spins[i][j]
		else:
			spins[i][j] = -spins[i][j] if (r.uniform(0,1) <= m.e**(-beta*eChange)) else spins[i][j]

		#Finds energy and magnetizations once equilibrium has been reached
		if(x >= trials / 2):
			energies.append(calculateEnergy(spins))
			magnetizations.append(average(spins))

	#The values of each after equilibrium
	return energies, magnetizations

#Creates a list of spins with the given spins and parallelization
def spinList(numSpins, parallel):
	if(parallel):
		return [[1]*numSpins]*numSpins
	else:
		return [[r.randint(0,1)*2-1 for _ in range(numSpins)] for __ in range(numSpins)]

#Finds the average of the input list
def average(inList):
	return np.sum(inList)/np.size(inList)

#Finds the total energy of the given spin list
def calculateEnergy(spins):
	energy = 0
	for x in range(len(spins)):
		for y in range(len(spins)):
			energy += -spins[x][y]*(spins[(x+1)%len(spins)][y] + spins[x][(y+1)%len(spins)])
	return energy/len(spins)

#Plots the given lists in 2d
def plotVals(X, Y, jackknifes):

	#Initializes the plot
	fig = plt.figure()

	#Plots the values.
	plt.errorbar(np.array(X), np.array(Y), yerr=jackknifes, linestyle="None", fmt='-o')

	#Shows the plot
	plt.show()




#Calculates the energy and magnetization lists for each time and mag field
for temp in temps:
	spins = spinList(numSpins, parallel)
	beta = 1/temp

	#Does a Monte-Carlo simulation as outlined in the assignment
	energy, magnetization = simulate(spins, trials, beta)
	eVals.append(energy.copy())
	mVals.append(magnetization.copy())

#Initializes heat capacity list
heatCapacities = []

jackknifes = []

#Finds the heat capacity for each temperature and external magnetic field
for i in range(numSims):

	out = jackknife_stats(np.array(eVals[i]), np.var, 0.95)
	heatCapacities.append(out[0]/(temps[i]*temps[i]))
	jackknifes.append(out[2])
	
	# #Finds the squared average of the energies
	# averageSquared = average(eVals[i])
	# averageSquared = averageSquared*averageSquared

	# #Finds the average of the energies squared
	# squares = [x*x for x in eVals[i]]
	# squaredAverage = average(squares)

	# #Finds the heat capacity
	# heatCapacity = (squaredAverage - averageSquared)/(temps[i] * temps[i])

	# #Appends to the heat capacities list
	# heatCapacities.append(heatCapacity)

#Plots the graph
plotVals(temps, heatCapacities ,jackknifes)