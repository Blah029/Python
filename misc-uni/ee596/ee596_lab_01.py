"""EE596 Lab 01 - Huffman coding
E/17/371

References:
    - https://stackoverflow.com/questions/2828059/sorting-arrays-in-numpy-by-column
    - https://stackoverflow.com/questions/483666/reverse-invert-a-dictionary-mapping
    - https://www.hdm-stuttgart.de/~maucher/Python/MMCodecs/html/basicFunctions.html
"""
import logging
import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt


def swapChannelLayers(image:np.ndarray):
    """Swap axes from(x,y,channel) to (channel,x,y) and vice versa"""
    ## Bring layers out
    if image.shape[2] == 3:
        swappedImage = np.swapaxes(image,1,2)
        swappedImage = np.swapaxes(swappedImage,0,1)
    ## Puch layers back
    elif image.shape[0] == 3:
        swappedImage = np.swapaxes(image,0,1)
        swappedImage = np.swapaxes(swappedImage,1,2)
    return swappedImage


def saveImage(image:np.ndarray, name:str=None):
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


def saveChannels(layers:np.ndarray, name:str=None):
    """Separately plot and save the Y, Cb, and Cr layers of an image given as 
    an array to the working directory as png
    """
    xSize = layers.shape[1]
    ySize = layers.shape[2]
    for i,layer in enumerate(layers):
        composite = np.zeros((layers.shape))
        composite[i] = layer.reshape(xSize,ySize)
        saveImage(swapChannelLayers(composite),f"{name} layer {i+1}")


def generateCodebook(symbolProb:np.ndarray):
    """Return a 2D array of sybols and their symbolCodes according to 
    Huffamn algorithm
    """
    symbolCodes = np.zeros(symbolProb.shape, dtype="object")
    symbolCodes[:,0] = symbolProb[:,0]
    c_carryOver = ""
    for i in range(symbolProb.shape[0] - 1):
        ## Probablities of the symbol under coideration
        p_symbol = symbolProb[i,1]
        ## Sum of remaining probabilities
        p_cumulative = 0
        for j in range(i+1,symbolProb.shape[0]):
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
    if symbolCodes.shape[0] == 1:
        symbolCodes[0,1] = "0"
    # logger.debug(f"symbolCodes: \n{symbolCodes}")
    return dict(symbolCodes)


def encodeSymbols(symbols:np.ndarray, codebook:dict):
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


def decodeBitstream(bitstream:str, codebook:dict, dimensions:list):
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


def calculateEntropy(layers:np.ndarray):
    """Calculate and return the entropy of the source imagae (default) 
    or quantised image
    """
    channelEntropy = np.zeros(3)
    if layers.shape[2] == 3:
        layers = swapChannelLayers(layers)
    layers = layers.reshape((layers.shape[0],
                                layers.shape[1]*layers.shape[2]))
    # logger.debug(f"reshaped layers: \n{np.round(layers*8)}")
    for i,layer in enumerate(layers):
        symbolSet = list(set(layer))
        symbolProbability = [np.size(layer[layer==i])/(layer.size)\
                                for i in symbolSet]
        channelEntropy[i] =  np.sum([p*np.log2(1.0/p) for p in symbolProbability])
        # logger.debug(f"layer entropy: {self.channelEntropy[i] }")
    return channelEntropy


def calculatePSNR(image1:np.ndarray, image2:np.ndarray):
    mse = np.mean((image1 - image2)**2)
    if mse == 0:
        psnr = None
    else:
        psnr = 10*np.log10(1/mse)
    return psnr


