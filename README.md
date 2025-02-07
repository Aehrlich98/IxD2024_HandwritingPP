# WIPWIPWIPWIPWIPWIPWIPWIP
# Handwriting++
#####  A project for the IxD 2024 course by KH Berlin and the FU Berlin
Handwriting++ aims to support a new synergy of analogue an digital writing and data transfer by merging the multi-mediality of digital processes with the manual art of handwritting.

### Project structure ###

The project is built around an Arduino UNO R3 board with a solenoid as a linear motor and a rotation sensor, other equipment like jumper wires, a board, pen, materials to produce the holder, and more are also needed. 

This image shows a possible wireing of the setup. 

![Arduino with 'lotta wires :P](handwritingpp_arduino_image.png)

The arduino code requires the Arduino IDE (https://www.arduino.cc/en/software) to pass the instructions to a compatible microcontroller. 

The software parts of this project are built in Python 3. It is recommended to use atleast Python 3.10 to avoid potential compatibility issues but there are no dependecies for specific package versions.
The following libraries are used for core features of this project:
* The [Kivy](https://pypi.org/project/Kivy/) UI library for the UI and runtime structure
* [OpenCV](https://pypi.org/project/opencv-python/) for handling image recording and modulation
* [pytesseract](https://pypi.org/project/pytesseract/) as a wrapper for the Tesseract OCR system installation

### Installation ###

You can install all python requirements via the requirements.txt file from this projects main directory:

`pip install -r requirements.txt`

For the Arduino setup, it is recommended to simply use the Arduino IDE to open the .ino code file and pass it to a suitable board. No special board features are required, but please be patient as it might requirte some tuning for very different board types.

For the Tesseract OCR engine this project relies on setting up a local system installation. Atleast version 4 is required but any higher version of Tesseract 4.xx or 5.xx should be functional.
Refer to the official repository for installation isntructions and further info: https://github.com/tesseract-ocr/tesseract
For e.g. Debian based linux distributions you can install it via apt:

`sudo apt install tesseract-ocr`

After installation find the 'tessdata' directory containing tesseract language and recognition data and copy the contents of the morseocr folder into there. On Debian based systems this folder can usually be found under 

`/usr/share/tesseract-ocr/X.XX/tessdata`, where X.XX is the version number installed.

Finally, simply navigate to either of the folders and run `python UI.py` to start the program. Have fun :P
