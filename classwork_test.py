import classwork
import psycopg2

hello = classwork.Connection()
print("after hello hello")
conn = hello.loginIn('postgres','Yaysql37')
hello.loginOut(conn)
exit(0)