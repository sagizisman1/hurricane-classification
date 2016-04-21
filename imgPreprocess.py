#This script performs the following functions:
#  1) Use the PIL to resize images to uniform size (500x500)
#  2) Read all images into a numpy array
#  3) Flatten the RGB array for each iamge and concatenate 
#       Note: Should be a (m x (p1*p2*3)) dimensional array where
#	          m = number of images, p1 = num vertical pixels, p2 = num horizontal pixels
#  4) Mean shift each feature (pixel)
#  5) Compress the image using PCA compression
#  6) Write the resulting CSV file to disk

#Input argument: path to images
#Output: A ready-to-model CSV file 
#Dependencies: numpy, scikit learn

#Sagi Zisman 4/18/2016

import sys
import os
from skimage import io
import numpy as np
import Image
from sklearn.decomposition import PCA
import pdb

def fetchImg(imgName,imgDir):
	filename = os.path.join(imgDir,imgName)
	img = Image.open(filename)
	return img

def img2flatArr(img):
	imgArr = np.array(img)
	flatArr = np.ndarray.flatten(imgArr)
	return flatArr

#This function will read the first image file in directory
#and sample it's pixel dimensions. It's assumed all other
#files have the same number of dimensions
def getPixelSize(imgName,imgDir):
	filename = os.path.join(imgDir,imgName)
	imgArr = io.imread(filename)
	size = imgArr.size
	return size


imgDir = sys.argv[1]
pixels = int(sys.argv[2])
imgType = sys.argv[3]

if imgType == 'RGB':
	pixelDepth = 3

imgFiles = os.listdir(imgDir)

#A flattened image file will have a pixel grid where each pixel
#will have 3 values when referring to a RGB image
designMatrix = np.zeros((len(imgFiles),pixels*pixels*pixelDepth))

#Generate the design matrix
for idx, imgFile in enumerate(imgFiles):
	imgObj = fetchImg(imgFile,imgDir)
	resizedImg = imgObj.resize((pixels,pixels), Image.BICUBIC)
	designMatrix[idx] = img2flatArr(resizedImg)

#Mean shift features
designMatrix = designMatrix - designMatrix.mean(axis = 0)

#Note that when the number of training examples is MUCH less than
#features, the number of dimensions of reduced subspace is equal
#to number of training examples.
pca = PCA()
ldArr = pca.fit_transform(designMatrix)
np.savetxt("designMatrix.csv",ldArr,delimiter=",")


	

