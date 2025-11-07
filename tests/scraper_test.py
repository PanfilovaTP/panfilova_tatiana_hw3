import pytest
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.append('.')

from scraper import get_book_data, scrape_books

def test_get_book_data_returns_dict():
    """Тест: функция get_book_data возвращает словарь с данными книги"""
    test_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    result = get_book_data(test_url)
    
    assert isinstance(result, dict), "Функция должна возвращать словарь"
    assert result != {}, "Словарь не должен быть пустым"

def test_get_book_data_has_required_keys():
    """Тест: словарь содержит все необходимые ключи"""
    test_url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    result = get_book_data(test_url)
    
    required_keys = ['title', 'price', 'rating', 'stock', 'description']
    for key in required_keys:
        assert key in result, f"Ключ '{key}' должен присутствовать в результате"

def test_scrape_books_returns_books():
    """Тест: функция scrape_books возвращает непустой список книг"""
    result = scrape_books(is_save=False, max_pages=1)
    
    assert isinstance(result, list), "Функция должна возвращать список"
    assert len(result) > 0, "Список книг не должен быть пустым"