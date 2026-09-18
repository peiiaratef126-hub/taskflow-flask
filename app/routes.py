from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Task
from app.validators import is_meaningful_text

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def index():
    """Display task dashboard with all tasks ordered by creation date descending."""
    tasks = db.session.scalars(
        db.select(Task).order_by(Task.created_at.desc())
    ).all()
    total_count = len(tasks)
    completed_count = sum(1 for t in tasks if t.done)
    pending_count = total_count - completed_count
    return render_template(
        "index.html",
        tasks=tasks,
        total_count=total_count,
        completed_count=completed_count,
        pending_count=pending_count,
    )


@main_bp.route("/tasks/add", methods=["POST"])
def add_task():
    """Validate user input, prevent duplicates, and create a new task."""
    title = request.form.get("title", "").strip()

    # 1. Whitespace & Length Limits (3 <= len <= 120)
    if not (3 <= len(title) <= 120):
        flash("يجب أن يتراوح طول المهمة بين 3 و 120 حرفاً.", "warning")
        return redirect(url_for("main.index"))

    # 2. Language-Agnostic Meaningful Text Check (Arabic & English Friendly)
    if not any(char.isalpha() for char in title):
        flash("يرجى إدخال نص مهمة صالح يحتوي على أحرف واضحة.", "warning")
        return redirect(url_for("main.index"))

    # 3. Anti-Gibberish & Readability Validation
    is_valid, error_msg = is_meaningful_text(title)
    if not is_valid:
        flash(error_msg, "warning")
        return redirect(url_for("main.index"))

    # 4. Duplicate Active Task Prevention (case-insensitive, trimmed, active only)
    existing_active_task = Task.query.filter(
        db.func.lower(Task.title) == title.lower(),
        Task.done == False
    ).first()
    if existing_active_task:
        flash("هذه المهمة مسجلة مسبقاً وقيد الانتظار.", "warning")
        return redirect(url_for("main.index"))

    task = Task(title=title)
    db.session.add(task)
    db.session.commit()
    flash(f"Task '{title}' created successfully.", "success")
    return redirect(url_for("main.index"))


@main_bp.route("/tasks/<int:id>/toggle", methods=["POST"])
def toggle_task(id):
    """Toggle completion status (done) of a specific task."""
    task = db.get_or_404(Task, id)
    task.done = not task.done
    db.session.commit()
    status_label = "completed" if task.done else "marked pending"
    flash(f"Task '{task.title}' {status_label}.", "info")
    return redirect(url_for("main.index"))


@main_bp.route("/tasks/<int:id>/delete", methods=["POST"])
def delete_task(id):
    """Permanently delete a task from the database."""
    task = db.get_or_404(Task, id)
    task_title = task.title
    db.session.delete(task)
    db.session.commit()
    flash(f"Task '{task_title}' was deleted successfully.", "danger")
    return redirect(url_for("main.index"))
