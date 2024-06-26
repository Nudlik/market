### Контекст

- Данная работа представляет собой backend-часть для сайта объявлений.
- Бэкенд-часть проекта предоставляет реализацию следующего функционала:
    - Авторизация и аутентификация пользователей.
    - Распределение ролей между пользователями.
    - Восстановление пароля через электронную почту.
    - CRUD для объявлений на сайте (админ может удалять или редактировать все объявления, а пользователи только свои).
    - Под каждым объявлением пользователи могут оставлять отзывы.
    - В заголовке сайта можно осуществлять поиск объявлений по названию.

### Для запуска backend локально необходимо:

- Склонировать репозиторий
  ``` PowerShell
  https://github.com/Nudlik/market.git
  ```

- Cоздать виртуальное окружение
  ``` PowerShell
  - python -m venv venv
  ```

- Активировать виртуальное окружение
  ``` PowerShell
  .\venv\Scripts\activate
  ```

- Установить зависимости
  ``` PowerShell
  pip install -r requirements.txt
  ```

- Прописать в .env ваши настройки(пример файла .env.example):

- Приминить миграции
  ``` PowerShell
  python .\manage.py migrate
  ```

- Запустить программу из консоли/среды разработки
  ``` PowerShell
  python .\manage.py runserver
  ```
  
### Для запуска frontend локально необходимо:

- Перейти в директорию /market/frontend_react и выполнить команду
  ``` PowerShell
  npm run start
  ```

### Для запуска в контейнере необходимо:

- Запустить и поднять через докер
``` PowerShell
  docker-compose build
```

- Запуск контейнеров на фоне с флагом -d
``` PowerShell
  docker-compose up 
```