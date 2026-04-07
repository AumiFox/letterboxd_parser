# letterboxd_parser
                                                                             Парсинг letterboxd
Краткое описание проета:
Парсер для сбора информации об оценках фильмов пользователя Letterboxd.

Задачи:
При создании рекомендательной системы фильмов необходимо иметь данные о предпочтениях пользователей. Letterboxd — это социальная сеть для любителей кино, где пользователи оценивают просмотренные фильмы.

                                                                            **Цель проекта:** 
Разработать парсер, который принимает уникальный идентификатор пользователя Letterboxd и возвращает информацию об оценках фильмов этим пользователем.

                                                                           **Результат:** 
Структурированные данные (название фильма, год выпуска, оценка пользователя) в форматах Excel, CSV или JSON.

                                                                            Установка и запуск
1.Установка зависимостей

```bash
pip install cloudscraper beautifulsoup4 pandas openpyxl

2.Запуск

bash
python letterboxd_parser.py rfeldman9 --format excel

3.Использование в коде

python
from letterboxd_parser import collect_user_rates

data = collect_user_rates('rfeldman9', save_format='excel')

                                                                               Пример результатов
Входные данные
Пользователь: rfeldman9

Выходные данные (Excel-файл)
название	год	рейтинг
The Nice Guys	2016	4.5
Last Action Hero	1993	3.5
Tokyo Godfathers	2003	5.0
Perfect Blue	1997	5.0
Picnic at Hanging Rock	1975	Нет оценки

Статистика:
Всего фильмов: 609
С оценкой: 580
Без оценки: 29
Средний рейтинг: 3.85

Форматы сохранения
Excel (.xlsx) -  данном случае
CSV (.csv)
JSON (.json)
