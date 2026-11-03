import csv
from connect import get_connection

def insert_contact(name, phone):
    """Добавление одного контакта через консоль."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO contacts (first_name, phone) VALUES (%s, %s);",
                (name, phone)
            )
            conn.commit()
            cursor.close()
            conn.close()
            print(f"✅ Контакт '{name}' успешно добавлен.")
        except Exception as e:
            print(f"Ошибка при добавлении контакта: {e}")

def import_from_csv(filename="contacts.csv"):
    """Массовый импорт контактов из CSV-файла."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cursor.execute(
                        "INSERT INTO contacts (first_name, phone) VALUES (%s, %s);",
                        (row['first_name'], row['phone'])
                    )
            conn.commit()
            cursor.close()
            conn.close()
            print(f"✅ Данные успешно импортированы из {filename}.")
        except Exception as e:
            print(f"Ошибка при импорте CSV: {e}")

def query_contacts(filter_type, value):
    """Поиск контактов по имени или префиксу телефона."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if filter_type == "name":
                cursor.execute("SELECT id, first_name, phone FROM contacts WHERE first_name ILIKE %s;", (f"%{value}%",))
            elif filter_type == "prefix":
                cursor.execute("SELECT id, first_name, phone FROM contacts WHERE phone LIKE %s;", (f"{value}%",))
            else:
                cursor.execute("SELECT id, first_name, phone FROM contacts;")
            
            rows = cursor.fetchall()
            print("\n--- Результаты поиска ---")
            for row in rows:
                print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
            print("------------------------\n")
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Ошибка при поиске контактов: {e}")

def update_contact(identifier_type, identifier_value, new_name=None, new_phone=None):
    """Обновление имени или телефона контакта."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if new_name:
                if identifier_type == "name":
                    cursor.execute("UPDATE contacts SET first_name = %s WHERE first_name = %s;", (new_name, identifier_value))
                elif identifier_type == "phone":
                    cursor.execute("UPDATE contacts SET first_name = %s WHERE phone = %s;", (new_name, identifier_value))
            if new_phone:
                if identifier_type == "name":
                    cursor.execute("UPDATE contacts SET phone = %s WHERE first_name = %s;", (new_phone, identifier_value))
                elif identifier_type == "phone":
                    cursor.execute("UPDATE contacts SET phone = %s WHERE phone = %s;", (new_phone, identifier_value))
            
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Контакт успешно обновлен.")
        except Exception as e:
            print(f"Ошибка при обновлении контакта: {e}")

def delete_contact(identifier_type, value):
    """Удаление контакта по имени или телефону."""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if identifier_type == "name":
                cursor.execute("DELETE FROM contacts WHERE first_name = %s;", (value,))
            elif identifier_type == "phone":
                cursor.execute("DELETE FROM contacts WHERE phone = %s;", (value,))
            
            conn.commit()
            cursor.close()
            conn.close()
            print(f"✅ Контакт успешно удален.")
        except Exception as e:
            print(f"Ошибка при удалении контакта: {e}")

def main():
    while True:
        print("\n=== Телефонный справочник (PhoneBook) ===")
        print("1. Импортировать контакты из CSV")
        print("2. Добавить контакт вручную")
        print("3. Найти/просмотреть контакты")
        print("4. Обновить контакт")
        print("5. Удалить контакт")
        print("6. Выход")
        
        choice = input("Выберите пункт (1-6): ").strip()
        
        if choice == '1':
            import_from_csv()
        elif choice == '2':
            name = input("Введите имя: ")
            phone = input("Введите телефон: ")
            insert_contact(name, phone)
        elif choice == '3':
            ftype = input("Фильтр (name / prefix / all): ").strip().lower()
            val = input("Введите значение для поиска (оставьте пустым для 'all'): ").strip() if ftype != 'all' else ""
            query_contacts(ftype, val)
        elif choice == '4':
            itype = input("Искать изменяемый контакт по (name / phone): ").strip().lower()
            ival = input(f"Введите текущее значение ({itype}): ").strip()
            n_name = input("Введите новое имя (нажмите Enter, чтобы пропустить): ").strip() or None
            n_phone = input("Введите новый телефон (нажмите Enter, чтобы пропустить): ").strip() or None
            update_contact(itype, ival, n_name, n_phone)
        elif choice == '5':
            itype = input("Удалить по (name / phone): ").strip().lower()
            val = input(f"Введите {itype} для удаления: ").strip()
            delete_contact(itype, val)
        elif choice == '6':
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 6.")

if __name__ == "__main__":
    main()