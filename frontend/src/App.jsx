import { useState, useEffect } from "react"
import WebApp from "@twa-dev/sdk"
import MatchList from "./pages/MatchList"
import Leaderboard from "./pages/Leaderboard"
import "./App.css"

export default function App() {
  const [page, setPage] = useState("matches")
  const [gameId, setGameId] = useState(null)

  useEffect(() => {
    if (WebApp.ready) WebApp.ready()
    // из Telegram
    const startParam = WebApp.initDataUnsafe?.start_param
    // из URL для локальной разработки
    const urlParam = new URLSearchParams(window.location.search).get("game_id")
    const id = startParam || urlParam
    if (id) setGameId(parseInt(id))
  }, [])

  return (
    <div className="app">
      <nav className="nav">
        <button
          className={page === "matches" ? "active" : ""}
          onClick={() => setPage("matches")}
        >
          Матчи
        </button>
        <button
          className={page === "leaderboard" ? "active" : ""}
          onClick={() => setPage("leaderboard")}
        >
          Таблица
        </button>
      </nav>

      <main>
        {page === "matches" && <MatchList gameId={gameId} />}
        {page === "leaderboard" && <Leaderboard gameId={gameId} />}
      </main>
    </div>
  )
}
