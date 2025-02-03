from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
import serial

class ArduinoApp(App):
    def build(self):
        # Set up the layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Morse-Code String und LookUp String
        self.morse_string = ""  # Der Morsecode wird vom Arduino empfangen
        self.look_up_symbol = []  # LookUp Array für Symbol-Index
        self.symbol_labels = []  # Labels für jedes Symbol im Morsecode

        # Setup serial connection
        self.serial_port = serial.Serial('COM3', 115200, timeout=1)

        # TextInput für die String-Eingabe: Nur eine Zeile zulassen
        self.input_text = TextInput(
            hint_text="Geben Sie einen String ein", 
            size_hint=(1, None), 
            height=100,
            multiline=False  # Nur eine Zeile zulassen
        )
        # Wenn Enter gedrückt wird, soll der Senden-Button ausgelöst werden
        self.input_text.bind(on_text_validate=self.send_string)

        # Button zum Senden des Strings an Arduino
        self.send_button = Button(text="An Stift senden", size_hint=(1, None), height=100)
        self.send_button.bind(on_press=self.send_string)

        # Füge Widgets hinzu
        self.layout.add_widget(self.input_text)
        self.layout.add_widget(self.send_button)

        # Label für die Aufforderung
        self.prompt_label = Label(text="Bitte Wort eingeben:", font_size=24, size_hint=(1, None), height=50)
        #self.layout.add_widget(self.prompt_label)
        
        # Label für Erklärung
        self.explain_label = Label(text="Fahre mit dem Stift über das Papier um den Morsecode zu schreiben.", 
                                   font_size=24, size_hint=(1, None), height=50)

        # Schedule serial reading
        Clock.schedule_interval(self.read_from_serial, 0.01)

        return self.layout

    def send_string(self, instance):
        """Sendet den eingegebenen String an den Arduino."""
        input_string = self.input_text.text.strip()
        if input_string:
            # Sendet den String über die serielle Schnittstelle an Arduino
            self.serial_port.write((input_string + '\n').encode())
            self.input_text.text = ""  # Eingabefeld zurücksetzen
            print(f"String gesendet: {input_string}")
        else:
            print("Bitte einen String eingeben")

    def read_from_serial(self, dt):
        """Liest Daten kontinuierlich von der seriellen Schnittstelle."""
        try:
            if self.serial_port.in_waiting > 0:
                line = self.serial_port.readline().decode('utf-8').strip()

                if line.startswith("Morsecode:"):
                    # Empfange den Morse-Code-String
                    self.morse_string = line.split(":")[1]
                    self.initialize_ui()
                    print(f"Morse-Code empfangen: {self.morse_string}")

                elif line.startswith("LookUp:"):
                    # Empfange den LookUp-String und umwandeln in eine Liste von Ganzzahlen
                    look_up_string = line.split(":")[1]
                    self.look_up_symbol = [int(x) for x in look_up_string.split(',')]
                    print(f"LookUp Array empfangen: {self.look_up_symbol}")

                elif line.isdigit():
                    # Aktualisiere den Status basierend auf impulseCount
                    impulse_count = int(line)
                    self.update_status(impulse_count)
                    print(f"Impulse Count: {impulse_count}")

                elif line == "Bitte einen neuen String eingeben:":
                    # Wenn der Arduino diese Nachricht sendet, UI zurücksetzen
                    self.reset_ui_for_new_word()
                    print("UI für neues Wort zurückgesetzt")
        except Exception as e:
            print(f"Error reading from serial: {e}")

    def initialize_ui(self):
        """Initialisiert die Benutzeroberfläche basierend auf dem Morsecode."""
        Clock.schedule_once(self._initialize_ui)

    def _initialize_ui(self, dt):
        """Setzt die UI auf und fügt Labels hinzu."""
        self.layout.clear_widgets()  # Entfernt alte Labels
        self.symbol_labels = []

        # Füge das Label für die Eingabeaufforderung hinzu
        #self.layout.add_widget(self.prompt_label)
        self.layout.add_widget(self.explain_label)

        # Äußeres FloatLayout für vollständige Zentrierung
        float_layout = FloatLayout()

        # Inneres BoxLayout für Morse-Code-Symbole
        morse_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), height=100)
        morse_layout.bind(minimum_width=morse_layout.setter('width'))  # Automatische Breitenanpassung
        morse_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Exakte Zentrierung

        # Morse-Code String darstellen
        for symbol in self.morse_string:
            label = Label(text=symbol, color=(0.5, 0.5, 0.5, 1), font_size=80, bold=True, size_hint=(None, 1))
            label.bind(texture_size=label.setter('size'))  # Automatische Breitenanpassung
            self.symbol_labels.append(label)
            morse_layout.add_widget(label)

        float_layout.add_widget(morse_layout)
        self.layout.add_widget(float_layout)  # Füge zentriertes Layout hinzu

        # Füge die Eingabe und den Senden-Button am unteren Rand hinzu
        self.layout.add_widget(self.input_text)
        self.layout.add_widget(self.send_button)

    def reset_ui_for_new_word(self):
        """Setzt die UI zurück, um den neuen String einzugeben."""
        # Entferne den Morsecode und führe eine Aufforderung ein
        self.morse_string = ""
        self.look_up_symbol = []
        self.symbol_labels = []

        # Setze das Label auf "Bitte Wort eingeben:"
        self.prompt_label.text = "Bitte Wort eingeben:"
        self.layout.clear_widgets()  # Entfernt alle Widgets
        self.layout.add_widget(self.prompt_label)  # Zeigt das Aufforderungslabel an

        # Zeigt das Eingabefeld und den Senden-Button an
        self.layout.add_widget(self.input_text)
        self.layout.add_widget(self.send_button)

    def update_status(self, impulse_count):
        """Aktualisiert die Statusanzeige basierend auf impulseCount."""
        Clock.schedule_once(lambda dt: self._update_status(impulse_count))

    def _update_status(self, impulse_count):
        """Färbt die Symbole grün, die bereits geschrieben wurden."""
        try:
            # Verwende lookUpSymbol Array
            if impulse_count < len(self.look_up_symbol):
                current_symbol_index = self.look_up_symbol[impulse_count]

                # Symbole grün färben, wenn der Index erreicht ist
                for i, label in enumerate(self.symbol_labels):
                    if i <= current_symbol_index:
                        label.color = (0, 1, 0, 1)  # Grün für geschrieben
                    else:
                        label.color = (0.5, 0.5, 0.5, 1)  # Grau für noch nicht geschrieben
        except ValueError as e:
            print(f"Error updating status: {e}")

if __name__ == '__main__':
    ArduinoApp().run()
