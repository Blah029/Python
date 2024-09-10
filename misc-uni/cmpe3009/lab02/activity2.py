"""COMP3009 Lab 02 - Encoding and Modulation
Activity 2
"""

import matplotlib.pyplot as plt
import numpy as np

num_levels = 16
num_symbols = 1000
bits_per_symbol = int(np.log2(num_levels))
num_bits = num_symbols * bits_per_symbol
levels_per_dimension = np.sqrt(num_levels)


def qam_modulate(symbols: np.ndarray):
    """Perform Quadrature Amplitude Modulation on symbols"""
    i_component = np.array(
        [
            (symbol // levels_per_dimension) - (levels_per_dimension // 2) + 0.5
            for symbol in symbols
        ]
    )
    q_component = np.array(
        [
            (symbol % levels_per_dimension) - (levels_per_dimension // 2) + 0.5
            for symbol in symbols
        ]
    )
    return i_component, q_component


def qam_demodulate(i_component: np.ndarray, q_component: np.ndarray):
    """Demodulate QAM signal into symbols"""
    quotient = i_component + levels_per_dimension // 2 - 0.5
    remainder = q_component + levels_per_dimension // 2 - 0.5
    return quotient * levels_per_dimension + remainder.astype(int)


if __name__ == "__main__":
    ## Generate input bitstream
    np.random.seed(0)
    input_bits = np.random.randint(0, 2, num_bits)
    ## Map bits to symbols
    input_symbols = np.array(
        [
            int("".join(input_bits[i : i + bits_per_symbol].astype(str)), 2)
            for i in range(0, num_bits, bits_per_symbol)
        ]
    )
    plt.figure(1)
    plt.stem(input_symbols[0:40])
    plt.title("Input Symbols")
    plt.xlabel("Bit")
    plt.ylabel("Level")
    plt.grid()
    plt.show()
    ## QAM modulation
    qam_i, qam_q = qam_modulate(input_symbols)
    ## Add noise to the signal
    noise_std = 0.1
    noisy_i = qam_i + np.random.normal(0, noise_std, qam_i.shape)
    noisy_q = qam_q + np.random.normal(0, noise_std, qam_q.shape)
    ## Visualise
    plt.figure(2)
    plt.scatter(noisy_i, noisy_q)
    plt.title("Noisy QAM Constellation")
    plt.xlabel("I component")
    plt.ylabel("Q component")
    plt.grid()
    plt.show()
    ## Democulate
    demodulated_symbols = qam_demodulate(noisy_i, noisy_q)
    plt.figure(3)
    plt.stem(demodulated_symbols[0:40])
    plt.title("Demodulated Symbols")
    plt.xlabel("Bit")
    plt.ylabel("Level")
    plt.grid()
    plt.show()
    symbol_errors = demodulated_symbols - input_symbols
    plt.figure(4)
    plt.stem(symbol_errors[0:40])
    plt.title("Symbol Errors")
    plt.xlabel("Bit")
    plt.ylabel("Level")
    plt.grid()
    plt.show()
