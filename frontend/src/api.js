import axios from "axios"

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
})

export const getMatches = (gameId) =>
  api.get(`/matches/game/${gameId}`).then((r) => r.data)

export const makePrediction = (data) =>
  api.post("/predictions/", data).then((r) => r.data)

export const getMatchPredictions = (matchId, userId) =>
  api.get(`/predictions/match/${matchId}?user_id=${userId}`).then((r) => r.data)

export const getLeaderboard = (gameId) =>
  api.get(`/games/${gameId}/leaderboard`).then((r) => r.data)

export const upsertUser = (data) =>
  api.post("/users/upsert", data).then((r) => r.data)