class Encoder:
    def __init__(self, image:np.ndarray, workingDirectory:str, 
                 label:str=None, qLevels=8):
        """Initialise encoder with image data, path to 
        wroking directory, and image label
        """
        ## Instance attributes
        self.image = image
        self.workingDirectory = workingDirectory
        self.label = label
        self.qLevels = qLevels
        self.xSize = self.image.shape[0]
        self.ySize = self.image.shape[1]
        self.layers = swapChannelLayers(self.image)
        # self.channelEntropy = np.zeros((3))
        logger.debug(f"size: {self.xSize}x{self.ySize}")
        # logger.info(f"{self.label} axes swapped")
        logger.debug(f"crop shape: {self.image.shape}")
        logger.debug(f"crop[0] shape: {self.image[0].shape}")
        logger.debug(f"crop[0,0] shape: {self.image[0,0].shape}")

        ## Step 4
        ## Quantise output to 8 levels
        bins = np.arange(0,1,1/self.qLevels)
        logger.debug(f"bins: {bins}")
        # self.quantisedLayers = np.digitize(self.layers,bins)/self.qLevels
        self.quantisedLayers = (np.digitize(self.layers,bins)-1)/(self.qLevels-1)
        # logger.info(f"{self.label} quantised")
        # logger.debug(f"quanitzed layers: \n{self.quantisedLayers}")

        ## Step 5 
        ## Find probabilities of each symbol
        uniqueSymbols_y,counts_y = np.unique(self.quantisedLayers[0],
                                            return_counts=True)
        uniqueSymbols_cb,counts_cb = np.unique(self.quantisedLayers[1],
                                                return_counts=True)
        uniqueSymbols_cr,counts_cr = np.unique(self.quantisedLayers[2],
                                                return_counts=True)
        probability_y = np.array(list(zip(uniqueSymbols_y,counts_y/(self.xSize*self.ySize))))
        probability_cb = np.array(list(zip(uniqueSymbols_cb,counts_cb/(self.xSize*self.ySize))))
        probability_cr = np.array(list(zip(uniqueSymbols_cr,counts_cr/(self.xSize*self.ySize))))
        encodeTestArray = np.array([[128, 0.47],[87, 0.25],
                                    [186, 0.25],[256, 0.03]])
        ## Sort in descending order of probablity
        self.probability_y = probability_y[probability_y[:, 1].argsort()[::-1]]
        self.probability_cb = probability_cb[probability_cb[:, 1].argsort()[::-1]]
        self.probability_cr = probability_cr[probability_cr[:, 1].argsort()[::-1]]
        encodeTestArray = encodeTestArray[encodeTestArray[:, 1].argsort()[::-1]]
        logger.debug(f"probabilities: \n{self.probability_y} \n{self.probability_cb} \n{self.probability_cr}")

        ## Step 6
        ## Construct the Huffamn coding algorith (see line 34)
        self.codebook_y = generateCodebook(self.probability_y)
        self.codebook_cb = generateCodebook(self.probability_cb)
        self.codebook_cr = generateCodebook(self.probability_cr)
        # logger.info(f"{self.label} codebooks generated")
        logger.debug(f"code dictionaries: \n {self.codebook_y} \n {self.codebook_cb} \n {self.codebook_cr}")

        ## Step 7
        ## Compress both original and cropped images
        ## Convert to a stream of symbols
        symbolStream_y = self.quantisedLayers[0].reshape(self.xSize*self.ySize)
        symbolStream_cb = self.quantisedLayers[1].reshape(self.xSize*self.ySize)
        symbolStream_cr = self.quantisedLayers[2].reshape(self.xSize*self.ySize)
        logger.debug(f"stream: {symbolStream_y.shape}, matrix: {self.quantisedLayers.shape}")
        ## Map sybols into codewords using the codebook
        bitstream_y = encodeSymbols(symbolStream_y,self.codebook_y)
        bitstream_cb = encodeSymbols(symbolStream_cb,self.codebook_cb)
        bitstream_cr = encodeSymbols(symbolStream_cr,self.codebook_cr)
        self.bitstream = "\n".join([bitstream_y,bitstream_cb,bitstream_cr])
        # logger.info(f"{self.label} encoded")

    def saveFigures(self):
        """Save raw image, raw channels, and quantised channels as png"""
        saveImage(self.image,f"Original {self.label} image")
        saveChannels(self.layers,f"Original {self.label} image")
        saveImage(swapChannelLayers(self.quantisedLayers),f"Quantised {self.label} image")           
        saveChannels(self.quantisedLayers,f"Quantised {self.label} image")

    def writeBitstream(self):
        """Write the bistream to a txt file"""
        with open(f"{self.workingDirectory}\\Encoded\\{self.label}.txt","w") \
            as file:
            file.write(f"{self.xSize}x{self.ySize}\n{self.bitstream}")
            file.close()
            logger.debug(f"Encoder.writeBitstream called")
    
    def getCodebooks(self):
        """Return the codebook of Y,Cb,Cr channels 
        as a list consisting of numpy arrays
        """
        return [self.codebook_y,self.codebook_cb,self.codebook_cr]


class Decoder:
    def __init__(self, path:str, codebooks:list, label:str=None):
        """Initialise the decoder with image data, path to 
        wroking directory, and image label
        """
        self.path = path
        self.codebooks = codebooks
        self.label = label
        with open(path,"r") as file:
            lines = [line.strip() for line in file.readlines()]
            self.dimensions = list(map(int,lines[0].split("x")))
            self.bitstream = lines[1:]
            file.close()
        ## Separate channel bitsreams
        bitstream_y = np.array(list(self.bitstream[0]))
        bitstream_cb = np.array(list(self.bitstream[1]))
        bitstream_cr = np.array(list(self.bitstream[2]))
        logger.debug(f"decoder bitstream sizes: y: {bitstream_y.size}, cb: {bitstream_cb.size}, cr: {bitstream_cr.size}")
        ## Decode bisteams
        decodedArray_y = decodeBitstream(bitstream_y,self.codebooks[0],
                                        self.dimensions)
        decodedArray_cb = decodeBitstream(bitstream_cb,self.codebooks[1],
                                        self.dimensions)
        decodedArray_cr = decodeBitstream(bitstream_cr,self.codebooks[2],
                                        self.dimensions)
        # logger.info(f"{label} decoded")
        # logger.debug(f"decoded array: \n{decodedArray_cb}")
        ## Merge channels
        self.decodedLayers = np.array([decodedArray_y,decodedArray_cb,decodedArray_cr])
        self.decodedImage = swapChannelLayers(self.decodedLayers)
        logger.debug(f"decoded image shape: {self.decodedImage.shape}")

    def saveFigures(self):
        """Save decoded channels, and decoded image as png"""
        saveImage(self.decodedImage,f"Decoded {self.label} image")
        saveChannels(self.decodedLayers,f"Decoded {self.label} image")


