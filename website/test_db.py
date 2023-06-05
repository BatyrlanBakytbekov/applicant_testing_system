"""import sqlite3

conn = sqlite3.connect('tests.db')

c = conn.cursor()

c.execute('''CREATE TABLE sql_test
             (question text, option1 text, option2 text, option3 text, option4 text, answer text, id integer)''')

c.execute("INSERT INTO sql_test VALUES ('What is the purpose of the SELECT statement in SQL?', 'To insert data into a table.', 'To update records in a table.', 'To retrieve data from a table.', 'To delete records from a table.', 'To retrieve data from a table.', 1)")
c.execute("INSERT INTO sql_test VALUES ('What is the purpose of the WHERE clause in SQL?', 'To specify the columns to be selected in the result set.', 'To specify the tables to be joined in a query.', 'To filter rows based on a specified condition.', 'To sort the result set in ascending or descending order.', 'To filter rows based on a specified condition.', 2)")
c.execute("INSERT INTO sql_test VALUES ('What is the purpose of the GROUP BY clause in SQL?', 'To sort the result set in ascending or descending order.', 'To filter rows based on a specified condition.', 'To group rows based on a specified column or columns.', 'To join multiple tables in a query.', 'To group rows based on a specified column or columns.', 3)")

conn.commit()

conn.close()"""

