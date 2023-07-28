import cv2
import numpy as np

def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr

def entropy(img):
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist /= np.sum(hist)
    hist = hist[hist > 0]
    entropy = -np.sum(hist * np.log2(hist))
    return entropy

workingdir = "D:\\User Files\\Documents\\University\\Misc\\4th Year Work\\Semester 7\\EE596\\EE506 Miniproject"
# Example usage
img1 = cv2.imread(f"{workingdir}\\Images\\DITF2.png")
img2 = cv2.imread(f"{workingdir}\\Output\\Test Image high.png")

psnr_value = psnr(img1, img2)
entropy_value = entropy(img1)

print(f"PSNR value: {psnr_value}")
print(f"Entropy value: {entropy_value}")
