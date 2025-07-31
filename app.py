import streamlit as st
import pandas as pd
import google.generativeai as genai  # Importar la biblioteca de Google

# --- Estructura del resto de la app (se mantiene igual) ---
st.set_page_config(page_title="Asesor de Compra de Autos", layout="wide")
st.title("🚗 Asesor de Compra de Autos con IA (Gemini)")
st.write("¡Hola! Estoy aquí para ayudarte a encontrar el auto perfecto para ti.")

try:
    df_autos = pd.read_csv('autos.csv')
except FileNotFoundError:
    st.error("Error: Archivo 'autos.csv' no encontrado.")
    st.stop()

# --- CAMBIO CLAVE: Conectar con la API de Gemini ---
try:
    # La clave de la API de Gemini se obtiene de los secretos de Streamlit
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except KeyError:
    st.error("Error: La clave de la API de Google (Gemini) no está configurada en los secretos de Streamlit.")
    st.stop()

# Inicializa el modelo de Gemini
model = genai.GenerativeModel('gemini-pro')

# --- CAMBIO CLAVE: Función para hacer la consulta a Gemini ---
def consultar_ia(prompt_del_usuario):
    """
    Función que envía la consulta del usuario a Gemini y devuelve la respuesta.
    """
    # Se inyecta el contexto de los datos en el prompt.
    datos_para_ia = df_autos.to_string()
    
    # Este es el prompt que se envía a la IA.
    system_prompt = f"""
    Eres un experto en automoción. Tu objetivo es asesorar a un cliente en la compra de un auto.
    Debes ser útil, objetivo y proporcionar información clara. Puedes hacer comparaciones,
    dar recomendaciones y crear listas o tablas. Usa los siguientes datos como referencia:
    {datos_para_ia}
    """
    
    # La forma de enviar el prompt a Gemini es un poco diferente
    full_prompt = f"{system_prompt}\n\nPregunta del usuario: {prompt_del_usuario}"
    
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"Ocurrió un error al contactar con la IA: {e}")
        return "Lo siento, no pude procesar tu solicitud en este momento."

# --- El resto de la UI (Interfaz de Usuario) se mantiene igual ---
with st.sidebar:
    st.header("Opciones y filtros")
    marcas = df_autos['Marca'].unique()
    marca_seleccionada = st.selectbox("Filtrar por marca", ["Todas"] + list(marcas))

    if marca_seleccionada != "Todas":
        st.write(df_autos[df_autos['Marca'] == marca_seleccionada])

pregunta = st.text_area("¿En qué puedo ayudarte hoy?", height=100, placeholder="Ejemplo: 'Compara el Toyota Corolla y el Honda Civic'")

if st.button("Obtener Asesoría"):
    if pregunta:
        with st.spinner("Pensando..."):
            respuesta_ia = consultar_ia(pregunta)
            st.markdown("---")
            st.subheader("Tu Asesoría:")
            st.write(respuesta_ia)
    else:
        st.warning("Por favor, escribe tu pregunta.")