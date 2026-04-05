# physics.py
# Teammate 2 - Physics & Model Engineer
# Handles all physical constants, material properties, and unit conversions

import math

# ─────────────────────────────────────────
# PHYSICAL CONSTANTS
# ─────────────────────────────────────────

h    = 6.626e-34   # Planck's constant (J·s)
hbar = 1.055e-34   # Reduced Planck's constant (J·s)
m0   = 9.109e-31   # Electron rest mass (kg)
e    = 1.602e-19   # Elementary charge (C)


# ─────────────────────────────────────────
# 1. MATERIAL PROPERTIES
# ─────────────────────────────────────────

def get_effective_mass(material):
    """
    Returns the effective mass of an electron in the given material.

    Input:
        material (str): 'GaAs' or 'CdSe'

    Output:
        effective mass in kg (float)
    """
    mass_table = {
        "GaAs": 0.067 * m0,   # Gallium Arsenide
        "CdSe": 0.130 * m0,   # Cadmium Selenide
    }

    if material not in mass_table:
        raise ValueError(f"Unknown material '{material}'. Choose from: {list(mass_table.keys())}")

    return mass_table[material]


# ─────────────────────────────────────────
# 2. ENERGY CONVERSION
# ─────────────────────────────────────────

def joule_to_ev(E_joules):
    """
    Converts energy from Joules to electron-volts (eV).

    Input:
        E_joules (float): energy in Joules

    Output:
        energy in eV (float)
    """
    return E_joules / e


# ─────────────────────────────────────────
# 3. WAVELENGTH CALCULATION
# ─────────────────────────────────────────

def energy_to_wavelength(E_ev):
    """
    Converts photon energy (in eV) to wavelength (in nm).
    Uses the formula: λ = 1240 / E

    Input:
        E_ev (float): energy in eV

    Output:
        wavelength in nm (float)
    """
    if E_ev <= 0:
        raise ValueError("Energy must be a positive value.")

    return 1240 / E_ev


# ─────────────────────────────────────────
# 4. BONUS - ANALYTICAL (THEORETICAL) ENERGY
# ─────────────────────────────────────────

def theoretical_energy(L, m_eff, num_levels=3):
    """
    Calculates energy levels analytically using the infinite square well formula:
        E_n = (n² * π² * hbar²) / (2 * m * L²)

    Inputs:
        L        (float): well size in meters
        m_eff    (float): effective mass in kg
        num_levels (int): number of energy levels to compute

    Output:
        list of energy values in eV
    """
    energies = []
    for n in range(1, num_levels + 1):
        E_joules = (n**2 * math.pi**2 * hbar**2) / (2 * m_eff * L**2)
        energies.append(joule_to_ev(E_joules))
    return energies


# ─────────────────────────────────────────
# QUICK TEST (only runs when you run this file directly)
# ─────────────────────────────────────────

if __name__ == "__main__":
    print("=== Testing physics.py ===\n")

    mass = get_effective_mass("GaAs")
    print(f"GaAs effective mass : {mass:.4e} kg")

    mass2 = get_effective_mass("CdSe")
    print(f"CdSe effective mass : {mass2:.4e} kg")

    print(f"\n1 eV in Joules      : {e:.4e} J")
    print(f"joule_to_ev test    : {joule_to_ev(1.602e-19):.4f} eV")

    print(f"\nWavelength @ 2 eV   : {energy_to_wavelength(2):.1f} nm")
    print(f"Wavelength @ 3 eV   : {energy_to_wavelength(3):.1f} nm")

    print("\nTheoretical energy levels for GaAs, L=5nm:")
    levels = theoretical_energy(5e-9, mass)
    for i, E in enumerate(levels):
        print(f"  E{i+1} = {E:.4f} eV  →  λ = {energy_to_wavelength(E):.1f} nm")
