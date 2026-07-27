import os
import time
from datetime import datetime

print("=== ЗАПУСК ПРОДВИНУТОГО МОНИТОРИНГА ===")
try:
    while True:
        try:
            with open("targets.txt", "r") as file:
                for line in file:
                    ip = line.strip()
                    if not ip:
                        continue
                    
                    print(f"[i] Проверяем {ip}...")
                    response = os.system(f"ping -c 1 {ip} > /dev/null 2>&1")

                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if response == 0:
                        print(f" [+] успех! хост {ip} доволен.")
                        with open("report.txt", "a") as log_file:
                            log_file.write(f"[{now}] [+] {ip} доступен\n")
                    else:
                        print(f" [-] Ошибка! хост {ip} НЕ отвечает.")
                        with open("report.txt", "a") as log_file:
                            log_file.write(f"[{now}] [-] {ip} НЕ ОТВЕЧАЕТ\n")
                            
        except FileNotFoundError:
            print(" [!] КРИТИЧЕСКАЯ ОШИБКА: файл 'targets.txt' не найден!")
            print(" [!] Пожалуйста, создай его и закинь туда IP-адреса.")
        
        print("\n[*] Засыпаю на 5 секунд...\n")
        time.sleep(5)

except KeyboardInterrupt:
    print("\n\n[-] Мониторинг принудительно остановлен пользователем.")
    print("[*] До встречи!")
