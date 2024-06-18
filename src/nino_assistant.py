import pyttsx3
import ollama
from langchain_community.llms import openllm

# from langchain.chat_models import ollama


class NinoAssistant:
    def __init__(self, context=""):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 225)     # setting up new voice rate
        self.engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
        voices = self.engine.getProperty('voices')       #getting details of current voice
        self.engine.setProperty('voice', voices[3].id)

        self.messages = [
            {'role': 'user', 'content': f"{context}"},
        ]

    def fetch_nino(self, prompt):
        self.messages.append(
            {'role': 'user', 'content': prompt},
        )

        ans = ''

        stream = ollama.chat(
            model='llama3',
            messages=self.messages,
            stream=True,
        )

        print("Nino: ", end='', flush=True)
        for chunk in stream:
            ans += chunk['message']['content']

            print(chunk['message']['content'], end='', flush=True)

        print("")

        self.messages.append(
            {'role': 'assistant', 'content': ans},
        )

        return ans

    def nino_say (self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.stop()
    
    