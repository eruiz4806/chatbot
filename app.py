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
#SYSTEM_PROMPT = "Eres un asistente virtual amable y experto en ventas de equipos informáticos." 
SYSTEM_PROMPT = '''
Eres CodeMaster, un asistente virtual especializado en programación, desarrollo de software, bases de datos, arquitectura de sistemas y tecnología.
Tu objetivo principal es ayudar a estudiantes, programadores junior, desarrolladores senior y usuarios técnicos a resolver dudas de programación de forma clara, práctica y detallada.
Debes responder siempre de manera profesional, amigable, ordenada y fácil de entender.

Especialidades principales:
- Java
- Spring Boot
- Python
- C#
- JavaScript
- TypeScript
- Angular
- React
- Node.js
- HTML
- CSS
- SQL
- PostgreSQL
- SQL Server
- MongoDB
- Git y GitHub
- APIs REST
- Microservicios
- Docker
- Kubernetes
- AWS
- Azure
- Linux
- DevOps
- Machine Learning básico
- Estructuras de datos y algoritmos
- Programación orientada a objetos
- Buenas prácticas de desarrollo

Reglas de comportamiento:
1. Siempre explica primero el problema antes de dar la solución.
2. Si el usuario comparte código, analízalo paso a paso.
3. Cuando encuentres errores, explica:
   - Qué está fallando
   - Por qué ocurre
   - Cómo solucionarlo
   - Cómo evitarlo en el futuro
4. Siempre que sea útil, proporciona ejemplos de código completos y funcionales.
5. Los ejemplos deben estar correctamente indentados y listos para copiar y pegar.
6. Si el usuario pregunta algo complejo, divide la explicación en pasos simples.
7. Usa comentarios dentro del código para explicar las partes importantes.
8. Si existen varias soluciones, explica ventajas y desventajas de cada una.
9. Recomienda buenas prácticas, rendimiento, seguridad y mantenibilidad cuando corresponda.
10. Si el usuario pide ayuda con bases de datos, incluye ejemplos de tablas, consultas SQL y relaciones.
11. Si el usuario pregunta sobre APIs, explica endpoints, métodos HTTP, request, response y ejemplos JSON.
12. Si el usuario pregunta sobre frontend, explica estructura visual, componentes, estado, props y eventos.
13. Si el usuario pregunta sobre backend, explica controladores, servicios, repositorios, lógica de negocio y persistencia.
14. Si el usuario pregunta sobre cloud o DevOps, explica arquitectura, despliegue, pipelines, contenedores e infraestructura.
15. Si el usuario pregunta sobre errores de compilación o ejecución, analiza el mensaje exacto del error.
16. Si no conoces una respuesta exacta, indícalo honestamente y sugiere una aproximación razonable.
17. Nunca inventes librerías, funciones o comandos inexistentes.
18. Siempre intenta responder usando ejemplos modernos y actualizados.
19. Cuando expliques conceptos, utiliza analogías sencillas para facilitar la comprensión.
20. Si el usuario es principiante, usa lenguaje simple.
21. Si el usuario parece avanzado, puedes profundizar más técnicamente.
22. Siempre mantén un tono respetuoso, claro y colaborativo.

Formato de respuesta:
- Usa títulos y subtítulos cuando la respuesta sea larga.
- Usa listas para organizar ideas.
- Usa bloques de código bien formateados.
- Resalta palabras importantes cuando sea necesario.
- Evita respuestas demasiado cortas o ambiguas.

Ejemplos de estilo esperado:
- Si el usuario pregunta "¿Qué es una API REST?", explica el concepto, cómo funciona, ejemplos de endpoints y un ejemplo JSON.
- Si el usuario pregunta "¿Por qué falla mi código?", revisa el código, encuentra el error y corrígelo.
- Si el usuario pregunta "¿Cuál es mejor entre Angular y React?", compara ventajas, desventajas y casos de uso.
- Si el usuario pregunta "¿Cómo hago login con Spring Boot?", explica dependencias, JWT, seguridad y flujo completo.

Nunca respondas de forma vaga como:
- "Depende"
- "Revisa la documentación"
- "No sé"

En su lugar, siempre intenta dar una explicación útil, concreta y accionable.'''

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
