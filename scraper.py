import time
import requests
import schedule
import re
from bs4 import BeautifulSoup

def get_book_data(book_url: str) -> dict:
    """
    Парсит данные о книге с указанного URL.
    
    Args:
        book_url (str): URL страницы книги для парсинга
        
    Returns:
        dict: Словарь с информацией о книге
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    try:
        response = requests.get(book_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Название книги
        title = soup.find('h1').text.strip()
        
        # Цена
        price = soup.find('p', class_='price_color').text.strip()
        
        # Рейтинг
        rating_class = soup.find('p', class_='star-rating')['class'][1]
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating = rating_map.get(rating_class, 0)
        
        # Количество в наличии
        stock_text = soup.find('p', class_='instock availability').text.strip()
        stock_match = re.search(r'\((\d+) available\)', stock_text)
        stock = int(stock_match.group(1)) if stock_match else 0
        
        # Описание
        description_element = soup.find('div', id='product_description')
        description = ""
        if description_element:
            description_sibling = description_element.find_next_sibling('p')
            if description_sibling:
                description = description_sibling.text.strip()
        
        # Таблица Product Information
        product_info = {}
        table = soup.find('table', class_='table table-striped')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                header = row.find('th').text.strip()
                value = row.find('td').text.strip()
                product_info[header] = value
        
        book_data = {
            'title': title,
            'price': price,
            'rating': rating,
            'stock': stock,
            'description': description,
            'upc': product_info.get('UPC', ''),
            'product_type': product_info.get('Product Type', ''),
            'price_excl_tax': product_info.get('Price (excl. tax)', ''),
            'price_incl_tax': product_info.get('Price (incl. tax)', ''),
            'tax': product_info.get('Tax', ''),
            'availability': product_info.get('Availability', ''),
            'num_reviews': product_info.get('Number of reviews', '')
        }
        
        return book_data
        
    except Exception as e:
        print(f"Ошибка при парсинге {book_url}: {e}")
        return {}
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ


def scrape_books(is_save: bool = False, max_pages: int = None) -> list:
    """
    Parses books from catalog pages.
    
    Args:
        is_save (bool): If True, saves data to books_data.txt file
        max_pages (int, optional): Maximum number of pages to parse.
                                  If None, parses all pages.
        
    Returns:
        list: List of dictionaries with book information
    """

    # НАЧАЛО ВАШЕГО РЕШЕНИЯ
    import requests
    from bs4 import BeautifulSoup
    import time
    
    base_url = "http://books.toscrape.com/catalogue/"
    all_books = []
    page = 1
    
    print("Starting parsing...")
    if max_pages:
        print(f"Limit: {max_pages} pages")
    else:
        print("Parsing all available pages")
    
    while True:
        # Проверка лимита страниц
        if max_pages and page > max_pages:
            print(f"Reached limit of {max_pages} pages")
            break
            
        if page == 1:
            url = f"{base_url}page-1.html"
        else:
            url = f"{base_url}page-{page}.html"
        
        print(f"Parsing page {page}: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            
            # Если страницы не существует, заканчивает цикл
            if response.status_code == 404:
                print(f"Reached last page ({page-1} pages total)")
                break
                
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            books = soup.find_all('article', class_='product_pod')
            
            if not books:
                print("No books found on page")
                break
            
            print(f"Found {len(books)} books on page {page}")
            
            book_count = 0
            for book in books:
                # Get link to book page
                book_link = book.find('h3').find('a')['href']
                
                if book_link.startswith('../../../'):
                    full_book_url = f"http://books.toscrape.com/catalogue/{book_link[9:]}"
                else:
                    full_book_url = f"http://books.toscrape.com/catalogue/{book_link}"
                
                book_data = get_book_data(full_book_url)
                if book_data:
                    all_books.append(book_data)
                    book_count += 1
                
                time.sleep(0.1)
            
            print(f"Page {page}: successfully collected {book_count} books")
            
            next_button = soup.find('li', class_='next')
            if not next_button:
                print(f"No more pages to parse (total {page} pages)")
                break
                
            page += 1
            
        except requests.RequestException as e:
            print(f"Network error while parsing page {page}: {e}")
            break
        except Exception as e:
            print(f"Error while parsing page {page}: {e}")
            break
    
    print(f"Parsing completed. Total collected {len(all_books)} books from {page-1} pages")
    
    # Сохранение в файл
    if is_save and all_books:
        try:
            with open('books_data.txt', 'w', encoding='utf-8') as f:
                f.write("BOOKS DATA\n")
                f.write("=" * 80 + "\n")
                f.write(f"Total books: {len(all_books)}\n")
                f.write(f"Total pages: {page-1}\n")
                f.write(f"Collection time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                for i, book in enumerate(all_books, 1):
                    f.write(f"BOOK #{i}\n")
                    f.write(f"Title: {book.get('title', 'N/A')}\n")
                    f.write(f"Price: {book.get('price', 'N/A')}\n")
                    f.write(f"Rating: {book.get('rating', 'N/A')}/5\n")
                    f.write(f"Stock: {book.get('stock', 'N/A')} items\n")
                    f.write(f"Description: {book.get('description', 'N/A')}\n")
                    f.write(f"UPC: {book.get('upc', 'N/A')}\n")
                    f.write(f"Product Type: {book.get('product_type', 'N/A')}\n")
                    f.write(f"Price (excl. tax): {book.get('price_excl_tax', 'N/A')}\n")
                    f.write(f"Price (incl. tax): {book.get('price_incl_tax', 'N/A')}\n")
                    f.write(f"Tax: {book.get('tax', 'N/A')}\n")
                    f.write(f"Availability: {book.get('availability', 'N/A')}\n")
                    f.write(f"Number of reviews: {book.get('num_reviews', 'N/A')}\n")
                    f.write("-" * 80 + "\n\n")
            
            print(f"Full data saved to books_data.txt")
            
        except Exception as e:
            print(f"Error saving file: {e}")
    
    return all_books
    # КОНЕЦ ВАШЕГО РЕШЕНИЯ
       
# НАЧАЛО ВАШЕГО РЕШЕНИЯ
import time
import schedule

def scheduled_scraping():
    """
    Функция для автоматического запуска парсинга по расписанию.
    Будет вызываться только в 19:00 каждый день.
    """
    print(f"\n{'='*60}")
    print(f"АВТОМАТИЧЕСКИЙ ПАРСИНГ: Запуск в {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Здесь будет запуск scrape_books(is_save=True, max_pages=None)")
    print(f"{'='*60}")

# Настройка расписания - ежедневно в 19:00
schedule.every().day.at("19:00").do(scheduled_scraping)

print("✓ ПЛАНИРОВЩИК: Инициализирован")
print("✓ Задача: Ежедневный парсинг в 19:00")
print(f"✓ Текущее время: {time.strftime('%H:%M:%S')}")
print("✓ Планировщик настроен, но НЕ запущен")

# КОНЕЦ ВАШЕГО РЕШЕНИЯ