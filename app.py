import json
import os
from typing import Any

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover - optional dependency for runtime only
    genai = None


ROLES = [
    "Sin rol específico",
    "Product Owner",
    "Scrum Master",
    "Business Analyst",
    "Consultor de Transformación",
]


def build_prompt(raw_request: str, role: str) -> str:
    role_hint = role if role and role != "Sin rol específico" else "usuario de negocio"
    return f"""
Eres un analista ágil experto en backlog refinement y escritura de historias de usuario.
Quiero que conviertas la siguiente solicitud de negocio en un artefacto listo para refinamiento técnico.

Instrucciones obligatorias:
1. Devuelve una historia de usuario en español y en formato: "Como [rol], quiero [acción], para [beneficio]".
2. Incluye criterios de aceptación en formato Gherkin con escenarios de camino feliz y validación/error cuando corresponda.
3. Añade una sección de dependencias técnicas o suposiciones que deban revisarse antes de la estimación.
4. Añade una sección de preguntas abiertas o decisiones que falten.
5. Mantén la intención original del negocio, sin inventar funcionalidades ajenas.
6. Usa markdown limpio y legible.

Solicitud de negocio:
{raw_request}

Rol sugerido para la historia: {role_hint}
""".strip()


def build_demo_fallback(raw_request: str, role: str) -> dict[str, Any]:
    role_hint = role if role and role != "Sin rol específico" else "usuario de negocio"
    normalized_request = raw_request.strip()
    story = (
        f"Como {role_hint}, quiero transformar una solicitud de negocio ambigua en una historia con criterio claro, "
        "para poder llevarla a refinamiento de backlog sin perder intención ni contexto."
    )
    return {
        "status": "partial",
        "message": "Se usó una respuesta de ejemplo porque no hay una clave GEMINI_API_KEY configurada. Añade la variable en tu .env para usar Gemini real.",
        "user_story": story,
        "acceptance_criteria": [
            "Dado que el usuario aporta una solicitud inicial, Cuando la solicitud se envía al sistema, Entonces la app la convierte en una historia de usuario estructurada.",
            "Dado que la solicitud contiene ambigüedad o requisitos incompletos, Cuando se genera el artefacto, Entonces el sistema identifica supuestos y preguntas abiertas para evitar una definición engañosamente completa.",
            "Dado que la solicitud ya fue revisada, Cuando el equipo copia el artefacto, Entonces el resultado refleja la intención original y es útil para refinamiento técnico."
        ],
        "technical_dependencies": [
            "Validar reglas de negocio y permisos cuando la solicitud implique acceso restringido.",
            "Confirmar si la funcionalidad requiere integración con sistemas actuales o flujos existentes."
        ],
        "open_questions": [
            "¿Qué evento o disparador inicia la funcionalidad propuesta?",
            "¿Qué datos o validaciones deben revisarse antes de implementar la historia?",
            f"¿Qué tan precisa es esta solicitud original? {normalized_request[:120]}..." if normalized_request else "¿Qué objetivo exacto está intentando resolver la solicitud?"
        ],
        "raw_request": normalized_request,
    }


def build_response_from_model(raw_text: str, raw_request: str, role: str) -> dict[str, Any]:
    if not raw_text or not raw_text.strip():
        return build_demo_fallback(raw_request, role)

    paragraphs = [p.strip() for p in raw_text.splitlines() if p.strip()]
    user_story = next((p for p in paragraphs if p.lower().startswith("como ") or p.lower().startswith("como")), "")
    criteria = []
    dependencies = []
    questions = []
    current_list = None

    for line in paragraphs:
        stripped = line.strip()
        lower = stripped.lower()
        if lower.startswith("##") or lower.startswith("###"):
            heading = lower.replace("#", "").strip()
            if "historia" in heading:
                current_list = "story"
            elif "criterio" in heading or "acceptance" in heading:
                current_list = "criteria"
            elif "dependencia" in heading or "tecnica" in heading:
                current_list = "dependencies"
            elif "pregunta" in heading or "abierta" in heading:
                current_list = "questions"
            else:
                current_list = None
            continue

        if current_list == "story" and stripped and not stripped.startswith("-"):
            user_story = stripped
        elif current_list == "criteria" and stripped:
            criteria.append(stripped)
        elif current_list == "dependencies" and stripped and stripped.startswith(("-", "*")):
            dependencies.append(stripped.lstrip("-* "))
        elif current_list == "questions" and stripped and stripped.startswith(("-", "*")):
            questions.append(stripped.lstrip("-* "))

    if not user_story:
        user_story = f"Como {role if role and role != 'Sin rol específico' else 'usuario de negocio'}, quiero convertir esta solicitud en un artefacto ágil, para reducir ambigüedad antes del desarrollo."
    if not criteria:
        criteria = [
            "Dado que la solicitud se envía al sistema, Cuando la app la procesa, Entonces genera una historia y criterios claros.",
            "Dado que la entrada es incompleta, Cuando se detecta ambigüedad, Entonces la salida resalta preguntas pendientes en lugar de asumir certeza."
        ]
    if not dependencies:
        dependencies = ["Validar si la solución necesita integración con sistemas o roles de negocio adicionales."]
    if not questions:
        questions = ["¿Qué detalle falta para convertir esta idea en un trabajo ejecutable?"]

    return {
        "status": "success",
        "message": "Generado con Gemini.",
        "user_story": user_story,
        "acceptance_criteria": criteria,
        "technical_dependencies": dependencies,
        "open_questions": questions,
        "raw_request": raw_request,
    }


