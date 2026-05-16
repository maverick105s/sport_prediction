from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import games, matches, predictions, users

app = FastAPI(title="Sport Predictions API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # в проде заменить на конкретный домен
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(games.router, prefix="/games", tags=["games"])
app.include_router(matches.router, prefix="/matches", tags=["matches"])
app.include_router(predictions.router, prefix="/predictions", tags=["predictions"])


@app.get("/health")
async def health():
    return {"status": "ok"}
