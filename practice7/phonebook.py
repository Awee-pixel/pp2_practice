import csv
from connect import get_db_connection, create_tables

def insert_from_csv(file_path='contacts.csv'):
    """Implement inserting data from a CSV file"""
    conn = get_db_connection()
    if not conn: return

    try:
        with conn.cursor() as cur:
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader) 
                for row in csv_reader:
                    if len(row) == 2:
                        cur.execute(
                            "INSERT INTO contacts (user_name, phone) VALUES (%s, %s)",
                            (row[0], row[1])
                        )
        conn.commit()
        print("Данные из CSV успешно загружены.")
    except Exception as e:
        print(f"Ошибка загрузки из CSV: {e}")
    finally:
        conn.close()

def insert_from_console():
    """Implement inserting data entered from the console (user name, phone)"""
    user_name = input("Введите имя (user name): ")
    phone = input("Введите телефон (phone): ")
    
    conn = get_db_connection()
    if not conn: return

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO contacts (user_name, phone) VALUES (%s, %s)",
                (user_name, phone)
            )
        conn.commit()
        print("Контакт успешно добавлен.")
    except Exception as e:
        print(f"Ошибка добавления контакта: {e}")
    finally:
        conn.close()

def update_contact():
    """Implement updating a contact's first name or phone number"""
    contact_id = input("Введите ID контакта для обновления: ")
    print("Что обновить? 1 - Имя, 2 - Телефон")
    choice = input("Выбор (1/2): ")

    conn = get_db_connection()
    if not conn: return

    try:
        with conn.cursor() as cur:
            if choice == '1':
                new_name = input("Введите новое имя: ")
                cur.execute("UPDATE contacts SET user_name = %s WHERE id = %s", (new_name, contact_id))
            elif choice == '2':
                new_phone = input("Введите новый телефон: ")
                cur.execute("UPDATE contacts SET phone = %s WHERE id = %s", (new_phone, contact_id))
            else:
                print("Неверный выбор.")
                return
            
            if cur.rowcount > 0:
                print("Контакт успешно обновлен.")
            else:
                print("Контакт с таким ID не найден.")
        conn.commit()
    except Exception as e:
        print(f"Ошибка обновления контакта: {e}")
    finally:
        conn.close()

def query_contacts():
    """Implement querying contacts with different filters (e.g. by name, by phone prefix)"""
    print("Тип поиска: 1 - По точному имени, 2 - По префиксу телефона")
    choice = input("Выбор (1/2): ")

    conn = get_db_connection()
    if not conn: return

    try:
        with conn.cursor() as cur:
            if choice == '1':
                name = input("Введите имя: ")
                cur.execute("SELECT * FROM contacts WHERE user_name = %s", (name,))
            elif choice == '2':
                prefix = input("Введите начало номера (например +7): ")
                cur.execute("SELECT * FROM contacts WHERE phone LIKE %s", (f"{prefix}%",))
            else:
                print("Неверный выбор.")
                return
            
            records = cur.fetchall()
            if records:
                print("\n--- Результаты поиска ---")
                for row in records:
                    print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
            else:
                print("Контакты не найдены.")
    except Exception as e:
        print(f"Ошибка поиска: {e}")
    finally:
        conn.close()

def delete_contact():
    """Implement deleting a contact by username or phone number"""
    print("Удалить по: 1 - Имени пользователя, 2 - Номеру телефона")
    choice = input("Выбор (1/2): ")

    conn = get_db_connection()
    if not conn: return

    try:
        with conn.cursor() as cur:
            if choice == '1':
                name = input("Введите имя для удаления: ")
                cur.execute("DELETE FROM contacts WHERE user_name = %s", (name,))
            elif choice == '2':
                phone = input("Введите номер телефона для удаления: ")
                cur.execute("DELETE FROM contacts WHERE phone = %s", (phone,))
            else:
                print("Неверный выбор.")
                return
                
            if cur.rowcount > 0:
                print(f"Удалено контактов: {cur.rowcount}.")
            else:
                print("Совпадений для удаления не найдено.")
        conn.commit()
    except Exception as e:
        print(f"Ошибка удаления: {e}")
    finally:
        conn.close()

def main():
    """Главная функция приложения."""
    create_tables() 
    
    while True:
        print("\n--- Телефонная книга (PhoneBook) ---")
        print("1. Вставить данные из CSV")
        print("2. Добавить контакт (консоль)")
        print("3. Обновить контакт")
        print("4. Найти контакт (фильтры)")
        print("5. Удалить контакт")
        print("6. Выход")
        
        choice = input("Выберите действие (1-6): ")
        
        if choice == '1':
            insert_from_csv()
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            print("Завершение работы...")
            break
        else:
            print("Неверная команда, попробуйте снова.")

if __name__ == "__main__":
    main()