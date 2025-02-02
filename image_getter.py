# imports: 
# openCV for camera handling
# Pillow for image procesing
# pytesseract as a python wrapper for the installed tesseract ocr engine
import cv2
from PIL import Image
import pytesseract

# start
camera = None

tess_config = r"--psm 11 tessedit_char_whitelist=-./"

camera = cv2.VideoCapture(0) # just takes default cam for now #/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_554792EF-video-index0")
if not camera.isOpened():
	raise Exception("OpenCV: Open camera failed. Exiting.")

# retreive a frame from the open global camera and return it
def cameraHandler():
	ret, frame = camera.read() # read returns: bool, frame
	if ret:
		print("got a frame! Saving it!")
		cv2.imwrite("test.png", frame)
		return frame
	else:    # camera not open or other failure
		return None


def preprocessImg(image):
	if image is not None:
		processedImage = cv2.threshold(image, 192, 255, cv2.THRESH_BINARY)[1] # reduce image to black and white and cut off background noise

		cv2.imwrite("test-return.png", processedImage)
		procImg_rgb = cv2.cvtColor(processedImage, cv2.COLOR_BGR2RGB)	
		cv2.imwrite("test-return2.png", processedImage)
	
		print(processedImage.shape)
		return procImg_rgb
	else:
		return None

def ocrHandler(image):
	text = pytesseract.image_to_string(image, config=tess_config)
	return text
	


# to test program
testimg = cv2.imread( "morseText001.png")    #"morseSOS_frInternet.png") #"morseText001.png")
testimg2 = preprocessImg(testimg)
testtext = ocrHandler(testimg2)
# testtext = ocrHandler( cameraHandler() )
print(testtext)


# close camera
camera.release()
