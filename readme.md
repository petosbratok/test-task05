# Тестовое задание в компанию Fabrique.

## Установка

 - Скачайте и распакуйте проект
 - Откройте консоль (или powershell) в папке с проектом
 - Установите зависимости, прописав `pip install -r requirements.txt`
 - Мигрируйте базу данных (автоматически создастся sqlite файл) `python manage.py migrate`
 - Для удобства пользования можно создать пользователя администратора `python manage.py createsuperuser`.
 - Запустите проект `python manage.py runserver`
 - Откройте еще одну консоль (или powershell) в папке с проектом
 - Пропишите команду `python -m celery -A app worker -l INFO -P eventlet`. Запустится сервер, отвечающий за распределение задач
 - Готово!

## API документация
Документация будет доступна по ссылке http://127.0.0.1:8000/#/.
Там можно прочитать все информацию по использованию методов, а также совершить запросы на любой метод.
![enter image description here](https://i.imgur.com/Vxhd9yu.jpg)
