import numpy as np
import matplotlib.pyplot as plt

f = np.logspace(1, 6, 500)
fc = 1e3
magnitude_db = 20 * np.log10(1 / np.sqrt(1 + (f / fc)**2))

plt.semilogx(f, magnitude_db)
plt.grid(True, which="both")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.title("Example Bode Plot")
plt.show()
