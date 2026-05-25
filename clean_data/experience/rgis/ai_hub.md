# RGIS — AI-HUB Refresh (Warmup Project)

## Summary
Before Leads Finder, my warmup project at RGIS was a refresh of AI-HUB — the company's internal web application that acts as the central hub for all AI services available to RGIS personnel. I owned it as the sole developer.

## Context
AI-HUB is the internal front door to RGIS's AI tooling. When I joined, it already hosted AI Translation (free-text translation plus file translation — docx, pptx, xlsx, and more). The refresh was a deliberate warmup: get familiar with the codebase and the environment while delivering real, visible value to internal users.

## What I Did
- **Visual refresh:** updated the core visual style — colors, fonts, and the overall design language.
- **Service integration:** integrated the AI Performance Review service into the HUB. The service already existed; I surfaced it through the HUB interface so personnel could reach it there. It provides KPI insights and improvement recommendations for RGIS personnel.
- **Maintenance & availability:** general maintenance and service-availability work so RGIS personnel could reliably access all the AI tools.

## Technical Details
Frontend: React, TypeScript. The HUB is the central access point; individual AI services (translation, performance review) are surfaced through it.

## Results
- Refreshed the visual design (colors, fonts, style) of the company's central AI tool.
- Integrated AI Performance Review, expanding the HUB's capability footprint for RGIS personnel.

## Lessons Learned
A warmup project is the right way to enter an unfamiliar production codebase under time pressure — it builds context and ships value at the same time, instead of doing neither while ramping.

## Keywords
RGIS, AI-HUB, React, TypeScript, internal tooling, AI translation, AI performance review, UI refresh, service integration, warmup project, frontend, FastAPI
