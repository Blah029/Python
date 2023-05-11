"""EE596 Lab 01 - generateCodebook COding
E/17/371

References:
    - https://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column
    - https://stackoverflow.com/questions/483666/reverse-invert-a-dictionary-mapping
"""

import logging
import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt


def swapChannelLayers(image):
    """Swap axes from(x,y,channel) to (channel,x,y)"""
    swappedImage = np.swapaxes(image,1,2)
    return  np.swapaxes(swappedImage,0,1)


def plotSave(image,name):
    """Plot an image given as an array, and save to 
    the working directory as png
    """
    global figNo
    global workingDirectory
    # plt.figure(f"Figure {figNo:02} - {name}")
    # plt.imshow(array)
    # plt.show()
    plt.imsave(f"{workingDirectory}\\Figures\\Figure {figNo:02} - {name}.png",image)
    figNo += 1


def plotSaveLayers(image,name):
    """Separately plot and save the Y, Cb, and Cr layers of an image given as 
    an array to the working directory as png
    """
    for i,layer in enumerate(image):
        plotSave(layer.reshape(16,16),f"{name} layer {i+1}")


def generateCodebook(symbolProb):
    """Return a 2D array of sybols and their symbolCodes according to 
    Huffamn algorithm
    """
    symbolCodes = np.zeros(np.shape(symbolProb), dtype="object")
    symbolCodes[:,0] = symbolProb[:,0]
    # logger.debug(f"inital symbolCodes: \n{symbolCodes}")
    c_carryOver = ""
    for i in range(np.shape(symbolProb)[0] - 1):
        ## Probablities of the symbol under coideration
        p_symbol = symbolProb[i,1]
        ## Sum of remaining probabilities
        p_cumulative = 0
        for j in range(i+1,np.shape(symbolProb)[0]):
            p_cumulative += symbolProb[j,1]
        ## Determine 1 or 0
        if p_cumulative >= p_symbol:
            c_cumulative = c_carryOver + "0"
            c_symbol = c_carryOver + "1"
            c_carryOver += "0"
        else:
            c_symbol = c_carryOver + "0"
            c_cumulative = c_carryOver + "1"
            c_carryOver += "1"
        # logger.debug(f"i: {i}, symbol: {p_symbol} {c_symbol}, \
        #              cumulative: {p_cumulative} {c_cumulative}")
        symbolCodes[i,1] = c_symbol
        symbolCodes[i+1,1] = c_cumulative
    logger.debug(f"symbolCodes: \n{symbolCodes}")
    return dict(symbolCodes)


def encodeSymbols(symbols,codebook):
    """Encode a 1D array of symbols into a sring of bits 
    accoring to a codebook
    """
    codewords = []
    for symbol in symbols:
        codewords.append(codebook.get(symbol))
    bitStream = "".join(codewords)
    return bitStream

def decodeBitstream(bitstream,codebook):
    inverseCodebook = {v:k for k,v in codebook.items()}
    symbols = []
    receivedBits = ""
    for bit in bitstream:
        receivedBits += bit
        if receivedBits in inverseCodebook:
            symbols.append(inverseCodebook.get(receivedBits))
            receivedBits = ""
        else:
            pass
    decodedArray = np.array(symbols)
    return decodedArray.reshape(16,16)


