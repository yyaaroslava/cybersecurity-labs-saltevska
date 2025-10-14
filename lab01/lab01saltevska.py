import re

def analyze_password(password, name, birth_date):
    recommendations = []
    score = 10

    # Розділяємо дату народження на день, місяць і рік
    day, month, year_full = birth_date.split('.')
    date_parts = [day, month, year_full]

    # Перевіряємо, чи міститься ім'я в паролі
    name_in_password = name.lower() in password.lower()
    # Перевіряємо, чи міститься будь-яка частина дати народження в паролі
    date_in_password = any(part in password for part in date_parts)
    
    # Відображаємо результати аналізу
    print("\nАналіз:")
    print("- Частини дати народження у паролі:", "так" if date_in_password else "ні")
    print("- Ім'я у паролі:", "так" if name_in_password else "ні")

    # Перевірка довжини пароля
    if len(password) < 8:
        recommendations.append("Пароль дуже короткий (мінімум 8 символів).")
        score -= 3
    # Перевірка наявності великої літери
    if not any(c.isupper() for c in password):
        recommendations.append("Додайте великі літери.")
        score -= 1
    # Перевірка наявності маленької літери
    if not any(c.islower() for c in password):
        recommendations.append("Додайте малі літери.")
        score -= 1
    # Перевірка наявності цифри
    if not any(c.isdigit() for c in password):
        recommendations.append("Додайте цифри.")
        score -= 1
    # Перевірка наявності спецсимволів
    if not any(not c.isalnum() for c in password):
        recommendations.append("Додайте спеціальні символи.")
        score -= 2

    # Рекомендації 
    if name_in_password:
        recommendations.append("Не використовуйте ім'я у паролі.")
        score -= 2
    if date_in_password:
        recommendations.append("Не використовуйте частини дати народження у паролі.")
        score -= 1
        
    # Оцінка пароля
    score = max(1, score)
    # Виводимо остаточну оцінку і рекомендації
    print(f"\nОцінка пароля: {score}/10")
    print("Рекомендації:")
    for rec in set(recommendations):
        print("-", rec)

# Функція для введення і перевірки коректності дати народження
def input_birth_date():
    while True:
        birth_date = input("Введіть дату народження (формат ДД.ММ.РРРР): ")
        # Перевірка формату за допомогою регулярного виразу
        if re.match(r'^\d{2}\.\d{2}\.\d{4}$', birth_date):
            day, month, year = birth_date.split('.')
            if 1 <= int(day) <= 31 and 1 <= int(month) <= 12:
                return birth_date
            else:
                print("Помилка: день або місяць некоректні. Спробуйте ще раз.")
        else:
            print("Невірний формат дати! Використайте ДД.ММ.РРРР.")  
            
# Додаткова перевірка логічної коректності дня і місяця
while True:
    name = input("\nВведіть ім'я (або введіть 'exit' для виходу): ")
    if name.lower() == 'exit':
        print("Завершення роботи програми.")
        break
    # Вводимо дату народження і перевіряємо її
    birth_date = input_birth_date()
    # Вводимо пароль для аналізу
    password = input("Введіть пароль для аналізу: ")
    # Аналізуємо пароль
    analyze_password(password, name, birth_date)
