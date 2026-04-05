import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Physical constants
h = 6.62607015e-34       # Planck constant, J*s
c = 299792458            # Speed of light, m/s
eV = 1.602176634e-19     # Electron volt in J
m_e = 9.10938356e-31     # Electron mass in kg

# Try to import backend functions; provide robust fallbacks if missing.
HAVE_SOLVER = False
HAVE_PHYSICS = False

try:
    from solver import compute_energy_levels  # expected to return energies in Joules
    HAVE_SOLVER = True
except Exception:
    HAVE_SOLVER = False

try:
    from physics import get_effective_mass, energy_to_wavelength
    HAVE_PHYSICS = True
except Exception:
    HAVE_PHYSICS = False

# Fallback: effective mass (as multiplier of electron mass) for common materials
def get_effective_mass_fallback(material: str) -> float:
    mapping = {
        "GaAs": 0.067,
        "CdSe": 0.13
    }
    m_rel = mapping.get(material, 0.1)
    return m_rel * m_e

# Fallback: compute energy levels using 1D particle-in-a-box approximation
def compute_energy_levels_fallback(size_m: float, m_eff: float, num_levels: int) -> np.ndarray:
    """
    E_n = (h^2 n^2) / (8 m L^2)  (1D infinite potential well)
    Returns energies in Joules for n = 1..num_levels
    """
    ns = np.arange(1, num_levels + 1)
    energies = (h ** 2) * (ns ** 2) / (8 * m_eff * (size_m ** 2))
    return energies

# Fallback: convert energy (J) to wavelength (m)
def energy_to_wavelength_fallback(E_joule: float) -> float:
    # For photon energy E = h*c / lambda  => lambda = h*c / E
    # Guard against zero or negative energies
    E_joule = np.maximum(E_joule, 1e-30)
    return (h * c) / E_joule

# Wrapper to get effective mass (tries backend then fallback)
def get_m_eff(material: str) -> float:
    if HAVE_PHYSICS:
        try:
            m_eff = get_effective_mass(material)
            # If backend returns relative mass instead of kg, attempt to detect and convert
            if m_eff > 1e-25:  # likely already in kg
                return float(m_eff)
            else:
                # treat as fraction of electron mass
                return float(m_eff) * m_e
        except Exception:
            return get_effective_mass_fallback(material)
    else:
        return get_effective_mass_fallback(material)

# Wrapper to compute energies (tries solver then fallback)
def compute_energies(material: str, size_m: float, num_levels: int) -> np.ndarray:
    m_eff = get_m_eff(material)
    if HAVE_SOLVER:
        try:
            energies = compute_energy_levels(size_m, m_eff, num_levels)
            energies = np.asarray(energies, dtype=float)
            # If solver returned energies in eV (detect by magnitude), convert to Joules
            if np.nanmax(energies) < 1e-3:  # tiny values -> likely eV; typical eV values ~ 0.1-4
                energies = energies * eV
            return energies
        except Exception:
            return compute_energy_levels_fallback(size_m, m_eff, num_levels)
    else:
        return compute_energy_levels_fallback(size_m, m_eff, num_levels)

# Wrapper for energy->wavelength conversion
def energy_to_wavelength_wrapper(E_joule: float) -> float:
    if HAVE_PHYSICS:
        try:
            wl = energy_to_wavelength(E_joule)
            return float(wl)
        except Exception:
            return energy_to_wavelength_fallback(E_joule)
    else:
        return energy_to_wavelength_fallback(E_joule)

# Small utility: format energy neatly
def format_energy(E_joule: float) -> str:
    E_eV = E_joule / eV
    if E_eV >= 1.0:
        return f"{E_eV:.3f} eV ({E_joule:.3e} J)"
    elif E_eV >= 1e-3:
        return f"{E_eV*1e3:.3f} meV ({E_joule:.3e} J)"
    else:
        return f"{E_joule:.3e} J"

# Streamlit UI
st.set_page_config(page_title="Quantum Dot Energy Simulator", layout="wide")
st.title("Quantum Dot Energy Simulator")

