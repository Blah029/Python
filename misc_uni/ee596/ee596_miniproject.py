"""EE506 Miniproject
E/17/371

Procedure:
    - Break into 8x8 macro blocks
    - Apply DCT to each macroblock
    - Quantise
    - Apply huffman encoding from Lab 01

References:
    - https://docs.python.org/3/library/logging.html
    - https://stackoverflow.com/questions/15978468/using-the-scipy-dct-function-to-create-a-2d-dct-ii
"""
import cv2
import logging
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import dct


def mergeblocks(macroblocks:np.ndarray):
    """Merge an array of macroblocks and return full image"""
    merged = []
    for row in macroblocks:
        merged.append(np.hstack(row))
    return (np.vstack(merged))


def plot_rgb(image:np.ndarray, figname:str=None):
    """Merge macroblocks if present, and plot RGB image"""
    global figno
    ## Merge macroblocks
    if len(image.shape) == 5:
        image = mergeblocks(image)
    if figname == None:
        plt.figure(f"Figure {figno}")
    else:
        plt.figure(f"Figure {figno} - {figname}")
    plt.imshow(image)
    plt.show()
    figno += 1


def plot_yuv(image:np.ndarray, figname:str=None):
    """Merge macroblocks if present, convert to RBG, 
    and plot given YUV image
    """
    ## Merge macroblocks
    if len(image.shape) == 5:
        image = mergeblocks(image)
    # logger.debug(f"image shape: \n{image.shape}")
    # logger.debug(f"image: \n{image}")
    image = cv2.cvtColor(image,cv2.COLOR_YUV2BGR)
    image = np.stack([image[:,:,2],image[:,:,1],image[:,:,0]], axis=2)
    plot_rgb(image,figname)


def plot_yuv_layers(image:np.ndarray, figname:str=None):
    """Merge macroblocks if present, and plot layers of YUV image"""
    ## Merge macroblocks
    if len(image.shape) == 5:
        image = mergeblocks(image)
    fig,ax = plt.subplots(2,2)
    if figname == None:
        fig.suptitle(f"Figure {figno} - YUV layers")
    else:
        fig.suptitle(f"Figure {figno} - {figname} YUV layers")
    ax[0,0].imshow(np.stack([image[:,:,0,],
                         image[:,:,0,],
                         image[:,:,0,]],axis=2))
    ax[0,1].set_axis_off()
    ax[1,0].imshow(np.stack([np.zeros(image[:,:,0].shape),
                           np.zeros(image[:,:,0].shape),
                           image[:,:,1,]], axis=2))
    ax[1,1].imshow(np.stack([image[:,:,2,],
                           np.zeros(image[:,:,0].shape),
                           np.zeros(image[:,:,0].shape)], axis=2))
    plt.show()


