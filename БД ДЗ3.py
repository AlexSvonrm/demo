import psycopg2
# Ваши функции возвращают результат. Следовательно, чтобы увидеть результат, который они возвращают, их необходимо принтить
# КАК??????????

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY NOT NULL,
            first_name VARCHAR(80) NOT NULL,
            last_name VARCHAR(80) NOT NULL,
            email VARCHAR(80) UNIQUE
            );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phonenumbers(
            phone VARCHAR(80) PRIMARY KEY,
            client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE
            );
        """)
        conn.commit()
    return

def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        if find_client(conn, email=email): 
            return "клиент с таким имейлом уже есть"
        cur.execute(
            """
            INSERT INTO clients (first_name, last_name, email)
            VALUES (%s, %s, %s) RETURNING id;
            """, 
            (first_name, last_name, email,) 
        )
        if phone is not None: 
            newclient = cur.fetchone() 
            client_id = newclient
            newphone = add_phone(conn, client_id, phone) 
            if newphone == 'такой номер есть': 
                conn.rollback() 
                return "Сообщаем что добавить невозможно"
        conn.commit() 
    return "Сообщаем что клиент добавлен"

def add_phone(conn, client_id: int, phone: int):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT phone from phonenumbers 
            WHERE phone = %s; 
            """,
            (phone, ) 
        )
        if cur.fetchone(): 
            return "такой номер есть" 
        cur.execute(
            """
            SELECT id from clients
            WHERE id = %s;
            """,
            (id, ) 
        )
        if not cur.fetchone():
            return "Соообщаем что такого клиента нет" 
        cur.execute(
            """
            INSERT INTO phonenumbers (phone, client_id) 
            VALUES (%s, %s);
            """,
            (phone, client_id)
        )
        conn.commit() 
    return "сообщение об успехе"

def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * from clients
            WHERE id = %s
            """, (client_id, ))
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
            """, (first_name, last_name, email, client_id))
        conn.commit()
    return client_id

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phonenumbers 
            WHERE phone = %s
            """, (phone, ))
    return phone

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM clients 
            WHERE id = %s
           """, (client_id,))
    return client_id

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
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

def delete_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE if exists clients, phonenumbers CASCADE;
        """)
    return
    
with psycopg2.connect(database = "clients_db", user= "postgres", password= "postgres") as conn:
    create_db(conn)
    print("База создана")
    add_client(conn, "Иван", "Иванов", "dfg@.com")
    add_client(conn, "Петр", "Петров", "ggff@.com")
    add_client(conn, "Денис", "Денисов", "jaxccxx@.com")
    add_client(conn, "Игорь", "Игорев", "vxcv@.com")
    add_client(conn, "Коля", "Колев", "xvcvcx@.com")
    add_phone(conn, 1, "1-111-11-11")
    add_phone(conn, 2, "2-222-22-22")
    add_phone(conn, 3, "3-333-33-33")
    add_phone(conn, 4, "4-444-44-44")
    add_phone(conn, 5, "5-555-55-55")
    change_client(conn, 2)
    delete_phone(conn, 3, "3-333-33-33")
    delete_client(conn, 4)
    find_client(conn, "Коля")

conn.close()