# Sidebar inputs
st.sidebar.header("Parameters")
size_nm = st.sidebar.slider("Quantum Dot Size (nm)", min_value=1.0, max_value=10.0, value=5.0, step=0.1)
material = st.sidebar.selectbox("Material", options=["GaAs", "CdSe"])
num_levels = st.sidebar.slider("Number of Energy Levels", min_value=1, max_value=5, value=3, step=1)
show_wavefunction = st.sidebar.checkbox("Show Wavefunction", value=False)

# Convert to SI
size_m = size_nm * 1e-9

# Compute energies
energies = compute_energies(material, size_m, num_levels)

# Display selected parameters
col1, col2 = st.columns([1, 1])
with col1:
    st.subheader("Selected Parameters")
    st.write(f"Size: **{size_nm:.2f} nm**")
    st.write(f"Material: **{material}**")
    st.write(f"Effective mass (approx): **{get_m_eff(material)/m_e:.3f} m_e**")

# Show ground state energy and wavelength
ground_E = energies[0]
ground_wl_m = energy_to_wavelength_wrapper(ground_E)
ground_wl_nm = ground_wl_m * 1e9

with col2:
    st.subheader("Ground State")
    st.write("Energy:")
    st.markdown(f"**{format_energy(ground_E)}**")
    st.write("Corresponding photon wavelength (if emitted):")
    st.markdown(f"**{ground_wl_nm:.1f} nm**")

# Energy vs Size plot
st.subheader("Energy vs Quantum Dot Size")
sizes_nm = np.linspace(1.0, 10.0, 200)
sizes_m = sizes_nm * 1e-9

# Compute energies for each level across sizes
def energies_across_sizes(material: str, sizes_m: np.ndarray, num_levels: int) -> np.ndarray:
    m_eff = get_m_eff(material)
    if HAVE_SOLVER:
        try:
            # Attempt batch call if solver supports vectorization: else fallback loop
            energies_matrix = []
            for L in sizes_m:
                try:
                    levels = compute_energy_levels(L, m_eff, num_levels)
                    levels = np.asarray(levels, dtype=float)
                    if np.nanmax(levels) < 1e-3:
                        levels = levels * eV
                    energies_matrix.append(levels)
                except Exception:
                    energies_matrix.append(compute_energy_levels_fallback(L, m_eff, num_levels))
            return np.array(energies_matrix)  # shape (len(sizes), num_levels)
        except Exception:
            # any failure -> fallback
            pass
    # fallback computation (fast vectorized particle-in-a-box)
    ns = np.arange(1, num_levels + 1)
    # E_n(L) = h^2 n^2 / (8 m L^2)
    E = (h ** 2) * (ns[np.newaxis, :] ** 2) / (8 * m_eff * (sizes_m[:, np.newaxis] ** 2))
    return E

E_matrix = energies_across_sizes(material, sizes_m, num_levels)

# Plot energies in eV for readability
fig, ax = plt.subplots(figsize=(8, 4))
for i in range(num_levels):
    ax.plot(sizes_nm, E_matrix[:, i] / eV, label=f"Level n={i+1}")
ax.set_xlabel("Size (nm)")
ax.set_ylabel("Energy (eV)")
ax.set_title("Energy Levels vs Quantum Dot Size")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Optional: wavefunction plot (1D infinite well sine wave)
if show_wavefunction:
    st.subheader("Wavefunction (1D infinite well approximation)")
    # Use ground state (n=1) for demonstration
    n = 1
    L = size_m
    x = np.linspace(0, L, 400)
    # psi_n(x) = sqrt(2/L) * sin(n*pi*x/L)
    psi = np.sqrt(2 / L) * np.sin(n * np.pi * x / L)
    # Normalize/display psi and probability density
    fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))
    ax1.plot(x * 1e9, psi, color="tab:blue")
    ax1.set_xlabel("Position (nm)")
    ax1.set_ylabel("ψ(x)")
    ax1.set_title(f"Wavefunction ψₙ (n={n})")
    ax1.grid(True)

    ax2.plot(x * 1e9, psi ** 2, color="tab:orange")
    ax2.set_xlabel("Position (nm)")
    ax2.set_ylabel("|ψ(x)|²")
    ax2.set_title("Probability density")
    ax2.grid(True)

    st.pyplot(fig2)

st.markdown("---")
st.caption("Note: This simulator uses a simplified particle-in-a-box fallback when backend solver/physics modules are unavailable. The physical model is illustrative and intended for exploration of trends due to quantum confinement.")