class ImageEncoder:
    def __init__(self, array:np.ndarray, blocksize:int=8, qlevels:int=8):
        """Initialise ImageEncoder object"""
        self.array = array[:,:,:3]
        self.array = cv2.cvtColor(self.array,cv2.COLOR_RGB2YUV)
        self.blocksize = blocksize
        self.qlevels = qlevels
        self.height = array.shape[0]
        self.width = array.shape[1]
        if self.height%self.blocksize != 0 or self.width%self.blocksize != 0:
            logger.warning(f"Image height or width is not divisible by {self.blocksize}")
        self.blocksegmentation()
        self.applydct()
        self.uniform_quantise()
        self.table_quantise()

    def blocksegmentation(self):
        """Segment image into 8x8 macroblocks"""
        macroblocks = []
        for i in range(0,int(self.height),self.blocksize):
            macroblocks_row = []
            for j in range(0,int(self.width),self.blocksize):
                macroblocks_row.append(self.array[i:i+self.blocksize,
                                             j:j+self.blocksize,:])
            macroblocks.append(macroblocks_row)
        self.macroblocks = np.array(macroblocks).squeeze()
        logger.debug(f"segemented shape: {self.macroblocks.shape}")

    def applydct(self):
        """Apply discrete cosine transform to segmented blocks"""
        self.dct_macroblocks = dct(dct(self.macroblocks,axis=2),axis=3)
        logger.debug(f"dct row shape: {self.dct_macroblocks[0].shape}")
        # plot_rgb(self.dct_macroblocks,"DCT")

    def uniform_quantise(self, qlevels:int=None):
        """Quantise the transformed macroblocks"""
        ## Set default quantisation levels
        if qlevels == None:
            qlevels = self.qlevels
        bins = np.arange(0,np.max(self.dct_macroblocks),
                        np.max(self.dct_macroblocks)/qlevels)
        self.quantised = np.digitize(self.dct_macroblocks,bins)/qlevels
        logger.debug(f"bins: {bins}")
        logger.debug(f"dct: \n{np.around(self.dct_macroblocks[0,0,:,:,0],2)}")
        logger.debug(f"quantised x qlevels: \n{np.around(self.quantised[0,0,:,:,0]*qlevels,2)}")
        plot_yuv_layers(self.quantised,"Uniform-quantised")

    def table_quantise(self, qtable_luma:np.ndarray=None, 
                       qtable_chroma:np.ndarray=None):
        """Quantise the transformed macroblocks using the given quantisation
        table, or the standard JPEG quantisation table
        """
        ## Set default quantisation tables
        if qtable_luma == None:
            qtable_luma = np.array([[16, 11, 10, 16,  24,  40,  51,  61],
                                    [12, 12, 14, 19,  26,  58,  60,  55],
                                    [14, 13, 16, 24,  40,  57,  69,  56],
                                    [14, 17, 22, 29,  51,  87,  80,  62],
                                    [18, 22, 37, 56,  68, 109, 103,  77],
                                    [24, 35, 55, 64,  81, 104, 103,  92],
                                    [49, 64, 78, 87, 103, 121, 120, 101],
                                    [72, 92, 95, 98, 112, 100, 103,  99]])
        if qtable_chroma == None:
            qtable_chroma = np.array([[17, 18, 24, 47, 99, 99, 99, 99], 
                                      [18, 21, 26, 66, 99, 99, 99, 99], 
                                      [24, 26, 56, 99, 99, 99, 99, 99], 
                                      [47, 66, 99, 99, 99, 99, 99, 99], 
                                      [99, 99, 99, 99, 99, 99, 99, 99], 
                                      [99, 99, 99, 99, 99, 99, 99, 99], 
                                      [99, 99, 99, 99, 99, 99, 99, 99], 
                                      [99, 99, 99, 99, 99, 99, 99, 99]])
        ## Resize quantisation tables to match macrobloack
        ## Truncate
        # qtable_luma = qtable_luma[:self.blocksize,:self.blocksize]
        # qtable_chroma = qtable_chroma[:self.blocksize,:self.blocksize]
        ## Interpolate
        qtable_luma = cv2.resize(qtable_luma.astype(np.int16),
                                 (self.blocksize,self.blocksize))
        qtable_chroma = cv2.resize(qtable_chroma.astype(np.int16),
                                 (self.blocksize,self.blocksize))
        logger.debug(f"luma shape: {qtable_luma.shape}, chroma shape: {qtable_chroma.shape}")
        self.qtable = np.stack([qtable_luma,qtable_chroma,qtable_chroma],axis=2)
        self.quantised = self.dct_macroblocks.copy()
        ## For RGB image
        # for i,block_row in enumerate(self.quantised):
        #     for j,block in enumerate(block_row):
        #         self.quantised[i,j] = np.round(block/qtable_rgb)
        ## For YUV image
        for i,block_row in enumerate(self.quantised):
            for j,block in enumerate(block_row):
                self.quantised[i,j] = np.round(block/self.qtable)
        logger.debug(f"dct: \n{np.around(self.dct_macroblocks[0,0,:,:,0],2)}")
        logger.debug(f"quantised & reconstructed: \n{self.quantised[0,0,:,:,0]*self.qtable[:,:,0]}")
        logger.debug(f"ymax: {np.max(self.quantised[:,:,0])}, bmax: {np.max(self.quantised[:,:,1])}, rmax: {np.max(self.quantised[:,:,2])}")
        plot_yuv_layers(self.quantised,"Table-quantised")

    def applyrlc(self):
        pass        


## Main sequence
if __name__ == "__main__":
    ## Set up the logger
    logging.basicConfig(format="[%(name)s][%(levelname)s] %(message)s")
    logger = logging.getLogger("ee596Lab01")
    logger.setLevel(logging.DEBUG)
    ## Turn off numpy scientific notation
    np.set_printoptions(suppress=True)
    ## Reset figure nummber
    figno = 1
    ## Set working directory and read image
    workingdir = "D:\\User Files\\Documents\\University\\Misc\\4th Year Work\\Semester 7\\EE596\\EE506 Miniproject"
    image = plt.imread(f"{workingdir}\\DITF2.png")
    logger.debug(f"image shape: {image.shape}")
    testframe = ImageEncoder(image)
    