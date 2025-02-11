# WIPWIPWIPWIPWIPWIPWIPWIP
# Handwriting++
######  A project for the IxD 2024 course by KH Berlin and the FU Berlin ######
##### Handwriting++ aims to support a new synergy of analogue an digital writing and data transfer by merging the multi-mediality of digital processes with the manual art of handwritting. #####

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

Here you will find the software part of this project. All project files rest on the main branch. The folders "encoding" and "decoding" contain the relevant python programs for this step of the device usage and necesssary auxiliary files. The encoding folder contains the UI program and the needed Arduino code files. The "decoding" folder contains the UI main program and the helper module scripts for reading and decoding images from a camera. 

The project is built around an Arduino UNO R3 board with a solenoid as a linear motor and a rotation sensor, other equipment like jumper wires, a board, pen, materials to produce the holder, and more are also needed. 
This image shows a possible wireing of the setup. 

SHOULDWESHOWANIMAGEHERE???
![Arduino with 'lotta wires :P](https://github.com/Aehrlich98/IxD2024_HandwritingPP/blob/main/Prototype.JPG?raw=true)

The arduino code requires the [Arduino IDE](https://www.arduino.cc/en/software) to pass the instructions to a compatible microcontroller. 

The user facing software parts of this project are built in Python 3. It is recommended to use atleast Python 3.10 to avoid potential compatibility issues but there are no dependecies for specific package versions.
The following libraries are used for core features of this project:
* The [Kivy](https://pypi.org/project/Kivy/) UI library for the UI and runtime structure
* [OpenCV](https://pypi.org/project/opencv-python/) for handling image recording and modulation
* [pytesseract](https://pypi.org/project/pytesseract/) as a wrapper for the Tesseract OCR system installation

### Installation ###

You can install all python requirements via the requirements.txt file from this projects main directory:

`pip install -r requirements.txt`

For the Arduino setup, it is recommended to use the Arduino IDE to open the .ino code file and pass it to a suitable board. This is also a good step to test the program and adjust any potential differing variables, like the serial port, or Baud rate.

For the Tesseract OCR engine this project relies on setting up a local system installation. Atleast version 4 is required but any higher version of Tesseract 4.xx or 5.xx should be functional.
Refer to the [official repository](https://github.com/tesseract-ocr/tesseract) for installation instructions and further info.

For e.g. Debian based linux distributions you can install it via apt:
`sudo apt install tesseract-ocr`

After installation find the 'tessdata' directory containing tesseract language and recognition data and copy the contents of the "morseocr" folder into there. On Debian based systems this folder can usually be found under 
`/usr/share/tesseract-ocr/X.XX/tessdata`, where X.XX is the version number installed. On Windows it might be under `%USERPROFILE%\AppData\Local\Programs\Tesseract-OCR\tessdata`.

### Running the programs ###

#### encoding ####
To start the encoding project, simply connect the Arduino to your computer and run the UI.py script—no parameters are required. The UI.py can be found in the encoding folder. A serial connection should open automatically, enabling communication between the Arduino and the PC. If everything is set up correctly, you will see an interface with a text input field prompting you to enter a word. Once you provide a word, it will be translated into Morse code and written using the pen.

#### decoding ####

To start the decoding project.... TO DO
The programs in each folder are independent of each other and can be run separately.

_Please note that the OCR model is not very reliable as of yet. Tesseract OCR is not aimed at recognising handwritting from camera images and we didn't quite get the training just right to minimise recognition errors._

### Acknowledgements ###
Thanks to all the amazing people that have helped us in this project!
* Our profs and experts who organized this awesome course and have so many tips and ideas for any questions! We learned a lot!
* Friends and family for their advice, interest and willing participation in our design research!
* The count-less help threads online for offering explanations for pretty much anything :P

This project was made by A. Ahmer (Product Design student at KHB), A. Ehrlich and L. Seggewies (computer science students at FUB).
