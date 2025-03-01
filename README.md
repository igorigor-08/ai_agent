# AI-ассистент ПРМ "Паром"

## Кейс 01.Риск-инструменты: AI-агент для портфельных аналитиков 
## Описание проекта

AI-ассистент ПРМ "Паром" — это интеллектуальный text2sql помощник для портфельных аналитиков.

## Как воспользоваться AI-агентом

Чтобы начать использовать AI-ассистента, перейдите по [http://212.67.8.208:5021/](#).

### Особенности взаимодействия с агентом

- AI-ассистент работает только с запросами, связанными с данными из нашей синтезированной базы данных.  
- Запросы должны быть четко сформулированы и касаться тематики анализа портфелей.  

### Краткое описание базы данных

#### **Таблица:** ***individual_borrowers***

**individual_id**: Уникальный идентификатор физического заемщика.

**date_of_birth**: Дата рождения заемщика.

#### **Таблица:** ***company_borrowers***

**company_id**: Уникальный идентификатор компании-заемщика.

**company_name**: Название компании (обязательное поле).

**business_sector**: Сектор бизнеса ('Информационные технологии', 'Финансовые организации', 'Коммерция', 'Энергетика', 'Производство', 'Недвижимость').

#### **Таблица:** ***credit_products***

**product_id**: Уникальный идентификатор кредитного продукта.

**product_name**: Тип продукта ('Потребительский кредит', 'Ипотека', 'Автокредит', 'Кредитная карта', 'Бизнес-кредит', 'Возобновляемая кредитная линия', 'Гарантия').

**interest_rate**: Процентная ставка (например, 5.25%).

**min_loan_amount**: Минимальная сумма займа.

**max_loan_amount**: Максимальная сумма займа.

**term_months**: Срок займа в месяцах.

#### **Таблица:** ***credits***

**credit_id**: Уникальный идентификатор кредита.

**individual_id**: Ссылка на физического заемщика (может быть NULL, если кредит выдан компании).

**company_id**: Ссылка на компанию-заемщика (может быть NULL, если кредит выдан физическому лицу).

**product_id**: Ссылка на кредитный продукт (обязательное поле).

**loan_amount**: Сумма кредита.

**interest_rate**: Процентная ставка по кредиту.

**start_date**: Дата начала кредита.

**end_date**: Планируемая дата погашения (может быть NULL для бессрочных кредитов).

**status**: Статус кредита ('Активный', 'Закрытый', 'Дефолт'). Значение по умолчанию — Активный.

#### **Таблица:** ***client_transactions***

**transaction_id**: Уникальный идентификатор транзакции.

**credit_id**: Ссылка на кредит.

**transaction_type**: Тип транзакции ('Выплата основного долга', 'Выплата просроченного долга', 'Выплата штрафов').

**amount**: Сумма транзакции.

**transaction_date**: Дата и время транзакции.

#### **Таблица:** ***risk_ratings***

**rating_id**: Уникальный идентификатор оценки риска.

**individual_id**: Ссылка на физического заемщика (может быть NULL, если оценка для компании).

**company_id**: Ссылка на компанию-заемщика (может быть NULL, если оценка для физического лица).

**credit_id**: Ссылка на кредит (обязательное поле).

**rating**: Оценка риска (1 — минимальный риск, 26 — максимальный риск).

**probability_of_default**: Вероятность дефолта (от 0.00 до 1.00).

**rating_date**: Дата оценки.

#### **Таблица:** ***defaults***

**default_id**: Уникальный идентификатор дефолта.

**credit_id**: Ссылка на кредит.

**default_date**: Дата наступления дефолта.

**default_amount**: Непогашенная сумма на момент дефолта.

**recovery_amount**: Сумма, восстановленная после дефолта (например, за счет взыскания).

**reason_for_default**: Причина дефолта ('Просрочка', 'Банкротство', 'Реструктуризация', 'Ликвидация', 'Цессия').

#### **Таблица:** ***credit_reserves***

**reserve_id**: Уникальный идентификатор резерва.

**credit_id**: Ссылка на кредит.

**reserve_stage**: Этап резервирования (Стадия 1 — стандартный риск, Стадия 2 — повышенный риск, Стадия 3 — критический риск).

**reserve_amount**: Зарезервированная сумма для покрытия потенциальных убытков.

### Примеры запросов

**Запрос:** "Выведи вероятность дефолта в зависимости от рейтинга?"  

**Запрос:** "Сколько было каких причин дефолта за последний месяц?"  

**Запрос:** "Выведи топ-10 наименее закредитованных компаний" 

**Запрос:** "Какая процентная ставка у активных кредитов?"
  

## Как собрать проект

Для корректного запуска проекта необходимо иметь:
* Ubuntu 20.02
* Python 3.11
* Nginx 
* PostgreSQL

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

2. **Откройте веб-интерфейс:**
   Перейдите по адресу, указанному в терминале после запуска (например, http://localhost:5000).

   ## Контакты
   **Email:** g22media@gmail.com
