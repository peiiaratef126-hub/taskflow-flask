# Software Architecture Document: TaskFlow Flask Application

## 1. System Overview & Core Principles

**TaskFlow** is a modern, production-grade personal task management system built with Python, Flask, SQLAlchemy, and modern front-end design standards. The application architecture adheres to industry software engineering best practices, focusing on:

* **Separation of Concerns:** Modular separation between routing, input validation, domain models, template rendering, and styling.
* **The Application Factory Pattern:** Dynamic initialization enabling isolated runtime environments (Development, Testing, Production, and Serverless).
* **Multi-Stage Defense-in-Depth Validation:** A dedicated anti-gibberish and physical keyboard adjacency engine that blocks meaningless input in both Arabic and English.
* **Modern Design Token Architecture (Taste Skills):** Accessible typography, frosted glassmorphism, dynamic telemetry, and dark/light theme switching.
* **Serverless Edge & Cloud Deployment:** Out-of-the-box compatibility with **Vercel Serverless Functions** via a custom WSGI routing adapter.
* **ACID-Compliant Relational Data Layer:** Transactional data persistence backed by SQLAlchemy, preventing race conditions and data corruption.

---

## 2. High-Level Architectural Topology

```text
                                 [Client Web Browser]
                                          │
                     ┌────────────────────┴────────────────────┐
                     │                                         │
            (Local Environment)                        (Cloud / Vercel)
                     │                                         │
                     ▼                                         ▼
            [Flask Dev Server]                         [Vercel Edge Router]
            `python run.py:5000`                     `vercel.json` (Rewrites)
                     │                                         │
                     │                                         ▼
                     │                             [WSGI Serverless Adapter]
                     │                              `api/index.py` (Path unwrapping)
                     │                                         │
                     └────────────────────┬────────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │    Application Factory: `create_app`  │
                      └───────────────────┬───────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │    Controller Blueprint: `main_bp`    │
                      │         (in `app/routes.py`)          │
                      └───────┬───────────────────────┬───────┘
                              │                       │
                       (Write Operations)       (Read / Render)
                              │                       │
                              ▼                       │
              ┌──────────────────────────────┐        │
              │  Anti-Mash Validator Engine  │        │
              │     (`app/validators.py`)    │        │
              │  - Physical Coordinate Check │        │
              │  - Keyboard Runs & Mash      │        │
              │  - Repetition & Entropy      │        │
              └──────────────┬───────────────┘        │
                             │ (Valid)                │
                             ▼                        │
              ┌──────────────────────────────┐        │
              │    SQLAlchemy ORM Layer      │        │
              │     (`app/models.py`)        │        │
              └──────────────┬───────────────┘        │
                             │                        │
                             ▼                        ▼
              ┌──────────────────────────────┐ ┌──────────────────────────────┐
              │      Relational Storage      │ │       View Presentation      │
              │   - SQLite (`/tmp/` / local) │ │  - Jinja2 (`base`, `index`)  │
              │   - PostgreSQL (Cloud URL)   │ │  - `style.css` (Glassmorphic)│
              └──────────────────────────────┘ └──────────────────────────────┘
```

---

## 3. Multi-Tier Validation & Anti-Mash Pipeline

To guarantee data cleanliness and prevent meaningless keyboard-smashing, user input undergoes a **4-stage validation pipeline** in `app/validators.py` and `app/routes.py` before touching the database:

### Stage 1: Length & Whitespace Boundaries
* Leading and trailing whitespace is stripped.
* Minimum length: **3 characters**.
* Maximum length: **120 characters**.
* Input consisting solely of whitespace or missing characters is immediately rejected.

### Stage 2: Language-Agnostic Alphabetical Presence
* Ensures the input contains at least one alphabetic character (`char.isalpha()`).
* Blocks strings composed entirely of digits, punctuation, or special symbols.

### Stage 3: Anti-Gibberish & Keyboard Adjacency Heuristics (`is_meaningful_text`)
The input is evaluated by heuristic algorithms targeting physical keyboard mechanics:

1. **Character Repetition Check:**
   * Scans for 3 or more consecutive identical characters (`re.search(r'(.)\1{2,}', text)`).
   * Rejects patterns like `aaaa`, `hhhh`, and `.....`.

2. **Physical Keyboard Adjacency Distance (Euclidean Matrix):**
   * Maps QWERTY coordinates (`QWERTY_COORDS`) and standard Arabic 101/102 coordinates (`ARABIC_COORDS`) into a 2D Cartesian grid:
     $$\text{dist}(p_1, p_2) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$$
   * Computes the average Euclidean distance between consecutive characters.
   * If the average distance between consecutive characters is $\le 1.15$ across 5+ characters, it is classified as a physical home-row / single-row key swipe (e.g., `lkjasd`, `kjfvbklmv`).

