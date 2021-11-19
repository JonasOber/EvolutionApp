import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(0, 1, 100)
y = np.exp(x)

x_randomlinear = np.random.random(10)
x_randomexp = -np.log(x_randomlinear)

plt.figure()
plt.plot(x_randomlinear, np.exp(x_randomlinear), marker='s', linestyle='None')
plt.plot(x_randomexp, np.exp(x_randomexp), marker='X', linestyle='None')
plt.plot(x, y, '-', color='black')
plt.show()