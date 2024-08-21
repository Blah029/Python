import math

# Given values
bandwidth = 1e6  # Bandwidth in Hz (1 MHz)
snr = 63  # SNR (linear scale)

# Shannon's Capacity Formula
C_max = bandwidth * math.log2(1 + snr)

# Calculate data rate for 2/3 of the maximum theoretical limit
C_practical = (2 / 3) * C_max

# Nyquist's Formula for number of signal levels
M = 2 ** (C_practical / (2 * bandwidth))

print(f"Upper limit to the data rate (C_max): {C_max:.2f} bits per second")
print(f"Practical data rate (C_practical): {C_practical:.2f} bits per second")
print(f"Number of signal levels (M): {M:.2f}")