3. **Continuous Keyboard Runs & Common Mash Substrings:**
   * Checks against known forward and reverse row patterns in both layouts:
     * English: `asdfg`, `qwerty`, `zxcvb`, `poiuy`, `lkjhg`
     * Arabic: `ضصثقف`, `شسيبل`, `ئءؤرى`, `كمنت`
   * Instantly rejects any token containing these contiguous sequence mashing strings.

4. **Arabic Home-Row Oscillation & Phonotactic Variety:**
   * Detects tight repetitive key alternation on the Arabic home row (e.g., `تن` + `تن` + `سي` in `تنتننتسي` or `نتشسابتن`).
   * Measures character set diversity relative to word length: words $\ge 5$ characters with $\le 3$ distinct characters are rejected.

### Stage 4: Duplicate Active Task Prevention
* Performs a case-insensitive lookup (`db.func.lower(Task.title) == title.lower()`).
* Only flags tasks where `Task.done == False`.
* Allows users to re-add previously completed tasks while strictly preventing duplicates in the pending queue.

---

## 4. UI/UX & Design Token Architecture (`taste-skills`)

The presentation layer is built upon modern design tokens defined in `app/static/css/style.css` and Jinja2 templates:

### 1. Color Foundations & Surfaces
* **Dark Mode Foundation:** `#0a0d14` (root canvas), `#0f131c` (elevated card backgrounds).
* **Light Mode Foundation:** `#f8fafc` (root canvas), `#ffffff` (elevated card surfaces).
* **Primary Accents:** Electric Indigo (`#6366f1`) with hover state (`#4f46e5`).
* **Success / Emerald Glow:** `#10b981` with radiant drop-shadows (`rgba(16, 185, 129, 0.4)`).
* **Border Radii:** Card surfaces use `16px` border-radius; buttons and input chips use `8px` to `12px`.

### 2. Glassmorphism Mechanics
* **Backdrop Filters:** `backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);`
* **Lighting Borders:** Subtly translucent `1px` border borders (`rgba(255, 255, 255, 0.08)` in dark mode, `rgba(0, 0, 0, 0.08)` in light mode).
* **Ambient Lighting:** Multi-stop radial gradients centered behind the viewport header to create depth without visual noise.

### 3. Typography Hierarchy
* **UI Typography:** **Inter** (`sans-serif`) across headings, buttons, alerts, and task titles.
* **Telemetry & Numeric Typography:** **JetBrains Mono** (`monospace`) with `font-variant-numeric: tabular-nums` to guarantee non-shifting metric counters and aligned IDs.

### 4. Interactive Components & Telemetry
* **Zero-FOUC Theme Switcher:** Inline script executes in `<head>` before DOM painting to read `localStorage.getItem('taskflow_theme')` and immediately apply the `data-theme` attribute to `<html>`.
* **ACID Telemetry Pill:** Real-time top navbar badge containing a live CSS pulsing dot and connection status.
* **Dynamic Progress Bar:** Dynamically calculates completion percentage from `completed_count / total_count * 100` and renders an animated linear gradient fill.
* **Client-Side Filter Tabs:** Instantaneous DOM filtering (`All`, `Pending`, `Completed`) driven by data attributes (`data-status="pending" | "completed"`), eliminating server roundtrips.
* **Thought-Trace Drawer:** Expandable `<details>` disclosure panel displaying runtime validator metrics, Euclidean adjacency thresholds, and architectural specifications directly to users.

---

## 5. Serverless & Cloud Infrastructure Topology (Vercel)

```text
HTTP Request: https://taskflow-flask-rho.vercel.app/tasks/add
                              │
                              ▼
                   [Vercel Global Edge CDN]
                              │
               (Rewrite Rule in vercel.json)
    "source": "/(.*)" -> "destination": "/api/index?__vercel_route=/$1"
                              │
                              ▼
                [Serverless Python 3.12 Runtime]
                 (AWS Lambda container in iad1)
                              │
                              ▼
               [WSGI Normalizer: `api/index.py`]
    1. Extracts `__vercel_route` from QUERY_STRING
    2. Sets `environ['PATH_INFO'] = '/tasks/add'`
    3. Cleans up internal query parameter
    4. Hands off to Flask Application Context
                              │
                              ▼
                     [Flask WSGI Handler]
                              │
                    (Ephemeral / Cloud DB)
          SQLite (`/tmp/tasks.db`) OR PostgreSQL (Neon/Supabase)
```

