# FancyBear — Overview

## What It Is

**FancyBear** is a **web-based stock trading simulator** — a virtual trading platform where users practice stock trading with virtual currency. Users can browse stocks, deposit virtual cash, buy and sell shares, track portfolio performance, view price graphs, favorite stocks, and review transaction history.

This was my **USC undergraduate Capstone project**, built with a five-person team. I was a **co-owner** of the project.

GitHub: https://github.com/david-eta/fancybear (repository under teammate David Eta's account)

## My Role and Contributions

I was one of five co-owners on this Capstone. My specific contributions were:

### UI / Frontend Work
I owned significant pieces of the user interface — the look and feel of the trading platform. Making the pages render cleanly, work on mobile, and feel polished.

### Automated Email Responses
I built the system that sends automated emails to users for things like account confirmations, transaction notifications, and similar lifecycle events. This involved Django's email tooling and integration with an SMTP provider.

### "Leave a Feedback" Page
A user feedback collection feature. Users can submit feedback about the platform, which is captured and stored for the team to review. This required form design, validation, server-side persistence, and admin views.

### "Leave a Comment" Page
A community comments system. Users can post comments visible to others, similar to a discussion or review board. Required moderation considerations, user attribution, and threading logic.

## The Team

Five contributors, listed on the repository:
- Christian Lee
- Mark Shperkin (me)
- David Eta (repo owner)
- Sid Gianey
- Travis Shuler

## Why It Mattered

This was my first **real team project** at USC at this scale — not a coursework assignment, but a Capstone-level build with sustained effort across a semester. Lessons that came out of it:

- Coordinating commits and code reviews with multiple developers
- Splitting features across teammates without stepping on each other
- Keeping a shared codebase coherent
- Building features that integrate cleanly with someone else's code

These soft skills — equally important to the technical ones — were the real takeaway from the project.

## What FancyBear Does

The platform simulates stock trading:

- **Account creation** and authentication
- **Deposit virtual cash** to start trading
- **Search and browse stocks** with detailed information
- **Buy and sell** with simulated market orders
- **Portfolio view** showing holdings and ROI
- **Trade history** logging every transaction
- **Stock favoriting** for quick access
- **Stock detail pages** with API-fetched price graphs
- **Responsive design** working on desktop, tablet, and mobile
- **User feedback and comments** (my contribution areas)

The point isn't real trading — it's a low-stakes way for users to learn how trading works without risking actual money.

## Tech Stack at a Glance

- **Backend**: Django (Python)
- **Database**: SQLite (development), PostgreSQL (production via Heroku)
- **Frontend**: HTML, CSS, vanilla JavaScript, Django templates
- **Hosting**: Heroku (production deployment)

Languages by proportion:
- Python: 68.3%
- HTML: 26.6%
- CSS: 3.7%
- JavaScript: 1.3%

## Capstone Context

This was my **USC undergraduate Capstone project** — the senior-year project that culminates the CS degree. The original repository may have been private; the public clone (`david-eta/fancybear`) hosts the team's collaborative work.

## Keywords

FancyBear, stock trading simulator, USC Capstone, capstone project, undergraduate Capstone, Django, Python web app, virtual trading, team project, five-person team, co-owner, UI development, email automation, feedback page, comments page, full-stack, Heroku deployment, PostgreSQL, SQLite
