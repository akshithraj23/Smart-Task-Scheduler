# Smart-Task-Scheduler
A simple yet intelligent task manager that helps you add, prioritize, and delete tasks easily. It even supports voice input for hands-free task management! 

🚀 Features

✅ Add Tasks – Enter tasks manually or use voice input.

✅ Set Priority – Choose between High, Medium, or Low priority.

✅ Reminders – Add a specific date and time for task reminders.

✅ Delete Tasks – Remove completed or unwanted tasks with one click.

✅ Real-time Updates – The task list updates dynamically.


🛠️ Technologies Used

Python (Flask) – Backend framework for handling requests.

JavaScript – Frontend logic and dynamic updates.

HTML & CSS – UI design and layout.

MySQL (SQLAlchemy) – Database to store tasks.

SpeechRecognition API – Enables voice input for tasks.


🎯 How to Run the Project

1️⃣ Install Dependencies

Make sure you have Python and MySQL installed.

2️⃣ Set Up the Database

Create a MySQL database called smart_todo and update your app.py with the correct credentials:

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://username:password@localhost/smart_todo"

Then, initialize the database:

from app import db

db.create_all()

3️⃣ Run the Flask App

Start the Flask server with:

python app.py

4️⃣ Open the App

Go to your browser and open:

👉 http://127.0.0.1:5000/

Start the Flask server with:

🎤 Voice Input

Click the microphone button 🎤 to add a task using your voice. The system will recognize your speech and input it into the task field automatically.

❌ Deleting a Task

Click the ❌ button next to a task to delete it from the list and database.

🛠️ Future Enhancements

🔹 Task Completion – Mark tasks as "Done" instead of deleting them.

🔹 Notifications – Set up real-time reminders for tasks.

🔹 User Authentication – Allow multiple users to manage their tasks separately.

🔹 Working on voice recognition.



