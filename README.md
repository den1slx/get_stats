## Сравниваем таблицы со статистикой

Выводит две таблицы со статистикой.

## Установка
Токен должен быть получен из окружения. (.env файл должен содержать переменную SJ_SECRET_KEY='вашsecretkey')  
Python3 должен быть уже установлен.  
Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
## Использование
* Получаем подсказку
```
python main.py -h
```
Если запущен без аргументов используются default-значения.
```
python main.py
```