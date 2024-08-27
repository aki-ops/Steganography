import numpy as np
import cv2
import random
import math

def main():
    

    with open("message.txt", "r") as file:
        message = file.read()
    message_length = len(message)
    G = 4
    
    image = cv2.imread('image.jpg')
    image_ycbcr = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    height, width, _ = image.shape   
    n = width
    array = np.zeros(n)
    message_length = 4
    array_mess = [-1 if bit == '0' else 1 for bit in message]
    
    
    
    signa = int(height / message_length)
    
    for j in range(height):
        if math.floor(j / signa) == message_length:
            break

        random.seed(j // signa)
        for i in range(width):
            array[i] = random.randint(0, 1)
            if array[i] == 0:
                array[i] = -1

        for i in range(width):
            y = image_ycbcr[j, i, 0]
            y = y + G * array[i] * array_mess[int(j / signa)]
            y = np.clip(y, 0, 255)
            image_ycbcr[j, i, 0] = y

        
    dem = 0
    new_array = np.empty((height, width))
    for i in range(height):
        random.seed(i // signa)
        for k in range(width):
            array[k] = random.randint(0, 1)
            if(array[k] == 0):
                array[k] = -1
        new_array[i] = array

    image_bgr = cv2.cvtColor(image_ycbcr, cv2.COLOR_YCrCb2BGR)      
    image_ycbcr = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)  
        
    for j in range(message_length):
        tong = 0
        
        for i in range(message_length):
            row = image_ycbcr[signa*i : signa*(i+1), :, 0]
            row = row.flatten()
            array = new_array[signa*j : signa*(j+1)]
            array = array.flatten()
            correlation_coefficient = np.corrcoef(array, row)[0, 1]
            tong += correlation_coefficient
        
        #print(tong)
        #print()
        print(np.sign(tong))
    #print(array_mess)

    # Hiển thị ảnh gốc và ảnh đã xử lý
    #cv2.imshow('Original Image', image)
    #cv2.imshow('Processed Image', image_bgr)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #cv2.imwrite('new_image.jpg', image_bgr)
    
    
if __name__ == "__main__":
    main()