if __name__ == "__main__":
    ## Set up the logger
    logging.basicConfig(format="[%(name)s][%(levelname)s] %(message)s")
    logger = logging.getLogger("ee596-lab-01")
    logger.setLevel(logging.DEBUG)
    ## Reset figure numbner
    figNo = 1    
    ## Select the starting point for the cropped window from E/17/371  
    start = np.array([3*60, 71*4])
    qLevels = 8
    workingDirectory = "D:\\User Files\\Documents\\University\\Misc\\4th Year Work\\Semester 7\\EE596\\EE596 Lab 01"
    ## Step 2
    ## Read image
    uncroppedImage = img.imread(f"{workingDirectory}\\Images\\Pattern-612x612.jpg")/256
    ## Step 3
    ## Select 16x16 cropped sub-image
    croppedImage = uncroppedImage[start[0]:start[0]+16, start[1]:start[1]+16]
    
    ## Cropped image
    ## Steps 4 to step 7
    croppedEncode = Encoder(croppedImage,workingDirectory,"cropped",qLevels)
    croppedEncode.saveFigures()
    ## Step 8
    ## Save the compressed image into a text file
    croppedEncode.writeBitstream()
    ## Step 10
    croppedDecode = Decoder(f"{workingDirectory}\\Encoded\\cropped.txt",croppedEncode.getCodebooks(),"cropped")
    croppedDecode.saveFigures()

    ## Original image
    ## Steps 4 to step 7
    uncroppedEncode = Encoder(uncroppedImage,workingDirectory,"uncropped",qLevels)
    uncroppedEncode.saveFigures()
    ## Step 8
    ## Save the compressed image into a text file
    uncroppedEncode.writeBitstream()
    ## Step 10
    uncroppedDecode = Decoder(f"{workingDirectory}\\Encoded\\uncropped.txt",uncroppedEncode.getCodebooks(),"uncropped")
    uncroppedDecode.saveFigures()

    ## Step 11
    ## Discussion 1. ii.
    logger.info(f"entropy - original cropped:   {calculateEntropy(croppedImage)}")
    ## Calculate the entropy of the source image
    logger.info(f"entropy - original uncropped: {calculateEntropy(uncroppedImage)}")
    ## Discussion 1. iii.
    logger.info(f"entropy - decoded cropped:    {calculateEntropy(croppedDecode.decodedImage)}")
    logger.info(f"entropy - decoded uncropped:  {calculateEntropy(uncroppedDecode.decodedImage)}")

    ## Step 12
    ## Evaluate PSNR
    ## Original images
    logger.info(f"psnr - original cropped:   {calculatePSNR(croppedImage,croppedImage)}")
    logger.info(f"psnr - original uncropped: {calculatePSNR(uncroppedImage,uncroppedImage)}")
    ## Decoded images
    logger.info(f"psnr - decoded cropped:    {calculatePSNR(croppedImage,croppedDecode.decodedImage)}")
    logger.info(f"psnr - decoded uncropped:  {calculatePSNR(uncroppedImage,uncroppedDecode.decodedImage)}")
    

    ## Discussion 2
    ## Calucale the average length of the cropped image
    decodedCroppedSize = len(croppedEncode.bitstream)-2
    decodedUncroppedSize =  len(uncroppedEncode.bitstream)-2
    logger.debug(f"size - decoded cropped:               {decodedCroppedSize}")
    logger.debug(f"size - decoded uncropped:             {decodedUncroppedSize}")
    logger.debug(f"single layer size - original cropped: {croppedImage.size/croppedImage.shape[2]}")
    logger.info(f"average length - cropped:              {decodedCroppedSize/(croppedEncode.xSize*croppedEncode.ySize)}")

    ## Discussion 3
    ## Compare compression ratios with matlab algorithm
    originalCroppedSize = 847*8
    origianlUncroppedSize = 812033*8
    logger.info(f"cr - cropped:   {originalCroppedSize/decodedCroppedSize}")
    logger.info(f"cr - uncropped: {origianlUncroppedSize/decodedUncroppedSize}")
    