# Text-to-SQL Converter

A lightweight, beginner-friendly web application built with Python and Flask that translates natural-language questions into SQL queries using Google's Gemini API (`gemini-3.5-flash-lite`).

The application features prompt-based guardrails, input validation, post-generation SQL sanitization, and a clean web interface with one-click query copying.

---

## Features

- **Natural Language to SQL Generation**: Converts plain English queries (e.g., *"Show students whose marks are greater than 80"*) into standard SQL syntax.
- **Schema-Aware Prompting**: Guides the Gemini model with a predefined database schema and strict generation constraints.
- **Empty-Input Validation**: Validates form inputs on the server before dispatching requests to the Gemini API.
- **Invalid-Column Detection**: Prompts the LLM to return a flag if requested attributes do not exist in the schema, displaying a clear warning to the user.
- **Out-of-Scope Filtering**: Identifies questions unrelated to the target database table and prompts the user for relevant input.
- **SQL Sanitization**: Strips Markdown code blocks (````sql ... ````) from the LLM response to ensure clean query output.
- **Table Verification**: Performs a sanity check ensuring that only the authorized `students` table is referenced.
- **State Preservation**: Keeps the user's submitted question in the textarea after generation for easy modification.
- **One-Click Clipboard Copy**: Built-in JavaScript button to quickly copy the generated SQL query.
- **Resilient Error Handling**: Catches API failures and network issues gracefully to prevent application crashes.

---

## Tech Stack

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python 3 | Core programming language |
| **Web Framework** | Flask | Handles HTTP routing (`GET`/`POST`) and template rendering |
| **AI / LLM** | Google Gemini API (`gemini-3.5-flash-lite`) | Natural language understanding and SQL translation |
| **SDK** | `google-genai` | Official Google GenAI Python client |
| **Configuration** | `python-dotenv` | Manages environment variables securely from `.env` |
| **Frontend** | HTML5, CSS, JavaScript | Interactive web UI with clipboard integration |
| **Version Control** | Git & GitHub | Source code management |

---

## How It Works

```text
User enters a natural-language question
                 ↓
      Flask receives POST request
                 ↓
      Empty / whitespace check?
       ├── [Empty] ──> Display "Please enter a question."
       └── [Valid]
                 ↓
  Construct prompt with schema & rules
                 ↓
    Call Google Gemini API
                 ↓
       Parse model response:
       ├── INVALID_QUESTION ──> "Invalid question: the requested column does not exist."
       ├── OUT_OF_SCOPE     ──> "Out of scope: the question is not related to the students table."
       └── [Valid SQL]
                 ↓
   Strip Markdown fences (```sql)
                 ↓
   Verify 'students' table is present
                 ↓
   Render generated SQL in browser
                 ↓
   User can copy SQL to clipboard
```

---

## Current Database Schema

The application is configured around a single demo table representing student records:

### Table: `students`

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Unique identifier for each student |
| `name` | VARCHAR | Full name of the student |
| `age` | INTEGER | Student's age |
| `marks` | INTEGER / FLOAT | Academic score or marks scored |
| `city` | VARCHAR | City of residence |

---

## Project Structure

```text
Text to Sql project/
├── templates/
│   └── index.html          # Web frontend (form, SQL display, copy button)
├── .env                    # Local environment variables (API keys - gitignored)
├── .gitignore              # Ignores venv, .env, and Python cache files
├── app.py                  # Main Flask application and Gemini API logic
├── geminiapitest.py        # Standalone test script for Gemini API verification
└── README.md               # Project documentation
```

---

## Installation and Setup

### Prerequisites
- Python 3.10 or higher installed on your system
- A Google Gemini API key (obtainable from [Google AI Studio](https://aistudio.google.com/))
- Git installed on your system

### 1. Clone the repository
```bash
git clone https://github.com/om-saxena34/Text-to-SQL-Project.git
cd Text-to-SQL-Project
```

### 2. Set up a virtual environment

- **On Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

- **On Windows (Command Prompt):**
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate.bat
  ```

- **On macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install dependencies
```bash
pip install flask google-genai python-dotenv
```

---

## Environment Variables

Create a file named `.env` in the root directory of the project:

```env
GEMINI_API_KEY="your_actual_gemini_api_key_here"
```

> [!IMPORTANT]
> Never commit your `.env` file or expose your API keys in public repositories. The `.env` file is already listed in `.gitignore` to prevent accidental commits.

---

## How to Run

### 1. (Optional) Test the Gemini API connection
You can run the standalone verification script to verify that your API key and connection are working:
```bash
python geminiapitest.py
```

### 2. Start the Flask application
```bash
python app.py
```

