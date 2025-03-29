import subprocess
from datetime import datetime
import re


def get_system_report():
    # Получаем вывод команды ps aux
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    processes = result.stdout.splitlines()[1:]  # Пропускаем заголовок

    # Инициализируем данные
    users = set()
    user_process_count = {}
    total_memory = 0.0
    total_cpu = 0.0
    max_memory_process = ("", 0.0)
    max_cpu_process = ("", 0.0)

    # Анализируем процессы
    for process in processes:
        parts = re.split(r'\s+', process.strip())
        if len(parts) < 11:
            continue

        user = parts[0]
        cpu = float(parts[2])
        memory = float(parts[3])
        command = ' '.join(parts[10:])[:20]  # Берем первые 20 символов команды

        # Собираем пользователей
        users.add(user)

        # Считаем процессы по пользователям
        user_process_count[user] = user_process_count.get(user, 0) + 1

        # Суммируем использование CPU и памяти
        total_cpu += cpu
        total_memory += memory

        # Находим процессы с максимальным использованием
        if memory > max_memory_process[1]:
            max_memory_process = (command, memory)
        if cpu > max_cpu_process[1]:
            max_cpu_process = (command, cpu)

    # Формируем отчет
    report = f"Отчёт о состоянии системы:\n"
    report += f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += f"Пользователи системы: {', '.join(sorted(users))}\n"
    report += f"Процессов запущено: {len(processes)}\n\n"
    report += "Пользовательских процессов:\n"
    for user, count in sorted(user_process_count.items(), key=lambda x: x[1], reverse=True):
        report += f"{user}: {count}\n"

    report += f"\nВсего памяти используется: {total_memory:.1f}%\n"
    report += f"Всего CPU используется: {total_cpu:.1f}%\n"
    report += f"Больше всего памяти использует: {max_memory_process[0]} ({max_memory_process[1]:.1f}%)\n"
    report += f"Больше всего CPU использует: {max_cpu_process[0]} ({max_cpu_process[1]:.1f}%)\n"

    return report


def save_report_to_file(report):
    filename = f"system_report_{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(filename, 'w') as f:
        f.write(report)
    print(f"Отчёт сохранён в файл: {filename}")


# Основная программа
if __name__ == "__main__":
    report = get_system_report()
    print(report)  # Выводим отчет в консоль
    save_report_to_file(report)  # Сохраняем в файл
