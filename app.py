from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = genai.Client()


@app.route("/", methods=["GET", "POST"])
def home():

    sql = ""
    question = ""

    if request.method == "POST":

        question = request.form["question"]

        prompt = f"""
Convert the following question into SQL.

Table: students
Columns: id, name, age, marks, city

Rules:
- Use only the table and columns provided above.
- If the question asks for a column that does not exist, return exactly:
INVALID_QUESTION
- Return only the SQL query if the question is valid.
- Do not use Markdown code fences.
- Do not include explanations.

Question: {question}
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        sql = response.text.strip()

        if sql == "INVALID_QUESTION":
            sql = "Invalid question: the requested column does not exist."
        else:
            sql = sql.replace("```sql", "").replace("```", "").strip()

    return render_template("index.html", sql=sql,question=question)


if __name__ == "__main__":
    app.run(debug=True)