# Cleanrate — HPXML Prototype

## Summary
The only project I did at Cleanrate, and the one that mattered: a client-side HTML prototype that collected house specs from a web form and generated a valid HPXML document accepted by the official US government Home Energy Score validator. I was the sole contributor on this deliverable, over ~1.5 months part-time.

## Context / Problem
Cleanrate needed to prove their core concept was technically feasible: take homeowner-submitted specs and produce a valid HPXML document that the US government's Home Energy Score system would accept. No existing implementation, no prior blueprint. If this couldn't be done, the product didn't exist.

## Technical Details
**Prototype stack:** client-side only. Plain HTML and JavaScript, no framework. No backend — the HPXML was generated entirely in the browser. No server, no database, no API calls.

**What it did:** an HTML web form collected house specifications from the user and generated a valid HPXML document on the client side.

**HPXML format:** HPXML (Home Performance XML) is the standardized XML format used by the US Department of Energy / NREL for the Home Energy Score program. A valid document captures comprehensive home characteristics:
- Building address and identification
- Property characteristics (year built, stories, bedrooms, floor area, orientation)
- Envelope components (attic/roof insulation, foundation type, wall construction, windows)
- HVAC system specs (heating, cooling, distribution)
- Domestic hot water systems
- Solar generation capacity

Each field has strict naming conventions, valid-value constraints, and required/optional rules defined by the NREL specification.

**Inputs/outputs:** Input — house specs entered via form fields (building details, insulation, HVAC, windows, hot water, etc.). Output — a valid HPXML XML document accepted by the official NREL/DOE validator.

## Process
- Read the NREL HPXML documentation to understand required fields, structure, and valid values.
- Built the form and XML-generation logic iteratively.
- Validated output against the official government HPXML validator tool after each iteration (the validator returned pass/fail with details on missing/invalid fields).
- Repeated build → validate → fix until all required fields passed.

NREL HPXML documentation was the primary source of truth.

## Results
Successfully produced a valid HPXML document accepted by the government system. This established the technical blueprint and proof-of-concept for Cleanrate's end-to-end energy-survey platform, and the foundation for future API-driven automation. The startup was later shut down due to a regulatory change before the prototype became a full product — the technical deliverable succeeded; the business outcome was outside engineering control.

## Lessons Learned
Iterating against an external validator as a feedback loop (submit → read error → fix → repeat) is a powerful way to reverse-engineer an underspecified standard. Poor documentation turned what looked like a straightforward task into a research-heavy exercise — and that's a normal, expected part of real engineering.

## Keywords
Cleanrate, HPXML, Home Energy Score, NREL, DOE, XML generation, client-side, HTML, JavaScript, validator, proof of concept, reverse engineering, iterative development, energy efficiency
