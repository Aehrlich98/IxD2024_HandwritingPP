#import needed UI modules from kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
# import our local module files
import image_getter
import decoder


class decoderUI(App):
# Variables: update frequency for image decoding process, output text storage, storage for helper classes from custom modules 
    update_freq_sec = 15
    outputtext = "...Here you will soon see the decoded text."
    ocrhandler = None
    decodeHandler = None
    top_label_text = "Hello, here you can see what secrets our image decoding program could uncover :)\nIt runs every " + str(update_freq_sec) + " seconds taking a picture with the webcam.\nTry to only center one line of code under the camera, make sure the paper is well lit and there is nothing else in the way."

    #update function for the UI, when called, takes an image via ImageGetter class and rectrieves morse code from it, then decodes the text via the custom decoder module. 
    def update(self, *args):
        """
        # Test function for all parts. Parameter either image file name or emtpy to use camera
        self.outputtext = self.test_all("testimg.png")
        self.l.text = self.outputtext
        """

        self.image = self.ocrhandler.camera_get_image()
        self.image = self.ocrhandler.preprocess_image(self.image)
        self.codeText = self.ocrhandler.read_from_image(self.image)
        self.clearText = decoder.decode_morse(self.codeText)
        print("Output code text: " + self.codeText, "\nOutput decoded text: " + self.clearText + "\n")
        self.l.text = self.clearText
        

    def build(self):
        """ Build function needed for the Kivy UI module to build the inital UI upon class instantiation """
        self.baselayout = FloatLayout() # BoxLayout(orientation='vertical', padding=10, spacing=10)
        # constant header displaying the text below, to help explain what's going on.
        self.header_label = Label(text= self.top_label_text, 
                                  font_size=32,
                                  size_hint=(0, 0.8),
                                  pos_hint={'x':0.5, 'y':0.5})
        self.baselayout.add_widget(self.header_label)
        # Label with dynamic size depending on the amount of text displayed:
        # Thanks, Stackoverflow :P (https://stackoverflow.com/questions/18670687/how-i-can-adjust-variable-height-text-property-kivy)
        self.b = GridLayout(
            cols=1,
            pos_hint={
                'center_x': .5,
                'center_y': .5},
            size_hint=(None, None),
            spacing=20,
            width=200)
        self.b.bind(minimum_height=self.b.setter('height'))
        self.baselayout.add_widget(self.b)

        self.l = Label(
            text=self.outputtext,
            size_hint_y=None)
        self.l.bind(width=lambda s, w:
            s.setter('text_size')(s, (w, None)))
        self.l.bind(texture_size=self.l.setter('size'))
        self.b.add_widget(self.l)

        self.start_all()
        Clock.schedule_interval(self.update, self.update_freq_sec) # time to update program: take picture, process, ocr, decode and present on screen.
        return self.baselayout

    def start_all(self):
        """ Start function, actually just to initiate the ImageGetter helper class """
        print("Started program. Setting up...")
        self.ocrhandler = image_getter.ImageGetter()
        print("Camera set up successfull.\nStarted program.")



    #BEGIN TEST function
    def test_all(self, testimg=""):
        print("::::::: Test function started :::::::")
        #Test functionality of the image receiving program and OCR model
        print("::::: Test camera and OCR :::::")
        test_code = self.ocrhandler.test_func(testimg)
        print("Morse code read from image: " + test_code)
        #Test functions for the decoder based on previously extracted code
        print("\n::::: Test decoder :::::")
        testout = decoder.decode_morse(test_code)
        print("Decoded message: " + testout)
        print("::::::: Test function finished :::::::")
        if testout is not None:
            return testout
        else:
            return "No text read from OCR."
    #END TEST function


# start program when running this script
if __name__ == "__main__":
    decoderUI().run()
