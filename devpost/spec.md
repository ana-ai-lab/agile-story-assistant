---
doc: spec
status: approved
---

# User Story & Acceptance Criteria Assistant — Technical Spec

## How This Works, In Plain Language
This app is a focused, single-screen backlog-refinement tool. A user pastes a rough business requirement, optionally selects a role, and the app turns that raw input into a reviewable agile artifact: a user story in the "Como [rol], quiero [acción], para [beneficio]" style, acceptance criteria written in Gherkin, and a list of technical dependencies, assumptions, and open questions.

The important part is not that it "chatbots" a requirement; it is that it gives structure to a messy idea and exposes the pieces a team still needs to clarify before estimating or delivering it. This keeps the product useful for Product Owners, Scrum Masters, and analysts without turning the app into a generic writing assistant.

For the proof of concept, we keep the stack intentionally small: a local Python app with a lightweight interface, connected to Google Gemini for text generation. That gives us a fast demo, clear error states, and a realistic path for learning without introducing auth, persistence, or multi-user features. If the request is vague, the app does not pretend certainty; it highlights what remains ambiguous instead of inventing a false sense of completeness.

## The Core Journey Through the System
The flow follows the PRD's Core Journey, step by step:

1. The user opens the app and sees a single screen with an input panel and a result panel.
2. They paste a raw business request and optionally choose a role such as Product Owner or Scrum Master.
3. The app validates the request and prepares a prompt that asks the model to produce a structured agile artifact.
4. The app sends that prompt to Google Gemini with explicit instructions to return a user story, Gherkin acceptance criteria, and a detected dependency/question list.
5. The response is parsed and normalized into a readable Markdown output that keeps the original requirement visible and the generated result easy to review.
6. The user reads the generated artifact and copies it into a backlog tool, meeting notes, or a refinement thread.
7. If the request is incomplete, the app surfaces assumptions and missing facts instead of producing a misleadingly complete answer.

This is the main data path:

```text
User input
   ↓
Streamlit form
   ↓
Prompt builder + validation
   ↓
Google Gemini API
   ↓
Markdown parser + formatter
   ↓
Single-screen output + copy-ready result
```

PRD ref: `prd.md > The Core Journey`, `prd.md > Request intake and role framing`, `prd.md > Story generation`, `prd.md > Acceptance criteria generation`, `prd.md > Dependency and question detection`, `prd.md > Copy-ready output`.

## Stack
Recommended stack for this proof of concept:

- Python 3.11
- Streamlit for the UI and single-screen workflow
- Google Generative AI Python SDK for the Gemini integration
- Python-dotenv for local environment configuration

Documentation links:
- Streamlit: https://streamlit.io/
- Google Gemini API docs: https://ai.google.dev/gemini-api/docs
- Python quickstart for Gemini: https://ai.google.dev/gemini-api/docs/quickstart?lang=python
- Google AI Studio API key page: https://aistudio.google.com/app/apikey

Why this stack is the right fit:
- It matches the PRD's preference for a minimal Python + Streamlit option and keeps the project easy to demo in a short time.
- It reduces setup overhead compared with a custom React or backend-heavy architecture.
- It is simple enough for the learner to understand the end-to-end flow without adding operational complexity.

Tradeoff accepted:
- The UI will be intentionally simpler than a fully custom frontend; this is acceptable because the product is a focused proof of concept rather than a full product platform.

## Where It Runs and How Someone Tries It
Runtime: local desktop app in the browser, no hosted deployment required for the MVP.

Environment required:
- Python 3.11 installed locally
- A Google Gemini API key in a local environment variable
- Access to a browser for the demo

