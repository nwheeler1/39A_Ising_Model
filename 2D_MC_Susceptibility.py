import random as r
import math as m
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from astropy.stats import jackknife_resampling
from astropy.stats import jackknife_stats
import scipy.integrate

#Input parameters. Stores start/end temps and external mag fields, 
#parallel spins, number of spins, number of trials, and number of simulations
#of both the temps and the external magnetic fields (so the total number of
#trials will be that number squared)
parallel = True
numSims = 20
numSpins = 16
trials = 2000000
startTemp = 0.2
endTemp = 4

#Initializes time and external mag field arrays
temps = np.linspace(startTemp, endTemp, numSims)





#Function definitions

#Simulates the flips with the given inputs, the spin list, the number of trials,
#the value of beta, and the strength of the external magnetic field.
#Equilibrium is assumed to be achieved prior to the sampling
def simulate(spins, trials, beta):
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

		#Finds magnetization once equilibrium has been reached
		if(x >=trials - 15000):
			magnetizations.append(average(spins))

	#The values of the magnetization after equilibrium
	return magnetizations

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
	plt.errorbar(np.array(X), np.array(Y), yerr=jackknifes)
	plt.xlabel('Temperature')
	plt.ylabel('Susceptibility')

	#Shows the plot
	plt.show()



#Initializes susceptibilities list
susceptibilities = []

jackknifes = []

i=1

#Calculates the susceptibility lists for each temp
for temp in temps:
	spins = spinList(numSpins, parallel)
	beta = 1/temp

	#Does a Monte-Carlo simulation as outlined in the assignment
	magnetization = simulate(spins, trials, beta)
	out = jackknife_stats(np.array(magnetization), np.var, 0.95)
	susceptibilities.append(out[0])
	jackknifes.append(out[2])

	#Flagpoint
	print(i)
	i += 1


plotVals(temps, susceptibilities, jackknifes)