import numpy as np
import matplotlib.pyplot as plt

# Define QAM parameters
M = 64  # Number of modulation levels (M=16 means 16-QAM)
num_symbols = 1000  # Number of symbols

# Generate random bits
bits = np.random.randint(0, M, num_symbols)
print(bits)

# Map bits to QAM symbols
def qam_modulate(bits, M):
    # Calculate the number of levels in each dimension (I and Q)
    num_levels = int(np.sqrt(M))
    
    # Gray coding mapping
    I = np.array([(bit // num_levels) - (num_levels // 2) + 0.5 for bit in bits])
    Q = np.array([(bit % num_levels) - (num_levels // 2) + 0.5 for bit in bits])
    
    return I, Q

I, Q = qam_modulate(bits, M)

# Add noise to the signal (optional, if needed)
noise_std = 0.1
I_noisy = I + np.random.normal(0, noise_std, I.shape)
Q_noisy = Q + np.random.normal(0, noise_std, Q.shape)

# Visualize the constellation diagram
plt.figure(figsize=(4, 4))
plt.scatter(I_noisy, Q_noisy, color='blue', s=10)
plt.title('Constellation IQ 16-QAM')
plt.xlabel('In-Phase')
plt.ylabel('Quadrature')
plt.grid(True)

# Set axis limits with expanded range
plt.xlim(-2.0, 2.0)
plt.ylim(-2.0, 2.0)

plt.show()


