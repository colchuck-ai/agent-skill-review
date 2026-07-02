# Lens 1 — Premise & Design

The adversarial lens. It answers: **should this skill exist, and is it shaped right?** Run it **first** — a failure here means later polish may be wasted, so you can judge how much effort the downstream lenses deserve before spending it on a skill that shouldn't exist or is mis-architected. A failure is a warning, not a hard stop.

## Stance

This lens is **subjective and adversarial** by design, unlike the doc-grounded lenses (Conformance, Activation, Craft, Outcome). Keep it walled off in the report: label its findings as judgment, and never present a premise or architecture opinion as a spec violation. Your job here is to take a stance on the *idea and its shape*, not on formatting.

Do not rewrite the author's domain content. Challenge the premise and structure; leave the substance to the author unless they ask.

## Gate A — Reason to Exist (funnel gate)

Answer these before anything else. If the honest answer to the first two is "no," recommend **deletion or rethink** and note it prominently — then continue the remaining lenses at your discretion, since conformance and craft findings may still help the author.

- **Real, recurring problem?** Does this solve a problem that actually recurs, or a hypothetical one? A skill for a one-off task rarely earns its maintenance cost.
- **Does the base agent already do this well?** Per [best-practices](https://agentskills.io/skill-creation/best-practices): *"if the agent already handles the entire task well without the skill, the skill may not be adding value."* If a capable agent handles it unaided, the skill is noise in the context window.
- **What does it add that the agent lacks?** It should encode project-specific conventions, non-obvious edge cases, or specific APIs/tools — not general knowledge the model already has.
- **Is there a leaner form?** Could this be a rule, a one-line convention, or a single bundled script instead of a full skill? Prefer the lightest artifact that solves the problem.

The strongest signal that a skill deserves to exist is that a capable agent gets the task *wrong or inconsistent* without it. If you can't articulate that failure, the premise is weak.

## Method — Steelman, then attack

1. **Steelman.** State the strongest case *for* the skill in one or two sentences — the scenario where it clearly earns its place. This guards against lazy negativity and gives the author a fair hearing.
2. **Attack.** Then make the strongest case *against* it:
   - What's the most likely way this skill is a solution to a non-problem?
   - Where does it encode a subtly wrong mental model of the domain — internally consistent but something an expert would reject?
   - When would activating it make things *worse* than not having it?

Report both. A premise that survives a genuine steelman-then-attack is trustworthy; one that only survives because you didn't really try isn't.

## Gate B — Architecture & Scope

Judge whether the skill is a **coherent unit of work** ([best-practices § Design coherent units](https://agentskills.io/skill-creation/best-practices)).

- **Too broad?** Does it bundle unrelated jobs (e.g., "query the database *and* administer it")? Broad skills won't trigger precisely. Recommend splitting.
- **Too narrow?** Would completing one natural task force several of these skills to load together, risking overhead and conflicting instructions? Recommend merging.
- **Right boundary?** Is the line drawn where a human would draw it — one job, composable with others?
- **Overlap with siblings.** Does it duplicate or contradict an existing skill in the same directory? Overlapping descriptions cause ambiguous activation.
- **Decomposition.** For anything non-trivial: is `SKILL.md` the orchestrator with detail pushed to `references/`/`scripts/` ([progressive disclosure](https://agentskills.io/specification#progressive-disclosure)), or is everything crammed inline?
- **Structural legibility (human).** Can a human grasp the *shape* — why it's split into these files, why something is a script rather than prose? A skill that is agent-navigable but whose structure baffles a human maintainer has a design-legibility defect. (Prose-level legibility is judged in Lens 4; the architectural form is judged here.)

## Cross-cutting: safety / blast radius (evaluated here)

- **Misactivation harm.** If the skill triggers on the wrong task, what's the worst outcome? Read-only guidance is low blast radius; a skill that runs destructive commands is high.
- **Conflicts.** Could its instructions override or fight another active skill in a way that degrades unrelated tasks?
- **Reversibility.** Does it push the agent toward irreversible actions without a plan-validate-execute or dry-run safeguard? (Script-level hygiene is Lens 4; the *architectural* risk of encouraging such actions is judged here.)

## Output of this lens

Produce, for the report's **Lens 1** section:

- **Reason-to-exist call** — justified / weak / fails (with the one-sentence failure mode a capable agent would hit without the skill).
- **Steelman + strongest counterargument.**
- **Scope & architecture** — coherent / too broad (split) / too narrow (merge) / boundary or overlap issues.
- **Blast-radius note** — low / medium / high, with the worst realistic misactivation outcome.
- **Verdict contribution** — if the reason-to-exist gate fails or the architecture is fundamentally wrong, this is a **Reject**. Surface it prominently; a Reject signals that later polish may be wasted but does not force you to stop, so continue the remaining lenses at your discretion. Otherwise carry forward to Lenses 2–5.
