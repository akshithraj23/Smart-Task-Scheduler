"""
Flask-based Smart To-Do List Application

This application allows users to add, view, and delete tasks with an AI-prioritized system.
It uses Flask for backend functionality, SQLAlchemy for database management, and supports
reminders for tasks.

Features:
- Add tasks with content, priority (low, medium, high), and optional reminder time.
- View all tasks stored in the database.
- Delete tasks based on content.
"""

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)

# Configure MySQL database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:sakrj@localhost/smart_todo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database instance
db = SQLAlchemy(app)

# Define Task model representing the tasks table in the database
class Task(db.Model):
    """
    Task model representing a to-do item.

    Attributes:
    - id (int): Unique identifier for each task.
    - content (str): Description of the task.
    - priority (int): Priority level (1 - low, 2 - medium, 3 - high).
    - remind_at (datetime, optional): Date and time to remind the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=2)  # Default priority: Medium
    remind_at = db.Column(db.DateTime, nullable=True)  # Optional reminder time

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    """
    Home route that retrieves all tasks from the database and displays them.

    Returns:
        Rendered HTML template with tasks data.
    """
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

# Priority mapping dictionary to convert string values to integer levels
priority_mapping = {"low": 1, "medium": 2, "high": 3}

@app.route("/add_task", methods=["POST"])
def add_task():
    """
    API endpoint to add a new task.

    Receives JSON data with task details (content, priority, remind_at),
    validates input, converts data, and stores it in the database.

    Returns:
        JSON response containing the updated list of tasks.
    """
    data = request.get_json()
    
    # Extract task details from request
    content = data.get("content", "").strip()
    priority_str = data.get("priority", "medium").lower()  # Default priority: Medium
    remind_at = data.get("remind_at", None)
    
    print(f"Received data - Content: {content}, Priority: {priority_str}, Remind At: {remind_at}")  # Debugging output

    if not content:
        return jsonify({"error": "Task content cannot be empty"}), 400  # Validation check

    # Convert priority string to integer value
    priority_value = priority_mapping.get(priority_str, 2)  # Default to 2 (medium) if not found

    # Convert remind_at to datetime object if provided
    remind_at_datetime = datetime.fromisoformat(remind_at) if remind_at else None

    # Create and store new task in the database
    new_task = Task(content=content, priority=priority_value, remind_at=remind_at_datetime)
    db.session.add(new_task)
    db.session.commit()

    # Retrieve updated task list after insertion
    tasks = Task.query.all()
    
    return jsonify({
        "tasks": [
            {
                "id": task.id,
                "content": task.content,
                "priority": task.priority,
                "remind_at": task.remind_at.strftime('%Y-%m-%d %H:%M') if task.remind_at else None
            }
            for task in tasks
        ]
    })

@app.route("/delete_task", methods=["POST"])
def delete_task():
    """
    API endpoint to delete a task by content.

    Receives JSON data containing the task content, finds the corresponding
    task in the database, deletes it, and returns the updated task list.

    Returns:
        JSON response containing the updated list of tasks.
    """
    task_content = request.json.get("task")
    task = Task.query.filter_by(content=task_content).first()
    
    if task:
        db.session.delete(task)
        db.session.commit()

    # Retrieve updated task list after deletion
    tasks = Task.query.all()
    
    return jsonify({
        "tasks": [
            {
                "id": task.id,
                "content": task.content,
                "priority": task.priority,
                "remind_at": task.remind_at.strftime('%Y-%m-%d %H:%M') if task.remind_at else None
            }
            for task in tasks
        ]
    })

if __name__ == "__main__":
    app.run(debug=True)
