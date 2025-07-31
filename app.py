import streamlit as st
import google.generativeai as genai

# --- 1. Configuración de la página ---
st.set_page_config(page_title="Asesor de Compra de Autos con IA", layout="wide")

st.title("🚗 Asesor de Compra de Autos con IA")
st.markdown("¡Hola! Soy tu asistente personal de compra de autos. Estoy aquí para ayudarte a tomar la mejor decisión.")
st.markdown("Puedes preguntarme sobre modelos, hacer comparativas o pedir recomendaciones. Utilizo el vasto conocimiento de la IA para darte respuestas precisas y actualizadas.")

# --- 2. Conectar con la API de Gemini ---
try:
    # La clave de la API de Gemini se obtiene de los secretos de Streamlit
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except KeyError:
    st.error("Error: La clave de la API de Google (Gemini) no está configurada en los secretos de Streamlit.")
    st.stop()

# --- 3. Función para hacer la consulta a la IA ---
def consultar_ia(prompt_del_usuario):
    """
    Función que envía la consulta del usuario a la IA y devuelve la respuesta.
    Utiliza un prompt de sistema para guiar el comportamiento de la IA.
    """
    try:
        # Intenta usar un modelo con alta disponibilidad
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # El prompt del sistema define el rol y las tareas de la IA
        system_prompt = """
        Eres un experto en automoción. Tu objetivo es asesorar a un cliente en la compra de un auto.
        Debes ser útil, objetivo y proporcionar información clara. Puedes hacer comparaciones entre
        diferentes modelos, dar recomendaciones basadas en las necesidades del cliente (como tamaño,
        consumo de combustible, precio, etc.) y crear listas o tablas comparativas. 
        Tu información debe ser precisa y actualizada hasta donde alcance tu conocimiento.
        Si la información no está disponible, indícalo de manera educada.
        """
        
        # Combinamos el prompt del sistema y la pregunta del usuario
        full_prompt = f"{system_prompt}\n\nPregunta del usuario: {prompt_del_usuario}"
        
        # Hacemos la llamada a la API
        response = model.generate_content(full_prompt)
        
        # Devolvemos el texto de la respuesta
        return response.text

    except Exception as e:
        # Manejo de errores en caso de que la API falle
        error_msg = f"Ocurrió un error al contactar con la IA: {e}"
        # Puedes imprimir el error en la consola de Streamlit para depuración
        print(error_msg) 
        st.error(f"Ocurrió un error al contactar con la IA. Por favor, inténtalo de nuevo más tarde. ({e})")
        return None

# --- 4. Interfaz de usuario (UI) ---
# Campo de texto para la interacción con el usuario
pregunta = st.text_area(
    "¿En qué puedo ayudarte hoy?", 
    height=100, 
    placeholder="Ejemplo: 'Compara el Toyota Corolla 2024 y el Honda Civic 2024. Haz una tabla con sus pros y contras.'"
)

# Botón para enviar la consulta
if st.button("Obtener Asesoría"):
    if pregunta:
        # Muestra un spinner mientras la IA procesa la solicitud
        with st.spinner("Buscando la mejor información para ti..."):
            respuesta_ia = consultar_ia(pregunta)
            if respuesta_ia:
                # Si se obtiene una respuesta, la muestra
                st.markdown("---")
                st.subheader("Tu Asesoría:")
                st.markdown(respuesta_ia)
    else:
        # Advertencia si el usuario no ha escrito nada
        st.warning("Por favor, escribe tu pregunta en el cuadro de texto.")
