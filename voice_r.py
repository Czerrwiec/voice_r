import speech_recognition as sr
import customtkinter as ctk
import csv
import keyboard
from keytracker import KeyTracker
 
ctk.set_appearance_mode("System")        
recognizer = sr.Recognizer()

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("voice_r")    
        self.geometry("300x400")  
        # self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')

        self.samples_dictionary = {}

        self.check_bool_var = ctk.BooleanVar(value=False)
        self.checkbox_01 = ctk.CTkCheckBox(self, text="Nagrywanie ciągiem", variable=self.check_bool_var)
        self.checkbox_01.pack(pady=(10, 10), padx=(20, 20), side="top")

        self.check_bool_var_02 = ctk.BooleanVar(value=False)
        self.checkbox_02 = ctk.CTkCheckBox(self, text="Nagrywanie przyciskiem [Z]", variable=self.check_bool_var_02)
        self.checkbox_02.pack(pady=(10, 10), padx=(20, 20), side="top")

        self.rec_button = ctk.CTkButton(self, text="Nagrywaj", width=100, height=40)
        self.rec_button.pack(pady=(10, 10), padx=(20, 20), side="top")



    def load_csv_to_dict(self):
        with open('samples.csv', encoding='UTF=8') as data:
            lists_of_samples = csv.reader(data)
            for item in lists_of_samples:
                self.samples_dictionary[item[0]] = item[1]
       
                
    def record_text(self):
        while(1):
            try:
                with sr.Microphone() as source2:
                    
                    recognizer.adjust_for_ambient_noise(source2, duration=0.01)

                    audio2 = recognizer.listen(source2)

                    MyText = recognizer.recognize_google(audio2, language="pl-PL")

                    return MyText

            except sr.RequestError as e:
                print("Nierozpoznany wynik: {0}".format(e))
            
            except sr.UnknownValueError:
                print("Nieznany błąd")
        return
    

    def start_recording(event=None):
        print('Recording right now!')


    def stop_recording(event=None):
        print('Stop recording right now!')

        

if __name__ == "__main__":
    app = App()
    app.load_csv_to_dict()
    
    keytracker = KeyTracker(app.start_recording, app.stop_recording)
    app.bind("<KeyPress-z>", keytracker.report_key_press)
    app.bind("<KeyRelease-z>", keytracker.report_key_release)

    app.mainloop()  