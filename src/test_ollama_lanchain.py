import streamlit as st # to render the user interface.
from langchain_community.llms import Ollama # to use Ollama llms in langchain
from langchain_core.prompts import ChatPromptTemplate # crafts prompts for our llm
from langchain_community.chat_message_histories import\
StreamlitChatMessageHistory # stores message history
from langchain_core.tools import tool # tools for our llm
from langchain.tools.render import render_text_description # to describe tools as a string 
from langchain_core.output_parsers import JsonOutputParser # ensure JSON input for tools
from operator import itemgetter # to retrieve specific items in our chain.
from email_sender import EmailSender

# Create a new Ollama instance
model = Ollama(model='llama3')

@tool
def add(first: int, second: int) -> int:
    """Suma dos enteros."""
    return first + second

@tool
def multiply(first: int, second: int) -> int:
    """Multiplica dos enteros."""
    return first * second

@tool
def converse(input: str) -> str:
    "Devuelve una respuesta en lenguaje natural en base al input del usuario."
    return model.invoke(input)

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Envía un correo electrónico."""

    # email_sender = EmailSender(password="Sebbacapo17ikki.", port=587, smtp_server="smtp.gmail.com", username="epache17@gmail.com")
    
    # email_sender.send_email(sender_email="epache17@gmail.com", body=body, receiver_email=to, subject=subject)

    return "Email enviado."

tools = [add, multiply, converse, send_email]
rendered_tools = render_text_description(tools)

system_prompt = f"""Vos sos un asistente que tiene acceso al siguiente conjunto de herramientas.
Aquí están los nombres y descripciones de cada herramienta:
{rendered_tools}
Dado el input del usuario, devuelve el nombre y el input de la herramienta a usar.
Devuelve tu respuesta como un bloque JSON con las claves 'name' y 'arguments'.
El valor asociado con la clave 'arguments' debería ser un diccionario de parámetros."""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{input}")]
)

def tool_chain(model_output):
    tool_map = {tool.name: tool for tool in tools}
    chosen_tool = tool_map[model_output["name"]]
    return itemgetter("arguments") | chosen_tool

chain = prompt | model | JsonOutputParser() | tool_chain

my_prompt = input("User: ")

response = chain.invoke({'input': my_prompt})
print(response)