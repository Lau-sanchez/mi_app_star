import streamlit as st
import openai

# Título
st.title("🧠 Cuenta tus experiencia sen formato STAR - Asistente IA")

# Instrucciones iniciales
st.markdown("""
**👋 Bienvenida**

Cuéntame tu experiencia de forma libre, la IA te ayudará a convertirla al formato STAR y hacer mejoras.
""")

# Paso 1: Entrada libre
experiencia_libre = st.text_area(
    "✍️ Escribe tu experiencia como si se la contaras a una amiga. Dale detalles del nombre de tu rol, en dónde trabajaste, qué hiciste durante ese tiempo y qué resultados lograste. No dudes en ser detallada, eso ayudará a la calidad de tu respuesta."
)


# Obtener API key
api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=api_key)

# Paso 2: Generar primer STAR
if st.button("🪄 Ver versión en formato STAR"):
    if experiencia_libre:
        with st.spinner("Generando primera versión..."):
            prompt_star = f"""
Actúa como un experto en empleabilidad. Recibirás una experiencia escrita libremente.

Tu tarea es transformar esa experiencia en una respuesta en formato STAR clara, profesional y lista para entrevista.

Sigue estas instrucciones:

1. Estructura la respuesta en cuatro secciones: **Situación**, **Tarea**, **Acciones** y **Resultados**.
2. En la sección **Acciones**, escribe en formato de viñetas (bullet points). Esta sección debe ser la más extensa (al menos el 60% del total).
3. En la sección **Resultados**, incluye números o datos cuantitativos concretos si están presentes en la experiencia o si se pueden inferir a partir del contexto.
4. Usa lenguaje profesional en primera persona, claro y directo.

Aquí está la experiencia:
\"\"\"
{experiencia_libre}
\"\"\"

Devuélveme únicamente el texto en formato STAR.
"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt_star}],
                max_tokens=1200,
                temperature=0.7,
            )

            respuesta_inicial = response.choices[0].message.content
            st.subheader("📄 Primera versión STAR:")
            st.write(respuesta_inicial)

            st.session_state["respuesta_inicial"] = respuesta_inicial
            st.session_state["experiencia"] = experiencia_libre
    else:
        st.warning("Por favor escribe tu experiencia antes de continuar.")

# Paso 3: Solicitar mejora
if "respuesta_inicial" in st.session_state:
    if st.button("🔍 Mejorar versión con preguntas"):
        with st.spinner("La IA está generando preguntas de seguimiento..."):
            prompt_preguntas = f"""
A continuación recibirás una experiencia ya organizada en formato STAR. 
Tu tarea ahora es hacer preguntas concretas para poder mejorarla. 
Evita preguntas genéricas. Haz entre 3 y 5 preguntas específicas que te ayuden a obtener más contexto o detalles relevantes.

Versión inicial STAR:
\"\"\"
{st.session_state["respuesta_inicial"]}
\"\"\"
"""

            response2 = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt_preguntas}],
                max_tokens=800,
                temperature=0.7,
            )

            preguntas_ia = response2.choices[0].message.content
            st.subheader("🤖 Preguntas de la IA para mejorar tu historia:")
            st.write(preguntas_ia)
