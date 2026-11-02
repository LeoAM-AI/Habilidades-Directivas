import streamlit as st

banco_reactivos = {
    "Delegacion": {
        "autoevaluacion": [
            {"id": 9, "texto": "Identifico qué actividades pueden realizar otras personas.", "inverso": False},
            {"id": 10, "texto": "Al delegar, explico el resultado esperado, el plazo y el nivel de autoridad.", "inverso": False},
            {"id": 11, "texto": "Cuando alguien me trae un problema que puede resolver, le pido que proponga una solución.", "inverso": False},
            {"id": 12, "texto": "Prefiero hacer las cosas yo mismo porque así salen mejor o más rápido.", "inverso": True}
        ],
        "conocimientos": [
            {"id": 5, "texto": "En el artículo de Oncken y Wass (1974), ¿qué representa el 'mono'?", "opciones": ["El siguiente paso...", "Un colaborador...", "Una tarea...", "Una junta..."], "respuesta_correcta": 0},
            {"id": 6, "texto": "¿Qué elementos debe incluir una instrucción eficaz?", "opciones": ["El procedimiento...", "La fecha...", "El resultado, plazo y autoridad.", "La supervisión..."], "respuesta_correcta": 2}
        ],
        "juicio_situacional": [
            {"id": 5, "texto": "Debes entregar un reporte estratégico y un colaborador te pide ayuda...", "opciones": [{"texto": "Lo resuelves tú.", "puntos": 0}, {"texto": "Le explicas paso a paso.", "puntos": 1}, {"texto": "Le pides que proponga una solución.", "puntos": 3}, {"texto": "Lo turnas a otro.", "puntos": 1}]}
        ]
    }
}

def calcular_dimension(respuestas_auto, aciertos_conocimiento, puntos_juicio):
    a = ((sum(respuestas_auto) - 4) / 16) * 100
    c = (aciertos_conocimiento / 2) * 100
    s = (puntos_juicio / 6) * 100
    nd = (0.50 * s) + (0.25 * c) + (0.25 * a)
    ba = a - s 
    
    clasificacion = "Fortaleza" if nd >= 75 else "En desarrollo" if nd >= 50 else "Prioritaria"
    sobreestimada = ba > 20
    if sobreestimada and clasificacion == "En desarrollo":
        clasificacion = "Prioritaria"
        
    return {"A": round(a,1), "C": round(c,1), "S": round(s,1), "ND": round(nd,1), "Clasificacion": clasificacion, "Sobreestimada": sobreestimada}

def renderizar():
    if 'puntos_auto' not in st.session_state: st.session_state.puntos_auto = [0]*4
    if 'aciertos_con' not in st.session_state: st.session_state.aciertos_con = [0]*2
    if 'puntos_sjt' not in st.session_state: st.session_state.puntos_sjt = [0]*1
    
    st.header("1. Autoevaluación Conductual")
    for i, reactivo in enumerate(banco_reactivos["Delegacion"]["autoevaluacion"]):
        val = st.slider(f"Q{i+1}: {reactivo['texto']}", 1, 5, 3, key=f"auto_{i}")
        st.session_state.puntos_auto[i] = (6 - val) if reactivo['inverso'] else val

    st.header("2. Verificación de Conocimientos")
    for i, preg in enumerate(banco_reactivos["Delegacion"]["conocimientos"]):
        opcion = st.radio(preg['texto'], preg['opciones'], key=f"con_{i}")
        st.session_state.aciertos_con[i] = 1 if preg['opciones'].index(opcion) == preg['respuesta_correcta'] else 0

    st.header("3. Prueba de Juicio Situacional")
    for i, caso in enumerate(banco_reactivos["Delegacion"]["juicio_situacional"]):
        opciones_texto = [op['texto'] for op in caso['opciones']]
        opcion = st.radio(caso['texto'], opciones_texto, key=f"sjt_{i}")
        st.session_state.puntos_sjt[i] = caso['opciones'][opciones_texto.index(opcion)]['puntos']

    if st.button("Calcular mi Perfil", type="primary"):
        resultados = calcular_dimension(st.session_state.puntos_auto, sum(st.session_state.aciertos_con), sum(st.session_state.puntos_sjt))
        
        # --- INICIALIZAR Y GUARDAR RESULTADOS EN SESSION_STATE PARA EL RADAR ---
        if "puntajes" not in st.session_state:
            st.session_state.puntajes = {
                'Delegación': 50,
                'Gestión del Tiempo': 65,
                'Comunicación': 80,
                'Liderazgo': 70,
                'Resolución de Conflictos': 75,
                'Inteligencia Emocional': 85
            }
        
        # Actualizamos la dimensión calculada con su valor real (ND)
        st.session_state.puntajes['Delegación'] = resultados['ND']

        # Muestra de métricas
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Autoevaluación (A)", resultados['A'])
        c2.metric("Conocimientos (C)", resultados['C'])
        c3.metric("Juicio (S)", resultados['S'])
        c4.metric("Nivel (ND)", resultados['ND'])
        
        st.info(f"Clasificación: **{resultados['Clasificacion']}**")
        st.success("¡Puntaje guardado! Ve al **Panel Admin** para ver el radar actualizado.")