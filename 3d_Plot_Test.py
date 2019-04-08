import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib as mpl


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
z = [0,1,2,3]
y = [3,2,1,0]
x = [3,2,1,0]
ax.plot(x,y,z)

plt.show()