def generate_content_with_model_fallback(prompt: str) -> Any:
    primary_model_name = "gemini-1.5-flash"
    primary_model = genai.GenerativeModel(primary_model_name)
    generation_config = {
        "temperature": 0.4,
        "top_p": 0.9,
        "max_output_tokens": 1200,
    }

    try:
        return primary_model.generate_content(prompt, generation_config=generation_config)
    except Exception as primary_error:
        try:
            available_models = genai.list_models()
        except Exception as list_error:
            raise RuntimeError(
                f"Falló el modelo {primary_model_name}: {primary_error}. "
                f"No se pudieron consultar modelos alternativos: {list_error}"
            ) from list_error

        tried_models = {primary_model_name, f"models/{primary_model_name}"}
        model_errors = []
        for available_model in available_models:
            supported_methods = getattr(available_model, "supported_generation_methods", [])
            model_name = getattr(available_model, "name", "")
            if "generateContent" not in supported_methods or not model_name or model_name in tried_models:
                continue

            tried_models.add(model_name)
            fallback_model = genai.GenerativeModel(model_name)
            try:
                return fallback_model.generate_content(prompt, generation_config=generation_config)
            except Exception as fallback_error:
                model_errors.append(f"{model_name}: {fallback_error}")

        if model_errors:
            fallback_error_details = "; ".join(model_errors)
        else:
            fallback_error_details = "No se encontraron modelos alternativos compatibles."
        raise RuntimeError(
            f"Falló el modelo {primary_model_name}: {primary_error}. "
            f"También fallaron los modelos alternativos: {fallback_error_details}"
        ) from primary_error


def generate_story_result(raw_request: str, role: str) -> dict[str, Any]:
    if not raw_request.strip():
        raise ValueError("La solicitud no puede estar vacía.")

    if genai is None or not os.getenv("GEMINI_API_KEY"):
        return build_demo_fallback(raw_request, role)

    try:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        prompt = build_prompt(raw_request, role)
        response = generate_content_with_model_fallback(prompt)
        text = getattr(response, "text", "") or str(response)
        return build_response_from_model(text, raw_request, role)
    except Exception as exc:  # pragma: no cover - runtime-only fallback
        return {
            "status": "error",
            "message": f"No se pudo conectar con Gemini: {exc}",
            "user_story": "",
            "acceptance_criteria": [],
            "technical_dependencies": [],
            "open_questions": [],
            "raw_request": raw_request,
        }


def build_markdown_output(result: dict[str, Any]) -> str:
    lines = [
        "## Historia de usuario",
        result.get("user_story") or "No se generó una historia de usuario.",
        "",
        "## Criterios de aceptación",
    ]
    for criterion in result.get("acceptance_criteria") or ["No se generaron criterios de aceptación."]:
        lines.append(f"- {criterion}")
    lines.extend(["", "## Dependencias técnicas"])
    for dep in result.get("technical_dependencies") or ["No se detectaron dependencias específicas."]:
        lines.append(f"- {dep}")
    lines.extend(["", "## Preguntas abiertas"])
    for question in result.get("open_questions") or ["No se identificaron preguntas abiertas."]:
        lines.append(f"- {question}")
    return "\n".join(lines)


def render_story_result(result: dict[str, Any]) -> None:
    st.markdown("### Resultado generado")
    if result.get("status") == "partial":
        st.caption(result["message"])
    elif result.get("status") == "error":
        st.error(result["message"])
    else:
        st.success(result["message"])

    st.markdown(f"**Solicitud original:** {result.get('raw_request', '')}")

    markdown_output = build_markdown_output(result)
    st.markdown(markdown_output)

    st.download_button(
        label="Descargar Markdown",
        data=markdown_output,
        file_name="historia-usuario.md",
        mime="text/markdown",
    )

    copy_html = f"""
    <div style="margin-top: 1rem; margin-bottom: 1rem;">
      <button id="copy-btn" style="padding: 0.6rem 1rem; border-radius: 0.5rem; border: 1px solid #e0e0e0; background: #f5f5f5; color: #111; cursor: pointer;">
        Copiar Markdown
      </button>
    </div>
    <script>
      const button = document.getElementById('copy-btn');
      button.addEventListener('click', () => {{
        const text = {json.dumps(markdown_output)};
        navigator.clipboard.writeText(text)
          .then(() => {{ button.textContent = 'Copiado'; }})
          .catch(() => {{ button.textContent = 'No se pudo copiar'; }});
      }});
    </script>
    """
    components.html(copy_html, height=90)


st.set_page_config(page_title="User Story & Acceptance Criteria Assistant", page_icon="🧭", layout="wide")
st.title("User Story & Acceptance Criteria Assistant")
st.caption("Convierte ideas de negocio vagas en historias, criterios de aceptación y dependencias para refinamiento de backlog.")

if "request_text" not in st.session_state:
    st.session_state.request_text = ""
if "selected_role" not in st.session_state:
    st.session_state.selected_role = ROLES[0]
if "generated_result" not in st.session_state:
    st.session_state.generated_result = None

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
        try:
            st.session_state.generated_result = generate_story_result(request_text, selected_role)
            render_story_result(st.session_state.generated_result)
        except ValueError as exc:
            st.warning(str(exc))

if not submitted and not st.session_state.generated_result:
    st.markdown("### Resultado")
    st.info("Ingresa una solicitud y presiona 'Generar historia' para comenzar.")
