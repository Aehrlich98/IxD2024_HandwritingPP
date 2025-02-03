#import needed UI modules from kivy
from doctest import OutputChecker
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
# import our local module files
import image_getter
import decoder


class decoderUI(App):
    # text variable which will contain the last received decoded text block
    outputtext = "Hello, here you will soon see what text our image recognition progra could recognise and translate :)"
#BEGIN TEST function
    def test_all(self):
        print("::::::: Test camera and OCR :::::::")
        testtext = image_getter.test_func("morseText001.png")  #"morseSOS_frInternet.png") # "morseText001.png")
        print(testtext)
        # test the decoder on an exmaple morse code block
        print("\n::::::: Test decoder:::::::")
        test_code = testtext    # "--- ..- -.-. .... / .----\n.-.. --- .-.." #ouch 1\nlol
        testout = decoder.decode_morse(test_code)
        print(testout)
        return testout
    #END TEST function

    def build(self):
        self.baselayout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        # Label with dynamic size depending on the amount of text displayed:
        # thanks to Stackoverflow :P (https://stackoverflow.com/questions/18670687/how-i-can-adjust-variable-height-text-property-kivy)

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

        Clock.schedule_interval(self.update, 10) # time to update program: take picture, process, ocr, decode and present on screen.
        return self.baselayout

    #MAIN function
    def start_all(self):
        print("Started program. Setting up...")
        check =  image_getter.start_this()
        # print(check)
        if check:
            raise Exception("Camera setup isn't working!\nPlease ensure the webcam is connected and reachable on the computer!")
        print("Camera set up successfull.\nStart automatic program:")

        #TEST all
        # self.test_all()
    def update(self, *args):
        print("Update function just called...")
        self.outputtext = self.test_all()
        self.l.text = self.outputtext    
    




# start program when running this script
if __name__ == "__main__":
    decoderUI().run()
