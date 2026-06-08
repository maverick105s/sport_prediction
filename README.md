# Sport Predictions

Telegram WebApp для прогнозов на спортивные матчи.

## Локальный запуск

```bash
cp .env.example .env
# заполнить .env своими значениями

docker-compose up -d       # БД + API + бот
alembic upgrade head       # миграции

cd frontend && npm install && npm run dev   # фронт
```

## Структура

```
app/
  api/routes/   — FastAPI endpoints
  bot/bot.py    — Telegram бот (/start /newgame /join)
  core/         — config, database
  models/       — SQLAlchemy models
  services/     — scoring (3/2/1/0)
  parsers/      — парсеры результатов (будущее)
frontend/       — React Telegram WebApp
alembic/        — миграции БД
```

## Деплой

- **API + бот** → Railway
- **Frontend** → GitHub Pages

## Система очков

| Результат | Очки |
|-----------|------|
| Точный счёт | 3 |
| Правильная разница | 2 |
| Правильный исход | 1 |
