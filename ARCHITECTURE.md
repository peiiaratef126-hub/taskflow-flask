# Software Architecture Document: Flask Task Manager

## 1. System Overview

**Flask Task Manager** is a production-grade web application designed for personal task management. The system architecture adheres to industry-standard software engineering practices, emphasizing:
- Separation of concerns
- The Application Factory pattern
- Robust persistence via an Object-Relational Mapping (ORM) layer with ACID guarantees
- Automated continuous integration (CI/CD via GitHub Actions)

---

## 2. Architectural Pattern

The application implements a **Modular Model-View-Controller (MVC)** architectural pattern:

```text
[Client Browser]
       │
       ▼ HTTP Request (GET / POST)
┌─────────────────────────────────────────────────────────────────┐
│               Application Factory (`create_app`)                 │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │       Controller Layer (Flask Blueprint: `main_bp`)     │   │
│   │   - Request routing & payload validation                │   │
│   │   - Flash messaging & client redirects                  │   │
│   └─────────────────┬─────────────────────┬─────────────────┘   │
│                     │                     │                     │
│                     ▼                     ▼                     │
│   ┌───────────────────────┐ ┌───────────────────────────────┐   │
│   │      Data Layer       │ │       Presentation Layer      │   │
│   │   (SQLAlchemy ORM)    │ │   (View Layer - Jinja2 + CSS) │   │
│   │   - Task Data Model   │ │   - base.html (Base Template) │   │
│   │   - Scoped Sessions   │ │   - index.html (Task View)    │   │
│   │   - ACID Transactions │ │   - style.css (Styling)       │   │
│   └───────────┬───────────┘ └─────────────┬─────────────────┘   │
└───────────────┼───────────────────────────┼─────────────────────┘
                ▼                           │
      [SQLite Database]                     ▼ HTTP Response (HTML)
   (ACID Compliant Storage)          [Client Browser]
```

---

## 3. Complete Repository Structure

```text
flask-task-manager/
├── .github/
│   └── workflows/
│       └── tests.yml            # CI Workflow: Automated testing via GitHub Actions on Push/PR
├── app/
│   ├── __init__.py              # Application Factory: Initializes Flask, Database, & Blueprints
│   ├── models.py                # Data Layer: Task ORM Entity and Schema
│   ├── routes.py                # Controller Layer: Blueprint routes (Add, Toggle, Delete, View)
│   ├── templates/
│   │   ├── base.html            # Base template containing header, alerts container, and layout
│   │   └── index.html           # Main view with input form and task list
│   └── static/
│       └── css/
│           └── style.css        # Responsive styling and CSS design rules
├── tests/
│   ├── __init__.py              # Test package initializer
│   ├── conftest.py              # Test configuration, fixtures, and in-memory SQLite isolation
│   └── test_tasks.py            # Automated functional and unit test scenarios
├── .env.example                 # Template for environment variables (secrets are omitted)
├── .gitignore                   # Excludes build artifacts, virtual environments, and local databases
├── ARCHITECTURE.md              # Software architecture and design documentation
├── config.py                    # Environment configuration classes (Dev, Test, Prod)
├── LICENSE                      # Open-source MIT License
├── pytest.ini                   # Pytest runtime configuration and test discovery rules
├── README.md                    # Project README, setup guide, and documentation
├── requirements.txt             # Pinned project dependencies and third-party libraries
└── run.py                       # Local development server entrypoint
```

---

## 4. File Roles & Module Responsibilities

### A. DevOps & Repository Configuration
* **`.github/workflows/tests.yml`**: Defines the CI pipeline. Automatically spins up an Ubuntu environment, installs dependencies, and executes `pytest` on every push and pull request.
* **`pytest.ini`**: Configures test execution flags, directory locations, and test discovery file patterns.
* **`.gitignore`**: Prevents accidental commits of volatile files: `__pycache__/`, `venv/`, `*.db`, and editor configuration directories (`.vscode/`, `.antigravity/`).
* **`.env.example`**: Documents required environment variables (such as `SECRET_KEY` and `DATABASE_URL`) without exposing sensitive production values.
* **`LICENSE`**: Grants permissive open-source usage rights under the standard MIT License.

### B. Core Application Package (`app/`)
* **`app/__init__.py`**: Contains the `create_app()` factory function. Encapsulates Flask extensions (`SQLAlchemy`), registers Blueprints, and initializes database tables within the application context.
* **`app/models.py`**: Defines the `Task` ORM entity:
  * `id` (Integer, Primary Key, Auto-increment)
  * `title` (String 200, Not Null)
  * `done` (Boolean, Default: False, Not Null)
  * `created_at` (DateTime, Default: UTC Now, Not Null)
* **`app/routes.py`**: Encapsulates routes within `Blueprint("main", __name__)`, enforcing RESTful principles:
  * `GET /`: Retrieves all tasks ordered by creation date descending.
  * `POST /tasks/add`: Validates input and creates a new task.
  * `POST /tasks/<id>/toggle`: Flips the completion status (`done`) of a task.
  * `POST /tasks/<id>/delete`: Permanently removes a task from the database.
* **`app/templates/` & `app/static/`**: Separates HTML structure and CSS styling entirely from application logic.

### C. Configuration & Runtime
* **`config.py`**: Implements class-based configuration:
  * **`DevelopmentConfig`**: Enables debug mode (`DEBUG=True`) and uses a local database file `tasks_dev.db`.
  * **`TestingConfig`**: Enables testing mode (`TESTING=True`) and binds to an ephemeral in-memory database (`sqlite:///:memory:`).
  * **`ProductionConfig`**: Disables debug mode and retrieves the database connection string and secret key from OS environment variables.
* **`run.py`**: Entry point that invokes `create_app()` and launches the development server.
* **`requirements.txt`**: Specifies version-pinned dependencies (`Flask>=3.0.0`, `Flask-SQLAlchemy>=3.1.0`, `pytest>=8.0.0`).

---

## 5. Architectural Strengths & Security

1. **Concurrency and Data Integrity (ACID):**
   Utilizing SQLAlchemy over SQLite eliminates race conditions and file corruption risks associated with plain file-based storage (e.g., JSON).
2. **SQL Injection Prevention:**
   SQLAlchemy's query builder abstracts raw SQL execution and uses parameterized queries by default.
3. **REST Compliance & Mutation Safety:**
   State-modifying operations (Add, Toggle, Delete) strictly enforce HTTP POST requests rather than unsafe GET requests.
4. **Test Isolation:**
   Unit and integration tests run entirely against an isolated in-memory SQLite database, guaranteeing zero interference with development or production data.
5. **Horizontal Extensibility:**
   The modular architecture enables straightforward transitions to production database engines (e.g., PostgreSQL or MySQL) simply by updating `DATABASE_URL` in `config.py`.