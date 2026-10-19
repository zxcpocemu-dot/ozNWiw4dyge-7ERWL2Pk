import requests
import base64
import urllib.parse

# Ваши исходные ссылки
SOURCES = [
    "https://codeberg.org/zieng2/wl/raw/branch/main/vless_universal.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/MahanKenway/Freedom-V2Ray/main/configs/mix_sub.txt"
]

# Ключевые слова для исключения РФ
RU_KEYWORDS = [
    "russia", "russian", "moscow", "msk", "spb", "saint-petersburg", 
    "россия", "москва", "питер", "рф", "ru-", "-ru", "_ru", ".ru", "ru_"
]

def decode_base64_if_needed(text):
    try:
        decoded = base64.b64decode(text).decode('utf-8')
        if "://" in decoded:
            return decoded
    except Exception:
        pass
    return text

def is_valid_vless_and_not_ru(link):
    if not link.startswith("vless://"):
        return False
    
    link_lower = link.lower()
    try:
        fragment = link.split("#")[-1]
        server_name = urllib.parse.unquote(fragment).lower()
    except:
        server_name = ""

    full_text_to_check = link_lower + " " + server_name
    
    for keyword in RU_KEYWORDS:
        if keyword in full_text_to_check:
            return False
            
    return True

def main():
    unique_links = set()

    print("Начинаем скачивание подписок...")
    for url in SOURCES:
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            content = decode_base64_if_needed(response.text)
            
            for line in content.splitlines():
                line = line.strip()
                if line.startswith("vless://"):
                    unique_links.add(line)
        except Exception as e:
            print(f"Ошибка при скачивании {url}: {e}")

    print(f"Всего найдено уникальных VLESS-ссылок: {len(unique_links)}")
    clean_links = [link for link in unique_links if is_valid_vless_and_not_ru(link)]
    print(f"Осталось после фильтрации (без РФ): {len(clean_links)}")

    with open("output.txt", "w", encoding="utf-8") as f:
        for link in clean_links:
            f.write(link + "\n")
            
    print("Готово! Результат сохранен в output.txt")

if __name__ == "__main__":
    main()
