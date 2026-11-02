import streamlit as st
import json
import google.generativeai as genai

# Streamlit lee automáticamente la clave desde .streamlit/secrets.toml
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def generar_jornada_ia(nivel, focos):
    # Usar directamente el modelo recomendado por la API
    modelo = genai.GenerativeModel('gemini-3.8-flash')
    
    prompt = f"""
    Eres un simulador avanzado de habilidades directivas. Genera un escenario de trabajo para un nivel de dificultad {nivel} (1=Básico, 3=Alto) enfocado en estas dimensiones: {', '.join(focos)}.
    
    Debes responder ÚNICAMENTE con un objeto JSON válido con esta estructura exacta, sin texto adicional ni bloques de código markdown:
    {{
        "contexto": {{"puesto": "Nombre del puesto directivo"}},
        "agenda": [
            {{"id": 1, "tarea": "Descripción de tarea operativa", "urgente": false}},
            {{"id": 2, "tarea": "Descripción de tarea estratégica", "urgente": true}},
            {{"id": 3, "tarea": "Descripción de tarea delegable", "urgente": false}}
        ],
        "eventos": [
            {{"hora": "10:30", "descripcion": "Descripción de un evento inesperado o interrupción"}}
        ]
    }}
    """
    
    try:
        respuesta = modelo.generate_content(prompt)
        texto_limpio = respuesta.text.strip().replace("```json", "").replace("```", "")
        return json.loads(texto_limpio)
    except Exception as e:
        st.error(f"Error al procesar la respuesta de la IA. Detalles: {e}")
        return None
def evaluar_decisiones_ia(escenario, decisiones):
    modelo = genai.GenerativeModel('gemini-3.8-flash')
    
    prompt = f"""
    Actúa como un coach experto en habilidades directivas.
    Aquí está el escenario al que se enfrentó el directivo: {json.dumps(escenario)}
    Aquí están las decisiones que tomó y sus justificaciones: {json.dumps(decisiones)}
    
    Analiza brevemente sus decisiones considerando la urgencia y el tipo de tarea. 
    Redacta una retroalimentación constructiva de máximo 2 párrafos y asigna una calificación final sobre 100 puntos.
    """
    
    try:
        respuesta = modelo.generate_content(prompt)
        return respuesta.text
    except Exception as e:
        return f"Error al generar la evaluación: {e}"

    # 2. Usar el modelo encontrado
    modelo = genai.GenerativeModel(modelo_disponible)
    
    prompt = f"""
    Eres un simulador avanzado de habilidades directivas. Genera un escenario de trabajo para un nivel de dificultad {nivel} (1=Básico, 3=Alto) enfocado en estas dimensiones: {', '.join(focos)}.
    
    Debes responder ÚNICAMENTE con un objeto JSON válido con esta estructura exacta, sin texto adicional ni bloques de código markdown:
    {{
        "contexto": {{"puesto": "Nombre del puesto directivo"}},
        "agenda": [
            {{"id": 1, "tarea": "Descripción de tarea operativa", "urgente": false}},
            {{"id": 2, "tarea": "Descripción de tarea estratégica", "urgente": true}},
            {{"id": 3, "tarea": "Descripción de tarea delegable", "urgente": false}}
        ],
        "eventos": [
            {{"hora": "10:30", "descripcion": "Descripción de un evento inesperado o interrupción"}}
        ]
    }}
    """
    
    try:
        respuesta = modelo.generate_content(prompt)
        texto_limpio = respuesta.text.strip().replace("```json", "").replace("```", "")
        return json.loads(texto_limpio)
    except Exception as e:
        st.error(f"Error al procesar la respuesta de la IA. Detalles: {e}")
        return None

def renderizar():
    c1, c2 = st.columns(2)
    nivel = c1.select_slider("Nivel de dificultad", [1, 2, 3])
    focos = c2.multiselect("Focos a entrenar", ["Delegación", "Interrupciones", "Micro-management"], default=["Delegación"])

    if st.button("Generar Jornada con IA", type="primary"):
        with st.spinner("Gemini está construyendo tu escenario a la medida..."):
            escenario = generar_jornada_ia(nivel, focos)
            if escenario:
                st.session_state.escenario = escenario
                st.session_state.decisiones = {}

    if "escenario" in st.session_state:
        escenario = st.session_state.escenario
        st.divider()
        st.subheader(f"Rol asignado: {escenario['contexto']['puesto']}")
        
        for ev in escenario.get("eventos", []):
            st.error(f"🚨 **Interrupción a las {ev['hora']}** - {ev['descripcion']}")

        st.write("**Bandeja de Entrada (Agenda)**")
        for item in escenario.get("agenda", []):
            urgencia_label = "🔥 Urgente" if item.get('urgente') else "📅 Normal"
            st.write(f"📌 {item['tarea']} ({urgencia_label})")
            
            ca, cb = st.columns([1, 2])
            accion = ca.selectbox("Acción", ["Hacer ahora", "Programar", "Delegar", "Ignorar"], key=f"acc_{item['id']}")
            justificacion = cb.text_input("Justifica tu decisión directiva:", key=f"just_{item['id']}")
            st.session_state.decisiones[item['id']] = {"accion": accion, "justificacion": justificacion}
            st.write("---")

        if st.button("Evaluar mis decisiones", type="primary"):
            with st.spinner("El coach IA está analizando tus justificaciones..."):
                feedback = evaluar_decisiones_ia(st.session_state.escenario, st.session_state.decisiones)
                st.success("**Retroalimentación del Coach IA**")
                st.write(feedback)