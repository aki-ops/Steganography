import random
import numpy as np
import math

# Passing the current time as the seed value
random.seed(5)
n = 100000
# Tạo mảng kích thước 5 với giá trị ban đầu là 0
array = np.zeros(n)
array1 = np.zeros(n)
tb = 0
tb1 = 0

for i in range(n):
    array[i] = random.randint(0, 1)
    if(array[i] == 0):
        tb = tb - 1
        array[i] = -1
    else: tb = tb + 1

random.seed(2)
for i in range(n):
    array1[i] = random.randint(0, 1)
    if(array1[i] == 0): 
        tb1 = tb1 - 1
        array1[i] = -1
    else: tb1 = tb1 + 1    

# Tính giá trị trung bình
tb = tb / n
tb1 = tb1 / n

cov = 0
o1 = 0
o2 = 0

for i in range(n):
    cov = cov + (array[i] - tb) * (array1[i] - tb1)

for i in range(n):
    o1 = o1 + (array[i] - tb) * (array[i] - tb)
    o2 = o2 + (array1[i] - tb1) * (array1[i] - tb1)
    
print("tuong quan", cov / math.sqrt(o2 * o1))



