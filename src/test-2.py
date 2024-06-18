from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

MODEL = "llama3"

llm = Ollama(
    model=MODEL,
    callback_manager=CallbackManager([
        StreamingStdOutCallbackHandler()
    ]),
    temperature=0.1,
)

from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=['topic'],
    template="Háblame sobre los países más destacados en {topic}"
)

chain = llm | prompt

print(chain)

response = chain.invoke("América Latina")

print(response)