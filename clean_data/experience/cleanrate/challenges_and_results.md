# Cleanrate — Challenges & Results

## Summary
The challenges at Cleanrate were poor/incomplete documentation, zero guidance or structure, and a company-level regulatory risk that ultimately ended the business. The result: I delivered a validated technical proof-of-concept that became the blueprint for Cleanrate's product, before the startup shut down.

## Challenges

**1. Poor and incomplete documentation.** The NREL HPXML documentation had significant gaps — it didn't clearly specify which fields were truly required, what valid values were accepted, or how the XML needed to be nested in certain cases. **Resolution:** extensive trial and error, using the official government validator as a feedback loop — submit, read the error, fix, repeat — for many iterations until the document was fully valid. **Impact:** what looked like a straightforward implementation became a research-heavy reverse-engineering exercise.

**2. Fully self-directed, no guidance.** No onboarding, no technical mentor, no defined timeline, no guidance on approach — just a task description and the expectation to figure out the rest. **Resolution:** self-managed the entire process — found the right documentation sources, set up a validation workflow, and iterated with no external checkpoints.

**3. Regulatory risk (company-level).** Cleanrate's entire business model depended on government policy around home energy scoring. A regulatory change eliminated the product's commercial viability. **Outcome:** the startup shut down; the prototype was never built into a full product. This was outside engineering control.

## Results

**Technical deliverable:**
- Designed and implemented a prototype generating valid HPXML documents accepted by the official US government Home Energy Score validator.
- Established the technical blueprint for Cleanrate's end-to-end energy-survey platform.
- Proved the core concept: homeowner-submitted specs → instant valid energy-score document, no specialist required.

**Product impact:**
- Drove a major product milestone — architected the flow for automated energy-efficiency scoring, replacing manual specialist inspections with a software-first approach that delivers results in minutes.
- Laid the foundation for future API-driven automation of the pipeline.

**Context:** the technical work was completed successfully; the business shut down for regulatory reasons unrelated to engineering.

## Personal Growth
- Got real practice reading and navigating poor, incomplete technical documentation.
- Practiced iterative development against an external validation system (build → validate → fix → repeat).
- Worked in a fully self-directed environment with no guidance, deadlines, or structured feedback — and still delivered.
- Foundational HTML and client-side development practice.

## Lessons Learned
You can deliver a validated result with zero scaffolding if you build your own feedback loop — the external validator was effectively my missing spec and my missing mentor. And business outcomes (regulation, shutdown) are sometimes entirely outside engineering control; the engineering still has to be right.

## Keywords
Cleanrate, challenges, results, HPXML, NREL documentation, validator feedback loop, self-directed, regulatory risk, startup shutdown, proof of concept, iterative development, reverse engineering
