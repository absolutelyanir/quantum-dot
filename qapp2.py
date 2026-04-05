import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Quantum Dot Simulator", layout="wide")

# ---------- TITLE ----------
st.title("⚛️ Quantum Dot Energy Simulator")
st.markdown("Explore how **quantum confinement** affects energy levels and optical properties of quantum dots.")

# ---------- CONSTANTS ----------
h = 6.62607015e-34
c = 299792458
eV = 1.602176634e-19
m_e = 9.10938356e-31

# ---------- BACKEND IMPORTS ----------
HAVE_SOLVER = False
HAVE_PHYSICS = False

try:
    from solver import compute_energy_levels
    HAVE_SOLVER = True
except:
    pass

try:
    from physics import get_effective_mass, energy_to_wavelength
    HAVE_PHYSICS = True
except:
    pass

# ---------- FALLBACKS ----------
def get_effective_mass_fallback(material):
    return {"GaAs": 0.067, "CdSe": 0.13}.get(material, 0.1) * m_e

def compute_energy_levels_fallback(L, m_eff, num_levels):
    n = np.arange(1, num_levels + 1)
    return (h**2 * n**2) / (8 * m_eff * L**2)

def energy_to_wavelength_fallback(E):
    return (h * c) / np.maximum(E, 1e-30)

# ---------- WRAPPERS ----------
def get_m_eff(material):
    if HAVE_PHYSICS:
        try:
            m = get_effective_mass(material)
            return m if m > 1e-25 else m * m_e
        except:
            return get_effective_mass_fallback(material)
    return get_effective_mass_fallback(material)

def compute_energies(material, L, levels):
    m_eff = get_m_eff(material)
    if HAVE_SOLVER:
        try:
            E = np.array(compute_energy_levels(L, m_eff, levels))
            if np.max(E) < 1e-3:
                E *= eV
            return E
        except:
            pass
    return compute_energy_levels_fallback(L, m_eff, levels)

def energy_to_wavelength_wrapper(E):
    if HAVE_PHYSICS:
        try:
            return energy_to_wavelength(E)
        except:
            pass
    return energy_to_wavelength_fallback(E)

# ---------- SIDEBAR ----------
st.sidebar.header("🎛️ Controls")

size_nm = st.sidebar.slider("Quantum Dot Size (nm)", 1.0, 10.0, 5.0)
material = st.sidebar.selectbox("Material", ["GaAs", "CdSe"])
num_levels = st.sidebar.slider("Energy Levels", 1, 5, 3)
show_wave = st.sidebar.checkbox("Show Wavefunction")

L = size_nm * 1e-9

# ---------- COMPUTE ----------
energies = compute_energies(material, L, num_levels)
ground_E = energies[0]
wavelength_nm = energy_to_wavelength_wrapper(ground_E) * 1e9

# ---------- METRICS ----------
st.subheader("📊 Key Results")

col1, col2, col3 = st.columns(3)

col1.metric("Size", f"{size_nm:.2f} nm")
col2.metric("Material", material)
col3.metric("Effective Mass", f"{get_m_eff(material)/m_e:.3f} mₑ")

col4, col5 = st.columns(2)

col4.metric("Ground Energy", f"{ground_E/eV:.3f} eV")
col5.metric("Wavelength", f"{wavelength_nm:.1f} nm")

# ---------- ENERGY LEVELS ----------
st.subheader("⚡ Energy Levels")

for i, E in enumerate(energies):
    st.write(f"Level {i+1}: **{E/eV:.3f} eV**")

# ---------- GRAPH ----------
st.subheader("📈 Energy vs Size")

sizes = np.linspace(1, 10, 200)
sizes_m = sizes * 1e-9

fig, ax = plt.subplots(figsize=(8, 4))

for n in range(1, num_levels + 1):
    E_vals = (h**2 * n**2) / (8 * get_m_eff(material) * sizes_m**2)
    ax.plot(sizes, E_vals / eV, label=f"n={n}")

ax.set_xlabel("Size (nm)")
ax.set_ylabel("Energy (eV)")
ax.set_title("Quantum Confinement Effect")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# ---------- WAVEFUNCTION ----------
if show_wave:
    st.subheader("🔬 Wavefunction")

    x = np.linspace(0, L, 400)
    psi = np.sqrt(2/L) * np.sin(np.pi * x / L)

    fig2, ax2 = plt.subplots(1, 2, figsize=(10, 3))

    ax2[0].plot(x * 1e9, psi)
    ax2[0].set_title("ψ(x)")
    ax2[0].set_xlabel("Position (nm)")
    ax2[0].grid()

    ax2[1].plot(x * 1e9, psi**2)
    ax2[1].set_title("|ψ(x)|²")
    ax2[1].set_xlabel("Position (nm)")
    ax2[1].grid()

    st.pyplot(fig2)

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Quantum confinement: smaller dots → higher energy → blue shift")