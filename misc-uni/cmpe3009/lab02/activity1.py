"""COMP3001 Lab 02 - Encoding and Modulation
Activity 1
"""

import matplotlib.pyplot as plt
import numpy as np

original_data = np.array([0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0])


def nrz_encoding(data: np.ndarray):
    """Perform Non Return to Zero Inverted endcoding
    1: transition
    0: no transition
    """
    output = []
    endcoded_bit = 0
    for bit in data:
        if bit == 1:
            endcoded_bit = int(not endcoded_bit)
        output.append(endcoded_bit)
    return np.array(output)


def bipolar_ami_encoding(data: np.ndarray):
    """Perform Bipolar AMI
    1: alternating +/-
    0: no transition
    """
    output = []
    positive_symbol_flag = False
    for bit in data:
        if bit == 1:
            if positive_symbol_flag:
                output.append(-1)
                positive_symbol_flag = 0
            else:
                output.append(1)
                positive_symbol_flag = 1
        else:
            output.append(0)
    return np.array(output)


def plot_signal(data: np.ndarray, title: str = "", no: int = None):
    """Configure matplotlib plot"""
    x_arr = np.arange(len(original_data))
    plt.figure(no)
    plt.step(x_arr, data)
    plt.xlabel("Time")
    plt.ylabel("Signal")
    plt.title(title)
    plt.grid()
    plt.show()


if __name__ == "__main__":
    # x_arr = np.arange(len(original_data))
    print(f"Input:       {' '.join(original_data.astype(str))}")

    ## Plot original
    plot_signal(original_data, "Original Data Plot", 1)

    ## Encode NRZI
    nrz_data = nrz_encoding(original_data)
    print(f"NRZ-I:       {' '.join(nrz_data.astype(str))}")
    plot_signal(nrz_data, "NRZ-I Encoding", 2)

    ## Encode Bipolar AMI
    bipolar_ami_data = bipolar_ami_encoding(original_data)
    print(f"Bipolar AMI: {' '.join(bipolar_ami_data.astype(str))}")
    plot_signal(bipolar_ami_data, "Bipolar AMI Encoding", 3)
