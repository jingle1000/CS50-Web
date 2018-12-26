import psycopg2
import pandas as pd

dataset = pd.read_csv('books.csv', sep=',')

conn = psycopg2.connect("dbname=d6pq4pd96n8bci user=cezykxbcbwguds password=ce990760be16388bf589436f85c415dae80eb7680b97ce724c2efd3e363fe04e host=ec2-54-235-247-209.compute-1.amazonaws.com")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS books (
id SERIAL PRIMARY KEY,
isbn VARCHAR NOT NULL,
title VARCHAR NOT NULL,
author VARCHAR NOT NULL,
year INTEGER NOT NULL
);""")
conn.commit()

for i in dataset.values:
    toex = """INSERT INTO books (isbn, title, author, year) VALUES ('{}', '{}', '{}', {})""".format(str(i[0]), str(i[1]), str( i[2]), int(i[3]))
    print(toex)
    cur.execute("INSERT INTO books (isbn, title, author, year) VALUES (%s, %s, %s, %s)", (str(i[0]), str(i[1]), str( i[2]), int(i[3])))
    conn.commit()

conn.close()
infile.close()
