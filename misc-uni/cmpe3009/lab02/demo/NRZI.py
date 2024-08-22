import matplotlib.pyplot as plt
import numpy as np

# Your original 11-bit data
data = [0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0]

# Create time values for the number of bits you have
time = np.arange(len(data) + 1)

# Adjust the data to have one more point for the last transition
adjusted_data = np.append(data, data[-1])

# Plotting the data
plt.figure(figsize=(10, 5))
plt.step(time, adjusted_data, where='post')
plt.ylim(-0.5, 1.5)
plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('Original Data Plot')
plt.grid(True)
plt.show()

def nrz_invert_encoding(data):
    encoded = []
    last_level = 0  # Start with 0 voltage level

    for bit in data:
        if bit == 1:
            last_level = 1 - last_level  # Toggle the level
        encoded.append(last_level)

    return encoded

#data = "010010110110"
encoded_data = nrz_invert_encoding(data)
print(*data)
print(*encoded_data)

# Create time values for the number of bits you have
time = np.arange(len(data) + 1)

# Adjust the data to have one more point for the last transition
adjusted_data = np.append(encoded_data, encoded_data[-1])

# Plotting the data
plt.figure(figsize=(10, 5))
plt.step(time, adjusted_data, where='post')
plt.ylim(-0.5, 1.5)
plt.xlabel('Time')
plt.ylabel('Signal')
plt.title('Encoded Data Plot')
plt.grid(True)
plt.show()




