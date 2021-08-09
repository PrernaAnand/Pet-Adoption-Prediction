import requests
import os
import heapq
import matplotlib.pyplot as plt
import json
from shutil import copyfile
from PIL import Image
from io import BytesIO
import time

from google.cloud import vision
from google.cloud.vision import enums
from google.cloud.vision import types

features = [
    types.Feature(type=enums.Feature.Type.CROP_HINTS),
    types.Feature(type=enums.Feature.Type.OBJECT_LOCALIZATION)
]

client = vision.ImageAnnotatorClient()
totalImages = 0

def cropAndSave(vertices, minIndex, previousPrefix):
    global totalImages
    im = Image.open(allImgs + '/' + previousPrefix + "-" + str(minIndex+1) + ".jpg")
    im2 = im.crop([vertices[0].x, vertices[0].y, vertices[2].x - 1, vertices[2].y - 1])

    im2.save('cropped_images/' + previousPrefix + "-" + str(minIndex+1) + ".jpg", 'JPEG')

    totalImages += 1
    print("Total Images: ", totalImages)

    if totalImages >= 500:
        print("Done")
        exit()

def runVision(requests, previousPrefix):
    numObjects = []
    verticesObj = []
    response = client.batch_annotate_images(requests)
    for annotation_response in response.responses:
        # print("Number of objects:", len(annotation_response.localized_object_annotations))
        numObjects.append(len(annotation_response.localized_object_annotations))
        verticesObj.append(annotation_response.crop_hints_annotation.crop_hints[0].bounding_poly.vertices)
    minIndex = numObjects.index(min(numObjects))

    if numObjects[minIndex] < 4 or len(numObjects) == 1:
        cropAndSave(verticesObj[minIndex], minIndex, previousPrefix)
    
    cropAndSave(response, previousPrefix)
    return response

root = "/Users/damansharma/Desktop/data/Test"
jsonMetadata = "metadata"
images = "images"
cropped_images = "cropped_images"
allImgs = "/Users/damansharma/Desktop/data/petfinder-adoption-prediction/train_images"

print(os.getcwd())

requests = []

os.chdir(root)
fileList = os.listdir(allImgs)
fileList.sort()

completedFileList = os.listdir(cropped_images)
completedFileList.sort()

previousPrefix = None
start_time = time.time()
requests = []
num = 0
names = []

for data in fileList:
    image_path = data
    prefix = image_path.split('-')[0]
    fileName = data.split('\n')[0]

    if "Icon" in prefix or ".DS_Store" in prefix:
        continue

    alreadyExists = False
    for check in completedFileList:
        if prefix in check:
            num +=1 
            alreadyExists = True
            break
        
    if alreadyExists:
        continue

    if not previousPrefix is None and previousPrefix != prefix:
        while len(requests) > 15:
            requests.pop()
        runVision(requests, previousPrefix)
        names.clear()
        requests.clear()
    
    with open(allImgs + "/" + fileName, 'rb') as image_file:
        image = vision.types.Image(content = image_file.read())
        print(fileName)
    request = vision.types.AnnotateImageRequest(image=image, features=features)
    requests.append(request)
    names.append(data)
    previousPrefix = prefix