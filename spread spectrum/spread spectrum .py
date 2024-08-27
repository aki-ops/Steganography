import numpy as np
import cv2
import random
import math

def main():
    print("1. Embed message in photo")
    print("2. Decode the image")
    n = int(input("Enter selection: "))
    
    if n == 1:
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
        cv2.imwrite('stego_image.jpg', image_bgr)
        
    elif n == 2:
        # Decode the stego image
        image_bgr = cv2.imread('stego_image.jpg')
        if image_bgr is None:
            print("Error: Could not load stego image.")
            return
        
        message_length = 4
        G = 4
        height, width, _ = image_bgr.shape
        signa = int(height / message_length)
        array = np.zeros(width)
        
        # Convert to YCbCr color space
        new_array = np.empty((height, width))
        for i in range(height):
            random.seed(i // signa)
            for k in range(width):
                array[k] = random.randint(0, 1)
                if(array[k] == 0):
                    array[k] = -1
            new_array[i] = array
        
        image_ycbcr = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)  
        
        decoded_message = ""    
        for j in range(message_length):
            ans = 0
            
            for i in range(message_length):
                row = image_ycbcr[signa*i : signa*(i+1), :, 0]
                row = row.flatten()
                array = new_array[signa*j : signa*(j+1)]
                array = array.flatten()
                correlation_coefficient = np.corrcoef(array, row)[0, 1]
                ans += correlation_coefficient
           
            sign_ans = np.sign(ans)
            decoded_message += '1' if sign_ans > 0 else '0'
        
        #print to file 
        with open('decrypted_message.txt', 'w') as file:
            file.write(decoded_message)

if __name__ == "__main__":
    main()
