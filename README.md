# AI-ассистент ПРМ "Паром"

## Кейс 01.Риск-инструменты: AI-агент для портфельных аналитиков 
## Описание проекта

AI-ассистент ПРМ "Паром" — это интеллектуальный text2sql помощник для портфельных аналитиков.

## Как воспользоваться AI-агентом

Чтобы начать использовать AI-ассистента, перейдите по [http://212.67.8.208:5021/]. Если кажется, что что-то пошло не так, то откройте страницу в режиме инкогнито (предварительно закрыв имеющиеся вкладки режима инкогнито)

### Особенности взаимодействия с агентом

- AI-ассистент работает только с запросами, связанными с данными из нашей синтезированной базы данных.  
- Запросы должны быть четко сформулированы и касаться тематики анализа портфелей.  

### Краткое описание базы данных
### Таблица: `individual_borrowers`

| Поле             | Тип данных | Описание                                  | Ограничения               |
|-------------------|------------|-------------------------------------------|---------------------------|
| individual_id    | SERIAL     | Уникальный идентификатор физического заемщика | PRIMARY KEY              |
| date_of_birth    | DATE       | Дата рождения заемщика                   | -                         |

---

### Таблица: `company_borrowers`

| Поле             | Тип данных   | Описание                                  | Ограничения                                      |
|-------------------|--------------|-------------------------------------------|-------------------------------------------------|
| company_id       | SERIAL       | Уникальный идентификатор компании-заемщика | PRIMARY KEY                                    |
| company_name     | VARCHAR(255) | Название компании                        | NOT NULL                                       |
| business_sector  | VARCHAR(100) | Сектор бизнеса                           | Допустимые значения: `Информационные технологии`, `Финансовые организации`, `Коммерция`, `Энергетика`, `Производство`, `Недвижимость` |

---

### Таблица: `credit_products`

| Поле              | Тип данных   | Описание                                  | Ограничения                                      |
|--------------------|--------------|-------------------------------------------|-------------------------------------------------|
| product_id        | SERIAL       | Уникальный идентификатор кредитного продукта | PRIMARY KEY                                    |
| product_name      | VARCHAR(100) | Тип продукта                             | Допустимые значения: `Потребительский кредит`, `Ипотека`, `Автокредит`, `Кредитная карта`, `Бизнес-кредит`, `Возобновляемая кредитная линия`, `Гарантия` |
| interest_rate     | NUMERIC(5,2) | Процентная ставка                        | Пример: 5.25                                   |
| min_loan_amount   | NUMERIC(15,2)| Минимальная сумма займа                  | -                                              |
| max_loan_amount   | NUMERIC(15,2)| Максимальная сумма займа                 | -                                              |
| term_months       | INT          | Срок займа в месяцах                     | -                                              |

---

### Таблица: `credits`

| Поле              | Тип данных   | Описание                                  | Ограничения                                      |
|--------------------|--------------|-------------------------------------------|-------------------------------------------------|
| credit_id         | SERIAL       | Уникальный идентификатор кредита         | PRIMARY KEY                                    |
| individual_id     | INT          | Ссылка на физического заемщика           | Может быть NULL (взаимоисключающее с company_id) |
| company_id        | INT          | Ссылка на компанию-заемщика              | Может быть NULL (взаимоисключающее с individual_id) |
| product_id        | INT          | Ссылка на кредитный продукт              | NOT NULL, внешний ключ (credit_products.product_id) |
| loan_amount       | NUMERIC(15,2)| Сумма кредита                            | -                                              |
| interest_rate     | NUMERIC(5,2) | Процентная ставка по кредиту             | -                                              |
| start_date        | DATE         | Дата начала кредита                      | NOT NULL                                       |
| end_date          | DATE         | Планируемая дата погашения               | Может быть NULL                                |
| status            | VARCHAR(50)  | Статус кредита                           | Допустимые значения: `Активный`, `Закрытый`, `Дефолт`. Значение по умолчанию: `Активный` |

---

### Таблица: `client_transactions`

| Поле               | Тип данных    | Описание                                  | Ограничения                                      |
|---------------------|---------------|-------------------------------------------|-------------------------------------------------|
| transaction_id     | SERIAL        | Уникальный идентификатор транзакции      | PRIMARY KEY                                    |
| credit_id          | INT           | Ссылка на кредит                         | NOT NULL, внешний ключ (credits.credit_id)      |
| transaction_type   | VARCHAR(100)  | Тип транзакции                           | Допустимые значения: `Выплата основного долга`, `Выплата просроченного долга`, `Выплата штрафов` |
| amount             | NUMERIC(15,2) | Сумма транзакции                         | NOT NULL                                       |
| transaction_date   | TIMESTAMP     | Дата и время транзакции                  | NOT NULL                                       |

---

### Таблица: `risk_ratings`

| Поле                  | Тип данных    | Описание                                  | Ограничения                                      |
|-----------------------|---------------|-------------------------------------------|-------------------------------------------------|
| rating_id            | SERIAL        | Уникальный идентификатор оценки риска    | PRIMARY KEY                                    |
| individual_id        | INT           | Ссылка на физического заемщика           | Может быть NULL (взаимоисключающее с company_id) |
| company_id           | INT           | Ссылка на компанию-заемщика              | Может быть NULL (взаимоисключающее с individual_id) |
| credit_id            | INT           | Ссылка на кредит                         | NOT NULL, внешний ключ (credits.credit_id)      |
| rating               | INT           | Оценка риска                             | Диапазон: 1–26                                 |
| probability_of_default | NUMERIC(3,2) | Вероятность дефолта                      | Диапазон: 0.00–1.00                            |
| rating_date          | DATE          | Дата оценки                              | NOT NULL                                       |

---

### Таблица: `defaults`

| Поле                  | Тип данных    | Описание                                  | Ограничения                                      |
|-----------------------|---------------|-------------------------------------------|-------------------------------------------------|
| default_id           | SERIAL        | Уникальный идентификатор дефолта         | PRIMARY KEY                                    |
| credit_id            | INT           | Ссылка на кредит                         | NOT NULL, внешний ключ (credits.credit_id)      |
| default_date         | DATE          | Дата наступления дефолта                 | NOT NULL                                       |
| default_amount       | NUMERIC(15,2) | Непогашенная сумма на момент дефолта     | NOT NULL                                       |
| recovery_amount      | NUMERIC(15,2) | Восстановленная сумма                    | Может быть NULL                                |
| reason_for_default   | VARCHAR(100)  | Причина дефолта                          | Допустимые значения: `Просрочка`, `Банкротство`, `Реструктуризация`, `Ликвидация`, `Цессия` |

---

### Таблица: `credit_reserves`

| Поле              | Тип данных    | Описание                                  | Ограничения                                      |
|--------------------|---------------|-------------------------------------------|-------------------------------------------------|
| reserve_id        | SERIAL        | Уникальный идентификатор резерва         | PRIMARY KEY                                    |
| credit_id         | INT           | Ссылка на кредит                         | NOT NULL, внешний ключ (credits.credit_id)      |
| reserve_stage     | VARCHAR(50)   | Этап резервирования                      | Допустимые значения: `Стадия 1`, `Стадия 2`, `Стадия 3` |
| reserve_amount    | NUMERIC(15,2) | Зарезервированная сумма                  | NOT NULL                                       |
### Примеры запросов

**Запрос:** "Когда в последний раз была произведена выдача кредита, размером более 100000?"  

**Запрос:** "Сколько было каких причин дефолта за последний месяц?"  

**Запрос:** "Выведи топ-10 наименее закредитованных компаний" 

**Запрос:** "Какая процентная ставка у активных кредитов?"
  

## Как собрать проект

Для корректного запуска проекта необходимо иметь:
* Ubuntu 20.02
* Python 3.11
* Nginx 
* PostgreSQL (инструкция ниже)

Для сборки и запуска проекта выполните следующие шаги:

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/igorigor-08/ai_agent.git

2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt

3. **Запустите проект:**
   ```bash
   python app.py

4. **Откройте веб-интерфейс:**
   Перейдите по адресу, указанному в терминале после запуска (например, http://localhost:5021).

   ## Контакты
   **Email:** g22media@gmail.com


# Руководство по установке и настройке PostgreSQL

## 1. Установка PostgreSQL и утилит
```bash
# Обновить пакеты
sudo apt update && sudo apt upgrade -y

# Установить PostgreSQL и клиентские утилиты
sudo apt install postgresql postgresql-contrib pg-top htop -y
```

## 2. Запуск службы PostgreSQL
### Проверка и управление службой
```bash
# Проверить статус службы
sudo systemctl status postgresql
# Запустить службу
sudo systemctl start postgresql
# Добавить в автозагрузку
sudo systemctl enable postgresql
```

## 3. Настройка пользователя и базы данных
### Создание пользователя
```bash
sudo -u postgres createuser --interactive
```
- Введите имя пользователя: `myuser`
- Сделать пользователя суперпользователем? Выберите `n` (нет)

### Создание базы данных
```bash
sudo -u postgres createdb mydb
```

### Установка пароля
```bash
sudo -u postgres psql -c "ALTER USER myuser WITH PASSWORD 'secure_password';"
```

## 4. Настройка конфигурации PostgreSQL (опционально)
1. Откройте файл конфигурации:
```bash
sudo nano /etc/postgresql/*/main/postgresql.conf
```

2. Добавьте/измените параметры (пример) и сохраните изменения:
```ini
listen_addresses = '*'
max_connections = 100
shared_buffers = 2GB
work_mem = 32MB
```

## 5. Настройка удалённого доступа
1. Отредактируйте файл доступа:
```bash
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

2. Добавьте строку для доступа:
```ini
# TYPE  DATABASE  USER    ADDRESS      METHOD
host    mydb      myuser  0.0.0.0/0    scram-sha-256
```

## 6. Применение изменений
```bash
sudo systemctl restart postgresql
```

### Проверка работы
```bash
# Подключение к базе
psql -h localhost -U myuser -d mydb
```

## 7. Наполнение базы данных
1. Откройте файл DataBase_creation.ipynb в Jupyter-редакторе

2. Измените конфиг для подключения к БД

3. Запустите все ячейки в нужном порядке

> **Примечание:**  
> - Замените `secure_password` на надёжный пароль  
> - Для внешнего доступа настройте фаервол  
> - Рекомендуется использовать SSL для удалённых подключений
```