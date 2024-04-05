import psycopg2

conn = psycopg2.connect(database="client_db", user="postgres", password="Lisyona")

def create_table_client(conn):
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS client_data(id SERIAL PRIMARY KEY, client_name text not null, client_surname text not null, client_mail text not null, UNIQUE(client_mail)); CREATE TABLE IF NOT EXISTS client_phone(phone_id serial PRIMARY KEY, FOREIGN KEY (id) integer references client_data(id) ON UPDATE CASCADE ON DELETE CASCADE, phone_number text not null, UNIQUE(phone_number))""")
        conn.commit()

def delete_table_client(conn):
    with conn.cursor() as cur:
        cur.execute("""
                DROP TABLE client_phone;
                DROP TABLE client_data;
                """)
def add_client(conn, id, name, surname, mail):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client_data(id, client_name, client_surname, client_mail) VALUES(%s, %s, %s, %s);
            """, (id, name, surname, mail))
        conn.commit()
def add_phone(conn, client_id_num, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client_phone(id, phone_number) VALUES(%s, %s);
            """, (client_id_num, phone,))
        conn.commit()
def change_client(conn, client_id, name=None, surname=None, mail=None):
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT client_name, client_surname, client_mail FROM client_data RIGHT JOIN client_phone ON client_data.id = client_phone.id WHERE client_data.id=%s;
                    """, (client_id,))
        data_list = cur.fetchone()  # Получаем данные пользователя в виде кортежа из запроса и сохраняем в переменную
        if cur.fetchone() == None:  # Если селект данные не вернул, то проваливаемся в блок
            return "Такого пользователя нет"  # Сообщаем, что такого пользователя нет
        if name==None:  # Если имя пустое, то проваливаемся в блок
            name = data_list[1]  # Изменяем имя клиента на значение из кортежа, который вернулся из запроса
        if surname==None:  # Если фамилия пустое, то проваливаемся в блок
            surname = data_list[2]  # Изменяем имя клиента на значение из кортежа, который вернулся из запроса
        if mail==None:  # Если почта пустая, то проваливаемся в блок
            mail = data_list[3]  # Изменяем почту клиента на значение из кортежа, который вернулся из запроса

        cur.execute("""
                    UPDATE client_data SET client_name=%s, client_surname=%s, client_mail=%s  WHERE id=%s;
                    """, (name, surname, mail, client_id,))
        conn.commit()

    return "Пользователь успешно изменен"
def delete_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client_phone WHERE phone_number=%s;
            """, (phone,))
        conn.commit()
def find_client(conn, name = None, surname = None, mail = None, phone = None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT client_name, client_surname, client_mail FROM client_data RIGHT JOIN client_phone ON client_data.id = client_phone.id WHERE client_name=%s OR client_surname=%s OR client_mail=%s OR phone_number=%s;
            """, (name, surname, mail, phone,))
        return(cur.fetchone())
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client_data WHERE id=%s;
            """, (client_id,))
        conn.commit()

create_table_client(conn)
new_client = add_client(1, 'Robert', 'Schmoegner', 'robsch@google.com')
new_clients_phone = add_phone(1, '+79503813552')
correct_client_data = change_client(1, 'Bob', 'Schmoegner', 'robo@google.com')
remove_phone = delete_phone('+79503813552')
look_for_client = find_client(name = 'Bob', surname = 'Schmoegner', mail = None, phone = None)
remove_client = delete_client(1)
conn.close()

