import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_sample_data():
    """
    Scrape sample quotes from quotes.toscrape.com
    """
    try:
        print("🚀 Starting web scraper...")
        
        url = "https://quotes.toscrape.com"
        
        # Send GET request
        response = requests.get(url, timeout=10)
        print(f"📡 Status code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # دیباگ: کل HTML رو save کنیم ببینیم چی داریم
            with open('data/debug_html.html', 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print("📄 Debug HTML saved to data/debug_html.html")
            
            # راه‌حل: تمام divها رو بررسی کنیم
            all_divs = soup.find_all('div')
            print(f"🔍 Found {len(all_divs)} div elements total")
            
            # پیدا کردن نقل قول‌ها با روش مختلف
            quotes_data = []
            
            # روش ۱: جستجو با کلاس‌های مختلف
            possible_classes = ['quote', 'text', 'quoteText', 'quote-text']
            
            for class_name in possible_classes:
                elements = soup.find_all(class_=class_name)
                print(f"🔎 Searching with class '{class_name}': found {len(elements)} elements")
            
            # روش ۲: پیدا کردن spanهایی که حاوی نقل قول هستند
            quote_spans = soup.find_all('span')
            print(f"🔎 Found {len(quote_spans)} span elements")
            
            for span in quote_spans:
                if span.get('class') and 'text' in span.get('class'):
                    text = span.text.strip()
                    # پیدا کردن نویسنده
                    author = "Unknown"
                    next_element = span.find_next('small')
                    if next_element:
                        author = next_element.text.strip()
                    
                    # پیدا کردن تگ‌ها
                    tags = []
                    tag_container = span.find_next('div', class_='tags')
                    if tag_container:
                        tags = [tag.text.strip() for tag in tag_container.find_all('a', class_='tag')]
                    
                    if text and text.startswith('“') and text.endswith('”'):
                        quotes_data.append({
                            'quote': text,
                            'author': author,
                            'tags': ', '.join(tags)
                        })
            
            print(f"📖 Found {len(quotes_data)} quotes after detailed search")
            
            # اگر بازم چیزی پیدا نکردیم، داده نمونه بسازیم
            if len(quotes_data) == 0:
                print("⚠️ No quotes found, creating sample data...")
                quotes_data = [
                    {'quote': '“The only way to do great work is to love what you do.”', 'author': 'Steve Jobs', 'tags': 'inspiration, work'},
                    {'quote': '“Innovation distinguishes between a leader and a follower.”', 'author': 'Steve Jobs', 'tags': 'innovation, leadership'},
                    {'quote': '“Stay hungry, stay foolish.”', 'author': 'Steve Jobs', 'tags': 'motivation, life'}
                ]
            
            # ذخیره در CSV
            os.makedirs('data', exist_ok=True)
            df = pd.DataFrame(quotes_data)
            df.to_csv('data/sample_quotes.csv', index=False, encoding='utf-8')
            
            print("✅ Successfully saved data to data/sample_quotes.csv")
            print("📊 Sample data:")
            for i, item in enumerate(quotes_data[:3], 1):
                print(f"  {i}. {item['quote']}")
                print(f"     — {item['author']}")
                print(f"     Tags: {item['tags']}")
                
            return quotes_data
            
        else:
            print(f"❌ Failed to retrieve page. Status: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"💥 Error occurred: {e}")
        return []

if __name__ == "__main__":
    scrape_sample_data()