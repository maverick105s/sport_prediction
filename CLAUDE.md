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
- [ ] Деплой: Railway (backend+bot+db) + GitHub Pages (frontend)
- [ ] Парсинг результатов матчей из внешних источников
- [ ] Бот: команды для матчей/прогнозов (пока только через WebApp)

## Следующий шаг
Деплой на Railway + GitHub Pages.

Railway проект создан (название: brave-manifestation), PostgreSQL Online.
API сервис не добавлен — Railway требует карту для деплоя GitHub репо.
Завтра: привязать карту → Add → GitHub Repository → sport_prediction → настроить Start Command + Variables → миграции → GitHub Pages для фронта.

## Заметки
- В корне есть лишний vite-каркас (src/, package.json, node_modules) — кандидат на удаление, реальный фронт в frontend/
- Старая копия в ~/Downloads/sport_predictions — НЕ трогать, не актуальна
