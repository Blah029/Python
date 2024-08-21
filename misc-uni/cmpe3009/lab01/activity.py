import math

# Q1
bandwidth = 7e6 - 5e6
snr_db = 20
# Linear SNR
snr_linear = 10**(snr_db/10)
# Theoretical max. datarate
c_max = bandwidth * math.log2(1 + snr_linear)
# No. of signal levels
m = math.ceil(2**(c_max/(2*bandwidth)))

print(f"Q1")
print(f"Theoretical max. datarate is {c_max:.2f} bps.")
print(f"No. of signal levels is {m:d}.\n")

#Q2
bandwidth = 2e6
snr_linear = 100
# Upper limit
c_max = bandwidth * math.log2(1 + snr_linear)
# Practical datarate
c_practical = c_max *2/3
# No. of signal levels
m = math.ceil(2**(c_practical/(2*bandwidth)))
print(f"Q2")
print(f"Upper limit to the datarate is {c_max:.2f} bps.")
print(f"Sinal levels needed for 2/3 of upper limit is {m:d}.\n")
