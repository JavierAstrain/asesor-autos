import streamlit as st
import google.generativeai as genai  # Para usar Gemini
# O: import openai as OpenAI          # Para usar OpenAI

# 1. Configuración de la página
st.set_page_config(page_title="Asesor de Compra de Autos con IA", layout="wide")

st.title("🚗 Asesor de Compra de Autos con IA (Gemini)")
st.write("¡Hola! Estoy aquí para ayudarte a encontrar el auto perfecto para ti. Puedes preguntarme sobre modelos, hacer comparativas o pedir recomendaciones. No necesito una base de datos, ¡la IA lo sabe todo!")

# 2. Conectar con la API de Gemini
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except KeyError:
    st.error("Error: La clave de la API de Google (Gemini) no está configurada en los secretos de Streamlit.")
    st.stop()

# 3. Función para hacer la consulta a la IA (simplificada)
def consultar_ia(prompt_del_usuario):
    """
    Función que envía la consulta del usuario a la IA y devuelve la respuesta.
    """
    # El prompt ahora no incluye datos de un CSV. Solo instrucciones.
    system_prompt = """
    Eres un experto en automoción. Tu objetivo es asesorar a un cliente en la compra de un auto.
    Debes ser útil, objetivo y proporcionar información clara. Puedes hacer comparaciones entre
    diferentes modelos, dar recomendaciones basadas en necesidades específicas del cliente (como tamaño,
    consumo de combustible, precio, etc.) y crear listas o tablas comparativas. 
    Tu información debe ser precisa y actualizada hasta donde alcance tu conocimiento.
    """
    
    full_prompt = f"{system_prompt}\n\nPregunta del usuario: {prompt_del_usuario}"
    
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"Ocurrió un error al contactar con la IA: {e}")
        return "Lo siento, no pude procesar tu solicitud en este momento."

# 4. Interfaz de usuario (UI)
# En este enfoque, no necesitas un sidebar para filtrar datos, ya que no tienes una base de datos local.
# Puedes eliminar la parte del sidebar si ya no la necesitas.
# with st.sidebar:
#     st.header("Opciones")
#     st.write("No hay filtros disponibles, la IA tiene el conocimiento.")

pregunta = st.text_area(
    "¿En qué puedo ayudarte hoy?", 
    height=100, 
    placeholder="Ejemplo: 'Compara el Toyota Corolla 2024 y el Honda Civic 2024. Haz una tabla con sus pros y contras.'"
)

if st.button("Obtener Asesoría"):
    if pregunta:
        with st.spinner("Buscando la mejor información para ti..."):
            respuesta_ia = consultar_ia(pregunta)
            st.markdown("---")
            st.subheader("Tu Asesoría:")
            st.write(respuesta_ia)
    else:
        st.warning("Por favor, escribe tu pregunta.")
