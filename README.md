# TaskFlow - Flask Task Manager

A modern, production-grade personal task management application built with Python and Flask. Designed using clean software architecture principles, featuring the Application Factory pattern, modular Blueprints, ACID-compliant persistence via SQLAlchemy, an advanced Anti-Gibberish & Keyboard-Mash Validation Engine (Arabic & English), a high-performance **Taste Skills** frosted glassmorphic UI with dark/light themes, automated Pytest test suite, and continuous deployment to **Vercel Serverless**.

[![CI Pipeline](https://github.com/peiiaratef126-hub/taskflow-flask/actions/workflows/tests.yml/badge.svg)](https://github.com/peiiaratef126-hub/taskflow-flask/actions/workflows/tests.yml)
[![Deployment: Vercel](https://img.shields.io/badge/Deployment-Vercel-black?logo=vercel)](https://taskflow-flask-rho.vercel.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)

---

## 🌐 Live Production Deployment

* **Production URL:** [https://taskflow-flask-rho.vercel.app](https://taskflow-flask-rho.vercel.app)
* **Vercel Direct Deployment:** [https://taskflow-flask-gtafkitir-ai-8413.vercel.app](https://taskflow-flask-gtafkitir-ai-8413.vercel.app)

---

## 🚀 Key Features & Highlights

### 1. Advanced Anti-Gibberish & Keyboard-Mash Validation Engine
* **Physical Keyboard Adjacency Matrix:** Detects and blocks home-row keyboard mashing using Euclidean distance coordinates across standard **QWERTY** (`QWERTY_COORDS`) and **Arabic 101/102** (`ARABIC_COORDS`) layouts (e.g., rejecting `lkjasd`, `kjfvbklmv`).
* **Arabic Phonotactic & Oscillation Heuristics:** Blocks repetitive Arabic home-row key oscillation patterns (e.g., rejecting `تنتننتسي`, `نتشسابتن`).
* **Repetition Checks:** Automatically rejects 3 or more identical consecutive characters (e.g., `aaaa`, `هههه`).
* **Continuous Keyboard Runs:** Detects continuous physical keyboard sequences (e.g., `asdfg`, `qwerty`, `ضصثقف`, `شسيبل`).
* **Entropy & Variety Heuristics:** Rejects low-entropy strings that lack character diversity.
* **Duplicate Active Task Prevention:** Case-insensitive, trimmed check ensuring active tasks cannot be duplicated while allowing completed tasks to be repeated.

### 2. Modern Glassmorphism & UI/UX Design System (Taste Skills)
* **Dark & Light Mode Engine:** Native dark foundation (`#0a0d14` background, `#0f131c` cards) paired with clean frosted light theme styles, animated SVG toggle, and zero-FOUC (Flash of Unstyled Content) localStorage hydration.
* **Frosted Glass Surfaces:** Glass cards featuring `backdrop-filter: blur(18px)`, `1px` subtle gradient lighting borders (`rgba(255, 255, 255, 0.08)`), and ambient shadow glows.
* **Accessible Typography:** Modern pairing of **Inter** for crisp UI reading and **JetBrains Mono** with `font-variant-numeric: tabular-nums` for counters, IDs, and telemetry.
* **Interactive 3-Card Metrics Grid:** Real-time counters for **Total Tasks**, **Pending Tasks**, and **Completed Tasks**.
* **Completion Velocity Progress Bar:** Dynamic animated gradient progress bar displaying the exact percentage of completed tasks.
* **Client-Side Filter Tabs:** Instantaneous `All`, `Pending`, and `Completed` tabs for zero-latency DOM filtering without page refreshes.
* **ACID Engine Telemetry Pill:** Real-time top navbar telemetry badge with an emerald pulsing beacon indicating database health.
* **Thought-Trace Architecture Drawer:** Collapsible system telemetry drawer showcasing live validator rules, keyboard adjacency heuristics, and database connection status.

### 3. Cloud & Serverless Ready (Vercel)
* **Vercel Serverless WSGI Adapter (`api/index.py`):** Dynamic route normalization and query-string unwrapping for seamless serverless execution.
* **Ephemeral Storage Compatibility:** Automatic fallback to writable `/tmp/tasks.db` when running on Vercel, with native connection support for external PostgreSQL databases (Neon, Supabase) via `DATABASE_URL`.
* **Static Asset Delivery:** Optimized asset routing for CSS stylesheets and icons.

### 4. Robust Testing & Quality Assurance
* **Full Automated Test Suite:** 25 pytest test cases verifying CRUD operations, anti-mash heuristics, Arabic string validation, duplicate prevention, and REST mutation safety.
* **CI/CD Integration:** Automated GitHub Actions test pipeline running on every `push` and `pull_request`.

---

## 📁 Project Structure

```text
taskflow-flask/
├── .github/
│   └── workflows/
│       └── tests.yml            # GitHub Actions CI automated testing pipeline
├── api/
│   └── index.py                 # Vercel serverless WSGI entrypoint & path normalizer
├── app/
│   ├── __init__.py              # Application factory & extension initialization
│   ├── models.py                # SQLAlchemy Task data model
│   ├── routes.py                # Web routes and CRUD controller logic (Blueprint)
│   ├── validators.py            # Anti-gibberish, keyboard adjacency & readability engine
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html            # Layout, ambient glows, telemetry pill & theme toggle
│   │   └── index.html           # Task dashboard, metrics grid, filter tabs & thought-trace
│   └── static/                  # Static assets
│       └── css/
│           └── style.css        # Taste-skills glassmorphic design system
├── tests/
│   ├── __init__.py              # Test package initializer
│   ├── conftest.py              # Pytest fixtures and in-memory test database setup
│   └── test_tasks.py            # 25 automated unit, validation & functional tests
├── .env.example                 # Example environment variable configurations
├── .gitignore                   # Ignored build, database, .vercel, and cache files
├── ARCHITECTURE.md              # Comprehensive software architecture document
├── config.py                    # Environment configuration classes (Dev, Test, Prod)
├── LICENSE                      # Open-source MIT License
├── pytest.ini                   # Pytest settings and discovery rules
├── README.md                    # Project documentation and quickstart guide
├── requirements.txt             # Version-pinned dependencies
├── run.py                       # Local development server entrypoint
└── vercel.json                  # Vercel deployment routing & rewrite specifications
```

---

## 🛠️ Getting Started

### Prerequisites
* **Python:** 3.10 or newer
* **pip:** Python package installer
* **Node.js & npm:** (Optional, for Vercel CLI deployment)
* **Git:** Version control

### Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/peiiaratef126-hub/taskflow-flask.git
   cd taskflow-flask
   ```

2. **Create and activate a virtual environment:**
   * **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   # Windows:
   copy .env.example .env

   # Linux / macOS:
   cp .env.example .env
   ```

---

## 🧪 Running Automated Tests

Execute the complete test suite across all 25 test scenarios using `pytest`:

```bash
pytest -v
```

### Test Coverage Highlights:
* `test_index_empty_state`: Empty state view rendering.
* `test_add_task_success`: Valid task creation and flash messaging.
* `test_reject_gibberish_keyboard_mash`: English keyboard mashing rejection (`kjfvbklmv`).
* `test_reject_english_home_row_mash`: English home-row adjacency rejection (`lkjasd`).
* `test_reject_arabic_home_row_oscillation`: Arabic repetitive oscillation rejection (`تنتننتسي`).
* `test_reject_arabic_keyboard_mash`: Arabic keyboard layout run rejection (`نتشسابتن`).
* `test_prevent_duplicate_active_task`: Active task uniqueness enforcement.
* `test_allow_duplicate_completed_task`: Re-adding completed tasks allowed.
* `test_rest_mutation_safety`: Verifies GET mutations are strictly disallowed.

---

## 💻 Running the Local Server

Start the Flask development server:

```bash
python run.py
```

Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🚀 Deploying to Vercel

The application is fully pre-configured for Vercel Serverless Functions.

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Authenticate with your Vercel account:**
   ```bash
   vercel login
   ```

3. **Deploy to Production:**
   ```bash
   vercel deploy --prod
   ```

---

## 📡 API & Route Reference

| Method | Endpoint | Description | Request Body / Parameters |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Displays the task dashboard, metrics, filter tabs, and all tasks. | None |
| `POST` | `/tasks/add` | Validates readability, keyboard adjacency, and length before creating task. | `title` (form-urlencoded, 3-120 chars) |
| `POST` | `/tasks/<id>/toggle` | Toggles the completion status (`done: true/false`). | `id` (integer URL path param) |
| `POST` | `/tasks/<id>/delete` | Permanently deletes the task from the database. | `id` (integer URL path param) |

---

## 🏛️ Architecture & System Design

For comprehensive architectural specifications, UML sequence diagrams, database schemas, and validator state machine documentation, refer to **[ARCHITECTURE.md](ARCHITECTURE.md)**.

---

## 📄 License

This project is licensed under the terms of the **[MIT License](LICENSE)**.