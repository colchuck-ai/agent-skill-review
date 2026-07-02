# Review rubric — Lenses 2–5

Detailed pass/fail criteria for the doc-grounded lenses. Lens 1 (Premise & Design) is adversarial and lives in [premise-and-design.md](premise-and-design.md); it is deliberately kept out of this file so subjective judgment never mixes with spec-grounded checks.

Grade each item Pass / Fail / N/A and map failures to a severity from `SKILL.md` § Severity levels. Each check links to its authoritative source so it stays correct as the spec evolves.

---

## Lens 2 — Conformance

"Is it a valid skill that will load and validate?" Objective and mostly scriptable — `scripts/validate_skill.py` checks most of these mechanically. Failures are **Blockers**. Source: [Specification](https://agentskills.io/specification).

- [ ] A `SKILL.md` exists at the skill directory root.
- [ ] `SKILL.md` begins with YAML frontmatter delimited by `---` lines.
- [ ] `name` is present, 1–64 chars, only lowercase `a-z`, `0-9`, and hyphens, does not start/end with a hyphen, and has no consecutive hyphens (`--`).
- [ ] `name` matches the parent directory name exactly.
- [ ] `description` is present, non-empty, and ≤ 1024 characters.
- [ ] `compatibility`, if present, is 1–500 characters and only used when the skill has real environment requirements.
- [ ] `metadata`, if present, is a string→string mapping.
- [ ] `license`, if present, is a short name or a reference to a bundled license file.
- [ ] `allowed-tools`, if present, is a space-separated string (experimental; support varies).
- [ ] No unknown/misspelled frontmatter keys presented as if standard.

**Structure (also Lens 2):** source [progressive disclosure](https://agentskills.io/specification#progressive-disclosure).

- [ ] `SKILL.md` body is ≤ 500 lines and roughly ≤ 5000 tokens. Longer → Major; recommend moving detail to `references/`.
- [ ] File references are relative paths, one level deep from `SKILL.md`. Deeply nested chains → Major.
- [ ] Every referenced file actually exists (no dead links). Missing → Blocker if load-bearing, else Major.
- [ ] Directory layout matches its contents (files placed in `scripts/`/`references/`/`assets/` as appropriate).

---

## Lens 3 — Activation

"Will it trigger when it should, and stay quiet when it shouldn't?" The `description` carries the entire burden. Source: [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions).

- [ ] Describes **what** the skill does and **when** to use it.
- [ ] Imperative, intent-focused phrasing ("Use when the user…") rather than "This skill does…".
- [ ] Lists concrete trigger contexts, including cases where the user won't name the domain explicitly.
- [ ] Specific enough to avoid firing on near-miss tasks; broad enough for varied phrasings/typos.
- [ ] Within 1024 chars (also enforced by the validator).
- [ ] If triggering reliability is in doubt, recommend the labeled eval-query method: ~20 queries (~half should-trigger, emphasizing near-misses), 3 runs each, with a train/validation split.

Distinct failure signature to watch for: a great body with a weak description is **never used**; a great description with a weak body **triggers then flounders** (that second case is Lens 4).

---

## Lens 4 — Instructional Craft

"Once triggered, will an agent execute well from the body and scripts?" Source: [best-practices](https://agentskills.io/skill-creation/best-practices), [using scripts](https://agentskills.io/skill-creation/using-scripts).

### Content quality

- [ ] **Adds what the agent lacks.** Project-specific conventions, non-obvious edge cases, specific APIs/tools. Content the agent already knows (what a PDF is, how HTTP works) → recommend cutting. *(Note: the deeper "does it add value at all" judgment is Lens 1; here it's about trimming known content from an already-justified skill.)*
- [ ] **Moderate detail.** Concise stepwise guidance with a working example beats exhaustive docs. Over-comprehensive coverage that invites unproductive paths → Major/Minor.
- [ ] **Grounded in real expertise**, not generic filler ("handle errors appropriately," "follow best practices").
- [ ] **Calibrated control.** Prescriptive (exact commands) for fragile/consistency-critical steps; flexible (explain the *why*) where multiple approaches are valid.
- [ ] **Defaults, not menus.** One recommended tool/approach with a brief escape hatch, not a list of equal options.
- [ ] **Procedures over declarations.** Teaches how to approach a class of problems, not a one-off answer for a single instance.
- [ ] **When to load each file** is stated (e.g., "Read `references/x.md` if …"), not a generic "see references/". Generic pointers → Minor/Major by size.
- [ ] **Tells the agent whether to run or read** each referenced script/file.

### Effective-instruction patterns (presence is a plus, not required)

Source: [best-practices § Patterns](https://agentskills.io/skill-creation/best-practices).

- [ ] **Gotchas** section for environment-specific facts that defy reasonable assumptions, kept in `SKILL.md`.
- [ ] **Output templates** for format-sensitive output (inline if short, `assets/` if long).
- [ ] **Checklists** for multi-step workflows with dependencies.
- [ ] **Validation loops** / plan-validate-execute for fragile or destructive operations.
- [ ] Reusable logic that would otherwise be re-derived each run is bundled as a tested script.

### Script hygiene (cross-cutting safety, evaluated here)

Source: [using scripts](https://agentskills.io/skill-creation/using-scripts).

- [ ] Bundled scripts are listed in `SKILL.md` so the agent knows they exist.
- [ ] Self-contained or declare dependencies inline (PEP 723 for Python, `npm:`/`bun` pins, `bundler/inline`).
- [ ] Versions pinned for one-off commands (`npx eslint@9`, `uvx ruff@0.8.0`).
- [ ] **No interactive prompts** — input via flags/env/stdin (agents run non-interactive shells). Interactive blocking → Blocker for that script.
- [ ] `--help` documents the interface; errors say what went wrong, what was expected, and what to try.
- [ ] Structured output (JSON/CSV) on stdout, diagnostics on stderr; idempotent; meaningful exit codes; safe defaults + `--dry-run`/`--confirm` for destructive ops; predictable output size.
- [ ] Prerequisites/runtime requirements stated (in `SKILL.md` or `compatibility`), not assumed.

### Anti-patterns (flag when present)

- [ ] No Windows-style backslash paths (`scripts\x.py`). Use forward slashes.
- [ ] No "too many options" without a default.
- [ ] No time-sensitive instructions ("before August 2025…"); use a "current" vs "deprecated (details)" split instead.
- [ ] Consistent terminology throughout (one term per concept).
- [ ] Non-vague skill name (not `helper`, `utils`, `tools`).
- [ ] Examples are concrete, not abstract placeholders.

### Human legibility (cross-cutting: maintainability, evaluated here)

Every other check in this lens asks whether an *agent* executes well. These ask whether a *human* can read, trust, audit, and safely change the skill — a skill can pass all five lenses and still be write-only. The agent-vs-human tension is narrow: most of the docs' craft advice (explain the *why*, consistent terms, concrete examples, progressive disclosure) serves both. Flag only where terseness crossed into opacity, not verbosity for its own sake.

- [ ] **Locatable.** Every major step has a descriptive heading; no unbroken section beyond ~30 lines without a subhead, so a maintainer finds the right place by scanning ([progressive disclosure](https://agentskills.io/specification#progressive-disclosure)).
- [ ] **Why-before-what.** Each non-obvious instruction carries its rationale, so a reader knows what breaks if they remove it ([best-practices](https://agentskills.io/skill-creation/best-practices)).
- [ ] **Self-contained vocabulary.** Acronyms and project jargon defined on first use; one term per concept (see Anti-patterns).
- [ ] **No unexplained magic.** Every bundled script has a stated purpose and `--help`; every non-obvious constant/threshold has a reason a human can evaluate.
- [ ] **Traceable claims.** Any normative rule links to its source so a human can verify it, rather than restating it verbatim.
- [ ] **No silent rot.** No content that will go stale (versions, dates, environment assumptions) without a deprecation path.

A legibility failure is **Major** if a competent maintainer cannot understand or *safely* change the skill (someone will "fix" it wrong); **Minor** for clarity polish. Never a Blocker or Reject.

---

## Lens 5 — Outcome (on-demand)

"Does it measurably beat no-skill?" The only lens that requires **running** the skill, not reading it. Skip for lightweight reviews; recommend it when the user wants assurance the skill actually improves outputs. Source: [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills).

- [ ] Test cases in `evals/evals.json` (prompt, expected output, optional input files).
- [ ] Each case run **with and without** the skill for a baseline comparison.
- [ ] Objective assertions added after seeing first outputs; graded PASS/FAIL with concrete evidence.
- [ ] Timing/tokens tracked to weigh cost vs. the quality delta.
- [ ] Iteration: failed assertions, human feedback, and execution transcripts fed back into the skill.
- [ ] Assertions that always pass (or always fail) in both configurations are pruned or fixed — they measure nothing.

### Cold-maintainer test (empirical human legibility)

The rigorous, vibes-free way to measure "easy for a human to follow." Give the skill to a fresh **subagent** prompted as a skeptical maintainer with **no prior context**, and have it answer, **without running anything and without the author**:

1. What does this skill do, and when does it fire? (one sentence)
2. Where would you change **X**? (point to the file/section for 2–3 realistic edits)
3. Why is instruction **Y** here — what breaks without it?
4. What does script **Z** do, from reading alone?
5. List anything you could not understand.

**Pass threshold:** Q1–Q4 answered correctly **and Q5 is empty.** The Q5 list *is* the defect list — it turns legibility into a countable failure set. Rerun it against a fresh subagent after edits, the same way Activation reruns trigger-eval queries.
