import base64
import os
import getpass  # Імпортуємо для прихованого введення пароля
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# --- Налаштування для генерації ключа ---
# Сіль (SALT) має бути однаковою для шифрування та розшифрування.
# У реальному додатку її потрібно передавати разом з повідомленням.
# Для простоти лабораторної роботи ми залишаємо її константою.
SALT = b'fixed_salt_for_lab_demo_123'

def generate_key_from_password(password: str) -> bytes:
    """
    Безпечно генерує 32-байтний ключ шифрування з пароля користувача
    за допомогою PBKDF2.
    """
    password_bytes = password.encode('utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=480000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key

def encrypt_message(message: str, fernet_key: bytes) -> bytes:
    """
    Шифрує повідомлення за допомогою симетричного ключа Fernet.
    """
    f = Fernet(fernet_key)
    message_bytes = message.encode('utf-8')
    token = f.encrypt(message_bytes)
    return token

def decrypt_message(token: bytes, fernet_key: bytes) -> str:
    """
    Розшифровує повідомлення за допомогою симетричного ключа Fernet.
    """
    f = Fernet(fernet_key)
    try:
        decrypted_bytes = f.decrypt(token)
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        # Це спрацює, якщо ключ невірний або дані пошкоджені
        return "[ПОМИЛКА РОЗШИФРУВАННЯ] Невірний ключ або пошкоджені дані."

# --- Інтерактивне меню для користувача ---

def main_menu():
    """
    Головне меню програми, що дозволяє користувачу
    вводити власні дані.
    """
    while True:
        print("\n--- 🔐 Інтерактивний Шифратор ---")
        print("Оберіть дію:")
        print("  1. Зашифрувати повідомлення")
        print("  2. Розшифрувати повідомлення")
        print("  3. Вийти")
        
        choice = input("Ваш вибір (1, 2 або 3): ")

        if choice == '1':
            # --- Шифрування ---
            print("\n[РЕЖИМ ШИФРУВАННЯ]")
            # Використовуємо getpass, щоб пароль не було видно при вводі
            password = getpass.getpass("  Введіть ваш секретний ключ (пароль): ")
            message = input("  Введіть повідомлення для шифрування: ")

            try:
                key = generate_key_from_password(password)
                encrypted_data = encrypt_message(message, key)
                print("\nУСПІХ!")
                print("  Ваші зашифровані дані (скопіюйте їх):")
                print(f"  {encrypted_data.decode()}")
            except Exception as e:
                print(f"\nПОМИЛКА під час шифрування: {e}")

        elif choice == '2':
            # --- Розшифрування ---
            print("\n[РЕЖИМ РОЗШИФРУВАННЯ]")
            password = getpass.getpass("  Введіть ваш секретний ключ (пароль): ")
            token_str = input("  Вставте зашифровані дані: ")

            try:
                token_bytes = token_str.encode('utf-8')
                key = generate_key_from_password(password)
                decrypted_message = decrypt_message(token_bytes, key)
                
                print("\nУСПІХ!")
                print(f"  Оригінальне повідомлення: {decrypted_message}")
            except Exception as e:
                print(f"\nПОМИЛКА: Неможливо розшифрувати. Перевірте дані та пароль.")

        elif choice == '3':
            # --- Вихід ---
            print("Завершення роботи...")
            break
            
        else:
            print("Невірний вибір. Будь ласка, введіть 1, 2 або 3.")

if __name__ == "__main__":
    main_menu()