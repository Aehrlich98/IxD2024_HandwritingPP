# imports: 
# openCV for camera handling and image processing
# pytesseract as a python wrapper for the installed tesseract ocr engine
import cv2
import pytesseract

class ImageGetter():
	# camera to be used
	camera = None
	# ocr language type and configurations for pytesseract call
	tess_lang = r"morseocr"
	tess_config = r"-c tessedit_char_whitelist=.-"	#Not needed --psm 6 #Set tesseract to use page segmentation mode, limit to only recognising characters ".-"

	def __init__(self):
		""" Init method which also instanciates the camera for OpenCV """		
		self.camera = cv2.VideoCapture(0) #access system's camera. 0 is default, 1+ denotes extra cameras, but the order can be sporadic 
		if not self.camera.isOpened():
			raise Exception("Camera opening failed!")
		print("ImageGetter class initialised, camera access successful.")

	def __del__(self):
		""" Object deletion method to assure the camera resource is released again """
		self.camera.release()
		print("ImageGetter class deleted, camera released.")

	def camera_get_image(self):
		""" Retreive a frame from the open camera and return it """
		if not self.camera.isOpened():
			raise Exception("Decoder Problem: OpenCV camera access failed! Please check if a camera is connected and functional.")

		ret, frame = self.camera.read() # read returns: bool, frame
		if ret:
			return frame
		else:    # camera not open or other failure
			return None

	def preprocess_image(self, image):
		"""	Adjust the image to be better readable by tesseract OCR """
		if image is not None:
			# camera is possitions upside down compared to the pages with code on them so flip on it's head
			image = cv2.flip(image, 0)
			# turn to grayscale to remove colour pixels
			processedImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			# check if image upscaling is needed, as tesseract struggles with to small characters, upscale by simply doubling every pixel
			img_height, img_width = processedImage.shape[:2]
			if img_height < 1000 and img_width < 1000:
				processedImage = cv2.resize(processedImage, None, fx = 2.0, fy = 2.0,  interpolation= cv2.INTER_NEAREST)
				cv2.imwrite("tttttt.png", processedImage)
			# reduce image to black and white at a pixel threshold to cut off background noise, the darker the image the higher it needs to be
			processedImage = cv2.threshold(processedImage, 72, 255, cv2.THRESH_BINARY)[1]
			# convert to RGB image, tesseract ocr prefers this
			processedImage = cv2.cvtColor(processedImage, cv2.COLOR_BGR2RGB)	
			return processedImage
		else:
			return None

	def read_from_image(self, image):
		""" Pass an opened image to the OCR engine """
		if image is not None:
			text = pytesseract.image_to_string(image, lang=self.tess_lang, config=self.tess_config)
			return text
		else:
			return None



    #BEGIN TEST function
	def test_func(self, imageStr=""):
		"""Test function which includes saving the received image to disk"""
		testimg = None
		# if image file name provided, use this, otherwise use camera
		if imageStr:
				testimg = cv2.imread(imageStr)
		else:
				testimg = self.camera_get_image()
		if testimg is not None:
			testimg2 = self.preprocess_image(testimg)
			testtext = self.read_from_image(testimg2)
			cv2.imwrite("testimg-raw.png", testimg)
			cv2.imwrite("testimg-processed.png", testimg2)
			return testtext
		else:
			return None
	#END TEST function
