from connect import get_db_connection, setup_database

def search_by_pattern():
    pattern = input("Введите часть имени или номера для поиска: ")
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
            records = cur.fetchall()
            if records:
                for row in records:
                    print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
            else:
                print("Ничего не найдено.")
    finally:
        conn.close()

def upsert_user():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
        conn.commit()
        print(f"Контакт {name} успешно добавлен или обновлен!")
    finally:
        conn.close()

def bulk_insert_with_validation():
    print("Режим массовой вставки (введите 'stop' для завершения)")
    names, phones = [], []
    while True:
        name = input("Имя (или 'stop'): ")
        if name.lower() == 'stop': break
        phone = input(f"Телефон для {name}: ")
        names.append(name)
        phones.append(phone)
    
    if not names: return

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL bulk_insert_contacts(%s, %s, %s)", (names, phones, []))
            
            invalid_data = cur.fetchone()[0] 
        conn.commit()
        
        print("\nМассовая вставка завершена.")
        if invalid_data:
            print("Внимание! Следующие контакты были отклонены (неверный формат телефона):")
            for err in invalid_data:
                print(f" - {err}")
        else:
            print("Все контакты прошли валидацию и добавлены!")
    finally:
        conn.close()

def view_paginated():
    limit = int(input("Сколько контактов выводить на одной странице? (LIMIT): "))
    offset = int(input("Сколько контактов пропустить с начала? (OFFSET): "))
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            records = cur.fetchall()
            if records:
                for row in records:
                    print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
            else:
                print("На этой странице пусто.")
    finally:
        conn.close()

def delete_user():
    val = input("Введите точное имя или телефон для удаления: ")
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s)", (val,))
        conn.commit()
        print("Команда на удаление выполнена.")
    finally:
        conn.close()

def main():
    setup_database()
    
    while True:
        print("\n--- PhoneBook (PL/pgSQL Edition) ---")
        print("1. Найти контакт по паттерну (Функция)")
        print("2. Вставить / Обновить контакт (Upsert Процедура)")
        print("3. Массовая вставка с валидацией (Процедура)")
        print("4. Вывести контакты постранично (Функция)")
        print("5. Удалить контакт (Процедура)")
        print("6. Выход")
        
        choice = input("Выбор (1-6): ")
        if choice == '1': search_by_pattern()
        elif choice == '2': upsert_user()
        elif choice == '3': bulk_insert_with_validation()
        elif choice == '4': view_paginated()
        elif choice == '5': delete_user()
        elif choice == '6': break
        else: print("Неверный ввод.")

if __name__ == "__main__":
    main()