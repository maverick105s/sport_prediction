import { useState, useEffect } from "react"
import { getLeaderboard } from "../api"

const medals = ["🥇", "🥈", "🥉"]

export default function Leaderboard({ gameId }) {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!gameId) { setLoading(false); return }
    getLeaderboard(gameId).then((data) => {
      setRows(data)
      setLoading(false)
    })
  }, [gameId])

  if (loading) return <div className="empty">Загрузка...</div>
  if (!gameId) return <div className="empty">Игра не выбрана.</div>
  if (!rows.length) return <div className="empty">Прогнозов пока нет.</div>

  return (
    <div className="card">
      {rows.map((row, i) => (
        <div key={i} className="leaderboard-row">
          <span className="rank">{medals[i] || i + 1}</span>
          <span style={{ flex: 1 }}>{row.user}</span>
          <span className="points">{row.points} очков</span>
        </div>
      ))}
    </div>
  )
}
