from PIL import Image
import sys

# 2-байтовий маркер завершення для пошуку кінця повідомлення
END_MARKER = bytes([0xFF, 0x00, 0xFF, 0x00])  # Позначає кінець вставленого тексту

# Функція перетворення байтів у бітову послідовність
def _to_bits(data_bytes):
    for byte in data_bytes:
        # Проходимо по кожному біту в байті від старшого до молодшого
        for i in range(7, -1, -1):
            yield (byte >> i) & 1  # Відокремлюємо біт за допомогою бітової маски

# Функція перетворення бітів назад у байти
def _from_bits(bits):
    out = bytearray()
    cur = 0  # Поточний байт
    count = 0  # Лічильник бітів у поточному байті
    for b in bits:
        cur = (cur << 1) | b  # Додаємо біт до поточного байта
        count += 1
        if count == 8:  # Якщо набрали 8 бітів — зберігаємо байт
            out.append(cur)
            cur = 0
            count = 0
    return bytes(out)

# Функція для приховання повідомлення у зображенні
def hide_message(cover_path, stego_path, message_text):
    img = Image.open(cover_path).convert('RGB')  # Відкриваємо зображення і конвертуємо у RGB
    pixels = img.load()  # Доступ до пікселів зображення
    w, h = img.size  # Ширина і висота зображення

    payload = message_text.encode('utf-8') + END_MARKER  # Перетворюємо текст у байти і додаємо маркер
    bits = list(_to_bits(payload))  # Перетворюємо повідомлення у бітову послідовність
    capacity_bits = w * h * 3  # Кількість доступних бітів (по 1 біту на кожний канал R, G, B)

    # Перевірка чи вистачає ємності зображення
    if len(bits) > capacity_bits:
        raise ValueError(f"Недостатня ємність: потрібно {len(bits)} біт, доступно {capacity_bits}")

    i = 0  # Лічильник бітів для вставки
    for y in range(h):
        for x in range(w):
            if i >= len(bits):
                break  # Якщо всі біти вставлені, вихід із циклу
            r, g, b = pixels[x, y]
            # Заміна молодшого біту у кожному каналі на біт повідомлення
            nr = (r & ~1) | bits[i] if i < len(bits) else r
            i += 1
            ng = (g & ~1) | bits[i] if i < len(bits) else g
            i += 1
            nb = (b & ~1) | bits[i] if i < len(bits) else b
            i += 1
            pixels[x, y] = (nr, ng, nb)  # Оновлюємо піксель
        if i >= len(bits):
            break

    img.save(stego_path, format='PNG')  # Зберігаємо нове зображення
    print(f"Готово! Секрет вставлено. Збережено у {stego_path}")
    print(f"Використано біт: {len(bits)}/{capacity_bits}, BPP: {round(len(bits)/(w*h), 3)}")  # Інформація про використання бітів

# Функція для витягування прихованого повідомлення
def extract_message(stego_path):
    img = Image.open(stego_path).convert('RGB')  # Відкриваємо стего-зображення
    pixels = img.load()
    w, h = img.size
    bits = []

    # Збираємо молодші біти з усіх пікселів
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            bits.append(r & 1)
            bits.append(g & 1)
            bits.append(b & 1)

    data = _from_bits(bits)  # Перетворюємо біти назад у байти
    idx = data.find(END_MARKER)  # Знаходимо маркер завершення
    if idx == -1:
        raise ValueError("Маркер завершення не знайдено — можливо, повідомлення не вставлялося або зображення оброблено не цим кодом!")
    print("Витягнутий текст:")
    print(data[:idx].decode('utf-8'))  # Декодуємо повідомлення з байтів у текст

# Основний блок для запуску з командного рядка
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання:")
        print("  python app.py hide test.png stego.png 'Ваш текст'")
        print("  python app.py extract stego.png")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    try:
        if cmd == "hide":
            if len(sys.argv) < 5:
                print("Приклад: python app.py hide test.png stego.png 'Ваш текст'")
                sys.exit(1)
            cover, stego, msg = sys.argv[2], sys.argv[3], " ".join(sys.argv[4:])
            hide_message(cover, stego, msg)  # Виклик функції приховання
        elif cmd == "extract":
            if len(sys.argv) < 3:
                print("Приклад: python app.py extract stego.png")
                sys.exit(1)
            stego = sys.argv[2]
            extract_message(stego)  # Виклик функції витягування
        else:
            print("Невідома команда:", cmd)
            sys.exit(1)
    except Exception as e:
        print("Помилка:", e)
        sys.exit(2)
