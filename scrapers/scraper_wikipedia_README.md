# Описание

Данный скрипт написан на Python и предназначен для извлечения названий растений из статей на Википедии, связанных с растениями. Он использует библиотеки `requests` и `BeautifulSoup` для скачивания HTML-кода страницы и последующего извлечения данных.

# Установка

1. Установите библиотеки `requests` и `BeautifulSoup` с помощью `pip`:
2. Клонируйте скрипт в свой проект.
3. Запустите скрипт с помощью Python.

# Функциональность

Скрипт выполняет следующие действия:

- Загружает страницу со списками растений с Википедии.
- Извлекает все ссылки со страницы.
- Ищет ссылки, начинающиеся с "List", что обычно указывает на список растений.
- Переходит по найденным ссылкам и извлекает названия растений со страницы.
- Фильтрует и очищает названия растений от ненужных символов и слов.
- Записывает очищенные названия в файл `cleaned_plant_names.txt`.

