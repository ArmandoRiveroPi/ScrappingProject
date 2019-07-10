#!/home/gauss/arm/importante/work/ai/ai_python/bin/python3

from RevolicoProject.DataBase import DataBase

dataB = DataBase()
dataB.create_ads_table()

print('Success')

# import psycopg2

# con = psycopg2.connect(database="postgres", user="postgres",
#                        password="root", host="127.0.0.1", port="5432")

# cur = con.cursor()
# cur.execute('''CREATE TABLE STUDENT
#       (ADMISSION INT PRIMARY KEY     NOT NULL,
#       NAME           TEXT    NOT NULL,
#       AGE            INT     NOT NULL,
#       COURSE        CHAR(50),
#       DEPARTMENT        CHAR(50));''')
# print("Table created successfully")

# cur.execute("INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3420, 'John', 18, 'Computer Science', 'ICT')")
# cur.execute("INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3419, 'Abel', 17, 'Computer Science', 'ICT')")
# cur.execute("INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3421, 'Joel', 17, 'Computer Science', 'ICT')")
# cur.execute("INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3422, 'Antony', 19, 'Electrical Engineering', 'Engineering')")
# cur.execute("INSERT INTO STUDENT (ADMISSION,NAME,AGE,COURSE,DEPARTMENT) VALUES (3423, 'Alice', 18, 'Information Technology', 'ICT')")

# cur.execute("SELECT admission, name, age, course, department from STUDENT")
# rows = cur.fetchall()

# for row in rows:
#     print("ADMISSION =", row[0])
#     print("NAME =", row[1])
#     print("AGE =", row[2])
#     print("COURSE =", row[3])
#     print("DEPARTMENT =", row[4], "\n")

# con.commit()
# print("Record inserted successfully")

# con.close()