if __name__ == "__main__":
    ## Set up the logger
    logging.basicConfig(format="[%(name)s][%(levelname)s] %(message)s")
    logger = logging.getLogger("ee596Lab01")
    logger.setLevel(logging.DEBUG)
    ## Reset figure numbner
    figNo = 1    
    ## Select the starting point for the cropped window from E/17/371  
    start = np.array([3*60, 71*4])
    workingDirectory = "D:\\User Files\\Documents\\University\\Misc\\4th Year Work\\Semester 7\\EE596\\EE596 Lab 01"
    
    ## Step 2
    ## Read image
    image = img.imread(f"{workingDirectory}\\Images\\Pattern-612x612.jpg")

    ## Step 3
    # Crop and separate Y, Cb, and Cr layers
    croppedImage = image[start[0]:start[0]+16, start[1]:start[1]+16]
    croppedLayers = swapChannelLayers(croppedImage)
    logger.debug(f"crop shape: {np.shape(croppedImage)}")
    logger.debug(f"crop[0] shape: {np.shape(croppedImage[0])}")
    logger.debug(f"crop[0,0] shape: {np.shape(croppedImage[0,0])}")
    ## Plot and save
    plotSave(image,"Original image")
    plotSave(croppedImage,"Cropped image")
    # plotSave(croppedLayers[0].reshape(16,16),"Cropped image layer 1")
    # plotSave(croppedLayers[1].reshape(16,16),"Cropped image layer 2")
    # plotSave(croppedLayers[2].reshape(16,16),"Cropped image layer 3")
    plotSaveLayers(croppedLayers,"Cropped image")

    ## Step 4
    ## Quantise output to 8 levels
    bins = np.arange(0,256,256/8)
    logger.debug(f"bins: {bins}")
    croppedQuantizedLayers = np.digitize(croppedLayers,bins)
    logger.debug(f"quantized: \n{croppedQuantizedLayers[1].reshape(16,16)}")
    ## Plot and save
    # plotSave(croppedQuantizedLayers[0].reshape(16,16),
    #          "Cropped image layer 1")
    # plotSave(croppedQuantizedLayers[1].reshape(16,16),
    #          "Cropped image layer 2")
    # plotSave(croppedQuantizedLayers[2].reshape(16,16),
    #          "Cropped image layer 3")
    plotSaveLayers(croppedQuantizedLayers,"Cropped and quantised image")

    ## Step 5 
    ## Find probabilities of each symbol
    logger.debug(f"uniqe elements: {np.unique(croppedQuantizedLayers[1],return_counts=True)}")
    croppedUniques_y,counts_y = np.unique(croppedQuantizedLayers[0],
                                          return_counts=True)
    croppedUniques_cb,counts_cb = np.unique(croppedQuantizedLayers[1],
                                            return_counts=True)
    croppedUniques_cr,counts_cr = np.unique(croppedQuantizedLayers[2],
                                            return_counts=True)
    # croppedProb_y = dict(zip(croppedUniques_y,counts_y/256))
    # croppedProb_cb = dict(zip(croppedUniques_cb,counts_cb/256))
    # croppedProb_cr = dict(zip(croppedUniques_cr,counts_cr/256))
    croppedProb_y = np.array(list(zip(croppedUniques_y,counts_y/256)))
    croppedProb_cb = np.array(list(zip(croppedUniques_cb,counts_cb/256)))
    croppedProb_cr = np.array(list(zip(croppedUniques_cr,counts_cr/256)))
    encodeTestArray = np.array([[128, 0.47],[87, 0.25],[186, 0.25],[256, 0.03]])
    ## Sort in descending order of probablity
    croppedProb_y = croppedProb_y[croppedProb_y[:, 1].argsort()[::-1]]
    croppedProb_cb = croppedProb_cb[croppedProb_cb[:, 1].argsort()[::-1]]
    croppedProb_cr = croppedProb_cr[croppedProb_cr[:, 1].argsort()[::-1]]
    encodeTestArray = encodeTestArray[encodeTestArray[:, 1].argsort()[::-1]]
    logger.debug(f"probabilities: {croppedProb_y} \n{croppedProb_cb} \n{croppedProb_cr}")

    ## Step 6
    ## Construct the Huffamn coding algorith (see line 34)
    croppedCodebook_y = generateCodebook(croppedProb_y)
    croppedCodebook_cb = generateCodebook(croppedProb_cb)
    croppedCodebook_cr = generateCodebook(croppedProb_cr)
    logger.debug(f"code dictionaries: \n {croppedCodebook_y} \n {croppedCodebook_cb} \n {croppedCodebook_cr}")
    logger.debug(f"cb symbol {8}, cb mapped codeword: {croppedCodebook_cb.get(4)}")

    ## Step 7
    ## Compress both original and cropped images
    ## Convert to a stream of symbols
    croppedSymbolStream_y = croppedQuantizedLayers[0].reshape(16*16)
    croppedSymbolStream_cb = croppedQuantizedLayers[1].reshape(16*16)
    croppedSymbolStream_cr = croppedQuantizedLayers[2].reshape(16*16)
    logger.debug(f"stream: {croppedSymbolStream_y[-16:-1]}, matrix: {croppedQuantizedLayers[0,15]}")
    logger.debug(f"stream: {croppedSymbolStream_cb[-16:-1]}, matrix: {croppedQuantizedLayers[1,15]}")
    logger.debug(f"stream: {croppedSymbolStream_cr[-16:-1]}, matrix: {croppedQuantizedLayers[2,15]}")
    ## Map sybols into codewords using the codebook
    croppedBitstream_y = encodeSymbols(croppedSymbolStream_y,croppedCodebook_y)
    croppedBitstream_cb = encodeSymbols(croppedSymbolStream_cb,croppedCodebook_cb)
    croppedBitstream_cr = encodeSymbols(croppedSymbolStream_cr,croppedCodebook_cr)

    ## Step 8
    ## Save the compressed image into a text file
    with open(f"{workingDirectory}\\Encoded\\pattern-cropped.txt","w") as file:
        file.write(f"{croppedBitstream_y} \n{croppedBitstream_cb} \n{croppedBitstream_cr}")
        file.close()

    ## Step 10
    ## Decode the images.
    with open(f"{workingDirectory}\\Encoded\\pattern-cropped.txt","r") as file:
        lines = [line.strip() for line in file.readlines()]
        file.close()
    readBitStream_y = np.array(list(lines[0]))
    readBitStream_cb = np.array(list(lines[1]))
    readBitStream_cr = np.array(list(lines[2]))
    decodedArray_y = decodeBitstream(readBitStream_y,croppedCodebook_y)
    decodedArray_cb = decodeBitstream(readBitStream_cb,croppedCodebook_cb)
    decodedArray_cr = decodeBitstream(readBitStream_cr,croppedCodebook_cr)
    logger.debug(f"error: \n{decodedArray_cb - croppedQuantizedLayers[1]}")
    # decodedLayers = 