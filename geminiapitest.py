from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="""
Convert the following question into SQL.

Table: students
Columns: id, name, age, marks, city

Question: Show students whose marks are greater than 80.

Return only the SQL query.
"""
)

print("Gemini response:")
print(response.text)