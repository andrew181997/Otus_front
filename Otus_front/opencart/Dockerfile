# Используем официальный образ Python с slim-версией
FROM python:3.9-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    # Для Chrome
    libnss3 \
    libgconf-2-4 \
    # Для Firefox
    libgtk-3-0 \
    libdbus-glib-1-2 \
    && rm -rf /var/lib/apt/lists/*

# Установка последней версии Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Установка ChromeDriver через Selenium Manager
ENV SELENIUM_GRID_URL=""
RUN pip install --upgrade selenium

# Проверка версий
RUN echo "Chrome version: $(google-chrome --version)" && \
    echo "ChromeDriver version: $(chromedriver --version || echo 'ChromeDriver will be auto-managed')"


RUN mkdir -p /tmp/chrome_profile && \
    chmod -R 777 /tmp/chrome_profile

# Установка Firefox
RUN apt-get update && apt-get install -y firefox-esr



# Устанавливаем GeckoDriver (фиксированная версия)
RUN GECKO_DRIVER_VERSION=v0.30.0 \
    && wget -q https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz \
    && tar -xzf geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем тесты
COPY . .

# Команда для передачи аргументов выбора браузера
ENTRYPOINT ["pytest"]
CMD ["test_opencart.py", "--url=http://host.docker.internal:8081"]