# TaskFlow - Flask Task Manager

A modern, production-grade web application for personal task management built with Python and Flask. Designed using clean software architecture principles, featuring the Application Factory pattern, modular Blueprints, ACID-compliant persistence via SQLAlchemy, an automated Pytest test suite, and continuous integration via GitHub Actions.

---

## Architecture & Design Highlights

* **Application Factory Pattern (`create_app`)**: Enables clean configuration decoupling and straightforward environment switching (Development, Testing, Production).
* **Modular Routing**: Routes are isolated within Flask Blueprints for maintainability and scalability.
* **Relational Data Layer**: Uses Flask-SQLAlchemy with SQLite to provide ACID guarantees and eliminate concurrency issues.
* **Automated Testing Suite**: Complete unit and integration test coverage using `pytest` and isolated in-memory databases (`:memory:`).
* **CI/CD Integration**: Built-in GitHub Actions workflow running tests automatically on every `push` and `pull_request`.
* **Detailed Architectural Documentation**: See [ARCHITECTURE.md](ARCHITECTURE.md) for full architectural diagrams and design specifications.

---

## Project Structure

```text
flask-task-manager/
├── .github/
│   └── workflows/
│       └── tests.yml        # GitHub Actions CI automated testing pipeline
├── app/
│   ├── __init__.py          # Application factory & extension initialization
│   ├── models.py            # SQLAlchemy Task data model
│   ├── routes.py            # Web routes and CRUD controller logic (Blueprint)
│   ├── templates/           # Jinja2 HTML templates
│   │   ├── base.html        # Main layout, header, and flash message container
│   │   └── index.html       # Task dashboard and input forms
│   └── static/              # Static assets
│       └── css/style.css    # Custom CSS styles
├── tests/
│   ├── __init__.py          # Test package initializer
│   ├── conftest.py          # Pytest fixtures and in-memory test database setup
│   └── test_tasks.py        # Automated test cases
├── .env.example             # Example environment variable configurations
├── .gitignore               # Ignored build, database, and cache files
├── ARCHITECTURE.md          # Comprehensive software architecture document
├── config.py                # Configuration classes (Dev, Test, Prod)
├── LICENSE                  # Open-source MIT License
├── pytest.ini               # Pytest settings and discovery rules
├── README.md                # Project documentation and quickstart guide
├── requirements.txt         # Project dependencies
└── run.py                   # Local development server entrypoint
```

---

## Getting Started

### Prerequisites
* Python 3.10+
* `pip` (Python package installer)
* Git

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/peiiaratef126-hub/taskflow-flask.git
   cd taskflow-flask
   ```

2. **Create and activate a virtual environment:**
   * **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   * **Windows (Command Prompt / PowerShell):**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # On Windows:
   copy .env.example .env

   # On Linux / macOS:
   cp .env.example .env
   ```

### Running Automated Tests

Run the full automated test suite using pytest:
```bash
pytest
```
*Tests execute against an isolated in-memory SQLite database, leaving your development database untouched.*

### Running the Application

Launch the local development server:
```bash
python run.py
```
Open your browser and navigate to:
`http://127.0.0.1:5000`

---

## API & Route Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Displays the task dashboard and all current tasks. |
| `POST` | `/tasks/add` | Validates input and creates a new task. |
| `POST` | `/tasks/<id>/toggle` | Toggles the completion status of a task. |
| `POST` | `/tasks/<id>/delete` | Deletes a task from the database. |

---

## Continuous Integration (CI)

Every commit pushed to `main` triggers a GitHub Actions runner defined in `.github/workflows/tests.yml`:
1. Checks out the code.
2. Sets up the Python matrix environment.
3. Installs dependencies from `requirements.txt`.
4. Runs `pytest`.

---

## License

This project is licensed under the terms of the MIT License.