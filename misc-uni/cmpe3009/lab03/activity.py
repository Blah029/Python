"""COMP3009 Lab 03 - Error Detection and Correction"""

import random


def crc_transmitter(data: str, generator: str):
    """Create CRC codeword"""
    data = data + "0" * (len(generator) - 1)
    remainder = modul0_2(data, generator)

    return bin(int(data, 2) | int(remainder, 2))[2:]


def crc_receiver(codeword: str, generator: str):
    """Check received codeword for bit errors"""
    error_flag = False
    remainder = int(modul0_2(codeword, generator), 2)

    if remainder != 0:
        error_flag = True

    return remainder, error_flag


def modul0_2(numerator: str, denominator: str):
    """Perform modulo-2 division and return remainder"""
    denominator_len = len(denominator)
    temp_num = numerator[:denominator_len]
    temp_remainder = "0" * (denominator_len - 1)

    for i in range(len(numerator) - denominator_len + 1):
        ## Check if modulo-2 division can be performed on ith digit
        # if temp_num[0] == "1":
        #     temp_denominator = denominator
        #     temp_remainder = format(
        #         int(temp_num, 2) ^ int(temp_denominator, 2), f"0{denominator_len - 1}b"
        #     )
        #     print("\t", i, numerator, temp_num, denominator, temp_remainder)
        #     ## Check if numerator has any digits left and take it
        #     if i + denominator_len < len(numerator):
        #         temp_num = temp_remainder + numerator[i + denominator_len]
        # else:
        #     temp_denominator = "0" * denominator_len
        #     temp_remainder = format(
        #         int(temp_num, 2) ^ int(temp_denominator, 2), f"0{denominator_len - 1}b"
        #     )
        #     print("\t", i, numerator, temp_num, denominator, temp_remainder)
        #     ## Check if numerator has any digits left and take it
        #     if i + denominator_len < len(numerator):
        #         temp_num = temp_num[1:] + numerator[i + denominator_len]
        if temp_num[0] == "1":
            temp_denominator = denominator
        else:
            temp_denominator = "0" * denominator_len
        temp_remainder = format(
            int(temp_num, 2) ^ int(temp_denominator, 2), f"0{denominator_len - 1}b"
        )
        print("\t", i, numerator, "->", temp_num, "%", denominator, "=", temp_remainder)
        ## Check if numerator has any bits left and take it
        if i + denominator_len < len(numerator):
            temp_num = temp_remainder + numerator[i + denominator_len]

    return temp_remainder


def introduce_error(bitstream: str):
    """Flip randomly selected bits"""
    bitstream = list(bitstream)
    num_bits = len(bitstream)
    num_flips = random.randint(1, num_bits // 2)
    indices = random.sample(range(num_bits), num_flips)

    for index in indices:
        bitstream[index] = str(int(not int(bitstream[index])))

    return "".join(bitstream), num_flips


if __name__ == "__main__":
    data_poly = "100100"
    generator_poly = "1101"

    ## Transmiter
    transmitted = crc_transmitter(data_poly, generator_poly)
    print("Transmiiited:", transmitted)
    ## Channel
    received, num_errors = introduce_error(transmitted)
    print("Received:    ", received, "Errors injected:", num_errors)
    ## Receiver
    crc_remainder, bit_error = crc_receiver(received, generator_poly)
    print("CRC remainder:  ", crc_remainder, "\nError detection:", bit_error)

    ## Test 1
    # test_remainder = modul0_2("000000101", "1101")
    # print(test_remainder)
