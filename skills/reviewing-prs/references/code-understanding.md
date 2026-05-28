# Code Understanding HTML Template

Use this template when the user wants to make a module, callstack, subsystem, or feature legible to a reviewer. The reader is approaching unfamiliar code with a reviewer's posture: they need to know the entry points, the hot path, the boundaries, and the gotchas before they can confidently say "this is fine" or "this is wrong." The artifact is an orientation aid, not a reference manual -- it traces a specific story through the code rather than enumerating every API.

This template is modelled on https://thariqs.github.io/html-effectiveness/04-code-understanding.html.

## Required sections, in order

1. **Title** in the form "How X flows through Y" or "Walkthrough: X in Y". Concrete is better than generic. "How authentication flows through example-app/web" beats "Authentication in example-app/web".

2. **Intro** -- one or two short paragraphs. Establish the trust boundary or framing assumption ("example-app uses cookie-based sessions with a single trust boundary: every API route runs `verifyToken()` before doing anything else"). Name the entry point and the exit point of the flow you're about to walk through.

3. **Request path / data flow diagram (Mermaid)** -- a horizontal flow showing the journey from input to output. For a request flow: `browser → API route → middleware → handler → store → db`. For a render flow: `state → selector → component → DOM`. Keep it small; six or seven nodes is plenty. Use a `flowchart LR`.

4. **Callstack walkthrough** -- a numbered sequence of three to seven steps. Each step contains:
   - **Step heading** -- short, action-oriented. "Cookie is parsed and validated."
   - **Location** -- `file_path:line_number` in monospace.
   - **Prose** -- two or three sentences in your own words. Explain *what* happens and *why* in the running narrative. Don't paraphrase the comments in the code; explain the role the function plays in the bigger story.
   - **Source snippet** -- the relevant lines (10-20 typically). In HTML, render this inside a `<details>` so the reader can expand only the steps they want to look at. The reader is following the story, not auditing every line.

5. **Key files** -- a bulleted list of the four to eight files that matter most, each with a one-line description. This is a navigation aid for the reader who already understood the flow and now wants to know where things live.

6. **Gotchas** -- two to five highlighted callouts for things that would surprise a careful reader. Real examples:
   - "The session cookie is set with `SameSite=Lax`, so OAuth callback redirects must come back through the canonical domain, not a preview URL."
   - "`verifyToken()` returns `null` for both missing and invalid tokens. Routes that need to distinguish must check the request headers directly."

   Render gotchas as a distinct visual block (subtle warning color, see `html-conventions.md`). They are where rereading the artifact six months from now will pay off.

Optional sections, when they earn space:

- **State machine (Mermaid `stateDiagram-v2`)** if the flow has discrete states (e.g. a job that goes `queued → running → succeeded|failed|retrying`).
- **Module dependency map (Mermaid)** if the prose mentions more than four files that import each other.
- **Sequence diagram (Mermaid `sequenceDiagram`)** when multiple processes or services are involved and the *timing* between them matters.
- **Glossary** for domain terms that recur (only if there are at least four).

## Writing style

- Tell a story. The reader is following a single representative path through the code, not auditing the module's complete surface. Subordinate completeness to clarity.
- Use the present tense and active voice. "The middleware reads the cookie", not "The cookie is read by the middleware (which was added in PR #482)".
- Cite real `file:line` everywhere. Treat unverified line numbers as a bug; if you didn't open the file, you can't cite it.
- Avoid negative documentation. Describe what the code does, not what it doesn't do, not what it used to do, not what lives elsewhere. (Cross-reference the project's CLAUDE.md if it has stricter rules on this.)

## What success looks like

A reader who has never touched this code opens the artifact, follows the request-path diagram, expands two or three callstack steps, glances at the gotchas, and can now make a small bug-fix change in this area without breaking anything. That is the bar.
