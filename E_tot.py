import numpy as np
import matplotlib.pyplot as plt

# lattice constant
a = 1.0
G0 = 2*np.pi/a

# k-mesh (two BZ for safety)
Nk = 1000
k_vals = np.linspace(-np.pi/a, np.pi/a, Nk)

# truncation parameter
n = 3
g_indices = np.arange(-n, n+1)
num_basis = len(g_indices)

# Fermi wavevector for 1 electron per unit cell
kF = np.pi/(2*a)

# range of potential strengths A
A_values = np.linspace(0,3.0,40)

E_cell_list = []

for A in A_values:

    energies_grid = []

    for k in k_vals:

        H = np.zeros((num_basis,num_basis))

        for i in range(num_basis):
            for j in range(num_basis):

                if i == j:
                    H[i,j] = 0.5*(k - g_indices[i]*G0)**2

                else:
                    delta = abs(g_indices[i] - g_indices[j])

                    if delta == 1:
                      H[i,j] = A/2
                    elif delta == 2:
                      H[i,j] = A/4
                    elif delta == 3:
                      H[i,j] = A/6
                    else:
                      H[i,j] = 0

        eigvals = np.linalg.eigvalsh(H)
        energies_grid.append(eigvals)

    energies_grid = np.array(energies_grid)

    # first band
    band1 = energies_grid[:,0]

    # occupied states
    occupied = np.abs(k_vals) <= kF

    # total energy per unit cell
    E_cell = 2*np.sum(band1[occupied]) / Nk

    E_cell_list.append(E_cell)

# plot total energy vs A
plt.figure(figsize=(7,5))
plt.plot(A_values,E_cell_list,'o-',lw=2)

plt.xlabel("Potential strength A")
plt.ylabel("Energy per unit cell")

plt.title("Total Band Energy vs Potential Strength")

plt.grid(True)
plt.show()
