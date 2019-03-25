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
def flipSpins(spins, numTrials, beta, J):
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

#Runs the Monte Carlo algorithm as outlined in Sec. 5.5.3
def OneD_Monte_Carlo(parallel, numSpins, numTrials, beta, J):

	spins = createSpins(numSpins, parallel)

	print(spins)

	flipSpins(spins, numTrials, beta, J)

	print(spins)

#Prints initial and final lists of spins

#Sample values, change as desired.
OneD_Monte_Carlo(False, 4, 10, 10, 10)
