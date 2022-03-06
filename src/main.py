import speech_recognition as sr
import webbrowser

class Lyza:
    
    def __init__ (self):

        self.r = sr.Recognizer()
        self.r.pause_threshold = 0.5
        self.active = False

    def record(self):
        
        with sr.Microphone() as source:

            try:
                audio = self.r.listen(source, 0.3, 2)
                command = self.r.recognize_google(audio)

            except:
                return 'sleep'

            if not self.active:
                if 'liza' in command.lower():
                    self.active = True
                    print("Hi, how can I help you?")
                else:
                    return 'sleep'
            return command.lower()
    
    @staticmethod
    def action(command):
        if 'youtube' in command:
            url = "https://www.youtube.com"
            webbrowser.get().open(url)



lyza = Lyza()

while True:
    command = lyza.record()
    if 'exit' == command:
        break
    if 'sleep' == command:
        continue
    lyza.action(command)


