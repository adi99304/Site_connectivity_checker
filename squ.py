
import mysql.connector

# Establishing connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Adit@1705",
    database="aditya"
)

# Creating cursor object
mycur = conn.cursor()

# Your database operations go here...
# For example:
# Execute SQL queries, fetch data, etc.

# Committing changes (if any)
conn.commit()

# Closing cursor
mycur.close()

# Closing connection
conn.close()

print("Connection successfully closed")
