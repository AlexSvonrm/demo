import psycopg2

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

# def add_client(conn, first_name=None, last_name=None, email=None, phone=None):
#     cur.execute("""
#         INSERT INTO clients(first_name, last_name, email)
#         VALUES (%s, %s, %s)
#         """, (first_name, last_name, email))
#     cur.execute("""
#         SELECT id from clients
#         ORDER BY id DESC
#         LIMIT 1
#         """)
#     id = cur.fetchone()[0]
#     if phone is None:
#         return id
#     else:
#         add_phone(cur, id, phone)
#         return id

def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:
        if find_client(conn, email=email): #Ищем клиента с таким имейлом
            return "клиент с таким имейлом уже есть"
        cur.execute(
            """
            INSERT INTO clients (first_name, last_name, email) --В таблицу клиентов втавляем имя, фамилию и почту
            VALUES (%s, %s, %s) RETURNING id; --Возвращаем поле, которое содержит идентификационный номер
            """, 
            (first_name, last_name, email,) #Передаем имя, фамилию и имейл
        )
        if phone is not None: #Проверяем передали ли телефон при добавлении контакта
            newclient = cur.fetchone() #получаем из запроса идентификационный номер и сохраняем в переменную
            client_id = newclient
            newphone = add_phone(conn, client_id, phone) #Вызываем функцию добавления номера телефона и рузультат сохраняем в переменную
            if newphone == 'такой номер есть': #Проверяем вернулось ли сообщение, которое равно тому, что сообщает о существовании номера
                conn.rollback() #Отменяем создание клиента
                return print("Сообщаем что добавить невозможно")
        conn.commit() #Делаем коммит у соединения
    return "Сообщаем что клиент добавлен"


def add_phone(conn, client_id: int, phone: int):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT phone from phonenumbers --Получаем телефон из таблицы телефонов
            WHERE phone = %s; --Где телефон равен %s
            """,
            (phone, ) #Передаем номер телефона
        )
        if cur.fetchone(): #Проверяем вернулась ли не пустая коллекция
            return "такой номер есть" 
        cur.execute(
            """
            SELECT client_id from clients --Получаем клиента из таблицы клиентов
            WHERE client_id = %s; --Где id клиента равен %s
            """,
            (client_id, ) #Передаем id клиента
        )
        if not cur.fetchone(): #Проверяем вернулась ли пустая коллекция
            return "Соообщаем что такого клиента нет" 
        cur.execute(
            """
            INSERT INTO phonenumbers (phone, client_id) 
            VALUES (%s, %s);
            """,
            (phone, client_id)
        )
        conn.commit() #Подтверждаем изменения
    return "сообщение об успехе"


# def add_phone(cur, client_id, phone):
#     cur.execute("""
#         INSERT INTO phonenumbers(phone, client_id)
#         VALUES (%s, %s)
#         """, (phone, client_id))
#     return client_id
    
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
        # cur.execute("""
        #     DELETE FROM phonenumbers
        #     WHERE client_id = %s
        #     """, (client_id, ))
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
