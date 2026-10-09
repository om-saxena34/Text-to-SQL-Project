from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import mysql.connector
import os
import re
import sqlglot
from sqlglot import exp

load_dotenv()

app = Flask(__name__)

client = genai.Client()

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return connection


def is_safe_select_query(query):
    if not query or not isinstance(query, str):
        return False

    cleaned = query.strip()

    # Reject SQL comments
    if "--" in cleaned or "/*" in cleaned or "*/" in cleaned or "#" in cleaned:
        return False

    try:
        # Parse the query using MySQL syntax
        statements = sqlglot.parse(cleaned, read="mysql")

        # Require exactly one statement
        if len(statements) != 1 or statements[0] is None:
            return False

        tree = statements[0]

        # Only allow SELECT queries
        if not isinstance(tree, exp.Select):
            return False

        # Reject joins, unions, subqueries, and CTEs
        if tree.find(exp.Join) or tree.find(exp.Union):
            return False

        if tree.find(exp.Subquery) or tree.find(exp.CTE):
            return False

        # Allow only the students table
        tables = list(tree.find_all(exp.Table))

        if not tables:
            return False

        if any(table.name.lower() != "students" for table in tables):
            return False

        # Allow only known columns
        allowed_columns = {"id", "name", "age", "marks", "city"}

        for column in tree.find_all(exp.Column):
            if column.name != "*":
                if column.name.lower() not in allowed_columns:
                    return False

            # Reject qualified columns that reference another table alias
            if column.table and column.table.lower() != "students":
                return False

        # Allow only these functions
        allowed_functions = {
            "COUNT", "AVG", "SUM", "MIN", "MAX", "ROUND"
        }

        for function in tree.find_all(exp.Func):
            function_name = function.sql_name().upper()

            if function_name not in allowed_functions:
                return False

        return True

    except Exception:# If parsing or validation fails,
        return False

@app.route("/", methods=["GET", "POST"])
def home():

    sql = ""
    question = ""
    columns = []
    rows = []
    db_error = ""
    query_executed = False

    if request.method == "POST":

        question = request.form["question"]

        # Check if question is empty
        if not question.strip():
            sql = "Please enter a question."
            return render_template(
                "index.html",
                sql=sql,
                question=question,
                columns=columns,
                rows=rows,
                db_error=db_error,
                query_executed=query_executed
            )

        prompt = f"""
Convert the following question into SQL.

Table: students
Columns: id, name, age, marks, city

Rules:
- Use only the table and columns provided above.
- If the question asks for a column that does not exist, return exactly:
INVALID_QUESTION
- If the question is not related to the students table, return exactly:
OUT_OF_SCOPE
- Return only the SQL query if the question is valid.
- Do not use Markdown code fences.
- Do not include explanations.

Question: {question}
"""

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            raw_text = response.text.strip()

            if raw_text == "INVALID_QUESTION":
                sql = "Invalid question: the requested column does not exist."
            elif raw_text == "OUT_OF_SCOPE":
                sql = "Out of scope: the question is not related to the students table."
            else:
                cleaned_sql = raw_text.replace("```sql", "").replace("```", "").strip()
                if "students" not in cleaned_sql.lower():
                    sql = "Invalid SQL: only the students table is allowed."
                else:
                    sql = cleaned_sql

                    # Validate that the query is a safe, read-only SELECT query
                    if is_safe_select_query(sql):
                        connection = None
                        cursor = None
                        try:
                            connection = get_db_connection()
                            cursor = connection.cursor()
                            cursor.execute(sql)

                            if cursor.description:
                                columns = [col[0] for col in cursor.description]
                            rows = cursor.fetchall()
                            query_executed = True

                        except Exception as e:
                            print("Database execution error:", e)
                            db_error = "An error occurred while executing the query on the database."
                        finally:
                            if cursor:
                                cursor.close()
                            if connection:
                                connection.close()
                    else:
                        db_error = "Query validation failed: only read-only SELECT queries on the students table are allowed."

        except Exception as e:
            print("Gemini API Error:", e)
            sql = "Something went wrong while generating SQL. Please try again."

    return render_template(
        "index.html",
        sql=sql,
        question=question,
        columns=columns,
        rows=rows,
        db_error=db_error,
        query_executed=query_executed
    )


if __name__ == "__main__":
    app.run(debug=True)