


# Визначення Алфавітів 
# Створюємо рядки, що містять всі літери кожного алфавіту.
UKR_ALPHABET = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
UKR_ALPHABET_LEN = len(UKR_ALPHABET) # Довжина = 33

ENG_ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ENG_ALPHABET_LEN = len(ENG_ALPHABET) # Довжина = 26


# Генерація ключів

# Генерує ключ для шифру Цезаря. Ключ = сума всіх цифр дати народження.
def get_caesar_key(date_str: str) -> int:
    shift = 0 # Початкове значення зсуву
    for char in date_str:
        if char.isdigit():  # Перевіряємо, чи є символ цифрою
            shift += int(char) # Якщо так, додаємо його числове значення до зсуву   
    return shift # Повертаємо "базовий" зсув. Він буде модулюватися.залежно від алфавіту (33 або 26) вже у функції шифрування.



# Генерує ключ для шифру Віженера. Ключ = прізвище (лише літери УКР або АНГЛ алфавіту, у нижньому регістрі). 
def get_vigenere_key(surname: str) -> str:
    key = "" # Початкове порожнє ключове слово
    for char in surname.lower(): # Переводимо прізвище у нижній регістр для уніфікації
        if char in UKR_ALPHABET or char in ENG_ALPHABET:  # Додаємо у ключ лише ті символи, що є в одному з алфавітів
            key += char
    return key


# Реалізація алгоритмів 


# Реалізація шифрування/розшифрування методом Цезаря. Автоматично обробляє українські та англійські літери окремо.
def caesar_cipher(text: str, base_shift: int, mode: str = 'encrypt') -> str:
    result = "" # Рядок для збереження результату
    shift_direction = 1 if mode == 'encrypt' else -1 # Визначаємо напрямок зсуву: 1 для шифрування, -1 для розшифрування
    for char in text:  # Проходимо по кожному символу вхідного тексту
        char_lower = char.lower() # Працюємо з малими літерами для пошуку в алфавіті
        
        # Визначаємо, з яким алфавітом працювати
        if char_lower in UKR_ALPHABET:
            alphabet = UKR_ALPHABET
            alphabet_len = UKR_ALPHABET_LEN
        elif char_lower in ENG_ALPHABET:
            alphabet = ENG_ALPHABET
            alphabet_len = ENG_ALPHABET_LEN
        else:
            result += char # Якщо символ не з алфавіту (пробіл, !, ?, 1), додаємо його як є
            continue # Переходимо до наступного символу
            
        # Обчислюємо реальний зсув для конкретного алфавіту. (base_shift * shift_direction) - зсув з урахуванням напрямку
        # % alphabet_len - "загортає" зсув, якщо він виходить за межі алфавіту
        shift = (base_shift * shift_direction) % alphabet_len
            
        # Знаходимо індекс початкової літери
        original_index = alphabet.find(char_lower)
        
        # Обчислюємо новий індекс
        # Додаємо alphabet_len, щоб уникнути від'ємних індексів при розшифруванні
        new_index = (original_index + shift + alphabet_len) % alphabet_len
        
        # Отримуємо нову літеру за новим індексом
        new_char = alphabet[new_index]
            
        # Зберігаємо регістр: якщо початкова літера була великою, робимо нову теж великою
        result += new_char.upper() if char.isupper() else new_char
            
    return result

def vigenere_cipher(text: str, key: str, mode: str = 'encrypt') -> str:
    """
    Реалізація шифрування/розшифрування методом Віженера.
    Автоматично обробляє українські та англійські літери окремо.
    """
    result = "" # Рядок для збереження результату
    key_index = 0 # Поточна позиція в ключовому слові
    key_len = len(key) # Довжина ключа
    
    # Перевірка, чи ключ не порожній (наприклад, якщо прізвище було "123")
    if key_len == 0:
        print("Помилка: Ключ Віженера порожній. Шифрування неможливе.")
        return text

    # Визначаємо напрямок зсуву (1 або -1)
    shift_direction = 1 if mode == 'encrypt' else -1

    # Проходимо по кожному символу вхідного тексту
    for char in text:
        char_lower = char.lower()
        
        # 1. Визначаємо алфавіт для СИМВОЛУ ТЕКСТУ
        if char_lower in UKR_ALPHABET:
            alphabet = UKR_ALPHABET
            alphabet_len = UKR_ALPHABET_LEN
        elif char_lower in ENG_ALPHABET:
            alphabet = ENG_ALPHABET
            alphabet_len = ENG_ALPHABET_LEN
        else:
            # Якщо символ не літера, додаємо його без змін
            result += char
            continue # Переходимо до наступного символу
            
        # Знаходимо індекс початкової літери
        original_index = alphabet.find(char_lower)
            
        # 2. Отримуємо символ ключа та його числовий зсув
        # (key_index % key_len) дозволяє "зациклити" ключ (напр., "KEYKEYKEY")
        key_char = key[key_index % key_len]
        key_shift = 0
        
        # 3. Визначаємо числовий зсув, який дає літера КЛЮЧА
        # Літера ключа може бути з будь-якого алфавіту
        if key_char in UKR_ALPHABET:
            key_shift = UKR_ALPHABET.find(key_char)
        elif key_char in ENG_ALPHABET:
            key_shift = ENG_ALPHABET.find(key_char)
            
        # Обчислюємо фінальний зсув з урахуванням напрямку (шифр./розшифр.)
        final_shift = (key_shift * shift_direction)
        
        # 4. Обчислюємо нову літеру в АЛФАВІТІ ТЕКСТУ
        new_index = (original_index + final_shift + alphabet_len) % alphabet_len
        new_char = alphabet[new_index]

        # Зберігаємо початковий регістр
        result += new_char.upper() if char.isupper() else new_char
        
        # Індекс ключа рухаємо, ЛИШЕ ЯКЩО ми обробили літеру
        # (тобто пробіли не "з'їдають" літери ключа)
        key_index += 1
            
    return result


