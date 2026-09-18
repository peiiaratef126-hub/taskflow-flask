from app import db
from app.models import Task
from app.validators import is_meaningful_text


def test_index_empty_state(client):
    """GET / should render the dashboard with 200 and show empty state."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Personal Task Manager" in response.data
    assert b"No tasks found" in response.data


def test_add_task_success(client, app):
    """POST /tasks/add with valid title should create task and redirect to /."""
    response = client.post(
        "/tasks/add",
        data={"title": "Write Automated Tests"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Write Automated Tests" in response.data

    with app.app_context():
        task = db.session.scalar(db.select(Task).filter_by(title="Write Automated Tests"))
        assert task is not None
        assert task.done is False


def test_add_task_empty_title(client, app):
    """POST /tasks/add with empty title should reject and not create task."""
    response = client.post(
        "/tasks/add",
        data={"title": ""},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "يجب أن يتراوح طول المهمة بين 3 و 120 حرفاً.".encode("utf-8") in response.data

    with app.app_context():
        count = len(db.session.scalars(db.select(Task)).all())
        assert count == 0


def test_add_task_whitespace_only(client, app):
    """POST /tasks/add with only spaces should be rejected."""
    response = client.post(
        "/tasks/add",
        data={"title": "     "},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "يجب أن يتراوح طول المهمة بين 3 و 120 حرفاً.".encode("utf-8") in response.data

    with app.app_context():
        count = len(db.session.scalars(db.select(Task)).all())
        assert count == 0


def test_add_task_title_too_long(client, app):
    """POST /tasks/add with title exceeding 120 characters should be rejected."""
    long_title = "A" * 121
    response = client.post(
        "/tasks/add",
        data={"title": long_title},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "يجب أن يتراوح طول المهمة بين 3 و 120 حرفاً.".encode("utf-8") in response.data

    with app.app_context():
        assert len(db.session.scalars(db.select(Task)).all()) == 0


def test_reject_too_short(client, app):
    """POST /tasks/add with 1-2 characters should be rejected."""
    for short_title in ["a", "hi", "  ok "]:
        response = client.post(
            "/tasks/add",
            data={"title": short_title},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "يجب أن يتراوح طول المهمة بين 3 و 120 حرفاً.".encode("utf-8") in response.data

    with app.app_context():
        assert len(db.session.scalars(db.select(Task)).all()) == 0


def test_reject_symbols_only(client, app):
    """POST /tasks/add with only numbers/symbols and no letters should be rejected."""
    for invalid_title in ["###", "--!?", "12345", "$$$ @@@"]:
        response = client.post(
            "/tasks/add",
            data={"title": invalid_title},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "يرجى إدخال نص مهمة صالح يحتوي على أحرف واضحة.".encode("utf-8") in response.data

    with app.app_context():
        assert len(db.session.scalars(db.select(Task)).all()) == 0


def test_reject_gibberish_keyboard_mash(client, app):
    """Confirm meaningless keyboard-mash word 'kjfvbklmv' is rejected."""
    response = client.post(
        "/tasks/add",
        data={"title": "kjfvbklmv"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "الكلمات الإنجليزية يجب أن تحتوي على حروف علة مقروءة.".encode("utf-8") in response.data

    with app.app_context():
        assert len(db.session.scalars(db.select(Task)).all()) == 0


def test_reject_english_home_row_mash(client, app):
    """Confirm English home-row mash 'lkjasd' is strictly rejected."""
    response = client.post(
        "/tasks/add",
        data={"title": "lkjasd"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "النص المدخل يبدو كضغط عشوائي على لوحة المفاتيح.".encode("utf-8") in response.data

    with app.app_context():
        assert len(db.session.scalars(db.select(Task)).all()) == 0


def test_reject_arabic_home_row_oscillation(client, app):
    """Confirm Arabic home-row oscillation 'تنتننتسي' is strictly rejected."""
    response = client.post(
        "/tasks/add",
        data={"title": "تنتننتسي"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "النص يبدو كضغط متكرر على لوحة المفاتيح.".encode("utf-8") in response.data

    with app.app_context():
        assert len(db.session.scalars(db.select(Task)).all()) == 0


def test_reject_repeated_characters(client, app):
    """Confirm 3 or more identical consecutive characters are rejected."""
    for title in ["aaaa", "hhhh task", "Finish homework....."]:
        response = client.post(
            "/tasks/add",
            data={"title": title},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "النص يحتوي على أحرف مكررة بشكل غير طبيعي.".encode("utf-8") in response.data

    with app.app_context():
        assert len(db.session.scalars(db.select(Task)).all()) == 0


def test_reject_keyboard_runs(client, app):
    """Confirm continuous keyboard runs in English and Arabic are rejected."""
    for title in ["asdfg project", "qwerty review", "مهمة ضصثقف", "شسيبل عمل"]:
        response = client.post(
            "/tasks/add",
            data={"title": title},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "النص المدخل يبدو كضغط عشوائي على لوحة المفاتيح.".encode("utf-8") in response.data

    with app.app_context():
        assert len(db.session.scalars(db.select(Task)).all()) == 0


def test_reject_arabic_keyboard_mash(client, app):
    """Confirm Arabic keyboard-mashing word 'نتشسابتن' and home-row mashes are rejected."""
    for mash_title in ["نتشسابتن", "شسيبلاتن", "ضصثقفغ", "كمنتالبيسش"]:
        response = client.post(
            "/tasks/add",
            data={"title": mash_title},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "النص المدخل يبدو كضغط عشوائي على لوحة المفاتيح.".encode("utf-8") in response.data

    with app.app_context():
        assert len(db.session.scalars(db.select(Task)).all()) == 0


def test_reject_low_entropy_words(client, app):
    """Confirm oscillating repeated patterns and low variety words are rejected."""
    for title in ["ababab", "ananan", "تنتنتن"]:
        response = client.post(
            "/tasks/add",
            data={"title": title},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert "النص يبدو كضغط متكرر على لوحة المفاتيح.".encode("utf-8") in response.data

    with app.app_context():
        assert len(db.session.scalars(db.select(Task)).all()) == 0


def test_validator_unit_checks():
    """Direct unit tests for is_meaningful_text validator."""
    # Character repetition
    ok, err = is_meaningful_text("aaaa")
    assert not ok and err == "النص يحتوي على أحرف مكررة بشكل غير طبيعي."

    # Keyboard mash substring
    ok, err = is_meaningful_text("qwerty")
    assert not ok and err == "النص المدخل يبدو كضغط عشوائي على لوحة المفاتيح."

    ok, err = is_meaningful_text("مهمة ضصثقف")
    assert not ok and err == "النص المدخل يبدو كضغط عشوائي على لوحة المفاتيح."

    # English home-row mash: lkjasd
    ok, err = is_meaningful_text("lkjasd")
    assert not ok and err == "النص المدخل يبدو كضغط عشوائي على لوحة المفاتيح."

    # Arabic home-row oscillation: تنتننتسي
    ok, err = is_meaningful_text("تنتننتسي")
    assert not ok and err == "النص يبدو كضغط متكرر على لوحة المفاتيح."

    # Arabic keyboard mash: نتشسابتن
    ok, err = is_meaningful_text("نتشسابتن")
    assert not ok and err == "النص المدخل يبدو كضغط عشوائي على لوحة المفاتيح."

    # No vowel in 4+ letter word (e.g. kjfvbklmv)
    ok, err = is_meaningful_text("kjfvbklmv")
    assert not ok and err == "الكلمات الإنجليزية يجب أن تحتوي على حروف علة مقروءة."

    # 4+ consecutive consonants
    ok, err = is_meaningful_text("catchword")
    assert not ok and err == "الكلمة تحتوي على تتابع غير طبيعي لحروف ساكنة."

    # Oscillating pattern
    ok, err = is_meaningful_text("ababab")
    assert not ok and err == "النص يبدو كضغط متكرر على لوحة المفاتيح."

    # Low character variety (< 50%)
    ok, err = is_meaningful_text("task aabbaa")
    assert not ok and err == "النص يفتقر للتنوع الطبيعي في الحروف."

    # Valid English and Arabic
    ok, err = is_meaningful_text("Study for software architecture exam")
    assert ok and err == ""

    ok, err = is_meaningful_text("مهمة جديدة باللغة العربية")
    assert ok and err == ""


def test_add_arabic_task(client, app):
    """Confirm valid Arabic text passes validation and is stored in database."""
    arabic_title = "مهمة جديدة باللغة العربية"
    response = client.post(
        "/tasks/add",
        data={"title": arabic_title},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert arabic_title.encode("utf-8") in response.data

    with app.app_context():
        task = db.session.scalar(db.select(Task).filter_by(title=arabic_title))
        assert task is not None
        assert task.title == arabic_title


def test_prevent_duplicate_active_task(client, app):
    """Confirm adding the same active task twice is blocked case-insensitively."""
    task_title = "Review Architecture Docs"
    # First submission succeeds
    res1 = client.post(
        "/tasks/add",
        data={"title": task_title},
        follow_redirects=True,
    )
    assert res1.status_code == 200
    assert b"created successfully" in res1.data

    # Second submission (differing case and extra spaces) is blocked
    res2 = client.post(
        "/tasks/add",
        data={"title": "  review architecture docs  "},
        follow_redirects=True,
    )
    assert res2.status_code == 200
    assert "هذه المهمة مسجلة مسبقاً وقيد الانتظار.".encode("utf-8") in res2.data

    with app.app_context():
        tasks = db.session.scalars(
            db.select(Task).filter(db.func.lower(Task.title) == task_title.lower())
        ).all()
        assert len(tasks) == 1


def test_allow_duplicate_completed_task(client, app):
    """Confirm adding a task whose prior instance is completed (done=True) succeeds."""
    task_title = "Submit Final Project"
    res1 = client.post(
        "/tasks/add",
        data={"title": task_title},
        follow_redirects=True,
    )
    assert res1.status_code == 200

    # Mark first instance as completed
    with app.app_context():
        task = db.session.scalar(db.select(Task).filter_by(title=task_title))
        task.done = True
        db.session.commit()

    # Re-adding the same title should now be permitted
    res2 = client.post(
        "/tasks/add",
        data={"title": task_title},
        follow_redirects=True,
    )
    assert res2.status_code == 200
    assert b"created successfully" in res2.data

    with app.app_context():
        tasks = db.session.scalars(
            db.select(Task).filter_by(title=task_title)
        ).all()
        assert len(tasks) == 2
        assert any(t.done for t in tasks)
        assert any(not t.done for t in tasks)


def test_toggle_task_status(client, app, sample_task):
    """POST /tasks/<id>/toggle should flip done between False and True."""
    # Toggle from False to True
    res1 = client.post(f"/tasks/{sample_task}/toggle", follow_redirects=True)
    assert res1.status_code == 200
    with app.app_context():
        task = db.session.get(Task, sample_task)
        assert task.done is True

    # Toggle from True back to False
    res2 = client.post(f"/tasks/{sample_task}/toggle", follow_redirects=True)
    assert res2.status_code == 200
    with app.app_context():
        task = db.session.get(Task, sample_task)
        assert task.done is False


def test_toggle_nonexistent_task(client):
    """POST /tasks/<id>/toggle for non-existent id should return 404."""
    response = client.post("/tasks/99999/toggle")
    assert response.status_code == 404


def test_delete_task(client, app, sample_task):
    """POST /tasks/<id>/delete should remove task from database."""
    response = client.post(f"/tasks/{sample_task}/delete", follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        task = db.session.get(Task, sample_task)
        assert task is None


def test_delete_nonexistent_task(client):
    """POST /tasks/<id>/delete for non-existent id should return 404."""
    response = client.post("/tasks/99999/delete")
    assert response.status_code == 404


def test_tasks_ordering_descending(client, app):
    """Tasks should be listed in descending order by created_at."""
    with app.app_context():
        t1 = Task(title="First Task")
        t2 = Task(title="Second Task")
        db.session.add_all([t1, t2])
        db.session.commit()

    response = client.get("/")
    assert response.status_code == 200
    content = response.data.decode("utf-8")
    pos_second = content.find("Second Task")
    pos_first = content.find("First Task")
    assert pos_second < pos_first


def test_model_representation_and_dict(app):
    """Verify Task.__repr__ and Task.to_dict serialization."""
    with app.app_context():
        task = Task(title="Model Serialization Test", done=True)
        db.session.add(task)
        db.session.commit()

        assert repr(task) == f"<Task id={task.id} title='Model Serialization Test' done=True>"
        data = task.to_dict()
        assert data["id"] == task.id
        assert data["title"] == "Model Serialization Test"
        assert data["done"] is True
        assert data["created_at"] is not None


def test_rest_mutation_safety(client, sample_task):
    """GET requests on mutation endpoints should return 405 Method Not Allowed."""
    assert client.get("/tasks/add").status_code == 405
    assert client.get(f"/tasks/{sample_task}/toggle").status_code == 405
    assert client.get(f"/tasks/{sample_task}/delete").status_code == 405
