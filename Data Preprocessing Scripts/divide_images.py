import requests
import os
import heapq
import matplotlib.pyplot as plt
import json
from shutil import copyfile
from PIL import Image
from io import BytesIO
import time
import numpy as np 

path = '/Users/damansharma/Desktop/data/petfinder-adoption-prediction/test_images'
os.chdir(path)
fileList = os.listdir()
fileList.sort()

print(len(fileList))

numOfBatches = 30
batchSize = int(len(fileList)/numOfBatches)

path = '/Users/damansharma/Desktop/data/petfinder-adoption-prediction/test_batches'
os.chdir(path)

lastIndex = 0
totalImages = 0
for batchNum in range(numOfBatches):
    if "DS_Store" in fileList[0] and batchNum == 0:
        lastIndex += 1

    if batchNum < (numOfBatches - 1):
        batch = fileList[lastIndex:lastIndex+batchSize]
        print("First element in batch" + str(batchNum) + ": ", batch[0])
        batchLastPrefix = batch[-1].split('-')[0]
        lastIndex += batchSize

        for data in fileList[lastIndex:]:
            prefix = data.split('-')[0]
            if batchLastPrefix == prefix:
                batch.append(data)
                lastIndex += 1
            else:
                break
        
        print("Last element in batch" + str(batchNum) + ": ", batch[-1], "Number of elements in batch" + str(batchNum), len(batch))
    else:
        print("First element in batch" + str(batchNum) + ": ", batch[0])
        batch = fileList[lastIndex:]
        print("Last element in batch" + str(batchNum) + ": ", batch[-1], "Number of elements in batch" + str(batchNum), len(batch))
    totalImages += len(batch)
    c = np.savetxt("batch" + str(batchNum) + ".txt", np.array(batch), delimiter =', ', fmt='%s')  

print(totalImages)