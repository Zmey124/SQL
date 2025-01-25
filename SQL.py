
import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE phone;
            DROP TABLE clients;        
                    """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    email VARCHAR(150),
                    phones VARCHAR(20)
                    );
                    """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER REFERENCES clients(id),
                    number VARCHAR(20));
                    """)
        conn.commit()

def add_client(conn,first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clients(first_name,last_name,email)
            VALUES (%s,%s,%s)
            RETURNING first_name,last_name,email;
            """, (first_name,last_name,email))    
        print(cur.fetchone())

def add_phone(conn,id, number):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Phone(id,number)
            VALUES (%s,%s)
            RETURNING id,number;
            """, (id,number))
        print(cur.fetchone())

def change_client(conn,id, first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE clients SET first_name=%s,last_name=%s,email=%s WHERE id=%s;
            """, (first_name,last_name,email,id))
        cur.execute("""
            SELECT * FROM clients;
        """)
        print(cur.fetchall())
        

def delete_phone(conn,id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone WHERE id=%s;
            """,(id,))
        cur.execute("""
            SELECT * FROM clients;
         """)
        print(cur.fetchall())

def delete_client(conn,id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM clients WHERE id=%s;
            """,(id,))
        cur.execute("""
            SELECT * FROM clients;
         """)
        print(cur.fetchall())

def find_client(conn,first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.first_name,c.last_name,c.email,p.number FROM clients c
            LEFT JOIN phone p ON c.id = p.id
            WHERE c.first_name=%s OR c.last_name=%s OR c.email=%s OR p.number=%s;
            """, (first_name,last_name,email,number,)
        )
        print(cur.fetchone())


with psycopg2.connect(database="test_netology", user="postgres", password="1234") as conn:
    create_db(conn)
    add_client(conn,'Альберт','Орешек','Kedr@mail.ru')
    #add_phone(conn,'1','89133453245')
    #change_client(conn,1,'Fogy','Bulkin','xzxzxz@chototam.com','89831543278')
    #delete_phone(conn,1)
    #delete_client(conn,1)
    find_client(conn,'Альберт')
conn.close() 

