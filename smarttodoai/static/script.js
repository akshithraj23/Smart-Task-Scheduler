/**
 * Smart To-Do List Script
 * 
 * This script handles adding tasks, deleting tasks, updating the task list dynamically, 
 * and voice input functionality using the Web Speech API.
 */

// Event listeners for button clicks and task deletions
document.getElementById("add-task-btn").addEventListener("click", addTask); // Listens for clicks on "Add Task" button
document.getElementById("voice-input-btn").addEventListener("click", startVoiceRecognition); // Listens for voice input button click
document.getElementById("task-list").addEventListener("click", deleteTask); // Listens for clicks on delete buttons in the task list

/**
 * Adds a new task by sending data to the backend via a POST request.
 * Retrieves task content, priority, and reminder time from input fields.
 */
function addTask() {
    // Get references to input fields
    const taskInput = document.getElementById("task-input");
    const priorityInput = document.getElementById("priority-input");
    const remindAtInput = document.getElementById("remind-at-input");

    // Extract values from input fields
    const content = taskInput.value.trim();
    const priority = priorityInput.value;
    const remindAt = remindAtInput.value;

    // Validate that the task is not empty
    if (!content) {
        alert("Task content cannot be empty!");
        return;
    }

    // Send a POST request to the backend to add the task
    fetch("/add_task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content, priority, remind_at: remindAt }),
    })
    .then((response) => response.json()) // Convert response to JSON
    .then((data) => {
        updateTaskList(data.tasks); // Update the task list with the new task
        taskInput.value = ""; // Clear input fields after adding task
        remindAtInput.value = "";
    })
    .catch((error) => console.error("Error adding task:", error)); // Log any errors
}

/**
 * Deletes a task when the delete button is clicked.
 * Identifies the task using the 'data-task' attribute and sends a request to remove it from the backend.
 */
function deleteTask(event) {
    // Check if the clicked element is a delete button
    if (event.target.classList.contains("delete-btn")) {
        const task = event.target.getAttribute("data-task"); // Get task content from button attribute

        // Send a POST request to delete the task
        fetch("/delete_task", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ task }),
        })
        .then((response) => response.json()) // Convert response to JSON
        .then((data) => {
            console.log("Updated task list:", data.tasks); // Debugging: Log updated tasks
            updateTaskList(data.tasks); // Update task list after deletion
        })
        .catch((error) => console.error("Error deleting task:", error)); // Log any errors
    }
}

/**
 * Updates the task list dynamically in the UI.
 * Converts task data into HTML and inserts it into the task list.
 * 
 * @param {Array} tasks - List of tasks retrieved from the backend
 */
function updateTaskList(tasks) {
    const taskList = document.getElementById("task-list"); // Get the task list element
    taskList.innerHTML = tasks
        .map((task) => `
            <li>
                <span>${task.content}</span>
                <span class="priority ${task.priority === 1 ? 'low' : task.priority === 2 ? 'medium' : 'high'}">
                    ${task.priority === 1 ? 'Low' : task.priority === 2 ? 'Medium' : 'High'}
                </span>
                <span class="remind-at">${task.remind_at ? new Date(task.remind_at).toLocaleString() : 'No reminder'}</span>
                <button class="delete-btn" data-task="${task.content}">❌</button>
            </li>
        `)
        .join(""); // Join the task list items into a single string
}

/**
 * Starts voice recognition to input tasks using the Web Speech API.
 * Captures spoken input and places it into the task input field.
 */
function startVoiceRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)(); // Create speech recognition instance
    recognition.lang = "en-US"; // Set language to English
    recognition.start(); // Start voice recognition

    // Event triggered when voice input is recognized
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript; // Get transcribed text
        document.getElementById("task-input").value = transcript; // Set input field to recognized text
    };
}
