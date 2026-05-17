# Academic Projects (Education Context)

## Summary
Three projects defined my academic work: the FancyBear B.S. capstone (a 5-person full-stack stock trading simulator), the HAR directed study (a hardware failure that pivoted into a successful ST-GCN paper), and the master's thesis (single-IMU swimming activity recognition). This file is the education-context summary; deeper technical detail lives in the projects/ and research/ sections.

## 1. FancyBear — B.S. Capstone (CSCE 490/492)
**Type:** Senior Capstone, the final project of the B.S. **Team:** 5 students (me, Christian Lee, David Eta, Sid Gianey, Travis Shuler). **My role:** co-owner; I owned the frontend/UI, the automated email system, the feedback page, and the comments page.

It's a web-based stock trading simulator — users trade with virtual currency: accounts, deposits, stock search, buy/sell, portfolio and trade history, favorites, price graphs. Stack: Django (Python) backend, SQLite (dev) / PostgreSQL (prod), HTML/CSS/vanilla JS with Django templates, hosted on Heroku.

This was my first large-scale team project. The real lessons were coordination: managing commits across multiple developers, splitting features cleanly, keeping a shared codebase coherent, and building features that integrate with other people's code. GitHub: https://github.com/david-eta/fancybear

## 2. Wearable Sensor-Based HAR — Directed Study (CSCE 798)
**Type:** individual research paper. **Supervisor:** Professor Ramtin Zand. **Semester:** Spring 2025. Sole author.

The original plan was a custom wearable motion-capture suit using 9-DOF IMUs (BNO055, Arduino MKR IMU, ESP32) for real-time human activity recognition. The hardware failed — sensor noise and drift made the data unusable, and even Extended Kalman Filter approaches couldn't correct it (twice-integrating noisy accelerometer data accumulates error exponentially; consumer IMUs aren't enough for 3D position tracking without heavy compensation).

I pivoted to a **Spatio-Temporal Graph Convolutional Network (ST-GCN)** on the NTU RGB+D benchmark (56,880 samples, 60 action classes, 25 joints), implemented in PyTorch. Result: 87.6% peak validation accuracy across 49 classes, with edge deployment confirmed (102.8 samples/sec on RTX 4070 Super, 6.8 on i7-14700F). The paper documents the failed hardware attempt honestly alongside the success. GitHub: https://github.com/markshperkin/HAR-STGCN

## 3. Master's Thesis — CSCE 799
**Title:** "Multi-Task Deep Learning Approach for Segmenting and Classifying Competitive Swimming Activities Using a Single IMU." Advisor: Professor Homayoun Valafar. Summer 2025, completed in ~2 months. Published on USC Scholar Commons; cited on Google Scholar.

An end-to-end deep learning pipeline that takes raw motion from a single wrist-worn IMU (smartwatch) and simultaneously does stroke classification, lap segmentation, stroke counting, and underwater kick counting. Architecture adapted from MTHARS (Duan et al.), tuned for competitive swimming. Leave-one-subject-out results: Micro-F₁ 0.7405 → 0.7709 with gyroscope; stroke count MAE ~3.5. This thesis directly connects my 20-year swimming career with my graduate AI research — I understood both the athletic problem and the ML solution. (Full technical detail is in research/thesis.)

## Lessons Learned
FancyBear taught team coordination; the HAR study taught research adaptability and honest documentation of failure; the thesis showed I can ship a publishable research result under extreme time compression and at the intersection of my own domain expertise.

## Keywords
FancyBear, capstone, CSCE 490, CSCE 492, Django, Heroku, stock trading simulator, HAR, ST-GCN, NTU RGB+D, PyTorch, IMU, master's thesis, MTHARS, swimming activity recognition, directed study, hardware failure, research pivot
