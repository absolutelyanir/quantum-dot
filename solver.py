import numpy as np
from scipy.linalg import eigh

def compute_energy_levels(L, m_eff, num_levels):
    """
    Solves the 1D Schrödinger equation for an infinite square well
    using the Finite Difference Method.
    """
    # 1. Discretize space
    N = 500  # Number of grid points
    x = np.linspace(0, L, N)
    dx = x[1] - x[0]
    
    # 2. Constants (hbar in J.s)
    hbar = 1.0545718e-34
    
    # 3. Build the Hamiltonian Matrix (H = T + V)
    # Since it's an infinite well, V=0 inside the box. 
    # We only need the Kinetic energy matrix (T) using the second derivative approximation.
    main_diag = 2 * np.ones(N-2)
    off_diag = -1 * np.ones(N-3)
    
    # Finite difference coefficient: hbar^2 / (2 * m_eff * dx^2)
    coeff = (hbar**2) / (2 * m_eff * (dx**2))
    
    H = coeff * (np.diag(main_diag) + np.diag(off_diag, k=1) + np.diag(off_diag, k=-1))
    
    # 4. Solve for Eigenvalues (Energy levels)
    # eigh is efficient for symmetric/Hermitian matrices
    energies_joules, wavefunctions = eigh(H)
    
    # Return only the requested number of levels
    return energies_joules[:num_levels]

def compute_wavefunction(L, m_eff, level_index=0):
    """
    Bonus: Returns x and psi for plotting the probability density.
    """
    N = 500
    x = np.linspace(0, L, N)
    dx = x[1] - x[0]
    hbar = 1.0545718e-34
    
    main_diag = 2 * np.ones(N-2)
    off_diag = -1 * np.ones(N-3)
    coeff = (hbar**2) / (2 * m_eff * (dx**2))
    H = coeff * (np.diag(main_diag) + np.diag(off_diag, k=1) + np.diag(off_diag, k=-1))
    
    energies, wavefunctions = eigh(H)
    
    # Get specific wavefunction and pad with zeros for boundaries
    psi = np.zeros(N)
    psi[1:-1] = wavefunctions[:, level_index]
    
    return x, psi
