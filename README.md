# Text-to-SQL Project

A simple, beginner-friendly learning project designed to convert natural-language questions into SQL queries using Python, Flask, and an LLM API.

---

## Project Description

Many developers and analysts want an intuitive way to interact with databases without manually writing SQL queries for every request. This project explores the fundamentals of web development and natural language processing by building a simple web application that accepts human language questions and translates them into valid SQL queries.

---

## Current Project Status

> [!NOTE]
> **Work in Progress**: This project is in its foundational setup phase. The basic Flask backend and HTML frontend are connected to receive user input, but **Text-to-SQL conversion is NOT yet implemented**. Currently, the application accepts user input and echoes it back.

---

## Features Completed

- [x] Python virtual environment configured using `venv`.
- [x] Flask framework installed and configured.
- [x] Basic web application created in `app.py`.
- [x] Flask local development server running successfully.
- [x] HTML frontend created using `templates/index.html`.
- [x] Textarea form input for entering natural-language questions.
- [x] Form submission configured with HTTP `POST` requests.
- [x] Flask backend receives question input using `request.form["question"]`.
- [x] Flask displays the received question back to the user.
- [x] Fundamental understanding and routing of `GET` and `POST` requests.
- [x] Git version control initialized.
- [x] `.gitignore` configured to ignore `venv/`, `__pycache__/`, `*.pyc`, and `.env`.
- [x] Code pushed to GitHub repository.

---

## Planned Features / Roadmap

### Step 4 — Learn Basic SQL
- Core SQL commands: `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `ORDER BY`
- Filtering conditions and basic comparison operators
- Database terminology: tables, columns, rows, and data types

### Step 5 — Learn LLM & API Basics
- Core concepts: What is an LLM and how web APIs work
- Structuring API requests and handling JSON responses
- Managing secrets securely with environment variables (`.env`)
- Security practice: Never expose API keys in public Git repositories

### Step 6 — Implement Text-to-SQL Conversion
- Connect Flask backend to an LLM API.
- Pass database schema / table structures into the model prompt.
- Instruct the model to generate accurate SQL based on user queries.
- Return the generated SQL query back to the frontend.
- **Example Scenario**:
  - **User Input:** `"Show all students whose marks are greater than 80"`
  - **Expected Generated SQL:**
    ```sql
    SELECT * FROM students WHERE marks > 80;
    ```

### Step 7 — Application Improvements
- Clean UI layout to clearly display generated SQL queries.
- Input validation (handle empty submissions and whitespace).
- Graceful error handling for API timeouts or failures.
- Enhance HTML and CSS design while keeping the codebase lightweight and minimal.

### Step 8 — Testing and Documentation
- Test edge cases, unsupported queries, and various question formats.
- Refine system prompts to improve SQL query generation accuracy.
- Update documentation with usage examples and project walkthroughs.
- Prepare clear explanations of the architecture for interview demonstrations.

---

## Technology Stack

- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS (Vanilla), JavaScript (if needed for copy/interactions)
- **Query Language:** SQL
- **AI Integration:** LLM API (planned in upcoming steps)
- **Version Control:** Git, GitHub

---

## Current Project Structure

```text
Text to Sql project/
│
├── venv/
├── templates/
│   └── index.html
├── .gitignore
├── app.py
└── README.md
```

---

## How the Application Currently Works

```text
Browser
   ↓
HTML Form
   ↓
POST Request
   ↓
Flask
   ↓
request.form["question"]
   ↓
Question returned to browser
```

1. The user opens the home page (`/`) in the browser.
2. The browser renders `templates/index.html` displaying a question form.
3. The user types a question (e.g., *"Show all students whose marks are greater than 80"*) into the textarea and submits the form.
4. The browser sends a `POST` request to Flask.
5. Flask extracts the string using `request.form["question"]`.
6. Flask returns the plain text question directly back to the browser.

---

## Planned Final Workflow

```text
User enters natural-language question
        ↓
HTML frontend
        ↓
Flask backend
        ↓
LLM API + database schema
        ↓
Generated SQL query
        ↓
Flask response
        ↓
SQL displayed to user
```

1. The user inputs their natural-language query in the frontend form.
2. The frontend submits the query to Flask backend via `POST`.
3. Flask prepares a prompt combining the user's question and the database schema.
4. Flask sends the prompt to an LLM API.
5. The LLM generates the corresponding SQL query.
6. Flask receives the query and renders it cleanly back in the user interface.

---

## How to Run the Project Locally

### 1. Clone the repository
```bash
git clone https://github.com/om-saxena34/Text-to-SQL-Project.git
cd Text-to-SQL-Project
```

### 2. Set up a virtual environment
- **On Windows:**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```
- **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install dependencies
```bash
pip install flask
```

### 4. Run the Flask application
```bash
python app.py
```

### 5. Access the application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## GitHub Repository

Source code and project updates are hosted on GitHub:
- [https://github.com/om-saxena34/Text-to-SQL-Project](https://github.com/om-saxena34/Text-to-SQL-Project)

---

## Future Improvements

- Add support for custom table schemas.
- Add a "Copy Query" button for generated SQL.
- Implement syntax highlighting for SQL output.
- Add sample query templates for quick user testing.
- Optional integration with a local SQLite database to test and execute generated queries.