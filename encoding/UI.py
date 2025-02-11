import time
import threading
from functools import partial
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
import serial


class ArduinoApp(App):
    def build(self):
        Window.fullscreen = 'auto'
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        Window.bind(on_keyboard=self.on_keyboard)

        # Variablen initialisieren
        self.morse_string = ""
        self.command_list = []     # Liste der Befehle für jeden Impuls
        self.symbol_indices = []   # Ordnet jedem Impuls den Index des zugehörigen Morse-Symbols zu
        self.symbol_labels = []    # Labels für die Anzeige des Morse-Codes

        #Timer für Timeout
        self.last_serial_time = time.time()
        self.last_processed_time = None

        # Serielle Schnittstelle initialisieren
        try:
            # Timeout auf 0.5 s gesetzt, sodass readline() nicht zu lange blockiert
            self.serial_port = serial.Serial('COM3', 230400, timeout=0.5)       #BaudeRate evtl anpassen
            print("Serielle Schnittstelle erfolgreich geöffnet.")
        except Exception as e:
            print(f"Fehler beim Öffnen des seriellen Ports: {e}")
            self.serial_port = None

        # Eingabefeld
        self.input_text = TextInput(
            hint_text="Geben Sie ein Wort ein...",
            size_hint=(1, None),
            height=80,
            font_size = 30,
            multiline=False
        )
        self.input_text.bind(on_text_validate=self.process_string)

        # button zum Senden
        self.send_button = Button(text="An Stift senden", size_hint=(1, None), height=100)
        self.send_button.bind(on_press=self.process_string)

        # Labels für Aufforderungen
        self.prompt_label = Label(text="Geben Sie ein Wort ein welches in Morsecode umwandelt werden soll:", font_size=35, size_hint=(1, None), height=50)
        self.explain_label = Label(
            text="Fahre mit dem Stift über das Papier, um den Morsecode zu schreiben.",
            font_size=35, 
            size_hint=(1, None), 
            height=50, 
            padding = [0,0,0,30]
        )

        # Eingabeaufforderung Textfeld und Button anzeigen
        self.layout.add_widget(self.prompt_label)
        self.layout.add_widget(self.input_text)
        self.layout.add_widget(self.send_button)

        # Starte den separaten Thread
        if self.serial_port and self.serial_port.is_open:
            self.stop_event = threading.Event()
            self.serial_thread = threading.Thread(target=self.serial_thread_func, daemon=True)
            self.serial_thread.start()
            print("Serieller Lese-Thread gestartet.")
        else:
            print("Serielle Schnittstelle nicht verfügbar oder nicht geöffnet.")

        # Timeout-Prüfung jede sek
        Clock.schedule_interval(self.check_process_timeout, 1)

        return self.layout
    
    
    def on_keyboard(self, window, key, scancode, text, modifiers):
        # Esc wird abgefangen
        if key == 27:  # (27 = Esc)
          return True 
    

    def process_string(self, *args):
        # Verarbeitet den eingegebenen Text
        input_string = self.input_text.text.strip()
        if input_string:
            self.last_processed_time = time.time()
            self.morse_string = self.text_to_morse(input_string)
            print(f"Text: {input_string} -> Morse: {self.morse_string}")
            self.command_list, self.symbol_indices = self.convert_morse_to_commands(self.morse_string)
            self.initialize_ui()
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.write("N\n".encode()) #Reset Arduino Impulse Count
            else:
                print("Serielle Schnittstelle nicht verfügbar")
            self.input_text.text = ""

    def serial_thread_func(self):
        # Thread um Serielle Nachrichten einzulesen
        while not self.stop_event.is_set():
            if self.serial_port and self.serial_port.is_open:
                try:
                    line = self.serial_port.readline()
                    if line:
                        try:
                            line = line.decode('utf-8').strip()
                        except Exception as decode_err:
                            print(f"Fehler beim Dekodieren: {decode_err}")
                            continue
                        self.last_serial_time = time.time()
                        print(f"Serielle Nachricht empfangen: '{line}'")
                        # Übergabe der Zeile an die UI-Verarbeitung im Hauptthread
                        Clock.schedule_once(partial(self.process_serial_line, line))
                    else:
                        time.sleep(0.0001)
                except Exception as e:
                    print(f"Error in serial thread: {e}")
            else:
                time.sleep(0.0001)

            # Timeout Prüfung
            if time.time() - self.last_serial_time >= 60:
                print("Timeout: Keine Serial-Nachricht in 60 Sekunden erhalten. Setze UI zurück.")
                Clock.schedule_once(lambda dt: self.reset_ui_for_new_word())
                self.last_serial_time = time.time()


    def process_serial_line(self, line, dt):
        if line.isdigit():
            impulse_count = int(line)
            self.update_status(impulse_count)
            print(f"Impulse Count: {impulse_count}")
            self.send_command(impulse_count)
        elif line == "Ready":
            self.reset_ui_for_new_word()
            print("UI für neues Wort zurückgesetzt")
        else:
            print(f"Unbekannte Nachricht: '{line}'")

    def check_process_timeout(self, dt):
        # Prüft ob seit der Eingabe mehr als 120 Sekunden vergangen sind.
        if self.last_processed_time is not None:
            if time.time() - self.last_processed_time >= 120:
                print("Timeout: 120 Sekunden seit der Verarbeitung des Strings vergangen. Setze UI zurück.")
                self.reset_ui_for_new_word()


    def send_command(self, impulse_count):
        if impulse_count < len(self.command_list):
            command = self.command_list[impulse_count]
            if command is None:
                pass
            elif command == 0:
                self.serial_port.write("U\n".encode())
            elif command == 1:
                self.serial_port.write("D\n".encode())
        else:
            self.reset_ui_for_new_word()
            


    def text_to_morse(self, text):
        morse_dict = {
            'A': '.-',    'B': '-...',  'C': '-.-.', 'D': '-..',  'E': '.',
            'F': '..-.',  'G': '--.',   'H': '....', 'I': '..',   'J': '.---',
            'K': '-.-',   'L': '.-..',  'M': '--',   'N': '-.',   'O': '---',
            'P': '.--.',  'Q': '--.-',  'R': '.-.',  'S': '...',  'T': '-',
            'U': '..-',   'V': '...-',  'W': '.--',  'X': '-..-', 'Y': '-.--',
            'Z': '--..',  '1': '.----', '2': '..---','3': '...--','4': '....-',
            '5': '.....', '6': '-....', '7': '--...', '8': '---..','9': '----.',
            '0': '-----', ' ': '/',
        }
        return ' '.join(morse_dict.get(char.upper(), '') for char in text)

    def convert_morse_to_commands(self, morse_code):
        """
        Konvertiert den Morsecode in zwei Listen:
         - command_list: enthält für jeden Impuls 0 (für "U") oder 1 (für "D")
         - symbol_indices: ordnet jedem Impuls den Index des zugehörigen Morse-Symbols zu
        """
        command_list = []
        symbol_indices = []
        symbol_index = 0

        for c in morse_code:
            if c == '.':
                command_list.extend([0, 0, 1])
                symbol_indices.extend([symbol_index, symbol_index, symbol_index])
                symbol_index += 1
            elif c == '-':
                command_list.extend([0, 0, 1, 1, 1, 1])
                symbol_indices.extend([symbol_index] * 6)
                symbol_index += 1
            elif c == ' ':
                command_list.extend([0, 0])
                symbol_indices.extend([symbol_index, symbol_index])
                symbol_index += 1
            elif c == '/':
                command_list.extend([0, 0])
                symbol_indices.extend([symbol_index, symbol_index])
                symbol_index += 1
        return command_list, symbol_indices

    def initialize_ui(self):
        self.serial_port.write("N\n".encode())
        self.layout.clear_widgets()
        self.symbol_labels = []
        self.layout.add_widget(self.explain_label)
        float_layout = FloatLayout()
        morse_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), height=100)
        morse_layout.bind(minimum_width=morse_layout.setter('width'))
        morse_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        for symbol in self.morse_string:
            label = Label(text=symbol, color=(0.5, 0.5, 0.5, 1), font_size=80, bold=True, size_hint=(None, 1))
            label.bind(texture_size=label.setter('size'))
            self.symbol_labels.append(label)
            morse_layout.add_widget(label)

        float_layout.add_widget(morse_layout)
        self.layout.add_widget(float_layout)

    def reset_ui_for_new_word(self):
        self.serial_port.write("N\n".encode())
        self.morse_string = ""
        self.command_list = []
        self.symbol_indices = []
        self.symbol_labels = []
        self.last_processed_time = None
        self.prompt_label.text = "Geben Sie ein Wort ein welches in Morsecode umwandelt werden soll:"
        self.layout.clear_widgets()
        self.layout.add_widget(self.prompt_label)
        self.layout.add_widget(self.input_text)
        self.layout.add_widget(self.send_button)
        #print("UI zurückgesetzt")

    def update_status(self, impulse_count):
        #Aktualisiert die Anzeige, basierend auf dem Impulszähler.
        Clock.schedule_once(lambda dt: self._update_status(impulse_count))

    def _update_status(self, impulse_count):
        if impulse_count < len(self.symbol_indices):
            current_symbol_index = self.symbol_indices[impulse_count]
            for i, label in enumerate(self.symbol_labels):
                label.color = (0, 1, 0, 1) if i <= current_symbol_index else (0.5, 0.5, 0.5, 1)
        else:
            self.reset_ui_for_new_word()

    def on_stop(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        if hasattr(self, 'stop_event'):
            self.stop_event.set()
        if hasattr(self, 'serial_thread'):
            self.serial_thread.join(timeout=1)
        print("App beendet und Ressourcen freigegeben.")


if __name__ == '__main__':
    ArduinoApp().run()
