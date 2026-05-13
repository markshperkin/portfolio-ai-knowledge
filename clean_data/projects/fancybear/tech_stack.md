# FancyBear — Tech Stack

## Backend

- **Django** — Python web framework (the dominant choice for full-featured Python web apps)
- **Python 3.x** — backend language

### Why Django
Django gave us:
- Built-in admin interface (free user/data management)
- ORM for database operations
- Template engine for HTML rendering
- Authentication framework (login, signup, sessions)
- CSRF protection and security defaults
- A standard project structure that everyone on the team could follow

For a five-person Capstone team, Django's "batteries included" philosophy was the right call. Less time spent on infrastructure, more time on features.

## Database

- **SQLite** — for local development
- **PostgreSQL** — for production deployment on Heroku

### Why Two Databases
This dual setup is a Django/Heroku convention:
- SQLite is zero-config for dev — no need to install or run a database server
- PostgreSQL is what Heroku provides for production via add-on
- Django's ORM abstracts over both, so the same code runs on either

The transition from SQLite to PostgreSQL is mostly transparent thanks to Django's database abstraction.

## Frontend

- **HTML** — markup
- **CSS** — styling
- **JavaScript** (vanilla) — client-side interactivity
- **Django templating** — server-side rendered HTML with template inheritance

### Why Server-Side Rendering
The team chose Django templates over a separate frontend framework (React, Vue, etc.). Reasons:

- **Simplicity** — no need to maintain a separate frontend deploy
- **Familiarity** — Django templates are easy to pick up
- **Less duplication** — auth state, user data are already on the backend; templates inherit it directly
- **SEO-friendly** — server-rendered content indexes well

The downside: dynamic interactivity is limited compared to a full SPA. For our scope (browse, search, buy, sell, view portfolio), server-side rendering was more than enough.

## Hosting

- **Heroku** — production hosting platform

### Why Heroku
- Free tier (at the time) for student projects
- Git-based deploy (`git push heroku main`)
- Built-in PostgreSQL add-on
- Standard practice in Django tutorials and Capstone projects
- No DevOps complexity

For a Capstone with limited time and no DevOps engineer, Heroku was the path of least resistance.

## Build/Deploy Configuration

- **Procfile** — tells Heroku how to run the app
- **requirements.txt** — Python dependencies pinned to versions
- **manage.py** — Django's management command interface

These files together define the deployable application. Anyone with `git`, Python, and Heroku CLI access could deploy it.

## Code Composition

The codebase is mostly Python (the Django backend), with HTML and CSS for the frontend layer:

| Language | Approximate share |
|----------|-------------------|
| Python | 68.3% |
| HTML | 26.6% |
| CSS | 3.7% |
| JavaScript | 1.3% |
| Procfile | 0.1% |

The 1.3% JavaScript reflects the server-side rendering choice. Most page state is server-managed; JS handles only minor client-side interactivity (form validation, dropdowns, etc.).

## Stock Data Source

Stock information and price graphs are fetched from an external API (likely a free tier stock data API like Alpha Vantage, Yahoo Finance, or similar). The platform isn't connected to real exchanges — all trades are simulated.

## Email Stack

For my contributions on automated emails:

- **Django's `django.core.mail`** — sending interface
- **SMTP backend** — talking to an outbound mail provider
- **HTML + plain text templates** — for email content
- **Background task** for async send (so web requests don't block)

## Authentication

- **Django's built-in auth system**
- Username/password credentials
- Session-based authentication (server-stored sessions, cookies for session ID)
- CSRF protection on all forms

## What I'd Reconsider

Looking back, a few things I'd think about differently:

### Frontend Framework
The vanilla JS + Django template approach was right for the scope. But if I were rebuilding this for a more interactive product, I'd use React or HTMX to get more dynamic UX without sacrificing simplicity.

### Email Sending
Using a transactional email service (SendGrid, Mailgun, Postmark) would have been more reliable than direct SMTP. Better deliverability, better error handling, better observability.

### Hosting
Heroku was great for the Capstone but isn't the obvious choice anymore (free tier was discontinued). Today I'd consider Render, Railway, or Fly.io — newer Heroku alternatives.

### Database
SQLite for dev is fine but having dev and prod on different databases occasionally caused subtle issues (different SQL features, different default behaviors). Running PostgreSQL locally via Docker is closer to "dev mirrors prod" and worth the small setup cost.

## Keywords

Django, Python web framework, SQLite, PostgreSQL, server-side rendering, Django templates, vanilla JavaScript, Heroku, full-stack, Procfile, requirements.txt, ORM, Django admin, authentication, sessions, CSRF, free tier hosting, transactional email, SMTP backend, stock API
