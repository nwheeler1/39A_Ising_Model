import random as r
import math as m
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Stores energy and magnetization lists
eVals = []
mVals = []

#Input parameters. Stores start/end temps and external mag fields, 
#parallel spins, number of spins, number of trials, and number of simulations
#of both the temps and the external magnetic fields (so the total number of
#trials will be that number squared)
parallel = False
numSims = 20
numSpins = 64
trials = 5000
startTemp = 0.2
endTemp = 4
startExtMag = -10
endExtMag = 10

#Initializes time and external mag field arrays
temps = np.linspace(startTemp, endTemp, numSims)
extMags = np.linspace(startExtMag, endExtMag, numSims)





#Function definitions

#Simulates the flips with the given inputs, the spin list, the number of trials,
#the value of beta, and the strength of the external magnetic field.
#Equilibrium is assumed to be achieved once half of the trials have completed.
def simulate(spins, trials, beta, extMag):
	energies = []
	magnetizations = []

	#Tries to flips the specified number of times
	for x in range(trials):

		#Finds a random index in the list
		i = r.randint(0, len(spins) - 1)

		#Finds the change in energy due to a flip
		eChange = 2*(spins[(i-1)%numSpins] + spins[(i+1)%numSpins])*spins[i] + 2*spins[i]*extMag

		#Flips if energy change is negative, checks random value if positive
		if(eChange <= 0):
			spins[i] = -spins[i]
		else:
			spins[i] = -spins[i] if (r.uniform(0,1) <= m.e**(-beta*eChange)) else spins[i]

		#Finds energy and magnetizations once equilibrium has been reached
		if(x >= trials / 2):
			energies.append(calculateEnergy(spins, extMag))
			magnetizations.append(average(spins))

	#The values of each after equilibrium
	return energies, magnetizations

#Creates a list of spins with the given spins and parallelization
def spinList(numSpins, parallel):
	if(parallel):
		return [1]*numSpins
	else:
		return [r.randint(0,1)*2-1 for _ in range(numSpins)]

#Finds the average of the input list
def average(inList):
	return sum(inList)/(float(len(inList)))

#Finds the total energy of the given spin list
def calculateEnergy(spins, extMag):
	energy = 0
	for x in range(len(spins)):
		energy += -spins[x]*spins[(x+1)%len(spins)] - extMag*spins[x]
	return energy/len(spins)

#Plots the given lists in 3d
def plotVals(X, Y, Z):

	#Initializes the plot and makes it 3d
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	#Calculates the index values for temperature and external magnetization
	X2, Y2 = np.meshgrid(X, Y)

	#Plots the surface
	urf = ax.plot_surface(X2, Y2, np.reshape(np.array(heatCapacities), (numSims, numSims)), cmap=mpl.cm.coolwarm,
                       linewidth=0, antialiased=False)

	#Shows the plot
	plt.show()




#Calculates the energy and magnetization lists for each time and mag field
for temp in temps:
	for extMag in extMags:
		spins = spinList(numSpins, parallel)
		beta = 1/temp

		#Does a Monte-Carlo simulation as outlined in the assignment
		energy, magnetization = simulate(spins, trials, beta, extMag)
		eVals.append(energy.copy())
		mVals.append(magnetization.copy())

#Initializes heat capacity list
heatCapacities = []

#Finds the heat capacity for each temperature and external magnetic field
for i in range(numSims*numSims):
	
	#Finds the squared average of the energies
	averageSquared = average(eVals[i])
	averageSquared = averageSquared*averageSquared

	#Finds the average of the energies squared
	squares = [x*x for x in eVals[i]]
	squaredAverage = average(squares)

	#Finds the heat capacity
	heatCapacity = (squaredAverage - averageSquared)/(temps[int(i/numSims)] * temps[int(i/numSims)])

	#Appends to the heat capacities list
	heatCapacities.append(heatCapacity)

#Plots the graph
plotVals(extMags, temps, heatCapacities)