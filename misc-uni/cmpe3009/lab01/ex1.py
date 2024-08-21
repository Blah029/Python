import math

# Given values
bandwidth = 4e6 - 3e6  # Bandwidth in Hz (1 MHz)
snr_db = 24  # SNR in decibels

# Convert SNR from dB to linear scale
snr_linear = 10 ** (snr_db / 10)

# Shannon's Capacity Formula
C = bandwidth * math.log2(1 + snr_linear)

# Nyquist's Formula for number of signal levels
M = 2 ** (C / (2 * bandwidth))

print(f"Theoretical maximum data rate (C): {C:.2f} bits per second")
print(f"Number of signal levels (M): {M:.2f}")
