# Sport Predictions

Pet project: угадываем счета матчей (хоккей/футбол). Замена Google Sheets.
Путь: /Users/sv/working_dir/sport_prediction (git repo)

## Стек
- Python, FastAPI, SQLAlchemy (async), Alembic, PostgreSQL
- python-telegram-bot 21.x
- React 19 + Vite + @twa-dev/sdk (Telegram Mini App)

## Запуск (из tmp)
```bash
docker compose up -d                      # БД + бот
cd frontend && npm run dev                # фронт
ngrok start --all --config ~/ngrok.yml    # туннель для Telegram WebApp
```

## Структура
```
app/
  api/routes/   — games, matches, predictions, users (готово)
  bot/bot.py    — /start, /newgame, /join (готово)
  models/       — User, Game, GameParticipant, Match, Prediction
  services/     — scoring.py (calculate_points: 3/2/1/0)
  parsers/      — пусто (будущий парсинг результатов)
frontend/       — РЕАЛЬНЫЙ фронт (App.jsx, api.js, pages/, components/)
src/, public/   — артефакт случайного `npm create vite` в корне, НЕ используется
```

## Бизнес-логика
- Создать игру → invite_code → другие вступают по коду
- Прогнозы соперников закрыты пока не сделаешь свой (403)
- /predictions/finalize/{match_id} начисляет очки после результата
- Очки: 3 (точный счёт), 2 (разница), 1 (исход)

## Статус
- [x] Модели, API, бот (start/newgame/join), фронт, scoring — локально работает
- [x] Деплой: Railway (backend+bot+db) + GitHub Pages (frontend)
- [ ] Парсинг результатов матчей из внешних источников
- [ ] Бот: команды для матчей/прогнозов (пока только через WebApp)

## Деплой
Railway проект: brave-manifestation (Postgres + 2 сервиса из репо sport_prediction).

- **API** (sport_prediction): Custom Start Command —
  `sh -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"`
  (миграции гоняются автоматически при каждом деплое)
  Публичный домен: https://sportprediction-production-5a1c.up.railway.app
- **Bot** (второй сервис из того же репо): Custom Start Command — `python -m app.bot.bot`
- Оба сервиса: `DATABASE_URL = postgresql+asyncpg://${{Postgres.PGUSER}}:${{Postgres.PGPASSWORD}}@${{Postgres.PGHOST}}:${{Postgres.PGPORT}}/${{Postgres.PGDATABASE}}`,
  `WEBAPP_URL = https://maverick105s.github.io/sport_prediction/`
- Деплой API/бота — автоматически при пуше в main (Railway GitHub-интеграция)

Фронт: GitHub Pages, автодеплой через `.github/workflows/deploy-frontend.yml` при пуше в main (paths: frontend/**).
- URL: https://maverick105s.github.io/sport_prediction/
- `frontend/.env.production` → `VITE_API_URL` = адрес API на Railway

Локальный `.venv` (gitignored) — на случай разовых alembic-команд через `railway run`.

## Следующий шаг
В `/start` бота захардкожен `game_id=1` (app/bot/bot.py) — в проде такой игры ещё нет.
Проверить полный сценарий на проде: `/newgame` → `/join` → открыть WebApp с реальным game_id (сейчас всегда 1).

## Заметки
- В корне есть лишний vite-каркас (src/, package.json, node_modules) — кандидат на удаление, реальный фронт в frontend/
- Старая копия в ~/Downloads/sport_predictions — НЕ трогать, не актуальна
