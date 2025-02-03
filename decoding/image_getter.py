# imports: 
# openCV for camera handling
# Pillow for image procesing
# pytesseract as a python wrapper for the installed tesseract ocr engine
import cv2
import pytesseract

# camera to be used
camera = None
# configurations for pytesseract call
tess_config = r"--psm 11 tessedit_char_whitelist=-./"

def start_this():
	camera = cv2.VideoCapture(0) # just takes default cam for now # later: /dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_554792EF-video-index0")
	if not camera.isOpened():
		return -1
	return 0

def end_this():
	# close camera
	camera.release()
	return 0

# retreive a frame from the open global camera and return it
def cameraHandler():
	if not camera.isOpened():
		raise Exception("OpenCV: Open camera failed. Exiting.")

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
def test_func(iamgeStr):
	testimg = cv2.imread(iamgeStr)
	testimg2 = preprocessImg(testimg)
	testtext = ocrHandler(testimg2)
	# testtext = ocrHandler( cameraHandler() )
	print(testtext)
