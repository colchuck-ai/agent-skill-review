# agent-skill-review

An Agent Skill that reviews other Agent Skills. It serves the person responsible for a skill — its author or maintainer, or an agent acting on their behalf — who must decide whether a `SKILL.md` and its bundled files are fit to rely on. The review evaluates a skill through five independent methods so that classes of failure one method cannot see are still caught, and reports actionable, source-grounded findings by severity.

## Jobs

### Judge whether a skill is fit to ship

> When I have an Agent Skill I am responsible for and must decide whether to rely on it, I want to judge whether it deserves to exist, is valid, will trigger, guides an agent well, and beats no-skill, so I can ship, fix, or retire it with confidence instead of discovering its failures in production.

#### O001 - Coverage of real defects

Minimize the likelihood that a skill judged fit still contains a defect the review failed to surface.

**Risks**

- **O001-RSK001** - Single-method blind spot: relying on one review method that is structurally blind to a whole class of failure lets that class pass unseen, increasing the likelihood a real defect goes unsurfaced.
- **O001-RSK002** - Surface-only reading: judging only the top-level description while skipping the bundled files leaves broken references, undocumented scripts, and stale content undetected, increasing the likelihood a real defect goes unsurfaced.
- **O001-RSK003** - Early abandonment: stopping the review after an apparent showstopper leaves later-stage defects unexamined, increasing the likelihood a real defect goes unsurfaced.
- **O001-RSK004** - Silent tool degradation: a validation tool that reports a clean result on input it actually mis-parsed gives false assurance, leaving a real spec violation unsurfaced.

**Requirements**

- **O001-R001** - Multi-method review: the review must evaluate the skill through multiple independent methods, each targeting a distinct class of failure.
- **O001-R002** - Read everything first: the review must read the skill definition and every bundled file before judging premise, conformance, or craft.
- **O001-R003** - Continue past early failure: the review must keep surfacing later-stage findings even after an early-stage failure, treating that failure as a warning rather than a hard stop.
- **O001-R004** - Trustworthy validation: the review must validate frontmatter with the spec-complete parser available and flag explicitly when it could not confirm the parse.

**Risk-Requirement Map**

- **O001-RSK001 - Single-method blind spot**: O001-R001 - Multi-method review
- **O001-RSK002 - Surface-only reading**: O001-R002 - Read everything first
- **O001-RSK003 - Early abandonment**: O001-R003 - Continue past early failure
- **O001-RSK004 - Silent tool degradation**: O001-R004 - Trustworthy validation

#### O002 - Precision of findings

Minimize the likelihood that the review flags a non-defect as a defect or presents subjective judgment as an objective violation.

**Risks**

- **O002-RSK001** - Opinion as rule: when subjective design judgment is expressed in the same terms as objective spec rules, opinion gets reported as a violation, increasing the likelihood a non-defect is flagged and eroding trust in the findings that are real.

**Requirements**

- **O002-R001** - Separate judgment from spec: the review must keep subjective design judgment separated from objective spec violations and label each for what it is.

**Risk-Requirement Map**

- **O002-RSK001 - Opinion as rule**: O002-R001 - Separate judgment from spec

#### O003 - Effort to a decision

Minimize the effort to reach a trustworthy ship / fix / retire decision for a skill under review.

**Risks**

- **O003-RSK001** - Manual re-derivation: re-deriving spec limits and mechanical rules by hand on every review increases the effort to reach a decision and invites arithmetic mistakes.
- **O003-RSK002** - Wasted polish: investing review effort in the execution details of a skill that should not exist wastes the effort spent before the premise is even examined.

**Requirements**

- **O003-R001** - Mechanical checks by tool: the review must check mechanical spec rules with a bundled tool rather than re-deriving limits by hand.
- **O003-R002** - Funnel ordering: the review must run its stages in order of consequence — the reason-to-exist judgment first — so effort on a skill that should not exist can be curtailed early.

**Risk-Requirement Map**

- **O003-RSK001 - Manual re-derivation**: O003-R001 - Mechanical checks by tool
- **O003-RSK002 - Wasted polish**: O003-R002 - Funnel ordering

#### O004 - Actionability of findings

Maximize the likelihood that each surfaced finding can be acted on directly, without the author needing further investigation, at the time of the decision.

**Risks**

- **O004-RSK001** - Unactionable finding: a finding that names a problem without a location, rationale, or concrete fix forces the author to re-investigate, reducing the likelihood it can be acted on directly.
- **O004-RSK002** - Stale restated rule: a finding that restates a spec rule from memory drifts as the spec evolves, so an author acting on it may follow a rule that no longer holds.

**Requirements**

- **O004-R001** - Actionable findings: each finding the review reports must state what is wrong, where it is, and the concrete change that resolves it.
- **O004-R002** - Cite the source: each finding that reflects a spec or best-practice rule must link to its authoritative source rather than restating the rule.

**Risk-Requirement Map**

- **O004-RSK001 - Unactionable finding**: O004-R001 - Actionable findings
- **O004-RSK002 - Stale restated rule**: O004-R002 - Cite the source
