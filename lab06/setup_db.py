import sqlite3

# Підключаємось (або створюємо) до файлу бази даних
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Видаляємо таблицю, якщо вона вже існує (для чистих тестів)
cursor.execute("DROP TABLE IF EXISTS students")

# Створюємо таблицю
cursor.execute('''
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT  NULL,
    grade TEXT NOT NULL
)
''')

# Вставляємо дані
students_data = [
    (1, 'Іван Петренко', 'Група A'),
    (2, 'Марія Сидоренко', 'Група Б'),
    (3, 'Петро Коваленко', 'Група A'),
    (4, 'Секретний Адмін', 'Група X (Прихована)') # Наша ціль для "злому"
]

cursor.executemany("INSERT INTO students VALUES (?, ?, ?)", students_data)

# Зберігаємо зміни та закриваємо з'єднання
conn.commit()
conn.close()

print("Базу даних 'students.db' успішно створено та заповнено.")