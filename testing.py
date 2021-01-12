import psycopg2

conn = psycopg2.connect(database="postgres", user = "postgres", password = "Yaysql37", host = "localhost", port = "5432")
cur = conn.cursor()

try:
    myCursor.execute("Insert into employee (employeeid,firstname,lastname,ssn,paytype,jobtype,salary) values (%s,%s,%s,%s,%s,%s,%s)", (employeeid,firstname,lastname,ssn,paytype,jobtype,salary))
    print("employee created successfully, employee id: %s" % (employeeid))

except:
    print("failed")

conn.commit()
conn.close()
