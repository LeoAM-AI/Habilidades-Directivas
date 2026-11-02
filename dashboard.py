import streamlit as st
import plotly.graph_objects as go

def mostrar_radar():
    st.subheader("Radar Directivo: Perfil de Habilidades")
    st.write("Balance actual de tus competencias clave basado en el diagnóstico.")

    categorias = ['Delegación', 'Gestión del Tiempo', 'Comunicación', 
                  'Liderazgo', 'Resolución de Conflictos', 'Inteligencia Emocional']
    
    # 1. Leer puntajes reales desde session_state si existen
    if "puntajes" in st.session_state:
        puntajes_dict = st.session_state.puntajes
        puntajes = [puntajes_dict.get(cat, 0) for cat in categorias]
        st.success("📊 Mostrando resultados actualizados de tu diagnóstico real.")
    else:
        # Valores por defecto de ejemplo antes de realizar el diagnóstico
        puntajes = [50, 50, 50, 50, 50, 50] 
        st.warning("⚠️ Aún no has completado el diagnóstico. Mostrando valores base de demostración.")

    # 2. Cerrar el polígono de Plotly
    cat_cierre = categorias + [categorias[0]]
    pts_cierre = puntajes + [puntajes[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=pts_cierre,
        theta=cat_cierre,
        fill='toself',
        name='Tu Perfil',
        line_color='#FF4B4B',
        fillcolor='rgba(255, 75, 75, 0.2)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)