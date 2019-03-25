import random
import math as m

#Initializes spins to either all parallel or randomly +-1
def createSpins(numSpins, parallel):
	if(parallel):
		spins = [1]*numSpins
	else:
		spins = [random.randint(0, 1)*2 - 1 for x in range(0,numSpins)]
	return spins


#Chooses random spin to flip and calculates whether it does or not.
#If change in energy is negative, flips. If not, flips with probability
#e^(-beta*delE). Does this for the specified number of times.
def flipSpins(spins, numTrials, equilibrium, beta, J):
	energyVals = []
	for x in range(0, numTrials):
		index = random.randint(0, len(spins)-1)

		#Edge case at beginning of list. Flips when different spins,
		#Possibly flips if not same.
		if(index == 0):
			if(spins[0]*spins[1] < 0):
				spins[0] = -spins[0]
			else:
				spins[0] = (-spins[0] if(random.uniform(0,1) <= m.pow(m.e, (-beta*J*2))) else spins[index])
		#Edge case at end of list. Flips when different spins,
		#Possibly flips if not same.
		elif(index == len(spins) - 1):
			if(spins[index]*spins[index - 1] < 0):
				spins[index] = -spins[index]
			else:
				spins[index] = (-spins[index] if(random.uniform(0,1) <= m.pow(m.e, (-beta*J*2))) else spins[index])
		#Middle of list. Calculates whether energy change based on neighbors will be + or -,
		#then determines whether to flip as outlined above.
		else:
			if(spins[index-1] != spins[index+1] or spins[index-1] != spins[index]):
				spins[index] = -spins[index]
			else:
				spins[index] = (-spins[index] if(random.uniform(0,1) <= m.pow(m.e, (-beta*J*2))) else spins[index])
		if(x < equilibrium and x % int((numTrials-equilibrium/20)):
			energyVals.append(calculateEnergy(spins))

#Calculates the dimensionless energy per spin.
def calculateEnergy(spins):
	N = len(spins)
	energy = 0
	for x in range(0, N-1):
		energy += -spins[x]*spins[x+1]
	return energy

#Calculates the dimensionless magnetization per spin.
def calculateMagnetization(spins):
	return sum(spins)/len(spins)


#Runs the Monte Carlo algorithm as outlined in Sec. 5.5.3.
def OneD_Monte_Carlo(parallel, numSpins, numTrials, equilibrium, beta, J):

	spins = createSpins(numSpins, parallel)

	print(spins)

	flipSpins(spins, numTrials, equilibrium, beta, J)

	print(spins)

	energy = calculateEnergy(spins)

	print(energy)

	magnetization = calculateMagnetization(spins)

	print(magnetization)



#Prints initial and final lists of spins

#Sample values, change as desired.
OneD_Monte_Carlo(False, 4, 100, 90, 10, 10)
