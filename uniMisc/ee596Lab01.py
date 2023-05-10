"""EE596 Lab 01 - generateCodebook COding
E/17/371

References:
    - https://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column
"""

import logging
import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt


def plotSave(array,name):
    """Plot an image given as an array, and save to the working directory as png"""
    global figNo
    global workingDirectory
    # plt.figure(f"Figure {figNo:02} - {name}")
    # plt.imshow(array)
    # plt.show()
    plt.imsave(f"{workingDirectory}\\Figures\\Figure {figNo:02} - {name}.png",array)
    figNo += 1


def plotSaveLayers(array,name):
    """Separately plot and save the Y, Cb, and Cr layers of an image given as an 
    array to the working directory as png
    """
    for i,layer in enumerate(array):
        plotSave(layer.reshape(16,16),f"{name} layer {i+1}")


def generateCodebook(symbolProb):
    """Return a 2D array of sybols and their symbolCodes according to generateCodebook algorithm"""
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
        # logger.debug(f"i: {i}, symbol: {p_symbol} {c_symbol}, cumulative: {p_cumulative} {c_cumulative}")
        symbolCodes[i,1] = c_symbol
        symbolCodes[i+1,1] = c_cumulative
    logger.debug(f"symbolCodes: \n{symbolCodes}")
    return dict(symbolCodes)


def encode(symbols,codebook):
    """Encode a 1D array of symbols into a sring of bits using accoring to a codebook"""
    codewords = []
    for symbol in symbols:
        codewords.append(codebook.get(symbol))
    bitStream = "".join(codewords)
    return bitStream

def decode(bits,codebook):
    pass


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
    croppedLayers = np.swapaxes(croppedImage,1,2)
    croppedLayers = np.swapaxes(croppedLayers,0,1)
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
    # plotSave(croppedQuantizedLayers[0].reshape(16,16),"Cropped image layer 1")
    # plotSave(croppedQuantizedLayers[1].reshape(16,16),"Cropped image layer 2")
    # plotSave(croppedQuantizedLayers[2].reshape(16,16),"Cropped image layer 3")
    plotSaveLayers(croppedQuantizedLayers,"Cropped and quantised image")

    ## Step 5 
    ## Find probabilities of each symbol
    logger.debug(f"uniqe elements: {np.unique(croppedQuantizedLayers[1],return_counts=True)}")
    croppedUniques_y,counts_y = np.unique(croppedQuantizedLayers[0],return_counts=True)
    croppedUniques_cb,counts_cb = np.unique(croppedQuantizedLayers[1],return_counts=True)
    croppedUniques_cr,counts_cr = np.unique(croppedQuantizedLayers[2],return_counts=True)
    # croppedProb_y = dict(zip(croppedUniques_y,counts_y/256))
    # croppedProb_cb = dict(zip(croppedUniques_cb,counts_cb/256))
    # croppedProb_cr = dict(zip(croppedUniques_cr,counts_cr/256))
    croppedProb_y = np.array(list(zip(croppedUniques_y,counts_y/256)))
    croppedProb_cb = np.array(list(zip(croppedUniques_cb,counts_cb/256)))
    croppedProb_cr = np.array(list(zip(croppedUniques_cr,counts_cr/256)))
    testArray = np.array([[128, 0.47],[87, 0.25],[186, 0.25],[256, 0.03]])
    ## Sort in descending order of probablity
    croppedProb_y = croppedProb_y[croppedProb_y[:, 1].argsort()[::-1]]
    croppedProb_cb = croppedProb_cb[croppedProb_cb[:, 1].argsort()[::-1]]
    croppedProb_cr = croppedProb_cr[croppedProb_cr[:, 1].argsort()[::-1]]
    testArray = testArray[testArray[:, 1].argsort()[::-1]]
    logger.debug(f"probabilities: \n{croppedProb_y} \n{croppedProb_cb}\n{croppedProb_cr}")

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
    croppedCodeStream_y = encode(croppedSymbolStream_y,croppedCodebook_y)
    croppedCodeStream_cb = encode(croppedSymbolStream_cb,croppedCodebook_cb)
    croppedCodeStream_cr = encode(croppedSymbolStream_cr,croppedCodebook_cr)

    ## Step 8
    ## Save the compressed image into a text file
    with open(f"{workingDirectory}\\Encoded\\pattern-cropped.txt","w") as file:
        file.write(f"{croppedCodeStream_y}\n{croppedCodeStream_cb}\n{croppedCodeStream_cr}")
        file.close()

    ## Step 10
    ## Decode the images.
    with open(f"{workingDirectory}\\Encoded\\pattern-cropped.txt","r") as file:
        lines = [line.strip() for line in file.readlines()]
        file.close()
    # logger.debug(f"lines: {lines}")