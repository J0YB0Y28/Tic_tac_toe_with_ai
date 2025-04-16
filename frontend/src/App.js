// App.jsx
import { useState, useEffect } from 'react';
import GameBoard from './components/GameBoard';
import { startGame, makeMove, aiMove, getState } from './services/api';
import victorySound from './assets/victory.mp3';

export default function App() {
  const [gameId, setGameId] = useState(null);
  const [state, setState] = useState(null);
  const [mode, setMode] = useState('pvp');
  const [difficulty, setDifficulty] = useState('hard');
  const [player1, setPlayer1] = useState('Joueur 1');
  const [player2, setPlayer2] = useState('Joueur 2');
  const [loading, setLoading] = useState(false);

  const playVictorySound = () => {
    const audio = new Audio(victorySound);
    audio.play();
  };

  const handleStart = async () => {
    setLoading(true);
    const response = await startGame(mode, player1, mode === 'ai' ? 'Computer' : player2, difficulty);
    setGameId(response.game_id);
    setState(response.state);
    setLoading(false);
  };

  const handleMove = async (col) => {
    if (!gameId || state?.game_over) return;
    const response = await makeMove(gameId, col);
    setState(response.state);
  };

  useEffect(() => {
    const playAI = async () => {
      if (
        mode === 'ai' &&
        gameId &&
        state &&
        !state.game_over &&
        state.current_player === 'Computer'
      ) {
        const aiResponse = await aiMove(gameId);
        setState(aiResponse.state);
      }
    };
    playAI();
  }, [state, gameId, mode]);

  useEffect(() => {
    if (state?.game_over && state?.winner) {
      playVictorySound();
    }
  }, [state?.game_over]);

  const symbols = state?.symbols || {};
  const p1Symbol = symbols[player1];
  const p2Symbol = symbols['Computer'];

  return (
    <div className="min-h-screen p-4 bg-blue-50 text-center">
      <h1 className="text-3xl font-bold mb-4">🎯 Puissance 4</h1>

      <div className="flex flex-wrap justify-center gap-4 mb-4">
        <input type="text" placeholder="Joueur 1" value={player1} onChange={(e) => setPlayer1(e.target.value)} className="px-2 py-1 border rounded" />
        {mode === 'pvp' && (
          <input type="text" placeholder="Joueur 2" value={player2} onChange={(e) => setPlayer2(e.target.value)} className="px-2 py-1 border rounded" />
        )}
        <select value={mode} onChange={(e) => setMode(e.target.value)} className="px-2 py-1 border rounded">
          <option value="pvp">Joueur vs Joueur</option>
          <option value="ai">Joueur vs IA</option>
        </select>
        {mode === 'ai' && (
          <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)} className="px-2 py-1 border rounded">
            <option value="easy">Facile</option>
            <option value="medium">Moyen</option>
            <option value="hard">Difficile</option>
          </select>
        )}
        <button onClick={handleStart} className="px-4 py-2 bg-blue-600 text-white rounded">Démarrer</button>
      </div>

      {loading && <p>Chargement...</p>}

      {state && (
        <>
          <p className="text-lg font-semibold mb-2 animate-pulse">Tour de : {state.current_player}</p>
          <p className="text-sm mb-2">
            🔴 {player1} ({p1Symbol}) vs 🟡 {mode === 'ai' ? 'Computer' : player2} ({p2Symbol})
          </p>
          <GameBoard
            board={state.board}
            onColumnClick={handleMove}
            winningCells={state.winning_cells}
          />

          {state.game_over && (
            <div className="mt-6 p-4 border rounded bg-green-50 shadow-md animate-bounce">
              <p className="text-xl font-bold text-green-600">
                {state.winner ? `${state.winner} a gagné ! 🎉` : 'Match nul !'}
              </p>
              <button onClick={handleStart} className="mt-3 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition">
                Rejouer
              </button>
            </div>
          )}

          <div className="mt-4 text-sm">
            ⏱️ Temps : {player1} - {state.move_times[player1] || 0}s | {mode === 'ai' ? 'Computer' : player2} - {state.move_times[mode === 'ai' ? 'Computer' : player2] || 0}s
          </div>
        </>
      )}
      <footer className="mt-16 text-center text-sm text-gray-600">
        <p>
          Projet réalisé par <strong>Teddy Kana</strong> — Étudiant en Génie logiciel à l’Université Laval
        </p>
        <p className="mt-2">
          📧 <a href="mailto:kanaboumkwoiit@outlook.com" className="text-blue-500 hover:underline">
            kanaboumkwoiit@outlook.com
          </a>{" | "}
          💻 <a href="https://github.com/J0YB0Y28" target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
            GitHub
          </a>{" | "}
          💼 <a href="https://www.linkedin.com/in/teddy-kana-6a26832b9/" target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
            LinkedIn
          </a>{" | "}
          🌐 <a href="https://j0yb0y28.github.io/portfolio/" target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
            Portfolio
          </a>
        </p>
      </footer>
    </div>
  );
}
