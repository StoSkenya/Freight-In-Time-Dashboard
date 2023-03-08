import psycopg2


conn = psycopg2.connect(dbname="freightintime_db_",user="postgres",host="localhost",password="mea4545Luda",port="5432")

print(conn)
# conn.close()
