"""Functions for manimulating R,B,G channels of images, and Huffman encoding 
and decoding
"""
import logging
import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt


def swap_channellayers(image:np.ndarray):
    """Swap axes from(x,y,channel) to (channel,x,y) and vice versa"""
    ## Bring layers out
    if image.shape[2] == 3:
        swapped_image = np.swapaxes(image,1,2)
        swapped_image = np.swapaxes(swapped_image,0,1)
    ## Puch layers back
    elif image.shape[0] == 3:
        swapped_image = np.swapaxes(image,0,1)
        swapped_image = np.swapaxes(swapped_image,1,2)
    return swapped_image


def save_image(image:np.ndarray, name:str=None):
    """Plot an image given as an array, and save to 
    the working directory as png
    """
    global fig_no
    global working_directory
    # plt.figure(f"Figure {fig_no:02} - {name}")
    # plt.imshow(array)
    # plt.show()
    plt.imsave(f"{working_directory}\\Figures\\Figure {fig_no:02} - {name}.png",image)
    fig_no += 1


def save_channels(layers:np.ndarray, name:str=None):
    """Separately plot and save the Y, Cb, and Cr layers of an image given as 
    an array to the working directory as png
    """
    size_x = layers.shape[1]
    size_y = layers.shape[2]
    for i,layer in enumerate(layers):
        composite = np.zeros((layers.shape))
        composite[i] = layer.reshape(size_x,size_y)
        save_image(swap_channellayers(composite),f"{name} layer {i+1}")


def generate_codebook(symbolprobs:np.ndarray):
    """Return a 2D array of sybols and their symbolcodes according to 
    Huffamn algorithm
    """
    symbolcodes = np.zeros(symbolprobs.shape, dtype="object")
    symbolcodes[:,0] = symbolprobs[:,0]
    c_carryover = ""
    for i in range(symbolprobs.shape[0] - 1):
        ## Probablities of the symbol under coideration
        p_symbol = symbolprobs[i,1]
        ## Sum of remaining probabilities
        p_cumulative = 0
        for j in range(i+1,symbolprobs.shape[0]):
            p_cumulative += symbolprobs[j,1]
        ## Determine 1 or 0
        if p_cumulative >= p_symbol:
            c_cumulative = c_carryover + "0"
            c_symbol = c_carryover + "1"
            c_carryover += "0"
        else:
            c_symbol = c_carryover + "0"
            c_cumulative = c_carryover + "1"
            c_carryover += "1"
        # logger.debug(f"i: {i}, symbol: {p_symbol} {c_symbol}, \
        #              cumulative: {p_cumulative} {c_cumulative}")
        symbolcodes[i,1] = c_symbol
        symbolcodes[i+1,1] = c_cumulative
    if symbolcodes.shape[0] == 1:
        symbolcodes[0,1] = "0"
    # logger.debug(f"symbolcodes: \n{symbolcodes}")
    return dict(symbolcodes)


def encode_symbols(symbols:np.ndarray, codebook:dict):
    """Encode a 1D array of symbols into a sring of bits 
    accoring to a codebook
    """
    codewords = []
    for symbol in symbols:
        codewords.append(codebook.get(symbol))
    # logger.debug(f"codebook: {codebook}")
    # logger.debug(f"codewords: {codewords}")
    bitstream = "".join(codewords)
    return bitstream


def decode_bitstream(bitstream:str, codebook:dict, dimensions:list):
    codebook_inverse = {v:k for k,v in codebook.items()}
    symbols = []
    received_bits = ""
    for bit in bitstream:
        received_bits += bit
        if received_bits in codebook_inverse:
            symbols.append(codebook_inverse.get(received_bits))
            received_bits = ""
            # logger.debug(f"decode_bitstream: {received_bits} in codebook_inverse")
        else:
            # logger.debug(f"decode_bitstream: {received_bits} not in codebook_inverse")
            pass
    decoded_array = np.array(symbols)
    # logger.debug(f"bitstream \n{bitstream}")
    # logger.debug(f"inverse codebook: {codebook_inverse}")
    # logger.debug(f"decoded symbols: {symbols}")
    return decoded_array.reshape(dimensions[0],dimensions[1])


def calculate_entropy(layers:np.ndarray):
    """Calculate and return the entropy of the source imagae (default) 
    or quantised image
    """
    channel_entropy = np.zeros(3)
    if layers.shape[2] == 3:
        layers = swap_channellayers(layers)
    layers = layers.reshape((layers.shape[0],
                                layers.shape[1]*layers.shape[2]))
    # logger.debug(f"reshaped layers: \n{np.round(layers*8)}")
    for i,layer in enumerate(layers):
        symbolSet = list(set(layer))
        probabilities = [np.size(layer[layer==i])/(layer.size)\
                                for i in symbolSet]
        channel_entropy[i] =  np.sum([p*np.log2(1.0/p) for p in probabilities])
        # logger.debug(f"layer entropy: {self.channel_entropy[i] }")
    return channel_entropy


