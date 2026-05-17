# USC — Automated Grading Pipeline

## Summary
I built a set of scripts (Python, Java, Bash) that automated the run-and-test phase of grading code assignments — the most time-consuming part of weekly TA evaluation. It cut grading time from 10–20 hours/week down to 1–2 hours/week, a 90%+ reduction, across 200+ weekly submissions.

## Context / Problem
Grading 200+ weekly code submissions by hand — running each one, testing behavior, checking outputs — took 10–20 hours per week. That was not sustainable on top of full-time 700-level graduate coursework. Time was the binding constraint, so I engineered around the bottleneck instead of absorbing it.

## Technical Details
**Stack:** Python, Java, Bash. Submission platform: Blackboard (the university LMS). Output: a CSV file with scores per student.

**Pipeline flow:**
1. **Manual pull** — I downloaded all student submissions from Blackboard (not automated).
2. **Automated execution** — scripts ran each submission's code against a predefined suite of test cases.
3. **Output comparison** — actual output compared against expected output per test case.
4. **Scoring** — scores computed from test-case pass/fail, following a strict grading rubric.
5. **CSV generation** — results written to a CSV.
6. **Manual upload** — I entered/uploaded the grades into Blackboard.

**Edge-case handling:**
- Failed compile / runtime crash → 0 points (default, per rubric).
- IDE compatibility issues (VS Code vs. Eclipse occasionally caused submission errors) → manual review; 1–2 cases per cycle.
- Suspected academic-integrity violations → flagged and reported; not auto-handled.

**Deliberately not automated:** downloading submissions from Blackboard, grading reports and written papers (done manually), and uploading final grades to Blackboard.

## Results
- Grading time: 10–20 hours/week → 1–2 hours/week (90%+ reduction).
- 200+ weekly submissions processed through the pipeline.
- Reclaimed 10–18 hours/week that would otherwise have gone to manual grading — directly bought back time for graduate coursework.

## Lessons Learned
The right scope for automation was the run-test-score loop, not the whole job. Leaving the Blackboard pull/upload and the written-work grading manual was a deliberate call — automating those would have cost more to build and maintain than the time it saved. Automate the bottleneck, not everything.

## Keywords
USC, automated grading, grading pipeline, Python, Java, Bash, Blackboard, test cases, CSV, rubric, automation, time management, edge case handling, TA
