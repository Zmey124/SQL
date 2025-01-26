
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

def add_client(conn,first_name, last_name, email, number=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clients(first_name,last_name,email)
            VALUES (%s,%s,%s)
            RETURNING first_name,last_name,email;
            """, (first_name,last_name,email)) 
        new_man = cur.fetchone()
        print(f"Добавлен новый клиент: {new_man}")
        if number:
            add_phone(conn,new_man[0],number)   
        return new_man
        

def add_phone(conn,id, number):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Phone(id,number)
            VALUES (%s,%s)
            RETURNING id,number;
            """, (id,number))
        phone_name = cur.fetchone()
        print(f"Добавлен телефон: {phone_name}")

def change_client(conn,id, first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        list_name = []
        paramms = []
        if first_name is not  None:
            list_name.append('first_name = %s')
            paramms.append(first_name)
        if last_name is not None:
            list_name.append('last_name = %s')
            paramms.append(last_name)
        if email is not None:
            list_name.append('email = %s')
            paramms.append(email)
        if number is not None:
            list_name.append('number = %s')
            paramms.append(number)
        paramms.append(id)
        value1 = f"UPDATE clients SET {','.join(list_name)} WHERE id = %s"
        cur.execute(value1,paramms)
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
            SELECT * FROM clients c
            LEFT JOIN phone p ON c.id = p.id
            WHERE (first_name = %(first_name)s OR %(first_name)s IS NULL)
            AND (last_name = %(last_name)s OR %(last_name)s IS NULL)
            AND (email = %(email)s OR %(email)s IS NULL)
            OR (number = %(number)s OR %(number)s IS NULL);
            """, {'first_name': first_name, 'last_name': last_name, 'email': email, 'number': number})
        return cur.fetchall()

if __name__=="__main__":
    with psycopg2.connect(database="test_netology", user="postgres", password="1234") as conn:
        create_db(conn)
        add_client(conn,'Альберт','Орешек','Kedr@mail.ru')
        add_phone(conn,'1','89133453245')
        change_client(conn,'1','Аристарх','Упырев')
        print(find_client(conn,'Аристарх'))
    conn.close() 

