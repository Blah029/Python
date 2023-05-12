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


def swapChannelLayers(pixelArray):
    """Swap axes from(x,y,channel) to (channel,x,y) and vice versa"""
    ## Bring layers out
    if np.shape(pixelArray)[2] == 3:
        swappedImage = np.swapaxes(pixelArray,1,2)
        swappedImage = np.swapaxes(swappedImage,0,1)
    ## Puch layers back
    elif np.shape(pixelArray)[0] == 3:
        swappedImage = np.swapaxes(pixelArray,0,1)
        swappedImage = np.swapaxes(swappedImage,1,2)
    return swappedImage


def plotSave(pixelArray, name=None):
    """Plot an image given as an array, and save to 
    the working directory as png
    """
    global figNo
    global workingDirectory
    # plt.figure(f"Figure {figNo:02} - {name}")
    # plt.imshow(array)
    # plt.show()
    plt.imsave(f"{workingDirectory}\\Figures\\Figure {figNo:02} - {name}.png",pixelArray)
    figNo += 1


def plotSaveLayers(pixelArray, name=None):
    """Separately plot and save the Y, Cb, and Cr layers of an image given as 
    an array to the working directory as png
    """
    xSize = np.shape(pixelArray)[1]
    ySize = np.shape(pixelArray)[2]
    for i,layer in enumerate(pixelArray):
        plotSave(layer.reshape(xSize,ySize),f"{name} layer {i+1}")


def generateCodebook(symbolProb):
    """Return a 2D array of sybols and their symbolCodes according to 
    Huffamn algorithm
    """
    symbolCodes = np.zeros(np.shape(symbolProb), dtype="object")
    symbolCodes[:,0] = symbolProb[:,0]
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
    if np.shape(symbolCodes)[0] == 1:
        symbolCodes[0,1] = "0"
    # logger.debug(f"symbolCodes: \n{symbolCodes}")
    return dict(symbolCodes)


def encodeSymbols(symbols,codebook):
    """Encode a 1D array of symbols into a sring of bits 
    accoring to a codebook
    """
    codewords = []
    for symbol in symbols:
        codewords.append(codebook.get(symbol))
    # logger.debug(f"codebook: {codebook}")
    # logger.debug(f"codewords: {codewords}")
    bitStream = "".join(codewords)
    return bitStream


def decodeBitstream(bitstream,codebook,dimensions):
    inverseCodebook = {v:k for k,v in codebook.items()}
    symbols = []
    receivedBits = ""
    for bit in bitstream:
        receivedBits += bit
        if receivedBits in inverseCodebook:
            symbols.append(inverseCodebook.get(receivedBits))
            receivedBits = ""
            # logger.debug(f"decodeBitstream: {receivedBits} in inverseCodebook")
        else:
            # logger.debug(f"decodeBitstream: {receivedBits} not in inverseCodebook")
            pass
    decodedArray = np.array(symbols)
    # logger.debug(f"bitstream \n{bitstream}")
    # logger.debug(f"inverse codebook: {inverseCodebook}")
    # logger.debug(f"decoded symbols: {symbols}")
    return decodedArray.reshape(dimensions[0],dimensions[1])


