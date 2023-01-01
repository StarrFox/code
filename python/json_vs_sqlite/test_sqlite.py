import sqlite3

connection = sqlite3.connect("test_data.db")
cursor = connection.cursor()

result = cursor.execute("""
SELECT COUNT(*)
FROM "data"
WHERE "category" = 2;
""")
print(result.fetchone()[0])
