# RGIS — Challenges

## Summary
The hard problems at RGIS were real engineering and operational ones: stitching a coherent profile out of 15+ heterogeneous, incomplete APIs; controlling LLM hallucinations that directly hurt the product's core metric; a self-refinement loop too slow to ship; noisy/expensive APIs; second-hand ambiguous requirements; and delivering all of it through an international relocation during an active war.

## 1. Heterogeneous, Incomplete API Data
15+ APIs each returned different formats and schemas, many with missing fields. Building one coherent, consistent company profile from that patchwork was the core data-engineering challenge. **Resolution:** a normalization layer in the pipeline to unify schemas across sources, Perplexity as a fallback for missing data, and a hard rule to prioritize verified API data over LLM-inferred data.

## 2. LLM Hallucinations Degrading Lead Quality
LLMs fabricated company facts and pushed irrelevant companies into final results — directly undermining lead quality, which was *the* success metric. **Resolution:** prompt engineering with explicit DO NOT constraints and behavioral guardrails, plus heavier reliance on verified API data to ground reasoning. Combined effect: hallucinations dropped to a level stakeholders no longer noticed. **Tradeoff:** solved with prompt constraints alone — no code-level validation layer against API data. Sufficient for production quality at that stage.

## 3. Self-Refinement Loop Latency
The pipeline included a loop where an LLM evaluated output quality and re-triggered the full pipeline if results were insufficient. One run took ~15 minutes; multiple iterations blew past stakeholder tolerance. **Decision:** the loop was built and functional but disabled in production. Single-pass output became the shipped behavior — a deliberate latency-vs-quality call.

## 4. API Inefficiency and Cost
Several APIs were noisy — low-quality data while consuming more calls than necessary, driving up cost and latency. **Resolution:** identified and fixed the offending integrations, and tuned LLM batch sizes (companies per LLM call) by testing different sizes and observing quality, which cut per-company LLM cost.

## 5. Ambiguous, Second-Hand Requirements
Stakeholders described problems in vague, non-technical terms, and requirements shifted between releases. **Compounding factor:** the AI Director took the stakeholder meetings (I couldn't, due to the 11am Israel / 3am US East Coast gap), so requirements reached me second-hand and further filtered. **Resolution:** translated ambiguous inputs into actionable tasks with the Director. In hindsight, direct stakeholder access would have produced more tailored solutions — the key lesson of the role.

## 6. Personal Circumstances + Timeline Pressure
I managed a 5-week international relocation (Israel → US) during an active war, with repeated flight cancellations, while shipping production releases twice a week and working 10–11 hours/day including weekends, often without a stable workspace or routine. **Outcome:** every deliverable shipped on schedule. This combination was the most significant operational challenge of the engagement.

## Lessons Learned
Two stick with me: ground LLMs in verified data instead of trusting their output, and get direct access to stakeholders — second-hand requirements are a quality tax you pay on every release. The second lesson is why I now specifically want Forward Deployed Engineer roles.

## Keywords
RGIS, challenges, API normalization, LLM hallucination, prompt guardrails, self-refinement loop, latency, cost optimization, batch size tuning, ambiguous requirements, second-hand requirements, relocation, war, production pressure, Forward Deployed Engineer
