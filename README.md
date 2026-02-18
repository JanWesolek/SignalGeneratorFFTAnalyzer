# PyQt5 Signal Generator & FFT Analyzer 📉🔊

A desktop application capable of synthesizing various waveforms, performing spectral analysis, and exporting data formats. The project demonstrates the practical application of **Digital Signal Processing (DSP)** algorithms within a **Python GUI** environment.

## 🎯 Key Features

* **Waveform Synthesis:** Generates Sine, Square, Sawtooth, Triangle, and White Noise signals.
* **Spectral Analysis:** Computes and visualizes the **Fast Fourier Transform (FFT)** in real-time.
* **Data Export:**
  * **Audio:** Saves generated signals as `.wav` files (16-bit PCM) using `scipy`.
  * **Data:** Exports time-domain and frequency-domain data to `.csv` using `pandas`.
* **Interactive GUI:** Built with **PyQt5** and **PyQtGraph** for high-performance plotting.

## 🛠️ Technology Stack

* **Language:** Python 3.x
* **GUI Framework:** PyQt5
* **Math & DSP:** NumPy (Vectorization), SciPy (Audio I/O)
* **Visualization:** PyQtGraph (Real-time plotting)
* **Data Handling:** Pandas (CSV Export)

## 🧠 Code Architecture (OOP)

The application follows **Object-Oriented Programming** principles by separating logic from the interface:
* **`class Krenarator` (Model):** Handles mathematical operations, signal generation logic (`np.sin`, `np.sign`), FFT calculations, and file I/O.
* **`class App` (View/Controller):** Manages the PyQt5 layout, user inputs, event handling (signals/slots), and graph updates.

## 💻 How to Run

1.  Install dependencies:
    ```bash
    pip install PyQt5 pyqtgraph numpy scipy pandas matplotlib
    ```
2.  Run the application:
    ```bash
    python main.py
    ```

---
**Author:** Jan Wesołek
