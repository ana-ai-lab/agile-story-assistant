---
doc: checklist
status: draft
---

# Build Checklist

Build mode: [learn]

## Slices

- [x] **1. App shell and request flow**
  Becomes usable: A single-screen app accepts a raw business request, keeps it visible, and shows a ready-for-generation empty-state or generated result without crashing.
  Why now: This proves the core interaction path and UI structure before we add the AI call, so the first usable behavior is real and testable.
  PRD ref: `prd.md > The Core Journey`, `prd.md > Request intake and role framing`, `prd.md > Copy-ready output`
  Spec ref: `spec.md > Components`, `spec.md > Look and Feel`, `spec.md > Where It Runs and How Someone Tries It`
  Build: Scaffold the Streamlit app, set up the input panel and output panel, add role selection, and validate empty input with a clear message.
  Verify (mechanical): Run the app, leave the request empty, confirm the validation message appears, then submit a sample request and confirm the result panel is ready for generation.
  Learner check: Open the app and try entering a rough requirement; confirm that the form is clear, the role selector is optional, and the app does not silently fail on empty input.
  Commit: `Create single-screen story generator UI`

- [x] **2. Gemini generation and structured markdown output**
  Becomes usable: The app sends the request to Gemini and renders a user story, Gherkin acceptance criteria, and technical dependencies/questions in a copy-ready Markdown block.
  Why now: The unique kernel is the structured transformation itself, so this is the earliest slice that proves the actual value of the product.
  PRD ref: `prd.md > Story generation`, `prd.md > Acceptance criteria generation`, `prd.md > Dependency and question detection`, `prd.md > Copy-ready output`
  Spec ref: `spec.md > Generation Orchestrator`, `spec.md > Output Renderer`, `spec.md > Data Model`, `spec.md > The Core Journey Through the System`
  Build: Add the prompt builder, Gemini client integration, parse/normalize the response, and render the three sections in Markdown with the original request preserved.
  Verify (mechanical): Run the app with a valid Gemini key and confirm the generated result contains a `Como ...` user story, Gherkin scenarios, and dependency/open-question output. Test failure path with a missing key or API error.
  Learner check: Paste a vague requirement, generate it, and check whether the result is structured enough to become a backlog item.
  Commit: `Generate structured agile output from Gemini`

- [ ] **3. Review, error handling, and copy workflow**
  Becomes usable: A user can review the final artifact, retry after a failure, and copy the Markdown output without losing context.
  Why now: This completes the demo-critical flow and ensures the app is resilient enough for the final review and a short hackathon demo.
  PRD ref: `prd.md > States and Boundaries`, `prd.md > API or generation failure`, `prd.md > Copy-ready output`
  Spec ref: `spec.md > Validation and Error Messaging`, `spec.md > Components`, `spec.md > Data Model`
  Build: Add retry-safe error messaging, keep the original request visible, add copy-to-clipboard support, and polish the layout to match the spec's professional backlog-refinement feel.
  Verify (mechanical): Trigger an empty request and an API-failure path, confirm clear messaging, then copy output and ensure the Markdown remains readable and complete.
  Learner check: Ask the app to generate a requirement, intentionally test a bad input or API failure, and confirm the app keeps context and makes the next attempt easy.
  Commit: `Harden review flow and copy-ready output`

## Hands-on Checkpoints

- [ ] Early usable behavior explored — [core interaction ready after slice 1]
- [ ] Final kick-the-tires exploration and feedback completed

## Final Review

- [ ] Final review complete — feedback resolved and learner confirms ready to ship

## Code Tour and App Map

- [ ] Learning activity complete — guided route, focused alternative, prior practice connected, or brief recap
- [ ] Optional edit and transfer reflection addressed — offered/declined/already covered/not applicable as appropriate
- [ ] `devpost/app-map.html` generated from finished code, checked, and shown, including a project-grounded practice to reuse

Activity and evidence: [what actually happened; real document/test/code references; unfinished work if interrupted]
Route and stops: [actual paths and symbols; guided stops completed, or reference-only route]
Edit outcome: [tried/kept/reverted/declined/not applicable; verification if changed]
Reflection: [offered/answered/declined/already covered — personal answer belongs only in the ignored profile]
Activity mode: [live app and editor, explicit static fallback, focused alternative, prior practice, or recap]

## Revisions