Start commands:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GEMINI_API_KEY="your_api_key_here"
streamlit run app.py
```

Then open:
- http://localhost:8501

What the demo should show:
- A raw requirement is pasted into the input box
- The user optionally selects a role
- A result appears in under a minute displaying the generated story, Gherkin scenarios, and dependency/open-question section
- The user can copy the Markdown output without leaving the page

Deployment is optional and not required to satisfy the submission. If the learner chooses to deploy later, the app can be containerized or hosted as a simple web app; this is explicitly deferred from the current proof of concept.

## Look and Feel
The interface should feel operational, disciplined, and business-credible rather than playful or consumer-facing. The PRD guidance is clear: the app should feel like a backlog-refinement tool, not a generic AI playground.

Design direction:
- Clean hierarchy with strong spacing
- Light neutral surfaces with restrained blue or slate accents
- Clear markdown sections for user story, acceptance criteria, and assumptions/questions
- Human-readable typography with strong emphasis on content over decoration
- Dense but calm layout: the user should be able to review the full generated artifact in one screenful without losing context

This is fully compatible with a Streamlit-based UI and keeps the app professional enough for agile planning workflows.

## Components

### Input and Role Framing
This component handles raw requirement intake and optional role selection. It collects the freeform business request and, if present, the expected persona for the story. It connects directly to the generation pipeline and keeps the original request visible for review.

PRD ref: `prd.md > Request intake and role framing`.

### Generation Orchestrator
This is the core application flow. It validates the input, builds a prompt, and calls the Gemini API with instructions for a strict output structure. It coordinates the required sections: user story, acceptance criteria, dependencies, and open questions.

PRD ref: `prd.md > Story generation`, `prd.md > Acceptance criteria generation`, `prd.md > Dependency and question detection`.

### Output Renderer
This component renders the generated result as Markdown in a readable, copy-friendly card. It preserves the original input and formats the output so that the user can quickly scan the artifact and copy it to a backlog tool, internal doc, or meeting thread.

PRD ref: `prd.md > Copy-ready output`.

### Validation and Error Messaging
This component handles empty input, weak or ambiguous requests, and API failures. Instead of hard failing silently, it gives the user guidance on what must be improved and keeps the original request visible so the user can retry without losing context.

PRD ref: `prd.md > States and Boundaries` and `prd.md > API or generation failure`.

## Data Model
The app does not require a database for the MVP. The data stays ephemeral in-memory while the user is interacting with the page, and no user accounts or stored sessions are required.

Primary data objects:

```python
raw_request = {
    "text": str,
    "role": str | None,
    "submitted_at": "ISO-8601 timestamp"
}
```

```python
generated_result = {
    "user_story": str,
    "acceptance_criteria": [str],
    "technical_dependencies": [str],
    "open_questions": [str],
    "raw_request": str,
    "status": "success" | "partial" | "error",
    "error_message": str | None
}
```

Data lifecycle:
- The user enters the raw requirement in the browser.
- The app binds it to a request object and sends it to the prompt builder.
- The answer is stored in memory as a generated result object.
- The UI reads that object and renders it in the output panel.
- When the browser refreshes or the user starts a new request, the object is replaced rather than retained.

This matches the POC boundary and keeps the system easy to demo and reason about.

## File Structure
Annotated file structure for the planned implementation:

```text
project/
├── app.py                              # Streamlit entry point and page layout
├── requirements.txt                    # Python dependencies for the MVP
├── .env.example                       # local env example for the Gemini key
├── .gitignore                         # ignores local venvs and secrets
├── README.md                          # local setup and demo instructions
├── src/
│   ├── __init__.py                    # package marker
│   ├── gemini_client.py               # wrapper for Google Gemini API calls
│   ├── prompt_builder.py              # assembles the agile prompt and output schema
│   ├── result_parser.py               # normalizes AI output into story + criteria + questions
│   ├── validation.py                  # input checks and graceful empty/error states
│   └── formatting.py                  # markdown rendering and output hygiene
├── devpost/
│   ├── learner-profile.md             # learner context and preferences
│   ├── scope.md                      # approved product scope and POC boundary
│   ├── prd.md                        # approved product requirements
│   ├── spec.md                       # technical blueprint (this file)
│   ├── spec.html                     # browser-friendly architecture overview
│   └── prd.html                      # visualized PRD reference
├── .venv/                             # local virtual environment (not committed)
└── sample_prompts.md                  # optional seed examples for demo and testing
```

This structure is intentionally narrow. It keeps the product easy to build, easy to explain, and easy to verify while still matching the PRD's core workflow.

## External Services and Dependencies

### Google Gemini API
- Purpose: generate user stories, Gherkin criteria, and dependency/open-question analysis from raw business requests.
- Documentation: https://ai.google.dev/gemini-api/docs
- Python SDK docs: https://ai.google.dev/gemini-api/docs/quickstart?lang=python
- Required key: `GEMINI_API_KEY`
- Calls: a single text-generation request to the model with a structured prompt that asks for Markdown blocks or a JSON-like schema.
- Rate limits: depend on the chosen Gemini tier and billing; the app should fail clearly if usage limits are reached.
- Cost: negligible for a small demo, but the app should show a clear error state if quota or billing blocks the call.

### Streamlit runtime
- Purpose: local browser UI and in-app interaction layer.
- Documentation: https://streamlit.io/
- No external account required for the MVP.

No database, auth system, or hosted deployment is required for the plan as written.

## Important Failure Modes
- Empty or whitespace-only input → the app shows a clear validation message and prevents generation.
- Invalid or missing Gemini API key → the app displays a friendly setup error and keeps the request visible for retry.
- Model returns malformed or weak output → the app keeps the original request visible, flags the issue, and asks the user to refine the text or retry.
- API quota or connectivity issue → the app shows a human-readable error and offers a retry path without losing the request context.

## What Was Simplified and Why
- No authentication or user accounts — the app is meant to be a quick, single-person workflow for a demo and a focused proof of concept.
- No persistent storage or sessions — the product value is in the generation quality and structure, not in long-term history.
- No Jira/Azure DevOps/GitHub integration — direct workflow integration is useful later, but it would add infrastructure without proving the main idea.
- No multi-user collaboration — the MVP is intentionally single-user to keep the build simple and the demo easy to understand.
- Local-only runtime — deployment is optional and can be added later once the core generation flow is proven.

## Decisions and Open Issues
Chosen decisions:
- The app will be a local Python + Streamlit frontend connected to the Google Gemini API.
- The result will remain in a single-page layout with an input panel and generated Markdown result panel.
- The app will keep no persistent data for the MVP; the original request and generated output live only in the current browser session.
- The app will explicitly surface assumptions and missing facts instead of hiding uncertainty.

Tradeoff accepted:
- The UI is intentionally simple and less custom than a full app shell. This is the right tradeoff for a POC where the business value is in the translation quality and the agile structure, not in a large interface system.

One genuine uncertainty discussed:
- Whether the demo should remain local-only or later be hosted for easier sharing. The current decision is to keep it local-only and treat deployment as an optional future improvement, because the submission requires a short demo video and a public GitHub repository, not necessarily a hosted web URL.
- This was clarified by the PRD's guidance that deployment is optional and not a substitute for the demo video or repository.

Open issues carried over from the product review:
- The output quality must be checked against a few representative inputs to verify that the model reliably produces a usable user story, scenarios, and dependency list.
- If the model is too loose, the prompt must be tightened to enforce the required structure and highlight uncertainty without inventing unsupported behavior.
- If the learner wants a shareable deployment later, a second iteration can add a one-click hosting target without changing the core proof of concept.

No major unresolved product ambiguity remains; this is a narrow, achievable MVP aligned with the approved PRD and POC boundary.