def steps4to8(pixelArray,workingDirectory, label=None):
    """Step 4 to step 8 of the lab assignemtn. 
    Repeated for original image and cropped image.
    """
    xSize = np.shape(pixelArray)[0]
    ySize = np.shape(pixelArray)[1]
    logger.debug(f"size: {xSize}x{ySize}")
    layers = swapChannelLayers(pixelArray)
    # logger.info(f"{label} axes swapped")
    logger.debug(f"crop shape: {np.shape(pixelArray)}")
    logger.debug(f"crop[0] shape: {np.shape(pixelArray[0])}")
    logger.debug(f"crop[0,0] shape: {np.shape(pixelArray[0,0])}")
    ## Plot and save
    plotSave(pixelArray,f"Raw {label} image")
    # plotSave(layers[0].reshape(xSize,ySize),"Cropped pixelArray layer 1")
    # plotSave(layers[1].reshape(xSize,ySize),"Cropped pixelArray layer 2")
    # plotSave(layers[2].reshape(xSize,ySize),"Cropped pixelArray layer 3")
    plotSaveLayers(layers,f"Raw {label} image")

    ## Step 4
    ## Quantise output to 8 levels
    bins = np.arange(0,256,256/8)
    logger.debug(f"bins: {bins}")
    quantizedLayers = np.digitize(layers,bins)
    # logger.info(f"{label} quantized")
    # logger.debug(f"quanitzed layers: \n{quantizedLayers}")
    ## Plot and save
    plotSaveLayers(quantizedLayers,f"Quantized {label} image")

    ## Step 5 
    ## Find probabilities of each symbol
    uniqueSymbols_y,counts_y = np.unique(quantizedLayers[0],
                                          return_counts=True)
    uniqueSymbols_cb,counts_cb = np.unique(quantizedLayers[1],
                                            return_counts=True)
    uniqueSymbols_cr,counts_cr = np.unique(quantizedLayers[2],
                                            return_counts=True)
    # probability_y = dict(zip(uniqueSymbols_y,counts_y/256))
    # probability_cb = dict(zip(uniqueSymbols_cb,counts_cb/256))
    # probability_cr = dict(zip(uniqueSymbols_cr,counts_cr/256))
    probability_y = np.array(list(zip(uniqueSymbols_y,counts_y/256)))
    probability_cb = np.array(list(zip(uniqueSymbols_cb,counts_cb/256)))
    probability_cr = np.array(list(zip(uniqueSymbols_cr,counts_cr/256)))
    encodeTestArray = np.array([[128, 0.47],[87, 0.25],[186, 0.25],[256, 0.03]])
    ## Sort in descending order of probablity
    probability_y = probability_y[probability_y[:, 1].argsort()[::-1]]
    probability_cb = probability_cb[probability_cb[:, 1].argsort()[::-1]]
    probability_cr = probability_cr[probability_cr[:, 1].argsort()[::-1]]
    encodeTestArray = encodeTestArray[encodeTestArray[:, 1].argsort()[::-1]]
    logger.debug(f"probabilities: \n{probability_y} \n{probability_cb} \n{probability_cr}")

    ## Step 6
    ## Construct the Huffamn coding algorith (see line 34)
    codebook_y = generateCodebook(probability_y)
    codebook_cb = generateCodebook(probability_cb)
    codebook_cr = generateCodebook(probability_cr)
    # logger.info(f"{label} codebooks generated")
    logger.debug(f"code dictionaries: \n {codebook_y} \n {codebook_cb} \n {codebook_cr}")

    ## Step 7
    ## Compress both original and cropped images
    ## Convert to a stream of symbols
    symbolStream_y = quantizedLayers[0].reshape(xSize*ySize)
    symbolStream_cb = quantizedLayers[1].reshape(xSize*ySize)
    symbolStream_cr = quantizedLayers[2].reshape(xSize*ySize)
    # logger.debug(f"stream: {symbolStream_y[-xSize:-1]}, matrix: {quantizedLayers[0,xSize-1]}")
    # logger.debug(f"stream: {symbolStream_cb[-xSize:-1]}, matrix: {quantizedLayers[1,xSize-1]}")
    # logger.debug(f"stream: {symbolStream_cr[-xSize:-1]}, matrix: {quantizedLayers[2,xSize-1]}")
    ## Map sybols into codewords using the codebook
    bitstream_y = encodeSymbols(symbolStream_y,codebook_y)
    bitstream_cb = encodeSymbols(symbolStream_cb,codebook_cb)
    bitstream_cr = encodeSymbols(symbolStream_cr,codebook_cr)
    bitstream = "\n".join([bitstream_y,bitstream_cb,bitstream_cr])
    # logger.info(f"{label} encoded")

    ## Step 8
    ## Save the compressed image into a text file
    with open(f"{workingDirectory}\\Encoded\\pattern-{label}.txt","w") as file:
        file.write(f"{xSize}x{ySize}\n{bitstream}")
        file.close()
    return bitstream, [codebook_y,codebook_cb,codebook_cr], quantizedLayers


def step10_1(path,codebooks, label=None):
    """Read from a text file and pass data to step10_2 function"""
    ## Read encoded file
    with open(path,"r") as file:
        lines = [line.strip() for line in file.readlines()]
        dimensions = list(map(int,lines[0].split("x")))
        bitsream = lines[1:]
        file.close()
        # logger.debug(f"read bitsream: \n{bitsream}")
    # logger.info(f"file read")

    ## Step 10
    ## Decompress the outputs
    step10_2(bitsream,dimensions,codebooks,label)


def step10_2(encodedData,dimensions,channelCodebooks, label=None):
    """Step 10 of the lab assignemtn.
    Repeated of original image and cropped image.
    """
    ## Separate channel bitsreams
    readBitStream_y = np.array(list(encodedData[0]))
    readBitStream_cb = np.array(list(encodedData[1]))
    readBitStream_cr = np.array(list(encodedData[2]))
    logger.debug(f"step10_2 bitstream sizes: y: {np.size(readBitStream_y)}, cb: {np.size(readBitStream_cb)}, cr: {np.size(readBitStream_cr)}")
    ## Decode bisteams
    decodedArray_y = decodeBitstream(readBitStream_y,channelCodebooks[0],dimensions)
    decodedArray_cb = decodeBitstream(readBitStream_cb,channelCodebooks[1],dimensions)
    decodedArray_cr = decodeBitstream(readBitStream_cr,channelCodebooks[2],dimensions)
    # logger.info(f"{label} decoded")
    # logger.debug(f"decoded array: \n{decodedArray_cb}")
    ## Merge channels
    decodedLayers = np.array([decodedArray_y,decodedArray_cb,decodedArray_cr])
    decodedImage = swapChannelLayers(decodedLayers)/8
    logger.debug(f"decoded image shape: {np.shape(decodedImage)}")
    plotSaveLayers(decodedLayers,f"Decoded {label} image")
    plotSave(decodedImage,f"Decoded {label} image")


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
    ## Crop
    croppedImage = image[start[0]:start[0]+16, start[1]:start[1]+16]

    ## Step 4 to step 8
    ## Cropped image
    croppedBitstream, croppedCodebooks, croppedQuantized = \
        steps4to8(croppedImage,workingDirectory,"cropped")
    ## Original image
    originalBitstream, originalCodebooks,originalQuantized = \
        steps4to8(image,workingDirectory,"original")
    
    ## Step 10
    ## Cropped image
    step10_1(f"{workingDirectory}\\Encoded\\pattern-cropped.txt",croppedCodebooks,"cropped")
    ## Original image
    step10_1(f"{workingDirectory}\\Encoded\\pattern-original.txt",originalCodebooks,"original")
