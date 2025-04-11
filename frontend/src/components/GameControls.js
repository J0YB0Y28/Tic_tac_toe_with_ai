// components/GameBoard.js
export default function GameBoardConnect4({ board, onColumnClick }) {
    return (
      <div className="inline-block">
        <div className="grid grid-cols-7 gap-1 bg-blue-700 p-2 rounded">
          {board[0].map((_, colIdx) => (
            <button
              key={`col-${colIdx}`}
              onClick={() => onColumnClick(colIdx)}
              className="h-6 w-full bg-blue-300 hover:bg-blue-500 transition rounded-t"
            >
              ▼
            </button>
          ))}
        </div>
        <div className="grid grid-cols-7 gap-1 bg-blue-700 p-2 rounded-b">
          {board.map((row, rowIdx) => (
            row.map((cell, colIdx) => (
              <div
                key={`cell-${rowIdx}-${colIdx}`}
                className={`w-12 h-12 flex items-center justify-center rounded-full 
                  transition-all duration-300 ease-out transform
                  ${cell === 'X' ? 'bg-red-500 scale-110 shadow-lg' : 
                    cell === 'O' ? 'bg-yellow-400 scale-110 shadow-lg' : 'bg-white hover:scale-105'}`}
              >
                {cell !== ' ' && <span className="text-white font-bold drop-shadow-sm">{cell}</span>}
              </div>
            ))
          ))}
        </div>
      </div>
    );
  }