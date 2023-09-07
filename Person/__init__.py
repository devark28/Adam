# import os
import time

import openai
import pyttsx3
import speech_recognition
# import openai_secret_manager


class Person:
    def __init__(self, name):
        self.__init_hearing()
        self.__init_speaking()
        self.__init_brains()
        print("I am alive!")
        self.in_routine = True
        self.name = name

    def routine(self):
        what = self.hear()
        print(f"User: ", end="")
        for char in what:
            print(char, end="")
            time.sleep(.1)
        print()
        what = self.__think(what)
        print(f"{self.name}: ", end="")
        for char in what:
            print(char, end="")
            time.sleep(.1)
        print()
        self.talk(what)
        if self.in_routine:
            self.routine()

    @staticmethod
    def __init_brains():
        # secrets = openai_secret_manager.get_secret("openai")
        # openai.api_key = secrets["api_key"]
        openai.organization = "ORGANIZATION_KEY"
        openai.api_key = "API_KEY"
        # openai.Model.list()

    def __init_speaking(self):
        self.BufOut = pyttsx3.init()
        self.BufOut.setProperty('volume', '1.0')
        self.BufOut.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN'
                                         '-US_ZIRA_11.0')
        self.BufOut.setProperty('rate', 150)

    def __init_hearing(self):
        self.MicIn = speech_recognition.Recognizer()

    def talk(self, what):
        self.BufOut.say(what)
        self.BufOut.runAndWait()
        self.BufOut.stop()

    def hear(self) -> str:
        output = ""
        try:
            with speech_recognition.Microphone() as source:
                self.MicIn.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.MicIn.listen(source, 6, 10)
                output = self.MicIn.recognize_google(audio)
                output = output.lower()
        except speech_recognition.RequestError:
            pass
            # speak("sorry, i can't connect to the servers, please check your internet connection and boot me again!")
        except speech_recognition.UnknownValueError:
            pass
            # speak("sorry, did you say anything?")
            # __reply = hear(10)
            # if __reply.__len__() > 0:
            #     speak('can you repeat clearly please!')
            #     __reply = hear(6)
            # else:
            #     speak('reboot me when you want !')
            # output = __reply
        except speech_recognition.WaitTimeoutError:
            pass
        return output.lower()

    def __think(self, what) -> str:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"User: {what}\n{self.name}:",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = response.choices[0].text.strip()
        if str(message).lower().__contains__("goodbye"):
            self.in_routine = False
        return message
