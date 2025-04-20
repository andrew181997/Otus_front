# Базовый запуск
`bash
python log_parser.py access.log`
Результат будет в log_stats.json

# Своё имя файла для результатов

`bash
python log_parser.py access.log -o my_stats.json`
Результат будет в my_stats.json

# Запуск парсера на директорию 
Как работает:

1.Получает путь к папке

2.Рекурсивно ищет все файлы *.log

3.Обрабатывает каждый найденный файл

Пример:

`bash
python log_parser.py /var/log/nginx/ -o nginx_stats.json`

В результате выполнения скрипты будут проверены все файлы в директории /var/log/nginx/ с расширением .log и результат записан в nginx_stats.json

# Рекурсивная обработка

`bash
python3 log_parser.py /путь/к/директории --recursive`
Просканирует все вложенные папки и выведет результат скрипта по всем вложенным файлам 

