import React, { useState, useEffect } from 'react';
import Chessboard from 'chessboardjsx';
import axios from 'axios';

// Async delay function
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

function ChessGame() {
  const [position, setPosition] = useState('start');
  const [boardWidth, setBoardWidth] = useState(600);
  const [legalMoves, setLegalMoves] = useState([]);
  const [gameOver, setGameOver] = useState(false);
  const [gameResult, setGameResult] = useState(null);
  const [error, setError] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      setBoardWidth(Math.min(window.innerWidth * 0.8, 600));
    };

    window.addEventListener('resize', handleResize);
    handleResize();
    startNewGame();

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const startNewGame = async () => {
    try {
      const response = await axios.get('http://localhost:5001/new-game');
      setPosition(response.data.board);
      fetchLegalMoves();
      setGameOver(false);
      setGameResult(null);
      setError(null);
    } catch (error) {
      console.error('Error starting new game', error);
      setError(`Failed to start game: ${error.message}. 
        Please ensure the backend server is running on http://localhost:5001`);
    }
  };

  const fetchLegalMoves = async () => {
    try {
      const response = await axios.get('http://localhost:5001/legal-moves');
      setLegalMoves(response.data.legal_moves);
    } catch (error) {
      console.error('Error fetching legal moves', error);
      setError(`Failed to fetch legal moves: ${error.message}`);
    }
  };

  const onDrop = async ({ sourceSquare, targetSquare }) => {
    // Prevent multiple moves while processing
    if (isProcessing) return false;

    const move = sourceSquare + targetSquare;

    // Check if the move is legal
    if (!legalMoves.includes(move)) {
      return false;
    }

    try {
      setIsProcessing(true);
      const response = await axios.post('http://localhost:5001/make-move', { move });

      // Update board position
      setPosition(response.data.board);

      // Check for game over
      if (response.data.game_over) {
        setGameOver(true);
        setGameResult(response.data.result);
      } else {
        // Wait 1 second before fetching bot's move
        await delay(1000);

        // Fetch bot's move
        const botMoveResponse = await axios.get('http://localhost:5001/bot-move');

        // Update board with bot's move
        setPosition(botMoveResponse.data.board);

        // Check for game over after bot's move
        if (botMoveResponse.data.game_over) {
          setGameOver(true);
          setGameResult(botMoveResponse.data.result);
        } else {
          // Refresh legal moves
          fetchLegalMoves();
        }
      }

      return true;
    } catch (error) {
      console.error('Error making move', error);
      setError(`Failed to make move: ${error.message}`);
      return false;
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        textAlign: 'center',
        padding: '20px',
        boxSizing: 'border-box'
      }}
    >
      <h1>Scout Chess Bot Challenge</h1>

      {error && (
        <div style={{
          color: 'red',
          marginBottom: '20px',
          padding: '10px',
          border: '1px solid red',
          borderRadius: '5px'
        }}>
          {error}
        </div>
      )}

      {gameOver ? (
        <div className="game-over">
          <h2>Game Over</h2>
          <p>Result: {gameResult}</p>
          <button onClick={startNewGame}>New Game</button>
        </div>
      ) : (
        <div style={{
          width: '100%',
          maxWidth: `${boardWidth}px`,
          margin: '0 auto'
        }}>
          <Chessboard
            width={boardWidth}
            position={position}
            orientation="white"
            onDrop={onDrop}
          />
        </div>
      )}
    </div>
  );
}

export default ChessGame;