# 4. Демонстрація та аналіз 

def main():
    print("=" * 60)
    print("  ПОРІВНЯЛЬНИЙ АНАЛІЗ КЛАСИЧНИХ ШИФРІВ (UA/EN)")
    print("=" * 60)

    # ІНТЕРАКТИВНЕ ВВЕДЕННЯ ДАНИХ 
    user_surname = input("Введіть ваше прізвище: ")
    user_birth_date = input("Введіть дату народження (у форматі ДД.ММ.РРРР): ")
    user_text = input("Введіть текст для шифрування: ")
    

    #Демонстрація Цезаря
    print("\n" + "-" * 60)
    print("1. Шифр Цезаря")
    
    # Отримуємо "базовий" ключ (суму цифр дати)
    caesar_key = get_caesar_key(user_birth_date)
    
    # Пояснення, як працює ключ.
    # (Вивід був трохи неточний, я його виправив, щоб показував обидва зсуви)
    print(f"Згенерований базовий ключ (сума цифр дати {user_birth_date}): {caesar_key}")
    print(f"(Зсув для УКР: {caesar_key % UKR_ALPHABET_LEN}, Зсув для АНГЛ: {caesar_key % ENG_ALPHABET_LEN})")
    
    # Викликаємо функцію шифрування
    encrypted_caesar = caesar_cipher(user_text, caesar_key, 'encrypt')
    print(f"\nЗашифровано (Цезар):\n\"{encrypted_caesar}\"")
    
    # Викликаємо ту саму функцію для розшифрування
    decrypted_caesar = caesar_cipher(encrypted_caesar, caesar_key, 'decrypt')
    print(f"\nРозшифровано (Цезар):\n\"{decrypted_caesar}\"")
    print("-" * 60)

    # Демонстрація Віженера 
    print("\n" + "-" * 60)
    print("2. Шифр Віженера")
    
    # Отримуємо ключ-слово з прізвища
    vigenere_key = get_vigenere_key(user_surname)
    print(f"Згенерований ключ (з прізвища {user_surname}): \"{vigenere_key}\"")
    
    # Викликаємо функцію шифрування
    encrypted_vigenere = vigenere_cipher(user_text, vigenere_key, 'encrypt')
    print(f"\nЗашифровано (Віженер):\n\"{encrypted_vigenere}\"")
    
    # Викликаємо ту саму функцію для розшифрування
    decrypted_vigenere = vigenere_cipher(encrypted_vigenere, vigenere_key, 'decrypt')
    print(f"\nРозшифровано (Віженер):\n\"{decrypted_vigenere}\"")
    print("-" * 60)



    # Порівняльний аналіз 
    print("\n3. Таблиця порівняльного аналізу (Загальні властивості)\n")
    
    header = f"{'Критерій':<25} | {'Шифр Цезаря':<35} | {'Шифр Віженера':<35}"
    print(header)
    print("-" * len(header))
    
    print(f"{'Тип шифру':<25} | {'Моноалфавітний підстановочний':<35} | {'Поліалфавітний підстановочний':<35}")
    print(f"{'Ключ':<25} | {'Числовий зсув':<35} | {'Ключове слово':<35}")
    print(f"{'Складність ключа':<25} | {'Дуже низька (25 або 32 варіанти)':<35} | {'Середня (залежить від довж. ключа)':<35}")
    print(f"{'Стійкість (Аналіз)':<25} | {'Дуже низька (частотний аналіз)':<35} | {'Середня (вразл. до методу Казіскі)':<35}")
    
    print("\n4. Висновки про стійкість \n")
    print("1. Шифр Цезаря є абсолютно нестійким, незалежно від алфавіту. "
          "Статистичні властивості мови (частота літер) повністю зберігаються, "
          "що дозволяє миттєвий злам частотним аналізом або простим перебором.")
    
    print("\n2. Шифр Віженера значно сильніший, оскільки він \"розмиває\" "
          "частотні характеристики. Однак він також вважається зламаним і "
          "вразливий до методу Казіскі (для пошуку довжини ключа) та подальшого "
          "частотного аналізу.")

    
    print("\nДемонстрацію завершено.")

if __name__ == "__main__":
    main() # Запускаємо головну функцію