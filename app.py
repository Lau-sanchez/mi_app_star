import streamlit as st
import openai

# Título
st.title("👩‍💻 Tu experiencia en Formato STAR ⭐️ con IA 🤖")

# Instrucciones iniciales
st.markdown("""
**👋 Bienvenida**

Cuéntame tu experiencia de forma libre. La IA te ayudará a convertirla al formato STAR y luego te hará preguntas para mejorarla.
""")

# Entrada de experiencia (única caja de texto)
experiencia = st.text_area(
    "✍️ Escribe tu experiencia como si se la contaras a una amiga. Dale detalles del nombre de tu rol, en dónde trabajaste, qué hiciste durante ese tiempo y qué resultados lograste. No dudes en ser detallada, eso ayudará a la calidad de tu respuesta.",
    height=350
)

# Obtener API key
api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=api_key)

# Paso 1: Generar primera versión STAR
if st.button("🪄 Ver versión en formato STAR"):
    if experiencia:
        with st.spinner("Generando primera versión..."):
            prompt_star = f"""
Actúa como un experto en empleabilidad. Recibirás una experiencia escrita libremente.

Tu tarea es transformarla en una respuesta en formato STAR clara, profesional y lista para entrevista.

Sigue estas instrucciones:
1. Estructura la respuesta en **Situación**, **Tarea**, **Acciones** (formato de viñetas, mínimo 60% del texto) y **Resultados** (con datos numéricos si es posible).
2. Usa lenguaje profesional, en primera persona.

Aquí está la experiencia:
\"\"\"
{experiencia}
\"\"\"

Devuélveme únicamente el texto en formato STAR.
"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt_star}],
                max_tokens=1200,
                temperature=0.7,
            )

            resultado = response.choices[0].message.content
            st.session_state["experiencia"] = resultado
            st.session_state["fase"] = "generado"

# Mostrar STAR generado en la misma caja
if st.session_state.get("fase") == "generado":
    st.subheader("📄 Tu experiencia en formato STAR:")
    experiencia_actualizada = st.text_area(
        "📝 Puedes editar directamente aquí o agregar información nueva",
        value=st.session_state["experiencia"],
        height=400
    )
    st.session_state["experiencia"] = experiencia_actualizada

# Paso 2: Mejorar con preguntas
if st.session_state.get("experiencia") and st.button("🔍 Mejorar versión con preguntas"):
    with st.spinner("La IA está generando preguntas de mejora..."):
        prompt_preguntas = f"""
Aquí tienes una experiencia ya escrita en formato STAR. Tu tarea es hacer entre 3 y 5 preguntas específicas para mejorar esta historia. Evita preguntas genéricas.

Texto STAR:
\"\"\"
{st.session_state["experiencia"]}
\"\"\"
"""

        response2 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_preguntas}],
            max_tokens=800,
            temperature=0.7,
        )

        preguntas = response2.choices[0].message.content

        st.subheader("🤖 Preguntas para mejorar tu historia:")
        st.markdown(preguntas)

        st.info("✍️ Responde directamente dentro del cuadro de texto donde está tu experiencia. Puedes agregar tus respuestas donde mejor encajen.")

