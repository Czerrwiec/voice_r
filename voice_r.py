import speech_recognition as sr
import customtkinter as ctk
import csv
import keyboard
import threading

from pathlib import Path

 
ctk.set_appearance_mode("System")        
recognizer = sr.Recognizer()


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("voice_r")    
        self.geometry("300x300")  
        # self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')

        self.samples_dictionary = {}
        self.isrecording = False

        self.rec_button = ctk.CTkButton(self, text="Nagrywaj", width=100, height=40, command=self.startrecording)
        self.rec_button.pack(pady=(10, 10), padx=(20, 20), side="top")

        self.stop_button = ctk.CTkButton(self, text="Stop", width=100, height=40, command=self.stoprecording)
        self.stop_button.pack(pady=(10, 10), padx=(20, 20), side="top")
        self.stop_button.configure(state='disabled')


    def load_csv_to_dict(self):
        file = Path(__file__).parent / 'samples.csv'
        with file.open('r', encoding='UTF=8') as data:
            lists_of_samples = csv.reader(data)
            for item in lists_of_samples:
                self.samples_dictionary[item[0]] = int(item[1])


                
    def record_text(self):
            while(self.isrecording):
                try:
                    with sr.Microphone() as source2:
                        
                        recognizer.adjust_for_ambient_noise(source2, duration=0.4)

                        audio2 = recognizer.listen(source2)

                        MyText = recognizer.recognize_google(audio2, language="pl-PL")
                        
                        print(MyText)

                        for key in self.samples_dictionary.keys():
                            if key == MyText:
                                self.samples_dictionary[key] += 1
                                print(self.samples_dictionary)
                        # return MyText

                except sr.RequestError as e:
                    print("Nierozpoznany wynik: {0}".format(e))
                    
                except sr.UnknownValueError:
                    print("Nieznany błąd")
                    
            

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

        

        

if __name__ == "__main__":
    app = App()
    app.load_csv_to_dict()
    
    app.mainloop()  