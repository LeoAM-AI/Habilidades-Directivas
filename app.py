import streamlit as st
import diagnostico
import simulador
import dashboard

st.set_page_config(page_title="Habilidades Directivas UP", layout="wide", initial_sidebar_state="expanded")

def renderizar_perfil():
    st.title("👤 Perfil del Directivo")
    st.write("Configura tu perfil para personalizar la experiencia del diagnóstico y el simulador de IA.")

    # Inicializar variables en session_state si no existen
    if "usuario" not in st.session_state:
        st.session_state.usuario = {
            "nombre": "",
            "rol": "Gerente de Operaciones",
            "tamano_equipo": 5,
            "experiencia": "Intermedio"
        }

    with st.form("form_perfil"):
        nombre = st.text_input("Nombre completo:", value=st.session_state.usuario["nombre"])
        rol = st.text_input("Puesto o Rol directivo:", value=st.session_state.usuario["rol"])
        tamano_equipo = st.number_input("Tamaño del equipo a cargo:", min_value=0, max_value=500, value=st.session_state.usuario["tamano_equipo"])
        
        # Selección segura de índice
        opciones_exp = ["Junior (0-2 años)", "Intermedio (3-5 años)", "Senior (6+ años)"]
        exp_guardada = st.session_state.usuario.get("experiencia_label", "Intermedio (3-5 años)")
        idx_exp = opciones_exp.index(exp_guardada) if exp_guardada in opciones_exp else 1

        experiencia = st.selectbox(
            "Nivel de experiencia directiva:",
            opciones_exp,
            index=idx_exp
        )
        
        guardar = st.form_submit_button("Guardar Perfil", type="primary")
        
        if guardar:
            st.session_state.usuario = {
                "nombre": nombre,
                "rol": rol,
                "tamano_equipo": tamano_equipo,
                "experiencia_label": experiencia
            }
            st.success("¡Perfil actualizado con éxito! La IA adaptará las simulaciones a tu puesto.")

    # Mostrar tarjeta con datos guardados
    if st.session_state.usuario["nombre"]:
        st.divider()
        st.info(f"**Usuario activo:** {st.session_state.usuario['nombre']} | **Rol:** {st.session_state.usuario['rol']} | **Equipo:** {st.session_state.usuario['tamano_equipo']} personas")

# Barra lateral de navegación
st.sidebar.title("Navegación")
menu = ["1. Perfil", "2. Diagnóstico de Tiempo", "3. Simulador IA", "4. Panel Admin"]
seleccion = st.sidebar.radio("Módulos", menu)

# Control de vistas
if seleccion == "1. Perfil": 
    renderizar_perfil()

elif seleccion == "2. Diagnóstico de Tiempo":
    st.title("Diagnóstico Profundo")
    diagnostico.renderizar()

elif seleccion == "3. Simulador IA":
    st.title("Simulador: Jornada Directiva")
    simulador.renderizar()

elif seleccion == "4. Panel Admin":
    st.title("Panel Administrador")
    c1, c2 = st.columns(2)
    c1.metric("Usuarios Activos", "32")
    c2.metric("Mejora Promedio (SJT)", "+15 pts")
    
    st.divider()
    dashboard.mostrar_radar()