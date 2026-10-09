
from app import is_safe_select_query

tests = [
    ("SELECT * FROM students", True),
    ("SELECT name FROM students WHERE marks > 80", True),
    ("SELECT COUNT(*) FROM students", True),
    ("SELECT name FROM students JOIN users ON 1=1", False),
    ("SELECT name FROM students UNION SELECT name FROM users", False),
    ("SELECT salary FROM students", False),
    ("DELETE FROM students", False),
    ("SELECT name FROM students; SELECT name FROM users", False),
    ("SELECT name FROM students WHERE city = 'Delhi'", True),
   ("SELECT SLEEP(5) FROM students", False),
("SELECT name FROM users", False),
("SELECT name FROM students WHERE id = 1 -- comment", False),
("SELECT s.name FROM students s", False),
]

for query, expected in tests:
    actual = is_safe_select_query(query)

    print("Query:", query)
    print("Expected:", expected)
    print("Actual:", actual)
    print("---")