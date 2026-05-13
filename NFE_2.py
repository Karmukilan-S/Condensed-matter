import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "axes.labelsize": 12,
    "xtick.direction": "in",
    "ytick.direction": "in",
})

def nfe_band_and_dos():

    a_ = 1.0
    G0 = 2*np.pi/a_

    # First two Brillouin zones
    k_min, k_max = -2, 2
    num_k_points = 1000

    n = int(input("Truncation parameter n: "))
    v_input = input(f"Enter {n} values for V_G (comma separated): ")

    v_list = [float(x.strip()) for x in v_input.split(',')]

    while len(v_list) < 2*n:
        v_list.append(0.0)

    g_indices = np.arange(-n, n+1)
    num_basis = len(g_indices)

    k_vals = np.linspace(k_min*G0, k_max*G0, num_k_points)

    energies_grid = []

    # Construct Hamiltonian and diagonalize
    for k in k_vals:

        H = np.zeros((num_basis, num_basis))

        for i in range(num_basis):
            for j in range(num_basis):

                if i == j:
                    H[i,j] = 0.5*(k - g_indices[i]*G0)**2

                else:
                    m = abs(g_indices[i]-g_indices[j])
                    if m <= len(v_list):
                        H[i,j] = v_list[m-1]

        energies_grid.append(np.linalg.eigvalsh(H))

    energies_grid = np.array(energies_grid)

    # =========================
    # Density of States
    # =========================

    energies_flat = energies_grid.flatten()

    bins = 1000
    dos, energy_bins = np.histogram(energies_flat, bins=bins, density=True)

    energy_centers = 0.5*(energy_bins[1:] + energy_bins[:-1])

    # =========================
    # Plotting
    # =========================

    fig = plt.figure(figsize=(10,6))

    gs = fig.add_gridspec(1,2,width_ratios=[3,1])

    ax_band = fig.add_subplot(gs[0])
    ax_dos = fig.add_subplot(gs[1], sharey=ax_band)

    colors = plt.cm.viridis(np.linspace(0,0.8,num_basis))

    for i in range(num_basis):
        ax_band.plot(k_vals/G0, energies_grid[:,i], color=colors[i], lw=2)

    ax_band.axvspan(-0.5,0.5,color='gray',alpha=0.15)

    for boundary in [-1,-0.5,0.5,1]:
        ax_band.axvline(boundary,color='black',linestyle=':',lw=0.8)

    kF = np.pi/(2*a_)

# find closest k-point
    k_index = np.argmin(np.abs(k_vals - kF))

# first band energy
    E_F = energies_grid[k_index,0]


    ax_band.set_xlim(k_min,k_max)
    ax_band.set_ylim(0,150)

    ax_band.set_xlabel(r"$k\,(2\pi/a)$")
    ax_band.set_ylabel("Energy")
    ax_band.axhline(E_F, color='red', linestyle='--', label="Fermi Energy")
    ax_band.axvline(kF/G0, color='red', linestyle='--')

    ax_band.set_title("Nearly Free Electron Band Structure")

    # DOS plot
    ax_dos.plot(dos, energy_centers, lw=2)

    ax_dos.set_xlabel("DOS")
    ax_dos.set_title("Density of States")

    ax_dos.spines['top'].set_visible(False)
    ax_dos.spines['right'].set_visible(False)

    ax_band.spines['top'].set_visible(False)
    ax_band.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.show()

nfe_band_and_dos()
