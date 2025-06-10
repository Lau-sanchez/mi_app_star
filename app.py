import streamlit as st
import openai

# Título
st.title("👩‍💻 Tu experiencia en Formato STAR ⭐️ con IA 🤖")

# Instrucciones iniciales
st.markdown("""
**👋 Bienvenida**

Cuéntame tu experiencia de forma libre. La IA te ayudará a convertirla al formato STAR y luego te hará preguntas para mejorarla.
""")

# Entrada de experiencia libre
if "experiencia_inicial" not in st.session_state:
    st.session_state["experiencia_inicial"] = ""

st.session_state["experiencia_inicial"] = st.text_area(
    "✍️ Escribe tu experiencia como si se la contaras a una amiga. Dale detalles del nombre de tu rol, en dónde trabajaste, qué hiciste durante ese tiempo y qué resultados lograste. No dudes en ser detallada, eso ayudará a la calidad de tu respuesta.",
    value=st.session_state["experiencia_inicial"],
    height=350
)

# Obtener API key
api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=api_key)

# Paso 1: Generar versión STAR
if st.button("🪄 Ver versión en formato STAR"):
    if st.session_state["experiencia_inicial"]:
        with st.spinner("Generando tu versión STAR..."):
            prompt_star = f"""
Actúa como un experto en empleabilidad. Recibirás una experiencia escrita libremente.

Tu tarea es transformarla en una respuesta en formato STAR clara, profesional y lista para entrevista.

Sigue estas instrucciones:
1. Estructura la respuesta en **Situación** (que nombre la empresa y por qué la tarea era importante), **Tarea** (corta que haga referencia a la principal responsabildiad que fue encargada), **Acciones** (formato de viñetas, mínimo 60% del texto, redactadas en primera persona, nombra metodologías, herramientas y programas utilizados) y **Resultados** (con datos numéricos si es posible y resultados sobre la influencia en los objetivos de la empresa).
2. Usa lenguaje profesional, en primera persona.

Aquí está la experiencia:
\"\"\"
{st.session_state["experiencia_inicial"]}
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
            st.session_state["star_generado"] = resultado
            st.session_state["fase"] = "generado"

# Mostrar STAR generado como texto (no editable)
if st.session_state.get("fase") == "generado":
    st.subheader("📄 Tu experiencia en formato STAR:")
    st.markdown(st.session_state["star_generado"])

# Paso 2: Mejorar con preguntas
if st.session_state.get("fase") == "generado" and st.button("🔍 Mejorar versión con preguntas"):
    with st.spinner("La IA está generando preguntas de mejora..."):
        prompt_preguntas = f"""
Aquí tienes una experiencia ya escrita en formato STAR. Tu tarea es hacer entre 3 y 5 preguntas específicas para mejorar esta historia. Evita preguntas genéricas, incluye al menos 1 pregunta que ayude a identificar herramientas, metodologías o programas usado por la persona en su experiencia y preguntas que le ayuden a identificar resultados cuantificables de su experiencia para la empresa.

Texto STAR:
\"\"\"
{st.session_state["star_generado"]}
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

        st.info("✍️ *Responde directamente dentro del cuadro de texto inicial donde escribiste tu experiencia. No borres lo anterior, solo agrégalo o edítalo para construir una versión más sólida.*")

