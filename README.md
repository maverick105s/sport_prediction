# Sport Predictions

Telegram WebApp для прогнозов на спортивные матчи.

## Локальный запуск

```bash
# 1. Клонировать и настроить окружение
cp .env.example .env
# заполнить .env своими значениями

# 2. Поднять БД и API
docker-compose up -d

# 3. Применить миграции
alembic upgrade head

# 4. API доступно на http://localhost:8000
# Документация: http://localhost:8000/docs
```

## Структура

```
app/
  api/routes/     # FastAPI endpoints
  bot/handlers/   # Telegram bot
  core/           # config, database
  models/         # SQLAlchemy models
  services/       # бизнес-логика (scoring и др.)
  parsers/        # парсеры результатов матчей
frontend/         # React Telegram WebApp
alembic/          # миграции БД
```

## Деплой

- **API** → Railway (автодеплой из main)
- **Frontend** → GitHub Pages (GitHub Actions)

## Система очков

| Результат | Очки |
|-----------|------|
| Точный счёт | 3 |
| Правильная разница голов | 2 |
| Правильный исход | 1 |
