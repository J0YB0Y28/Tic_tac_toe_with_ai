// services/api.js
const API_URL = 'https://power4-app.onrender.com/start';

export const startGame = async (mode, player1, player2, difficulty = 'hard') => {
  const res = await fetch(`${API_URL}/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mode, player1, player2, difficulty })
  });
  return res.json();
};

export const makeMove = async (game_id, column) => {
  const res = await fetch(`${API_URL}/move`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game_id, column })
  });
  return res.json();
};

export const aiMove = async (game_id) => {
  const res = await fetch(`${API_URL}/ai-move`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game_id })
  });
  return res.json();
};

export const getState = async (game_id) => {
  const res = await fetch(`${API_URL}/state?game_id=${game_id}`);
  return res.json();
};