def calculate_psnr(image1:np.ndarray, image2:np.ndarray):
    mse = np.mean((image1 - image2)**2)
    if mse == 0:
        psnr = None
    else:
        psnr = 10*np.log10(1/mse)
    return psnr


class Encoder:
    def __init__(self, image:np.ndarray, working_directory:str, 
                 label:str=None, qlevels=8):
        """Initialise encoder with image data, path to 
        wroking directory, and image label
        """
        ## Instance attributes
        self.image = image
        self.working_directory = working_directory
        self.label = label
        self.qlevels = qlevels
        self.size_x = self.image.shape[0]
        self.size_y = self.image.shape[1]
        self.layers = swap_channellayers(self.image)
        # self.channel_entropy = np.zeros((3))
        logger.debug(f"size: {self.size_x}x{self.size_y}")
        # logger.info(f"{self.label} axes swapped")
        logger.debug(f"crop shape: {self.image.shape}")
        logger.debug(f"crop[0] shape: {self.image[0].shape}")
        logger.debug(f"crop[0,0] shape: {self.image[0,0].shape}")

        ## Step 4
        ## Quantise output to 8 levels
        bins = np.arange(0,1,1/self.qlevels)
        logger.debug(f"bins: {bins}")
        # self.quantised_layers = np.digitize(self.layers,bins)/self.qlevels
        self.quantised_layers = (np.digitize(self.layers,bins)-1)/(self.qlevels-1)
        # logger.info(f"{self.label} quantised")
        # logger.debug(f"quanitzed layers: \n{self.quantised_layers}")

        ## Step 5 
        ## Find probabilities of each symbol
        uniqueSymbols_y,counts_y = np.unique(self.quantised_layers[0],
                                            return_counts=True)
        uniqueSymbols_cb,counts_cb = np.unique(self.quantised_layers[1],
                                                return_counts=True)
        uniqueSymbols_cr,counts_cr = np.unique(self.quantised_layers[2],
                                                return_counts=True)
        probability_y = np.array(list(zip(uniqueSymbols_y,counts_y/(self.size_x*self.size_y))))
        probability_cb = np.array(list(zip(uniqueSymbols_cb,counts_cb/(self.size_x*self.size_y))))
        probability_cr = np.array(list(zip(uniqueSymbols_cr,counts_cr/(self.size_x*self.size_y))))
        testarray = np.array([[128, 0.47],[87, 0.25],
                                    [186, 0.25],[256, 0.03]])
        ## Sort in descending order of probablity
        self.probability_y = probability_y[probability_y[:, 1].argsort()[::-1]]
        self.probability_cb = probability_cb[probability_cb[:, 1].argsort()[::-1]]
        self.probability_cr = probability_cr[probability_cr[:, 1].argsort()[::-1]]
        testarray = testarray[testarray[:, 1].argsort()[::-1]]
        logger.debug(f"probabilities: \n{self.probability_y} \n{self.probability_cb} \n{self.probability_cr}")

        ## Step 6
        ## Construct the Huffamn coding algorith (see line 34)
        self.codebook_y = generate_codebook(self.probability_y)
        self.codebook_cb = generate_codebook(self.probability_cb)
        self.codebook_cr = generate_codebook(self.probability_cr)
        # logger.info(f"{self.label} codebooks generated")
        logger.debug(f"code dictionaries: \n {self.codebook_y} \n {self.codebook_cb} \n {self.codebook_cr}")

        ## Step 7
        ## Compress both original and cropped images
        ## Convert to a stream of symbols
        symbolStream_y = self.quantised_layers[0].reshape(self.size_x*self.size_y)
        symbolStream_cb = self.quantised_layers[1].reshape(self.size_x*self.size_y)
        symbolStream_cr = self.quantised_layers[2].reshape(self.size_x*self.size_y)
        logger.debug(f"stream: {symbolStream_y.shape}, matrix: {self.quantised_layers.shape}")
        ## Map sybols into codewords using the codebook
        bitstream_y = encode_symbols(symbolStream_y,self.codebook_y)
        bitstream_cb = encode_symbols(symbolStream_cb,self.codebook_cb)
        bitstream_cr = encode_symbols(symbolStream_cr,self.codebook_cr)
        self.bitstream = "\n".join([bitstream_y,bitstream_cb,bitstream_cr])
        # logger.info(f"{self.label} encoded")

    def save_figures(self):
        """Save raw image, raw channels, and quantised channels as png"""
        save_image(self.image,f"Original {self.label} image")
        save_channels(self.layers,f"Original {self.label} image")
        save_image(swap_channellayers(self.quantised_layers),f"Quantised {self.label} image")           
        save_channels(self.quantised_layers,f"Quantised {self.label} image")

    def write_bitstram(self):
        """Write the bistream to a txt file"""
        with open(f"{self.working_directory}\\Encoded\\{self.label}.txt","w") \
            as file:
            file.write(f"{self.size_x}x{self.size_y}\n{self.bitstream}")
            file.close()
            logger.debug(f"Encoder.write_bitstram called")
    
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
        decoded_array_y = decode_bitstream(bitstream_y,self.codebooks[0],
                                        self.dimensions)
        decoded_array_cb = decode_bitstream(bitstream_cb,self.codebooks[1],
                                        self.dimensions)
        decoded_array_cr = decode_bitstream(bitstream_cr,self.codebooks[2],
                                        self.dimensions)
        # logger.info(f"{label} decoded")
        # logger.debug(f"decoded array: \n{decoded_array_cb}")
        ## Merge channels
        self.decodedLayers = np.array([decoded_array_y,decoded_array_cb,decoded_array_cr])
        self.decodedImage = swap_channellayers(self.decodedLayers)
        logger.debug(f"decoded image shape: {self.decodedImage.shape}")

    def save_figures(self):
        """Save decoded channels, and decoded image as png"""
        save_image(self.decodedImage,f"Decoded {self.label} image")
        save_channels(self.decodedLayers,f"Decoded {self.label} image")