### 3. Open the application in your browser
Navigate to:
```text
http://127.0.0.1:5000
```

Type a question into the text area, click **Convert to SQL**, and view or copy the resulting SQL query.

---

## Example Questions and Generated SQL

| User Question | Generated SQL Query | Notes |
| :--- | :--- | :--- |
| *"Show all students whose marks are greater than 80"* | `SELECT * FROM students WHERE marks > 80;` | Filtering condition |
| *"List the names and cities of all students"* | `SELECT name, city FROM students;` | Specific column projection |
| *"Find students who live in Delhi"* | `SELECT * FROM students WHERE city = 'Delhi';` | String equality filter |
| *"Show the top 5 students sorted by marks"* | `SELECT * FROM students ORDER BY marks DESC LIMIT 5;` | Ordering and row limiting |
| *"Count the total number of students in each city"* | `SELECT city, COUNT(*) FROM students GROUP BY city;` | Aggregation & grouping |

---

## Error Handling & Validation

The application applies validation across multiple stages of execution:

1. **Pre-flight Input Validation**:
   - If the user submits an empty or whitespace-only query, the application returns `"Please enter a question."` without making an API request.
2. **Schema Integrity Guardrails**:
   - If the user requests a column not in the schema (e.g., *"Show students by email"*), the model returns `INVALID_QUESTION`, which is displayed as:
     `Invalid question: the requested column does not exist.`
3. **Domain Relevance Guardrails**:
   - If the user asks a question unrelated to the student records (e.g., *"What is the capital of France?"*), the model returns `OUT_OF_SCOPE`, which is displayed as:
     `Out of scope: the question is not related to the students table.`
4. **Table Name Sanitization**:
   - Verifies that the string `students` is present in the generated SQL. If absent, the query is rejected with:
     `Invalid SQL: only the students table is allowed.`
5. **API Exception Handling**:
   - In case of network errors, invalid keys, or quota issues with Gemini, a `try/except` block logs the exception to the server console and displays a friendly notice to the user:
     `Something went wrong while generating SQL. Please try again.`

---

## Current Limitations

To maintain clear project scope, please note the following current boundaries:
- **No Direct Database Execution**: The app generates and displays SQL syntax; it does not connect to or execute queries against a live MySQL or SQLite database.
- **No Query Results Display**: Because no live database is connected, no data rows or query outputs are retrieved.
- **Single-Table Scope**: The model is restricted strictly to the `students` table schema.
- **Basic String-Based Validation**: Verification relies on prompt constraints and substring checks rather than a full SQL AST parser.
- **Development Server**: The application runs via the built-in Flask development server and is not configured for production deployment (WSGI/Gunicorn).
- **No User Management**: Does not include user authentication, sessions, or query history persistence.

---

## Future Improvements

The following items represent planned enhancements for subsequent phases:

- [ ] **Live Database Integration**: Connect the backend to a local or cloud-hosted MySQL / SQLite database.
- [ ] **Query Execution & Result Display**: Execute the generated SQL query safely and render results in a structured HTML table.
- [ ] **Advanced SQL Parsing & Security**: Integrate a SQL parser (such as `sqlglot`) to validate syntax and block destructive operations (`DROP`, `DELETE`, `UPDATE`, `ALTER`).
- [ ] **Multi-Table & Custom Schemas**: Support multiple relational tables, table joins (`INNER JOIN`, `LEFT JOIN`), and user-defined schemas.
- [ ] **Enhanced UI/UX**: Introduce a modern responsive design with syntax highlighting, dark mode toggle, and execution time indicators.
- [ ] **Production Deployment**: Containerize with Docker and deploy to a cloud platform (such as Render, Railway, or AWS).

---

## Learning Outcomes

Building this project provided hands-on experience with:
- **LLM Prompt Engineering**: Designing system instructions with explicit boundaries, output formatting rules, and sentinel tokens (`INVALID_QUESTION`, `OUT_OF_SCOPE`).
- **Full-Stack Flask Architecture**: Managing HTTP request lifecycles (`GET`/`POST`), form processing, and dynamic template rendering with Jinja2.
- **Defensive API Integration**: Handling asynchronous AI services with fallback states, error catches, and response sanitization.
- **Environment & Secrets Management**: Safeguarding API keys using environment variables and `.gitignore`.
- **Client-Side Clipboard Interactions**: Integrating vanilla JavaScript for clipboard copy actions directly from rendered templates.

---

## Author

**Om Saxena**
- GitHub: [@om-saxena34](https://github.com/om-saxena34)
- Repository: [Text-to-SQL-Project](https://github.com/om-saxena34/Text-to-SQL-Project)