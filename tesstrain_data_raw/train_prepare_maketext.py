import os
# Script to create correctly named txt files for the givern png images for tesseract training. Must still manually fill the file swith content
currentpath = input("please provide path to png files to create blank '.gt.txt' files for.\nE.g. type './' for current directory...\n")

localfiles = next(os.walk(currentpath), (None, None, []))[2] 

for file in localfiles:
	if ".png" in file:
        # if txt file doesn't exist create it, otherwise pass exception
        try:
            file = open(file[:-4] + ".gt.txt", "w")
            file.close() 
        except FileExistsError:
            pass
    else:
		print("Can't make a gt.txt file for this file: " + file)
