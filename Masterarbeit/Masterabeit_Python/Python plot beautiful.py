"""
https://towardsdatascience.com/an-introduction-to-making-scientific-publication-plots-with-python-ea19dfa7f51e
https://pypi.org/project/SciencePlots/
and then tikzplotlib
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

x = np.linspace(0,2*np.pi, 100)
y = np.sin(x)

x_2 = np.linspace(0, 2*np.pi, 10)
y_2 = np.sin(x_2)
fig = plt.figure(figsize=(6,6), dpi=150)
ax = fig.add_subplot(111)
ax.plot(x, y, label='-', linestyle='dashed')
ax.plot(x, y, label=r'$\cdot$', linestyle='None', marker='.', markersize=5)
ax.legend()
ax.set_ylabel('y (m)')
ax.set_xlabel('x (m)')
ax.set_title("Ein schöner Plot")
ax.grid()
#plt.show()
tikzplotlib.save("test.tex")
import matplotlib.font_manager as fm# Collect all the font names available to matplotlib
font_names = [f.name for f in fm.fontManager.ttflist]
print(font_names)