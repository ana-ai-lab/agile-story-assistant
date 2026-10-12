import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="User Story & Acceptance Criteria Assistant", page_icon="🧭", layout="wide")
st.title("User Story & Acceptance Criteria Assistant")
st.caption("Convierte ideas de negocio vagas en historias, criterios de aceptación y dependencias para refinamiento de backlog.")

ROLES = [
    "Sin rol específico",
    "Product Owner",
    "Scrum Master",
    "Business Analyst",
    "Consultor de Transformación",
]

if "request_text" not in st.session_state:
    st.session_state.request_text = ""
if "selected_role" not in st.session_state:
    st.session_state.selected_role = ROLES[0]
if "generated_result" not in st.session_state:
    st.session_state.generated_result = ""

with st.form("story_form"):
    request_text = st.text_area(
        "Solicitud o idea de negocio",
        key="request_text",
        height=180,
        placeholder="Ejemplo: Quiero que solo los administradores puedan descargar reportes de ventas para reducir riesgo de información sensible.",
    )
    selected_role = st.selectbox(
        "Rol (opcional)",
        options=ROLES,
        index=ROLES.index(st.session_state.selected_role),
        help="Se usa como contexto para redactar la historia, pero no es obligatorio.",
    )
    st.session_state.selected_role = selected_role
    submitted = st.form_submit_button("Generar historia")

if submitted:
    if not request_text.strip():
        st.warning("Escribe una solicitud o idea de negocio antes de generar la historia.")
    else:
        st.success("Listo para generar la historia a partir de la solicitud actual.")
        st.markdown("### Resultado")
        st.markdown(f"**Solicitud original:** {request_text}")
        st.markdown(f"**Rol seleccionado:** {selected_role}")
        st.info("La historia estructurada, los criterios Gherkin y las dependencias se mostrarán aquí una vez que se conecte el generador.")

else:
    st.markdown("### Resultado")
    st.info("Ingresa una solicitud y presiona 'Generar historia' para comenzar.")
