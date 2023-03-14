## Сравниваем таблицы со статистикой

Выводит две таблицы со статистикой.

### Установка
Токен должен быть получен из окружения. (.env файл должен содержать переменную SJ_SECRET_KEY='вашsecretkey')  
Получить secretkey можно [здесь](https://api.superjob.ru/).  
Python3 должен быть уже установлен.  
Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```commandline
pip install -r requirements.txt
```
### Использование
* Получаем подсказку
```commandline
python main.py -h
```
Если запущен без аргументов используются default-значения.
```commandline
python main.py
```
Передаем keywords для поиска
```commandline
python main.py -t "Программист Python", "Программист C#" 
```
Передаем параметры для поиска в hh. Это должна быть json строка.
[Подробнее про параметры поиска](https://github.com/hhru/api/blob/master/docs/vacancies.md#search)
```commandline
python main.py -hp '{\"professional_role\": \"96\",\"area\": \"1\", \"date_from\": \"2000-01-01\", \"per_page\": 100}' 
```
Передаем параметры для поиска в sj. Это тоже должна быть json строка.
[Подробнее про параметры поиска](https://api.superjob.ru/#search_vacanices)
```commandline
python main.py -sp '{\"period\": 0, \"town\": 4, \"catalogues\": 48, \"count\": 100}'
```
Можно настроить заголовки таблиц.
Для hh:
```commandline
python main.py -thh "Заголовок 1", "Заголовок 2", "3", "особый"
```
Для sj:
```commandline
python main.py -tsj "Заг", "оло", "вок", "особый"
```

Можно и всё вместе:
```commandline
python main.py -t "программист python" -thh "1", "2", "3", "4" -tsj "5", "6", "7", "8" -hp '{\"professional_role\"
: \"96\",\"area\": \"1\", \"date_from\": \"2000-01-01\", \"per_page\": 100}' -sp '{\"period\": 0, \"town\": 4, \"catalogues\": 48, \"count\": 100}'

```
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).