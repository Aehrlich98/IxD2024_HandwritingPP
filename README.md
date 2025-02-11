# Handwriting++
######  A project for the Coding IxD course of winter semester, 2024, by KH Berlin and the FU Berlin ######
##### Handwriting++ aims to support a new synergy of analogue an digital writing and data transfer by merging the multi-mediality of digital processes with the manual art of handwritting. #####

![The code pen wired to an Arduino board](https://github.com/Aehrlich98/IxD2024_HandwritingPP/blob/main/Prototype.JPG?raw=true)

In our modern lives, digital communication has become the quasi default mode of interaction, allowing us to share any kind of data instantly with anyone. With that, it is no surprise that handwriting is becoming less important. And yet, it remains a constant in our lives: 
In our research, we discovered people still prefer handwriting for storing their personal information, avoiding digital distractions, and sharing personal messages with loved ones.
Handwriting++ is a concept for augmenting our handwriting. It preserves the personality of the text but adds some of the convenience of the digital space. Imagine watching a video that you want to share with a friend, maybe not through a text or email, but in a handwritten letter. 
With Handwriting++, you can simply underline the title or a key phrase in your note to link it to digital content. Your friend can then scan the underlined text with an accompanying app and is forwarded to the video—similar to a QR-Code. 

What's even more exciting is that you can write an entire letter or message in the Handwriting++ code. The receiver can scan the whole text, and it will automatically be translated into normal language. This seamless blend of analog and digital enhances how we share and experience information.


## Table of Contents  
<!--ts-->
* [Project structure](#project-structure)  
* [Installation](#installation)
* [Running the programs](#running-the-programs)
* [Acknowledgements](#acknowledgements)
<!--te-->

### Project structure ###

Here you will find the software part of this project. All project files rest on the main branch. The folders "encoding" and "decoding" contain the relevant python programs for this step of the device usage and necesssary auxiliary files. The encoding folder contains the UI program for handling the message input and the needed Arduino code file. The "decoding" folder contains the UI main program and the helper modules for reading and decoding images from a camera. 

The project is built around an Arduino UNO R3 board with a solenoid as a linear motor and a rotation sensor, other equipment like jumper wires, a board, materials to produce the holder, etc. and more are also needed. 

The arduino code requires the [Arduino IDE](https://www.arduino.cc/en/software) to pass the instructions to a compatible microcontroller. 

The user facing software parts of this project are built in Python 3. It is recommended to use something generally recent like Python 3.9 to avoid potential compatibility issues but there are no dependecies on super specific package versions.
The following libraries are used for core features of this project:
* The [Kivy](https://pypi.org/project/Kivy/) UI library for the UI and runtime structure
* [pySerial](https://pythonhosted.org/pyserial/) Python library enabling serial communication with the Arduino Uno
* [OpenCV](https://pypi.org/project/opencv-python/) for handling image recording and modulation
* [pytesseract](https://pypi.org/project/pytesseract/) as a wrapper for the Tesseract OCR system installation

For the decoding the project further uses an OCR engine to scan the images and recognise the code text. For this the open source Tesseract OCR engine, currently maintained by Google, was used. See the [official repository here](https://github.com/tesseract-ocr/tesseract).

The engine was further trained using the [tesstrain project](https://github.com/tesseract-ocr/tesstrain) via fine-tuning an english language base model. The language model files are part of the [tessdata-best](https://github.com/tesseract-ocr/tessdata_best) set, which are the only data files usable for fine-tuning. 
We collected custom data from our project to utilize with the training, a dataset corresponding to our final model is provided in the "tess-training" folder. 
Please note that we didn't manage to get the model to be very precise, it performs marginaly better than the standard eng-language model but improvements can definitely be made. 

__To enjoy all of our fun work, follow the below instructions:__


### Installation ###

To run the python scripts you need the aforementioned modules available in your Python environment. You can install all Python requirements via the requirements.txt file from this projects main directory:

`pip install -r requirements.txt`

For the Arduino setup, it is recommended to use the Arduino IDE to open the .ino code file and pass it to a suitable board. This is also a good step to test the program and adjust any potential differing variables, like the serial port, or Baud rate.

For the Tesseract OCR engine this project relies on setting up a local system installation. Atleast version 4 is required but higher versions of Tesseract 4 or 5 should be functional. This project was tested with versions 4.1.1 and 5.3.0. 

For e.g. Debian based linux distributions you can install it via apt:
`sudo apt install tesseract-ocr`
On macOS tesseract can be installed via Mac Ports or Home Brew. For Windows supported installers exist. See the [official repository](https://github.com/tesseract-ocr/tesseract) and [documentation](https://tesseract-ocr.github.io/tessdoc/Installation.html).  


After installation copy the contents of the _'/decoding/morseocr'_ folder from here to the _'tessdata'_ folder of your Tesseract installation.<br/>
On Debian based systems this folder can usually be found under `/usr/share/tesseract-ocr/X.XX/tessdata`, where X.XX is the version number installed.<br/>
On Windows it might be under `%USERPROFILE%\AppData\Local\Programs\Tesseract-OCR\tessdata`, if installed locally.<br/>
Under MacOS the directory might differ depending on your isntallation method, find it using e.g. `brew list tesseract`, if installed via Home Brew.

### Running the programs ###

#### encoding ####
To start the encoding project, simply connect the Arduino to your computer and run the UI.py script—no parameters are required. The UI.py can be found in the encoding folder. A serial connection should open automatically, enabling communication between the Arduino and the PC. If everything is set up correctly, you will see an interface with a text input field prompting you to enter a word. Once you provide a word, it will be translated into Morse code and written using the pen.


<img src="https://github.com/Aehrlich98/IxD2024_HandwritingPP/blob/main/EncodingRunning.gif?raw=true" width="750"/>

<img src="https://github.com/Aehrlich98/IxD2024_HandwritingPP/blob/main/PenInAction.gif?raw=true" width="750"/>


#### decoding ####

To start the decoding project run the UI.py file in its folder, it will automatically import the other two class/module files 'image_getter.py' and 'decoder.py'. 
A simple black window will open, displaying a headline text and below the decoded message. 
Make sure that a camera is connected to the system and fully framing the code you wish to translate. 

For the purposes of the exhibition the program will automatically take a picture every 15 seconds and pass it through the OCR and decoding routines. Close the window to quit the program. <br/>
_Please note that this will probably not be very accurate, assure good lighting and centering of the code image in a straight line to increase effectiveness, but that might still not be enough. The program should display what parts of the text it failed to recognise._

### Acknowledgements ###
Thanks to all the amazing people that have helped us in this project: 
* Our profs and experts who organized this awesome course and have so many tips and ideas for any questions! We learned a lot!
* Friends and family for their advice, interest and willing participation in our design research!
* The countless manuals & help threads online offering explanations for pretty much anything :P

This project was made by A. Ahmer (Product Design student at KHB), A. Ehrlich and L. Seggewies (Computer Science students at FUB).
