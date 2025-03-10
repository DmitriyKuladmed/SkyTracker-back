# SkyTracker Backend

**SkyTracker** — это веб-приложение для отслеживания погоды в городах. 

## Выполненные пункты

В процессе разработки проекта были реализованы следующие пункты:
- написаны тесты
- всё помещено в докер контейнер
- сделаны автодополнение (подсказки) при вводе города
- при повторном посещении сайта будет предложено посмотреть погоду в городе, в котором пользователь уже смотрел ранее
- будет сохраняться история поиска для каждого пользователя, и будет API, показывающее сколько раз вводили какой город

## Основыне используемые технологии
  - Django: Основной фреймворк для построения серверной части приложения.
  - Django REST Framework: Для создания API.
  - PostgreSQL: Реляционная база данных для хранения данных о городах и пользователях.
  - Docker: Для контейнеризации приложения и упрощения процесса развертывания.

## Как запустить проект

1. Убедитесь, что Docker установлен на вашей машине.

2. В данном случае для быстрого запуска файл .env уже создан и находиться в проекте.

3. Запустите Docker Compose для создания и запуска всех контейнеров:

    ```
    docker-compose up --build
    ```

---

**Автор**: [Кулага Дмитрий]  