if __name__ == "__main__":
    ## Set up the logger
    logging.basicConfig(format="[%(name)s][%(levelname)s] %(message)s")
    logger = logging.getLogger("ee596Lab01")
    logger.setLevel(logging.DEBUG)
    ## Reset figure numbner
    fig_no = 1    
    ## Select the starting point for the cropped window from E/17/371  
    start = np.array([3*60, 71*4])
    qlevels = 8
    working_directory = "D:\\User Files\\Documents\\University\\Misc\\4th Year Work\\Semester 7\\EE596\\EE596 Lab 01"
    ## Step 2
    ## Read image
    image_uncropped = img.imread(f"{working_directory}\\Images\\Pattern-612x612.jpg")/256
    ## Step 3
    ## Select 16x16 cropped sub-image
    image_cropped = image_uncropped[start[0]:start[0]+16, start[1]:start[1]+16]
    
    ## Cropped image
    ## Steps 4 to step 7
    cropped_encode = Encoder(image_cropped,working_directory,"cropped",qlevels)
    cropped_encode.save_figures()
    ## Step 8
    ## Save the compressed image into a text file
    cropped_encode.write_bitstram()
    ## Step 10
    cropped_decode = Decoder(f"{working_directory}\\Encoded\\cropped.txt",cropped_encode.getCodebooks(),"cropped")
    cropped_decode.save_figures()

    ## Original image
    ## Steps 4 to step 7
    uncropped_encode = Encoder(image_uncropped,working_directory,"uncropped",qlevels)
    uncropped_encode.save_figures()
    ## Step 8
    ## Save the compressed image into a text file
    uncropped_encode.write_bitstram()
    ## Step 10
    uncropped_decode = Decoder(f"{working_directory}\\Encoded\\uncropped.txt",uncropped_encode.getCodebooks(),"uncropped")
    uncropped_decode.save_figures()

    ## Step 11
    ## Discussion 1. ii.
    logger.info(f"entropy - original cropped:   {calculate_entropy(image_cropped)}")
    ## Calculate the entropy of the source image
    logger.info(f"entropy - original uncropped: {calculate_entropy(image_uncropped)}")
    ## Discussion 1. iii.
    logger.info(f"entropy - decoded cropped:    {calculate_entropy(cropped_decode.decodedImage)}")
    logger.info(f"entropy - decoded uncropped:  {calculate_entropy(uncropped_decode.decodedImage)}")

    ## Step 12
    ## Evaluate PSNR
    ## Original images
    logger.info(f"psnr - original cropped:   {calculate_psnr(image_cropped,image_cropped)}")
    logger.info(f"psnr - original uncropped: {calculate_psnr(image_uncropped,image_uncropped)}")
    ## Decoded images
    logger.info(f"psnr - decoded cropped:    {calculate_psnr(image_cropped,cropped_decode.decodedImage)}")
    logger.info(f"psnr - decoded uncropped:  {calculate_psnr(image_uncropped,uncropped_decode.decodedImage)}")
    

    ## Discussion 2
    ## Calucale the average length of the cropped image
    size_decoded_cropped = len(cropped_encode.bitstream)-2
    size_decoded_uncropped =  len(uncropped_encode.bitstream)-2
    logger.debug(f"size - decoded cropped:               {size_decoded_cropped}")
    logger.debug(f"size - decoded uncropped:             {size_decoded_uncropped}")
    logger.debug(f"single layer size - original cropped: {image_cropped.size/image_cropped.shape[2]}")
    logger.info(f"average length - cropped:              {size_decoded_cropped/(cropped_encode.size_x*cropped_encode.size_y)}")

    ## Discussion 3
    ## Compare compression ratios with matlab algorithm
    size_original_cropped = 847*8
    size_original_uncropped = 812033*8
    logger.info(f"cr - cropped:   {size_original_cropped/size_decoded_cropped}")
    logger.info(f"cr - uncropped: {size_original_uncropped/size_decoded_uncropped}")
    