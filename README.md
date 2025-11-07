# Books Scraper Project

## Цель проекта
Разработка системы для автоматического сбора данных о книгах с сайта [Books to Scrape](http://books.toscrape.com). Проект включает функции для парсинга всех страниц сайта, извлечения информации о книгах, автоматического ежедневного запуска задачи и сохранения результатов.

## Функциональность
- Парсинг данных о книгах (название, цена, рейтинг, описание, наличие на складе)
- Парсинг всех страниц каталога
- Автоматический запуск по расписанию каждый день в 19:00
- Сохранение результатов в текстовый файл
- Модульное тестирование функций парсера

## Используемые сторонние  библиотеки
- `requests` - для выполнения HTTP-запросов
- `beautifulsoup4` - для парсинга HTML-страниц
- `schedule` - для настройки автоматического запуска по расписанию
- `pytest` - для написания и запуска тестов

## Структура проекта
panfilova_tatiana_hw3/
├── artifacts/ # Результаты парсинга
│ └── books_data.txt
├── notebooks/ # Jupyter ноутбуки
│ └── HW_03_python_ds_2025.ipynb
├── tests/ # Тесты
│ └── scraper_test.py
├── scraper.py # Основной скрипт парсера
├── requirements.txt # Зависимости проекта
├── README.md # Документация
└── .gitignore # Игнорируемые файлы

## Инструкции по запуску

### 1. Клонирование репозитория
```bash
git clone https://github.com/PanfilovaTP/panfilova_tatiana_hw3.git
cd panfilova_tatiana_hw3'

### 2. Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Для Windows:
venv\Scripts\activate
# Для Linux/Mac:
source venv/bin/activate

### 3. Установка зависимостей
pip install -r requirements.txt

### 4. Запуск парсера
python scraper.py
 
### 5. Запуск тестов

pytest tests/test_scraper.py -v
