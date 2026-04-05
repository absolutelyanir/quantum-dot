# ⚛️ Quantum Dot Energy Level Simulator

A computational physics project that simulates the energy levels of a 0D quantum dot as a function of its size using the Schrödinger equation.

---

## 📌 Overview

Quantum dots are nanoscale semiconductor particles where electrons are confined in all three dimensions. This project models quantum confinement and demonstrates how reducing the size of a quantum dot (1–10 nm) affects its energy levels and optical properties.

---

## 🎯 Objectives

* Simulate energy levels using the Schrödinger equation
* Study the effect of quantum dot size on energy
* Visualize quantum confinement effects
* Compare analytical and numerical approaches

---

## ⚙️ Features

* 📊 Energy vs Quantum Dot Size graph
* ⚡ Multiple energy levels (ground + excited states)
* 🌈 Energy to wavelength conversion
* 🔬 Optional wavefunction visualization
* 🎛️ Interactive UI using Streamlit

---

## 🧠 Physics Background

The system is modeled using the time-independent Schrödinger equation:

Hψ = Eψ

Using:

* Finite Difference Method (FDM) for numerical solution
* Effective mass approximation (GaAs / CdSe)

Energy levels follow:

E ∝ 1 / L²

Where L is the size of the quantum dot.

---

## 🧱 Project Structure

```bash id="v24p1o"
quantum-dot/
│
├── app.py              # Streamlit frontend
├── solver.py           # Numerical Schrödinger solver
├── physics.py          # Constants and physics functions
└── README.md
```

---

## 🚀 How to Run

1. Clone the repository:

```bash id="p7af8m"
git clone https://github.com/your-username/quantum-dot.git
cd quantum-dot
```

2. Install dependencies:

```bash id="l8m3qa"
pip install -r requirements.txt
```

3. Run the app:

```bash id="5o3qsy"
streamlit run app.py
```

---

## 👥 Team Roles

* **Frontend (UI & Visualization)**
  **Anirudh V — 25BAI1596**

* **Physics (Model & Constants)**
  **Adidev Premanand — 25BAI1720**

* **Solver (Numerical Computation)**
  **Josh Joseph — 25BAI1675**

---

## 📊 Expected Results

* Smaller quantum dots → higher energy levels
* Larger quantum dots → lower energy levels
* Demonstrates quantum confinement and bandgap shift

---

## 🧪 Technologies Used

* Python
* NumPy
* SciPy
* Matplotlib
* Streamlit

---

## 🔮 Future Improvements

* 3D quantum dot modeling
* Finite potential well implementation
* Enhanced UI/UX
* Material comparison

---

## 📚 References

* Griffiths, D. J. *Introduction to Quantum Mechanics*
* Kittel, C. *Solid State Physics*
* Online resources on numerical Schrödinger equation

---

## ✨ Demo

Interactive simulation showing how quantum dot size affects energy levels and optical properties.

---

## 📌 Note

This project is developed as part of a computational physics study on quantum confinement.
