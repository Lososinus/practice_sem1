import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import collections

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

fig, ax = plt.subplots()

x = [[0.470, 0.440, 0.410, 0.380, 0.350, 0.320, 0.290, 0.260, 0.230, 0.200, 0.170, 0.140, 0.110, 0.080, 0.050]]
y = [[1.62, 1.57, 1.57, 1.56, 1.53, 1.52, 1.52, 1.53, 1.55, 1.57, 1.64, 1.72, 1.86, 2.12, 2.64]]

xer = 0  # change errors
yer = 0

xline = []
z = []
yline = []
for i in range(len(x)):
    xline.append(np.linspace(0, 30, 100))  # change limits (llim, rlim, ...)
    z.append(np.polyfit([0] + x[i], [0] + y[i], 1, cov=True))
    print(z[i][0][1])
    yline.append(np.polyval(z[i][0], xline[i]))

colors = ['slateblue', 'hotpink']
Ts = [10.887, 15.721, 20.643, 25.589, 28.932]
lbls = [f'$\Delta l$ (P)' for i in range(len(x))]

for i in range(len(x)):
    ax.errorbar(x[i], y[i], c=colors[i], marker='', linestyle='', xerr=xer, yerr=yer)
    ax.scatter(x[i], y[i], c=colors[i], marker='.')
    ax.plot(xline[i], yline[i], c=colors[i], marker='', label=lbls[i])

plt.legend()

plt.ylabel(r'$\Delta l$, мкм', fontsize=15)  # change axis names
plt.xlabel(r'P, Н', fontsize=15)

plt.xlim(0, 0.5)  # change axis limits
plt.ylim(0, 4)

ax.minorticks_on()
ax.grid(which='major', axis='both')
ax.grid(which='minor', axis='y', linestyle=':')

ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))

ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(50))

fig.set_figheight(7)
fig.set_figwidth(10)
plt.show()

slopes = [[z[i][0][0], np.sqrt(np.diag(z[i][1]))[0]] for i in range(len(x))]

for i in range(len(x)):
    print(f'k = {slopes[i][0]}, dk = {slopes[i][1]}$')
