import numpy as np
import cv2 as ocv
import scipy.stats as stats
import glob

def calcChiSquare(T, auxZ):
    chi_square = 0
    for observed, expected in zip(T, auxZ):
        if expected != 0:
            chi_square += ((observed - expected) ** 2) / expected
    return chi_square

def chiSquareAttack(image_path, block_size = 324):  # threshold for dof=2
    img_r = ocv.imread(image_path, ocv.IMREAD_GRAYSCALE)
    if img_r is None:
        raise ValueError("Image not found or unable to read")

    img = np.ndarray.flatten(img_r)
    padding = block_size - len(img) % block_size
    if padding != block_size:
        img = np.append(img, np.full(padding, 0))

    # Chia ảnh thành các block
    blocks = np.split(img, len(img) // block_size)

    suspicious_blocks = 0

    for block in blocks:
        auxX = [0] * 128
        auxY = [0] * 128

        for c in block:
            if c % 2 == 0:
                auxX[c // 2] += 1
            else:
                auxY[c // 2] += 1

        T = []
        auxZ = []
        v = -2 
        for i in range(128):
            if auxX[i] + auxY[i] != 0:
                T.append(auxX[i])
                auxZ.append((auxX[i] + auxY[i]) / 2)
                v += 1
        chi_square = calcChiSquare(T, auxZ)
        #print(chi_square)
        
        if chi_square >= stats.chi2.ppf(0.95, df=v):
            suspicious_blocks += 1
    #print(f"Suspicious blocks: {suspicious_blocks}/{len(blocks)}")
    print(f"Percentage of suspicious blocks: {(suspicious_blocks / len(blocks)) * 100:.2f}%")

# Đường dẫn tới ảnh cần kiểm tra
folder_path = "test/*.png"
image_paths = glob.glob(folder_path)
for image_path in image_paths:
    print(image_path.split('/')[-1])
    chiSquareAttack(image_path)
    print()
