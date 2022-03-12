import os

from bs4 import BeautifulSoup
import speech_recognition as sr, pandas as pd
import webbrowser, requests, twint, bs4

class Lyza:
    
    def __init__ (self):

        self.r = sr.Recognizer()

        self.r.dynamic_energy_ratio  = 1.5
        self.r.dynamic_energy_adjustment_damping = 0.15
        self.r.dynamic_energy_threshold = True

        self.active = False

        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration = 1)
        
            
        

    def record(self):  

        with sr.Microphone() as source:

            try:

                audio = self.r.listen(source, phrase_time_limit=4, timeout=0.5)
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

        elif 'search' in command:

            word = ""
            command_words = command.split(' ')
            for i in range(len(command_words)):
                if command_words[i] == 'search':
                    word = ("_").join(piece.capitalize() for piece in command_words[i+1:])

            if word == "":
                return

            url = "https://en.wikipedia.org/wiki/" + word

            webpage = requests.get(url)
            soup = BeautifulSoup(webpage.content, 'html.parser')
            details = soup('table', {'class': 'infobox'})

            i = 1
            j = 3
            
            os.system('cls' if os.name == 'nt' else 'clear') # nt is for Windows, otherwise Linux or Mac


            word_to_print = []
            for char in word:
                if char != "_":
                    word_to_print.append(char)

            print(("").join(word_to_print) + "\n")

            while i < j:
                
                if (len(soup('p')[i].text) == 1):

                    i += 1
                    j += 1

                    continue

                k = 0
                buffer = []
                content = soup('p')[i].text
                while k < (len(content)):
                    if content[k] == '[':
                        k += 3 
                        continue
                    else:
                        buffer.append(content[k])
                        k += 1
                i += 1
                print(("").join(buffer))


        elif 'trending' in command:
            
            word = ""
            command_words = command.split(' ')
            
            for i in range(len(command_words)):
                if command_words[i] == 'search':
                    word = ("_").join(piece.capitalize() for piece in command_words[i+1:])
            
            if word == "":
                return

            scraper = twint.Config()
            scraper.Search = [word]       # topic
            scraper.Store_csv = True       # store tweets in a csv file
            scraper.Output = "dummy.csv"     # path to csv file

            twint.run.Search(scraper)


            df = pd.read_csv('dummy.csv')
            tweets = dict(zip(df['username'], df['tweet']))
            

            
            os.system('cls' if os.name == 'nt' else 'clear') # nt is for Windows, otherwise Linux or Mac
            tweets_scrapped = 0
            print("TWEETS ON: " + word + "\n")
            
            for username in tweets:

                print(username + ": " + tweets[username] + "\n")
                tweets_scrapped += 1
                if tweets_scrapped == 3:
                    break

            os.remove('dummy.csv')
            


lyza = Lyza()
    

while True:
    command = lyza.record()
    if 'exit' == command:
        break
    if 'sleep' == command:
        continue
    lyza.action(command)


