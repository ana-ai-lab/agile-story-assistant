---
doc: prd
status: approved
---

# User Story & Acceptance Criteria Assistant — Product Requirements

One line: a lightweight agile assistant that turns informal business requests into a backlog-ready user story, executable acceptance criteria in Gherkin, and a clear list of technical dependencies and open questions for refinement.
Source: `scope.md > The Unique Kernel`, `scope.md > The Core Loop`, and `scope.md > What "Working" Looks Like`.

## The Core Journey

1. The user opens the app and sees a single interaction surface for turning a rough business idea into a refined agile artifact.
2. The user pastes a raw requirement or business request into a text area and optionally selects a role such as Product Owner, Scrum Master, or business analyst.
3. The user clicks a generate action to trigger the transformation flow.
4. The system analyzes the request and produces a structured Markdown output with:
   - a user story written in the INVEST-aligned format "Como [rol], quiero [acción], para [beneficio]"
   - acceptance criteria in Gherkin syntax covering the happy path and validation or error path
   - a list of technical dependencies, assumptions, and open questions that should be resolved before the story is ready for estimation
5. The user reviews the generated artifact, copies it into a backlog tool or meeting thread, and uses the clarified questions to drive refinement.
6. Success is defined by a raw business idea becoming a structured, reviewable backlog artifact in a short, visible flow, without requiring the user to manually rewrite the requirement into agile language.

## Screens and Layout

The product is a lightweight, single-screen workflow with two connected zones:

- Input panel: a text area for the raw business request, with an optional selector for the likely user role or audience.
- Output panel: a Markdown result card that shows the generated story, acceptance criteria, and dependency/question list.

The layout should feel operational and disciplined rather than playful. The user should be able to read the request, trigger generation, and immediately assess the quality of the output without navigating multiple screens.

## Look and Feel

The product should feel clear, structured, and professional. The tone should be execution-oriented and business-credible, not generic consumer-AI styling. The visual treatment should support fast comprehension of a backlog-ready artifact: clean hierarchy, strong spacing, and readable Markdown output. It should feel more like a refinement tool for agile teams than a creative prompt playground.

## Features and Behavior

### Request intake and role framing

The user can enter a raw business request in freeform text and optionally choose a role or perspective. This helps transform the story so it reflects the person requesting the value.

- As a user, I want to paste an informal requirement so that I can quickly convert it into an agile artifact.
  - [ ] Acceptance criterion — the app accepts freeform text and keeps the full original request visible for review
  - [ ] Acceptance criterion — the app allows a role or perspective to be selected without making it mandatory

### Story generation

The app converts the raw requirement into a structured user story that follows a clear cause-and-value pattern and preserves the business intent without inventing unrelated functionality.

- As a Product Owner, I want a clear user story so that the backlog item states the value and goal unambiguously.
  - [ ] Acceptance criterion — the generated story uses a readable "Como [rol], quiero [acción], para [beneficio]" structure
  - [ ] Acceptance criterion — the story preserves the original intent of the request without adding speculative features

### Acceptance criteria generation

The app translates the requirement into acceptance criteria using Gherkin syntax, with enough structure to be used as validation criteria in an agile backlog.

- As a Scrum Master, I want acceptance criteria in Gherkin so that the team can verify the outcome with objective test conditions.
  - [ ] Acceptance criterion — at least one happy-path scenario is generated in "Dado / Cuando / Entonces" format
  - [ ] Acceptance criterion — the output distinguishes expected behavior from validation or error conditions

### Dependency and question detection

The app highlights technical dependencies, missing facts, assumptions, and unanswered questions that the team must resolve before the work can be estimated or delivered.

- As a business analyst, I want detected dependencies and open questions so that I can spot hidden complexity before refinement.
  - [ ] Acceptance criterion — the output explicitly lists technical dependencies or implementation blockers when they are implied by the request
  - [ ] Acceptance criterion — the output calls out missing information or ambiguous decisions that still need clarification

### Copy-ready output

The generated result is formatted for easy sharing in backlog artifacts, documentation, or discussion threads.

- As a user, I want the result in a copy-paste-friendly format so that I can move quickly from idea to backlog refinement.
  - [ ] Acceptance criterion — the result is rendered as plain Markdown, easy to select and copy
  - [ ] Acceptance criterion — the output stays compact and reviewable within a single screenful of content

## States and Boundaries

- **First use** — the user sees a clean input area and can immediately test the flow without setup or login.
- **Empty input** — the user receives a clear validation message telling them that a request is needed before generation can proceed.
- **Vague or incomplete request** — the system still generates a best-effort output, but it flags missing information and open questions instead of pretending the requirement is fully formed.
- **Successful generation** — the output includes the user story, acceptance criteria, and dependency/open-question list in a structured and copyable format.
- **API or generation failure** — the system communicates the failure clearly and preserves the user’s original request so they can retry without losing context.

## Product Decisions

- Single-screen workflow with input and output visible together — keeps the PM and engineering review cycle fast and reduces friction in a proof of concept.
- Optional role selection — adds context without forcing unnecessary complexity into the MVP.
- Output as Markdown, not rich app-specific formatting — makes the artifact easy to copy into backlog tools, docs, or status threads.
- Keep the stack intentionally light: a minimal Python + Streamlit option or a direct HTML/JS frontend is preferred, connected to the Google Gemini API for text processing — this keeps the MVP fast to build and easy to demo.
- Copy-to-clipboard for Markdown output — the user should be able to move the generated result into a backlog tool or session quickly without manual selection and reformatting.
- No authentication or persistence in the MVP — keeps the scope tight and aligned with the proof-of-concept boundary.
- Clear detection of assumptions and technical dependencies — this is the differentiation point of the product and the main value over a generic AI writing tool.

## What We're Building

- a simple text input for a raw business requirement
- optional role selection
- generation of a user story in the format "Como [rol], quiero [acción], para [beneficio]"
- generation of acceptance criteria in Gherkin for the happy path and validation/error path
- explicit detection of dependencies, technical gaps, and unanswered questions
- readable Markdown output for easy copy-paste into agile artifacts
- a minimal frontend connected to the Google Gemini API

## Deferred From the POC

- user accounts or authentication
- historical storage or saved project sessions
- direct integration with Jira, Azure DevOps, or GitHub Issues
- team collaboration features or multi-user workflows
- analytics on story quality or backlog refinement outcomes

These are out of scope because they would add infrastructure or workflow depth without helping the proof-of-concept demonstrate the core value: turning ambiguous business input into structured, reviewable agile output.

## Possible Later Enhancements

- export to JSON, CSV, or HTML card layouts
- saved templates for different story patterns or team standards
- configurable organization-level quality rules for story generation
- retrospective feedback loop to improve the quality of generated acceptance criteria
- integrations with backlog tools for direct publishing

## Non-Goals

- building a full backlog management system
- allowing multi-user collaboration in the MVP
- implementing persistent user settings or accounts
- generating marketing copy or generic proposal text instead of backlog-ready artifacts
- replacing the team’s actual refinement process; the tool supports the process, but does not make it automatic

## Open Questions

- Must the app include a default sample prompt for first use, or should it start empty? This should be answered before implementation because it influences the initial UX and first-run clarity.
- Should the output always include a section for "questions to resolve" even when the request is already clear? This can be decided in the build phase if the team prefers to keep the interface lean.
- Is the role selector optional or mandatory for the MVP? This is a product decision that affects how much friction the app adds to the flow.
