import speech_recognition as sr
import customtkinter as ctk
import csv
import threading
from datetime import datetime



from pathlib import Path

 
ctk.set_appearance_mode("System")        
recognizer = sr.Recognizer()


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("voice_r")    
        self.geometry("200x200")  
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')

        self.samples_dictionary = {}
        self.isrecording = False

        self.rec_button = ctk.CTkButton(self, text="Nagrywaj", width=100, height=40, command=self.startrecording)
        self.rec_button.pack(pady=(10, 10), padx=(20, 20), side="top")

        self.stop_button = ctk.CTkButton(self, text="Stop", width=100, height=40, command=self.stoprecording)
        self.stop_button.pack(pady=(10, 10), padx=(20, 20), side="top")
        self.stop_button.configure(state='disabled')

        self.label02 = ctk.CTkLabel(self, text="", fg_color="transparent")
        self.label02. pack(side="top")


    def load_csv_to_dict(self):
        file = Path(__file__).parent / 'samples.csv'
        with file.open('r', encoding='UTF=8') as data:
            lists_of_samples = csv.reader(data)
            for item in lists_of_samples:
                self.samples_dictionary[item[0]] = int(item[1])

   
    def record_text(self):
            while(self.isrecording):
                try:
                    with sr.Microphone() as source:
                        
                        recognizer.adjust_for_ambient_noise(source, duration=0.4)

                        audio = recognizer.listen(source)

                        text = recognizer.recognize_google(audio, language="pl-PL")
                        

                        for key in self.samples_dictionary.keys():
                            if key == text:
                                self.samples_dictionary[key] += 1

                                
                                self.label02.configure(text=f"{text} + 1")

                                self.do_backup(text)
                        # return MyText


                except sr.RequestError as e:
                    # pass
                    print("Nierozpoznany wynik: {0}".format(e))
                    self.label02.configure(text="Nierozpoznany wynik")
                    
                except sr.UnknownValueError:
                    # pass
                    print("Nieznany błąd")
                    self.label02.configure(text="Nierozpoznany wynik")
                    
            

    def startrecording(self):
        self.rec_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        self.isrecording = True

        record = threading.Thread(target=self.record_text)
        record.start()


    def stoprecording(self):
        self.stop_button.configure(state='disabled')
        self.rec_button.configure(state='normal')
        print("Stoped recording")
        self.isrecording = False
        self.label02.configure(text="")
        self.save_to_csv()       


    def do_backup(self, data):
        file = open("backup.txt", 'a', encoding="utf-8")
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        line = data + " " + dt_string
        file.write(line)
        file.write('\n')
        file.close()


    def save_to_csv(self):
        file = Path(__file__).parent / 'samples.csv'

        with file.open('w', encoding="utf-8", newline='') as csv_file: 

            writer = csv.writer(csv_file)

            for key, value in self.samples_dictionary.items():
                writer.writerow([key, value])
            


if __name__ == "__main__":
    app = App()
    app.load_csv_to_dict()
    app.mainloop()  