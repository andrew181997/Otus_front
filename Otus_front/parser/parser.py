import re
import json
from collections import defaultdict
from pathlib import Path


def parse_log_line(line):
    pattern = r'^(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" (\d+)$'
    match = re.match(pattern, line)

    if not match:
        return None

    ip = match.group(1)
    date = match.group(2)
    request = match.group(3)
    duration = int(match.group(8))

    try:
        method, url, _ = request.split(' ', 2)
    except ValueError:
        method = request.split(' ', 1)[0]
        url = ""

    return {
        "ip": ip,
        "date": date,
        "method": method,
        "url": url,
        "duration": duration
    }


def analyze_logs(log_entries):
    # Инициализация счетчиков
    ip_counts = defaultdict(int)
    method_counts = defaultdict(int)
    all_requests = []

    # Обработка всех записей
    for entry in log_entries:
        ip_counts[entry["ip"]] += 1
        method_counts[entry["method"]] += 1
        all_requests.append(entry)

    # Топ 3 IP
    top_ips = sorted(
        [{"ip": ip, "count": count} for ip, count in ip_counts.items()],
        key=lambda x: x["count"],
        reverse=True
    )[:3]

    # Топ 3 самых долгих запросов
    slowest_requests = sorted(
        all_requests,
        key=lambda x: x["duration"],
        reverse=True
    )[:3]

    # Форматирование медленных запросов
    formatted_slow_requests = []
    for req in slowest_requests:
        formatted_slow_requests.append({
            "method": req["method"],
            "url": req["url"],
            "ip": req["ip"],
            "duration": req["duration"],
            "date": req["date"]
        })

    return {
        "total_requests": len(log_entries),
        "methods": dict(method_counts),
        "top_ips": top_ips,
        "slowest_requests": formatted_slow_requests
    }


def process_logs(input_path, output_path):
    if isinstance(input_path, str):
        input_path = Path(input_path)

    # Чтение логов
    log_entries = []
    with open(input_path, 'r') as f:
        for line in f:
            if entry := parse_log_line(line.strip()):
                log_entries.append(entry)

    # Анализ
    stats = analyze_logs(log_entries)

    # Сохранение
    with open(output_path, 'w') as f:
        json.dump(stats, f, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Log parser with statistics')
    parser.add_argument('input', help='Input log file path')
    parser.add_argument('-o', '--output', default='log_stats.json',
                        help='Output JSON file path')

    args = parser.parse_args()

    process_logs(args.input, args.output)
    print(f"Statistics saved to {args.output}")