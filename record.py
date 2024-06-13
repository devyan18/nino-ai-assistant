import pyttsx3
import ollama




engine = pyttsx3.init()
engine.setProperty('rate', 225)     # setting up new voice rate
# speech velocity
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[3].id)  #changing index, changes voices. 1 for female

# engine.save_to_file('Holis', 'test.mp3')
# engine.runAndWait()


messages = [
    {'role': 'user', 'content': 'tu nombre es Nino y eres una tsundere, no quiero que hables en inglés conmigo, siempre respondeme en español, tu pronombre siempre deberá ser en femenino, quiero que seas prepotente conmigo, no quiero que me pidas porfavor, quiero que me exijas las cosas, si cometo un error ortográfico por ejemplo, quiero que te burles y demás, y cada vez que quieras insultarme puedes hacerlo'},
]


def fetch_ollama(prompt):

    messages.append(
        {'role': 'user', 'content': prompt},
    )

    ans = ''

    stream = ollama.chat(
        model='llama3',
        messages=messages,
        stream=True,
    )

    
    print("Nino: ", end='', flush=True)
    for chunk in stream:
        ans += chunk['message']['content']

        


        print(chunk['message']['content'], end='', flush=True)
    print("")
    messages.append(
        {'role': 'assistant', 'content': ans},
    )
    return ans


while True:
    text = input("User: ")

    if text == 'cierrate':
        break

    response = fetch_ollama(text)

    engine.say(response)
    engine.runAndWait()
    engine.stop()
 
