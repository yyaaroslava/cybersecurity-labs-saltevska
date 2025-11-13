import hashlib
from pathlib import Path

MOD = 1_000_007
PUB_MULT = 7  # за умовою прикладу (спрощена «публічна математика»)

def sha256_bytes(data: bytes) -> bytes:
    # Обчислити SHA-256 та повернути 32 байти дайджесту
    return hashlib.sha256(data).digest()

def sha256_hex(data: bytes) -> str:
    # Варіант для зручного виводу: гекс-рядок хешу
    return hashlib.sha256(data).hexdigest()

def derive_private_key(lastname: str, birthday: str, secret: str) -> bytes:
    # «Приватний ключ» отримуємо як SHA-256 від конкатенації персональних даних
    # Приклад: ("Петренко", "15031995", "secret_word")
    seed = (lastname + birthday + secret).encode("utf-8")
    return sha256_bytes(seed)

def public_key_from_private(private_key_bytes: bytes) -> int:
    # «Публічний ключ» у спрощеній схемі:
    # інтерпретуємо приватний ключ як велике ціле та рахуємо (priv * 7) mod 1_000_007
    priv_int = int.from_bytes(private_key_bytes, byteorder="big")
    return (priv_int * PUB_MULT) % MOD

def xor_bytes(a: bytes, b: bytes) -> bytes:
    # Побайтова операція XOR: повторюємо ключ b до довжини a і застосовуємо XOR
    kb = (b * (len(a) // len(b) + 1))[:len(a)]
    return bytes(x ^ y for x, y in zip(a, kb))

def sign_file(path: str, private_key_bytes: bytes) -> bytes:
    # «Підпис»: обчислюємо SHA-256 файлу та робимо XOR із приватним ключем
    content = Path(path).read_bytes()
    h = sha256_bytes(content)
    return xor_bytes(h, private_key_bytes)

def verify_file(path: str, signature: bytes, public_key: int, private_key_bytes: bytes) -> bool:
    # Перевірка підпису (демо-логіка):
    # 1) Переконатись, що публічний ключ узгоджується з приватним у межах спрощеної схеми
    if public_key_from_private(private_key_bytes) != public_key:
        return False  # ключі неконсистентні за нашою «іграшковою» формулою
    # 2) Порахувати поточний хеш файлу та «розшифрувати» підпис
    content = Path(path).read_bytes()
    current_hash = sha256_bytes(content)
    recovered_hash = xor_bytes(signature, private_key_bytes)
    # 3) Якщо збігаються — підпис дійсний для цього вмісту
    return recovered_hash == current_hash

def main():
    print("=== Спрощена система «цифрового підпису» (демо) ===")

    # Інтерактивне введення користувачем персональних даних і шляху до файлу
    lastname = input("Введіть прізвище (напр. Петренко): ").strip()
    birthday = input("Введіть дату народження (ДДММРРРР, напр. 15031995): ").strip()
    secret = input("Введіть secret_word: ").strip()
    doc_path = input("Шлях до файлу-документа (напр. резюме_Петренко.pdf): ").strip()

    # Генерація «приватного» та «публічного» ключів
    priv = derive_private_key(lastname, birthday, secret)
    pub = public_key_from_private(priv)

    print(f"\nПриватний ключ (hex): {priv.hex()}")
    print(f"Публічний ключ (int): {pub}")

    # Просте меню дій
    while True:
        print("\nОберіть дію:")
        print("1) Створити підпис для файлу")
        print("2) Перевірити підпис для файлу")
        print("3) Демонстрація виявлення підробки")
        print("4) Вийти")
        choice = input("Ваш вибір (1-4): ").strip()

        if choice == "1":
            # Створення підпису
            try:
                signature = sign_file(doc_path, priv)
                print(f"Підпис (hex): {signature.hex()}")
            except FileNotFoundError:
                print("Помилка: файл не знайдено. Перевірте шлях.")
        elif choice == "2":
            # Перевірка підпису, введеного користувачем у hex
            sig_hex = input("Введіть підпис (hex): ").strip()
            try:
                signature = bytes.fromhex(sig_hex)
                is_valid = verify_file(doc_path, signature, pub, priv)
                print("Результат:", "Підпис ДІЙСНИЙ" if is_valid else "Підпис ПІДРОБЛЕНИЙ")
            except ValueError:
                print("Некоректний формат підпису (hex).")
            except FileNotFoundError:
                print("Помилка: файл не знайдено. Перевірте шлях.")
        elif choice == "3":
            # Показати, що зміна одного байта у вмісті вже ламає відповідність хешів
            try:
                signature = sign_file(doc_path, priv)          # оригінальний підпис
                recovered_hash = xor_bytes(signature, priv)    # «розшифрований» хеш оригіналу

                content = Path(doc_path).read_bytes()
                fake_content = content + b"X"                  # моделюємо зміну документа
                fake_hash = hashlib.sha256(fake_content).digest()

                print(f"Ориг. підпис (hex): {signature.hex()}")
                print("Демонстрація підробки:",
                      "ВИЯВЛЕНО" if recovered_hash != fake_hash else "НЕ ВИЯВЛЕНО")
            except FileNotFoundError:
                print("Помилка: файл не знайдено. Перевірте шлях.")
        elif choice == "4":
            print("Вихід.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
