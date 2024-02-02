import psycopg2

COUNT = 1


def print_values():
    global COUNT
    print(f"Запрос #{COUNT}")
    for val in cur.fetchall():
        print(val)
    COUNT += 1
    print('\n')


conn = psycopg2.connect(dbname='fast_api_bd',
                        user='postgres',
                        host='localhost',
                        password='919'
                        )

cur = conn.cursor()

cur.execute("SELECT * FROM student")
print_values()

# - всех студентов, включая student_id, first_name, last_name и email
cur.execute("SELECT student_id, first_name, last_name, email FROM student")
print_values()

# - - студентов старше 15 лет
cur.execute("""
                SELECT student_id, DATE_PART('day', NOW() - date_of_birth) / 365
                FROM student
                WHERE DATE_PART('day', NOW() - date_of_birth) / 365 > 15;
                """)
print_values()

# - всех студентов, включая student_id, first_name, last_name и email
cur.execute("SELECT student_id, first_name, last_name, email FROM student")
print_values()