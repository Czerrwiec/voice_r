import speech_recognition as sr
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import csv
import threading
from datetime import datetime
import pyttsx3
from os import path
from sys import argv
from json import load


ctk.set_appearance_mode("System")        
recognizer = sr.Recognizer()

with open(path.dirname(path.realpath(argv[0])) + '\\' + 'config.json') as file:
    json_data = load(file)


recognizer.energy_threshold = json_data['recognizer.energy_threshold']
recognizer.dynamic_energy_adjustment_ratio = json_data['r.dynamic_energy_adjustment_ratio']
recognizer.pause_threshold = json_data['r.pause_threshold']
if json_data['recognizer.dynamic_energy_threshold'] == 'True':
    recognizer.dynamic_energy_threshold = True
elif json_data['recognizer.dynamic_energy_threshold'] == 'False':
    recognizer.dynamic_energy_threshold = False


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("voice_r")    
        self.geometry("200x230")  
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')

        self.samples_dictionary = {}
        self.isrecording = False

        self.rec_button = ctk.CTkButton(self, text="Nagrywaj", width=100, height=40, command=self.startrecording)
        self.rec_button.pack(pady=(10, 10), padx=(20, 20), side="top")

        self.stop_button = ctk.CTkButton(self, text="Stop", width=100, height=40, command=self.stoprecording)
        self.stop_button.pack(pady=(10, 10), padx=(20, 20), side="top")
        self.stop_button.configure(state='disabled')

        self.check_var = ctk.IntVar()

        self.checkbox01 = ctk.CTkCheckBox(self, text="announcer", variable=self.check_var, onvalue=1, offvalue=0)
        self.checkbox01.pack(pady=(10, 10), padx=(20, 20), side="top")

        self.label02 = ctk.CTkLabel(self, text="", fg_color="transparent")
        self.label02. pack(pady=(10, 10), padx=(20, 20), side="top")
 
        self.engine = pyttsx3.init()
        self.newVoiceRate = 165
        self.engine.setProperty('rate',self.newVoiceRate)
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[2].id)


    def load_csv_to_dict(self):
        file = path.dirname(path.realpath(argv[0])) + '\\' + 'samples.csv'

        try:
            with open(file, 'r', encoding='UTF=8') as data:
                lists_of_samples = csv.reader(data)
                for item in lists_of_samples:
                    self.samples_dictionary[item[0]] = int(item[1])
        except: 
            FileNotFoundError
            self.samples_dictionary = {"sample" : 0}
            self.save_to_csv()
            CTkMessagebox(title="Info", message="Dodano plik samples.csv, zamknij program i uzupełnij plik.")

   
    def record_text(self):
            while(self.isrecording):
                try:
                    with sr.Microphone() as source:
                        
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)

                        audio = recognizer.listen(source, phrase_time_limit=None)

                        text = recognizer.recognize_google(audio, language="pl-PL")
                        
                        for key in self.samples_dictionary.keys():
                            if key == text.lower():
                                self.samples_dictionary[key] += 1
                                self.label02.configure(text=f"{text.lower()} + 1")

                                threading.Timer(2, self.label_reset).start()

                                self.do_backup(text.lower())

                                if self.check_var.get() == 1:            
                                    self.engine.say('saved')
                                    self.engine.runAndWait()
                      
                except sr.RequestError as e:
                    print("Nierozpoznany wynik: {0}".format(e))
                    self.label02.configure(text="Nierozpoznany wynik")
                    threading.Timer(2, self.label_reset).start()
                           
                except sr.UnknownValueError:
                    print("Nieznany błąd")
                    self.label02.configure(text="Nierozpoznany wynik")
                    threading.Timer(2, self.label_reset).start()
                    
                           

    def startrecording(self):
        self.rec_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        self.isrecording = True

        record = threading.Thread(target=self.record_text)
        record.start()


    def stoprecording(self):
        self.stop_button.configure(state='disabled')
        self.rec_button.configure(state='normal')
        self.isrecording = False
        self.label02.configure(text="")
        self.save_to_csv()       


    def do_backup(self, data):
        file = path.dirname(path.realpath(argv[0])) + '\\' + 'backup.txt'

        file = open(file, 'a', encoding="utf-8")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        line = data + " " + dt_string
        file.write(line)
        file.write('\n')
        file.close()


    def save_to_csv(self):
        file = path.dirname(path.realpath(argv[0])) + '\\' + 'samples.csv'

        with open(file, 'w', encoding="utf-8", newline='') as csv_file: 

            writer = csv.writer(csv_file)

            for key, value in self.samples_dictionary.items():
                writer.writerow([key, value])
            

    def label_reset(self):
        self.label02.configure(text="")


if __name__ == "__main__":
    app = App()   
    app.load_csv_to_dict()     
    app.mainloop()  
    