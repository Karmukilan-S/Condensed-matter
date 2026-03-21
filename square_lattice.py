import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Brillouin zone grid
# -----------------------------
N = 300
kx = np.linspace(-np.pi, np.pi, N)
ky = np.linspace(-np.pi, np.pi, N)
KX, KY = np.meshgrid(kx, ky)

# -----------------------------
# 2. Parameters
# -----------------------------
t = -2.0  # eV
fillings = np.arange(0.5, 2.01, 0.25)

# -----------------------------
# 3. Dispersion function
# -----------------------------
def energy(kx, ky, t, t_prime):
    return 2*t*(np.cos(kx) + np.cos(ky)) + 4*t_prime*np.cos(kx)*np.cos(ky)

# -----------------------------
# 4. Plot function
# -----------------------------
def plot_band_and_fermi(t_prime, title):

    # Compute energy over BZ
    E = energy(KX, KY, t, t_prime)

    # Flatten and sort once
    E_sorted = np.sort(E.flatten())

    # Plot band contour
    plt.figure(figsize=(7, 6))
    contour = plt.contourf(KX, KY, E, levels=60)
    plt.colorbar(contour, label="Energy (eV)")

    # Plot Fermi surfaces
    for n in fillings:
        frac = n / 2.0  # spin degeneracy
        E_F = np.quantile(E_sorted, frac)

        plt.contour(
            KX, KY, E,
            levels=[E_F],
            linewidths=1.5,
            linestyles='solid',
            label=f"n={n:.2f}"
        )

    plt.title(title)
    plt.xlabel(r"$k_x$")
    plt.ylabel(r"$k_y$")
    plt.xlim(-np.pi, np.pi)
    plt.ylim(-np.pi, np.pi)
    plt.grid(alpha=0.2)

    plt.show()

# -----------------------------
# 5. Run cases
# -----------------------------

# (a) Nearest neighbour only
plot_band_and_fermi(0.0, "Square lattice (NN only)")

# (b) With diagonal hopping
plot_band_and_fermi(1.0, "Square lattice with t' = +1 eV")
plot_band_and_fermi(-1.0, "Square lattice with t' = -1 eV")
print(f"n = {n:.2f}, E_F = {E_F:.3f}")