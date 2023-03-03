mport psycopg2
from pprint import pprint

def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY NOT NULL,
        first_name VARCHAR(80) NOT NULL,
        last_name VARCHAR(80) NOT NULL,
        email VARCHAR(80) NOT NULL
        );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonenumbers(
        phone VARCHAR(80) PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id)
        );
    """)
    return

def add_client(cur, first_name=None, last_name=None, email=None, phone=None):
    cur.execute("""
        INSERT INTO clients(first_name, last_name, email)
        VALUES (%s, %s, %s)
        """, (first_name, last_name, email))
    cur.execute("""
        SELECT id from clients
        ORDER BY id DESC
        LIMIT 1
        """)
    id = cur.fetchone()[0]
    if phone is None:
        return id
    else:
        add_phone(cur, id, phone)
        return id

def add_phone(cur, client_id, phone):
    cur.execute("""
        INSERT INTO phonenumbers(phone, client_id)
        VALUES (%s, %s)
        """, (phone, client_id))
    return client_id
    
def change_client(cur, client_id, first_name=None, last_name=None, email=None):
    cur.execute("""
        SELECT * from clients
        WHERE id = %s
        """, (id, ))
    info = cur.fetchone()
    if first_name is None:
        first_name = info[1]
    if last_name is None:
        last_name = info[2]
    if email is None:
        email = info[3]
    cur.execute("""
        UPDATE clients
        SET first_name = %s, last_name = %s, email =%s 
        where id = %s
        """, (first_name, last_name, email, id))
    return id


def delete_phone(cur, client_id, phone):
    cur.execute("""
        DELETE FROM phonenumbers 
        WHERE client_id=%s AND phone = %s
        """, (phone, ))
    return phone


def delete_client(cur, client_id):
    cur.execute("""
        DELETE FROM phonenumbers
        WHERE client_id = %s
        """, (client_id, ))
    cur.execute("""
        DELETE FROM clients 
        WHERE id = %s
       """, (client_id,))
    return client_id

def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    if first_name is None:
        first_name = '%'
    else:
        first_name = '%' + first_name + '%'
    if last_name is None:
        last_name = '%'
    else:
        last_name = '%' + last_name + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if phone is None:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, p.phone FROM clients c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            WHERE c.first_name LIKE %s AND c.last_name LIKE %s
            AND c.email LIKE %s
            """, (first_name, last_name, email))
    else:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, p.phone FROM clients c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            WHERE c.first_name LIKE %s AND c.last_name LIKE %s
            AND c.email LIKE %s AND p.phone like %s
            """, (first_name, last_name, email, phone))
    return cur.fetchall()

def delete_db(cur):
    cur.execute("""
        DROP TABLE clients, phonenumbers CASCADE;
        """)
  
    
with psycopg2.connect(database = "clients_db", user= "postgres", password= "postgres") as conn:
    with conn.cursor() as cur:
        create_db(cur)
        add_client(cur, "Иван", "Иванов", "dfg@.com")
        add_client(cur, "Петр", "Петров", "ggff@.com")
        add_client(cur, "Денис", "Денисов", "jaxccxx@.com")
        add_client(cur, "Игорь", "Игорев", "vxcv@.com")
        add_client(cur, "Коля", "Колев", "xvcvcx@.com")
        add_phone(cur, 1, "1-111-11-11")
        add_phone(cur, 2, "2-222-22-22")
        add_phone(cur, 3, "3-333-33-33")
        add_phone(cur, 4, "4-444-44-44")
        add_phone(cur, 5, "5-555-55-55")
        change_client()
        delete_phone()
        delete_client()
        find_client()

conn.close()
