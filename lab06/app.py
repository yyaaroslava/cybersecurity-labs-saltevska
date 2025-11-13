import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

# Функція для підключення до БД
def get_db_connection():
    conn = sqlite3.connect('students.db')
    # Це дозволить нам отримувати результати як словники (dict)
    conn.row_factory = sqlite3.Row 
    return conn

# Головна сторінка, яка показує наші форми пошуку
@app.route('/')
def index():
    # Просто показуємо HTML-сторінку
    return render_template('index.html')


# ☠️ КРОК 3.3: ВРАЗЛИВА ВЕРСІЯ (НЕБЕЗПЕЧНО!)
@app.route('/search_vulnerable', methods=['POST'])
def search_vulnerable():
    # Отримуємо ім'я з форми
    name = request.form['name']
    
    # "Склеюємо" SQL-запит із даними (ЦЕ І Є УРАЗЛИВІСТЬ!)
    query = "SELECT * FROM students WHERE name = '" + name + "'"
    
    conn = get_db_connection()
    
    try:
        # Виконуємо "злий" запит
        students = conn.execute(query).fetchall()
    except sqlite3.Error as e:
        # Якщо ін'єкція спричинить помилку, ми її побачимо
        students = []
        print(f"ПОМИЛКА У ВРАЗЛИВОМУ ЗАПИТІ: {e}")

    conn.close()
    
    # Повертаємо результати на ту ж сторінку
    return render_template('index.html', students=students, search_type="Вразливий")


# ✅ КРОК 3.4: ЗАХИЩЕНА ВЕРСІЯ (БЕЗПЕЧНО!)
@app.route('/search_secure', methods=['POST'])
def search_secure():
    # Отримуємо ім'я з форми
    name = request.form['name']
    
    # 1. Запит - це ШАБЛОН з плейсхолдером (?)
    query = "SELECT * FROM students WHERE name = ?"
    
    conn = get_db_connection()
    
    # 2. Дані (name,) передаються ОКРЕМО
    # База даних сама безпечно підставить дані, не виконуючи їх
    students = conn.execute(query, (name,)).fetchall()
    
    conn.close()
    
    # Повертаємо результати на ту ж сторінку
    return render_template('index.html', students=students, search_type="Безпечний")


# Запуск нашого веб-сервера
if __name__ == '__main__':
    app.run(debug=True) # debug=True показує помилки у браузері