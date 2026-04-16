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

MAX_HISTORY = 30
st.session_state.chat_history = st.session_state.chat_history[-MAX_HISTORY:]

MODEL_NAME = "llama-3.1-8b-instant"
TEMPERATURE = 0.7
SYSTEM_PROMPT = "Eres un asistente virtual amable y experto en ventas de equipos informáticos." 

st.title(" 🤖 Chatbot de La Casita Informática - Demo") 
st.write("Hola soy Vicky, en qué puedo ayudarte?") 

for msg in st.session_state.chat_history: 
    with st.chat_message(msg["role"]): 
        st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")
        #st.markdown(msg["content"])

user_input = st.chat_input("Escribe aquí...") 

if user_input: 
    # Mostrar el mensaje del usuario 
    st.session_state.chat_history.append({"role": "user", "content": user_input}) 
    with st.chat_message("user"): 
        st.markdown(user_input) 
    # Construir mensajes para el modelo 
    messages = [] 
    if SYSTEM_PROMPT: 
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
        messages.extend(st.session_state.chat_history)  

    # Llamar a la API **solo** si hay user_input (evita NameError)     
    try:         
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
        )         
        respuesta_texto = response.choices[0].message.content  # objeto, no dict     
    except Exception as e:         
        respuesta_texto = f"Lo siento, ocurrió un error al llamar a la API: `{e}`"      
    # Mostrar respuesta del asistente     
    with st.chat_message("assistant"):         
        st.markdown(respuesta_texto)      
    
    # Guardar en historial     
    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_texto})
