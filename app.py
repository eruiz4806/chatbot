import os 
import streamlit as st 
from groq import Groq 
from dotenv import load_dotenv 

st.set_page_config(page_title="Chatbot con IA", page_icon=" 💬 ", layout="centered") 

# Cargar la API key de forma segura 
try: 
    load_dotenv()  # Carga variables desde .env si existe (entorno local) 
    API_KEY = os.getenv("GROQ_API_KEY")  #para Groq; usar "OPENAI_API_KEY" si es OpenAI 
except: 
    API_KEY = st.secrets["GROQ_API_KEY"]

os.environ["GROQ_API_KEY"] = API_KEY 
client = Groq()  # Cliente para invocar la API de Groq

# Inicializar el historial de chat en la sesión 
if "chat_history" not in st.session_state: 
    st.session_state.chat_history = []  # lista de dicts: {"role": ..., "content": ...}

SYSTEM_PROMPT = "Eres un asistente virtual amable y experto en diversos temas." 

st.title(" 🤖 Chatbot IA - Demo") 
st.write("Puedes hacer preguntas y el chatbot responderá usando un modelo de lenguaje.") 