### Serverless Compatibility Considerations:
1. **Read-Only File System:** Vercel serverless containers mount `/var/task` as read-only. `config.py` automatically detects `os.environ.get("VERCEL")` and routes SQLite storage to the writable `/tmp/tasks.db` partition.
2. **External Database Readiness:** If `DATABASE_URL` is configured (e.g. Supabase, Neon, or Railway PostgreSQL), `config.py` automatically normalizes legacy `postgres://` protocols to `postgresql://` for SQLAlchemy 2.0+ compliance.
3. **Cold-Start Optimization:** Lightweight dependencies (`Flask`, `Flask-SQLAlchemy`) ensure serverless cold-start execution times remain well under 500ms.

---

## 6. Detailed File Roles & Module Responsibilities

| File Path | Architecture Tier | Responsibility |
| :--- | :--- | :--- |
| `run.py` | Runtime Entrypoint | Local development server runner with hot-reload and environment loading. |
| `config.py` | Configuration Layer | Environment configurations (`Development`, `Testing`, `Production`) with cloud fallbacks. |
| `api/index.py` | Serverless Adapter | WSGI serverless function wrapper that unwraps Vercel route parameters. |
| `vercel.json` | Cloud Infrastructure | Vercel deployment specifications and edge rewrite definitions. |
| `app/__init__.py` | Application Factory | Factory pattern (`create_app`), Blueprint registration, and database context initialization. |
| `app/models.py` | Domain Model | SQLAlchemy `Task` entity with table schema, serialization (`to_dict`), and representations. |
| `app/routes.py` | Controller Layer | RESTful request handling, validation orchestrations, flash notifications, and template binding. |
| `app/validators.py` | Validation Engine | Euclidean keyboard adjacency matrix, repetition checks, phonotactics, and readability engine. |
| `app/templates/base.html` | Presentation Layout | HTML shell, ambient background glows, ACID telemetry pill, theme toggle, and flash alerts. |
| `app/templates/index.html` | View Layer | Dashboard cards, 3-card metrics grid, velocity progress bar, task list, and thought-trace drawer. |
| `app/static/css/style.css` | Design System | Glassmorphic design tokens, dark/light styles, animations, and responsive media queries. |
| `tests/conftest.py` | Test Infrastructure | Pytest fixtures providing isolated app instances and clean in-memory databases per test. |
| `tests/test_tasks.py` | Quality Assurance | 25 automated unit, functional, and edge-case validation test cases. |
| `.github/workflows/tests.yml`| DevOps / CI | GitHub Actions workflow executing pytest across Python matrix on push and PR. |

---

## 7. Database Entity Schema & ACID Guarantees

### Schema Definition (`app/models.py`)

```sql
CREATE TABLE task (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    done BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### ACID Characteristics:
* **Atomicity:** All database updates in `app/routes.py` use scoped transactions (`db.session.add()` / `db.session.commit()`). If validation or persistence fails, changes are not persisted.
* **Consistency:** Constraints (`NOT NULL`, `DEFAULT`, `PRIMARY KEY`) prevent orphaned or malformed records.
* **Isolation:** SQLite's WAL (Write-Ahead Logging) mode and in-memory isolated sessions in testing prevent dirty reads.
* **Durability:** Committed transactions are immediately synced to non-volatile disk storage (or `/tmp` in serverless).

---

## 8. Security & Hardening Measures

1. **SQL Injection Prevention:** 100% parameterization via SQLAlchemy ORM query builders; zero raw SQL string concatenation.
2. **Cross-Site Scripting (XSS) Mitigation:** Jinja2 contextual auto-escaping is active across all templates. User-supplied task titles are rendered as escaped text.
3. **REST Mutation Safety:** State-altering operations (`/tasks/add`, `/tasks/<id>/toggle`, `/tasks/<id>/delete`) strictly reject HTTP `GET` and require HTTP `POST`.
4. **Environment Secret Protection:** Production secret keys and database URLs are bound via environment variables with `.gitignore` exclusion for `.env` and `.env.local`.
5. **Anti-Flooding Length Restrictions:** Task titles are strictly capped at 120 characters to prevent buffer and denial-of-service payload bloating.

---

## 9. Testing Strategy

Testing follows the **Test Pyramid** model:

```text
          /\
         /  \     Integration Tests (REST API routes, flash alerts, HTTP redirect checks)
        /────\
       /      \   Functional Tests (Add, Toggle, Delete, Active Duplicate prevention)
      /────────\
     /          \ Unit Tests (Validator adjacency, repetition, Arabic phonotactics, entropy)
    /────────────\
```

Every test run executes with `TestingConfig` utilizing `sqlite:///:memory:`, ensuring zero test crosstalk, sub-second execution speeds, and complete environment isolation.