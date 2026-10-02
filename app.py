from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = genai.Client()


@app.route("/", methods=["GET", "POST"])
def home():

    sql = ""

    if request.method == "POST":

        question = request.form["question"]

        prompt = f"""
Convert the following question into SQL.

Table: students
Columns: id, name, age, marks, city

Question: {question}

Return only the SQL query.
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        sql = response.text

    return render_template("index.html", sql=sql)


if __name__ == "__main__":
    app.run(debug=True)