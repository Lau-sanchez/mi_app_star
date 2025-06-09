import streamlit as st
import openai
import os

# Título de la app
st.title("Creador de Experiencias en Formato STAR ⭐️ con IA 🤖 (Versión con Secrets)")

# Instrucciones
st.write("Paso 1: Cuéntame tu experiencia de manera libre. No te preocupes por el formato. La IA te hará preguntas para ayudarte a estructurarla en formato STAR.")

# Entrada de experiencia libre
experiencia_libre = st.text_area("✍️ Escribe aquí tu experiencia (libre):")

# Obtener API Key desde secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Botón para generar preguntas
if st.button("🤖 Empezar coaching con IA"):
    if experiencia_libre:
        with st.spinner("La IA está generando preguntas... ⏳"):
            # Prompt mejorado
            prompt = f"""
Actúa como coach experto en empleabilidad.

Voy a darte una experiencia profesional o personal que quiero usar como ejemplo en entrevistas.

Tu tarea es:
1️⃣ Leer atentamente la experiencia que te daré.
2️⃣ Hacer todas las preguntas que consideres necesarias para entender bien:
   - La Situación
   - La Tarea
   - Las Acciones
   - Los Resultados

No te limites a 4 preguntas. Formula todas las preguntas que necesites hasta que sientas que tienes un contexto completo y detallado.

Cuando creas que ya tienes suficiente información, avísame y luego genera el ejemplo completo en formato STAR, claro, profesional, en primera persona, listo para usar en entrevistas.

Aquí va la experiencia:
\"\"\"
{experiencia_libre}
\"\"\"

Empecemos: primero hazme tus preguntas.
"""

            # Llamada a la API de OpenAI
            client = openai.OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model="gpt-4o",  # Si da error, cambiar a "gpt-3.5-turbo"
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7,
            )

            # Obtener respuesta de la IA
            respuesta_ia = response.choices[0].message.content

            # Mostrar resultado
            st.subheader("📝 Respuesta de la IA:")
            st.write(respuesta_ia)

    else:
        st.warning("Por favor escribe primero tu experiencia.")
