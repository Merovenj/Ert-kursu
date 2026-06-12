import mysql.connector

# 1. Connect to your MySQL server instance
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password"
)
cursor = db_connection.cursor()

# 2. Read the script from your .sql file
with open("mysql_schema.sql", "r", encoding="utf-8") as file:
    sql_script = file.read()

# 3. Split individual statements by the semicolon delimiter
# (Note: Using multi=True in execute() is also an option for simple scripts)
queries = sql_script.split(';')

for query in queries:
    clean_query = query.strip()
    if clean_query:  # Skip empty strings resulting from the split
        cursor.execute(clean_query)

# 4. Commit transactions and clean up
db_connection.commit()
cursor.close()
db_connection.close()

print("MySQL script executed successfully on the server!")
