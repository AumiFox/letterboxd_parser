import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
import time


def parse_letterboxd_diary(username):
    scraper = cloudscraper.create_scraper()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    diary_data = []
    page = 1

    print(f">>> Начинаем сбор данных для: {username}")

    while True:
        url = f"https://letterboxd.com/{username}/diary/page/{page}/"
        try:
            response = scraper.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all('tr', class_='diary-entry-row')

            if not rows:
                break

            page_count = 0
            for row in rows:
                # 1. Название фильма - из data-item-name
                title = "Неизвестно"
                film_div = row.find('div', class_='react-component')
                if film_div and film_div.get('data-item-name'):
                    title = film_div['data-item-name']
                    # Убираем год из названия (если есть в скобках)
                    if '(' in title:
                        title = title.split('(')[0].strip()

                # 2. Год выпуска
                year = "Неизвестно"
                # Из data-film-release-year
                poster_div = row.find('div', class_='poster')
                if poster_div and poster_div.get('data-film-release-year'):
                    year = poster_div['data-film-release-year']
                else:
                    # Ищем в data-item-name (год в скобках)
                    if film_div and film_div.get('data-item-name'):
                        item_name = film_div['data-item-name']
                        import re
                        year_match = re.search(r'\((\d{4})\)', item_name)
                        if year_match:
                            year = year_match.group(1)

                # 3. Оценка
                rating = None
                rating_span = row.find('span', class_='rating')
                if rating_span:
                    classes = rating_span.get('class', [])
                    for c in classes:
                        if c.startswith('rated-'):
                            rating = int(c.split('-')[1]) / 2.0
                            break

                # Добавляем запись
                diary_data.append({
                    'название': title,
                    'год': year,
                    'рейтинг': rating if rating is not None else 'Нет оценки'
                })
                page_count += 1

                # Отладка
                if len(diary_data) <= 10:
                    rating_str = str(rating) if rating else 'Нет оценки'
                    print(f"  [{len(diary_data)}] {title} | {year} | {rating_str}")

            print(f"Страница {page}: +{page_count} фильмов. Всего: {len(diary_data)}")
            page += 1
            time.sleep(1)

        except Exception as e:
            print(f"Ошибка на странице {page}: {e}")
            break

    return diary_data


# --- ЗАПУСК ---
if __name__ == "__main__":
    user = 'rfeldman9'
    data = parse_letterboxd_diary(user)

    if data:
        df = pd.DataFrame(data)

        print(f"\n{'=' * 50}")
        print(f"ПЕРВЫЕ 10 ЗАПИСЕЙ:")
        print('=' * 50)
        for i, row in df.head(10).iterrows():
            print(f"{i + 1}. {row['название']} ({row['год']}) - {row['рейтинг']}")

        filename = f'letterboxd_{user}_diary.xlsx'
        df.to_excel(filename, index=False)
        print(f"\n--- ГОТОВО ---")
        print(f"Файл '{filename}' создан. Всего записей: {len(data)}")

        # Статистика
        with_rating = len([d for d in data if d['рейтинг'] != 'Нет оценки'])
        print(f"Фильмов с оценкой: {with_rating}")
        print(f"Фильмов без оценки: {len(data) - with_rating}")
    else:
        print("\nДанные не найдены!")