from app import app
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.schema import User, Task, TaskStatus
from app.models.controller import hash_password, verify_password
from datetime import datetime


@app.route(
    "/",
)
@app.route(
    "/login",
    methods=["GET", "POST"],
)
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))
        valid_password = verify_password(user.password_hash, password)

        if valid_password:
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.", "error")

    return render_template("login.html", title="Student Study")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "error")
            return redirect(url_for("register"))

        hashed_password = hash_password(password)
        new_user = User(email=email, name=name, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/dashboard")
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    chart_data = [{
        "id": task.id,
        "task_name": task.task_name,
        "start_date": task.start_date.isoformat() if task.start_date else None,
        "end_date": task.end_date.isoformat() if task.end_date else None,
        "category": task.category,
    } for task in tasks if task.start_date is not None and task.end_date is not None ]
    return render_template("dashboard.html", tasks=tasks, task_statuses=TaskStatus, chart_data=chart_data)


@app.route("/add_task", methods=["POST"])
@login_required
def add_task():
    task_name = request.form["task_name"]
    category = request.form["category"]  # New field
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    # Parse dates from string input
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
    
    new_task = Task(
        user_id=current_user.id,
        task_name=task_name,
        status=TaskStatus.Not_Started,
        category=category,
        start_date=(start_date),
        end_date=end_date,
    )
    db.session.add(new_task)
    db.session.commit()
    flash("Task added successfully!", "success")
    return redirect(url_for("dashboard"))


@app.route("/update_task/<int:task_id>", methods=["POST"])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)  # Ensure users can only modify their own tasks

    task.status = TaskStatus(request.form["status"])
    db.session.commit()
    flash("Task updated successfully!", "success")
    return redirect(url_for("dashboard"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))
