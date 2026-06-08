import { useState, useEffect } from "react"
import WebApp from "@twa-dev/sdk"
import { getMatches, makePrediction, getMatchPredictions, upsertUser } from "../api"

export default function MatchList({ gameId }) {
  const [matches, setMatches] = useState([])
  const [user, setUser] = useState(null)
  const [predictions, setPredictions] = useState({})
  const [inputs, setInputs] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
async function init() {
  const tgUser = WebApp.initDataUnsafe?.user
  console.log("tgUser:", tgUser)
      if (tgUser) {
        const u = await upsertUser({
          telegram_id: tgUser.id,
          username: tgUser.username,
          first_name: tgUser.first_name,
        })
        setUser(u)
      } else {
        // для локальной разработки
        const u = await upsertUser({
          telegram_id: 123456789,
          username: "testuser",
          first_name: "Test",
        })
        setUser(u)
      }
      if (gameId) {
        const m = await getMatches(gameId)
        setMatches(m)
      }
      setLoading(false)
    }
    init()
  }, [gameId])

  async function submitPrediction(matchId) {
    console.log("submitPrediction called", matchId, inputs[matchId])
    const { home, away } = inputs[matchId] || {}
    console.log("home, away, user:", home, away, user)
    if (home === undefined || away === undefined) return
    try {
      await makePrediction({
        match_id: matchId,
        user_id: user.id,
        home_score: parseInt(home),
        away_score: parseInt(away),
      })
      // после прогноза загружаем прогнозы других
      const others = await getMatchPredictions(matchId, user.id)
      setPredictions((p) => ({ ...p, [matchId]: others }))
      WebApp.HapticFeedback?.notificationOccurred("success")
    } catch (e) {
      WebApp.HapticFeedback?.notificationOccurred("error")
    }
  }

  if (loading) return <div className="empty">Загрузка...</div>
  if (!gameId) return <div className="empty">Игра не выбрана.<br/>Зайди через бота.</div>
  if (!matches.length) return <div className="empty">Матчей пока нет.</div>

  return (
    <div>
      {matches.map((match) => {
        const myPreds = predictions[match.id]
        const inp = inputs[match.id] || {}

        return (
          <div key={match.id} className="card">
            <div className="match-teams">
              <span>{match.home_team}</span>
              <span className="match-score">
                {match.is_finished
                  ? `${match.home_score} : ${match.away_score}`
                  : "vs"}
              </span>
              <span>{match.away_team}</span>
            </div>

            {!myPreds ? (
              <div className="prediction-form">
                <input
                  type="number"
                  min="0"
                  placeholder="0"
                  value={inp.home ?? ""}
                  onChange={(e) =>
                    setInputs((s) => ({
                      ...s,
                      [match.id]: { ...s[match.id], home: e.target.value },
                    }))
                  }
                />
                <span>:</span>
                <input
                  type="number"
                  min="0"
                  placeholder="0"
                  value={inp.away ?? ""}
                  onChange={(e) =>
                    setInputs((s) => ({
                      ...s,
                      [match.id]: { ...s[match.id], away: e.target.value },
                    }))
                  }
                />
                <button onClick={() => submitPrediction(match.id)}>
                  Поставить
                </button>
              </div>
            ) : (
              <div>
                <div className="hint">Прогнозы участников:</div>
                {myPreds.map((p) => (
                  <div key={p.id} className="leaderboard-row">
                    <span>Игрок {p.user_id}</span>
                    <span>{p.home_score} : {p.away_score}</span>
                    {p.points !== null && (
                      <span className="points">+{p.points}</span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
