import os
import cv2
# Simple script to prepare png images for teseract training: 
# Grayscaling, Thresholding, conversion to RGB, rotate and copy to create addtional training image.
# Images should be single lines of text with no background disturbances. HIgh image quality seems needed for enough pixels in characters.

currentpath = input("please provide path to png files to binarize.\nE.g. type './' for current directory...\n")

localfiles = next(os.walk(currentpath), (None, None, []))[2] 

print(localfiles)

for file in localfiles:
   if ".png" in file:
     img = cv2.imread(file)
     # reduce noise from image
     procImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
     procImg = cv2.threshold(procImg, 192, 255, cv2.THRESH_BINARY)[1]    # Here 192, thresholding value might vary, the darker the image the higer.
     procImgRgb = cv2.cvtColor(procImg, cv2.COLOR_BGR2RGB)	
     imgname = file[:-4] + "-bw.png"
     cv2.imwrite(imgname, procImgRgb)
     # rotate the image by 180 degrees to create another, backwards training image
     procImg = cv2.rotate(procImg, cv2.ROTATE_180)
     procImgRgb = cv2.cvtColor(procImg, cv2.COLOR_BGR2RGB)
     cv2.imwrite(file[:-4] + "-bw-rot.png", procImgRgb)
   else:
     print("File found that's not a png: " + file)

