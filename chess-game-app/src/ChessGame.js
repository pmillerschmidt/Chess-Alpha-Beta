import React, { useState, useEffect } from 'react';
import Chessboard from 'chessboardjsx';
import axios from 'axios';

const AGENTS = [
  { id: 'random', name: 'Random Agent', description: 'Makes completely random legal moves' },
  { id: 'greedy', name: 'Greedy Agent', description: 'Captures pieces whenever possible' },
  { id: 'minimax', name: 'Minimax Agent', description: 'Uses minimax algorithm to look ahead' },
  { id: 'scout', name: 'Scout Agent', description: 'Advanced agent using scout search' }
];

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

function ChessGame() {
  const [position, setPosition] = useState('start');
  const [boardWidth, setBoardWidth] = useState(600);
  const [legalMoves, setLegalMoves] = useState([]);
  const [gameOver, setGameOver] = useState(false);
  const [gameResult, setGameResult] = useState(null);
  const [error, setError] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState('random');

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
      const response = await axios.get(`http://localhost:5001/new-game?agent=${selectedAgent}`);
      setPosition(response.data.board);
      fetchLegalMoves();
      setGameOver(false);
      setGameResult(null);
      setError(null);
    } catch (error) {
      console.error('Error starting new game', error);
      setError(`Failed to start game: ${error.message}`);
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
    if (isProcessing) return false;

    const move = sourceSquare + targetSquare;
    if (!legalMoves.includes(move)) {
      return false;
    }

    try {
      setIsProcessing(true);
      const response = await axios.post(`http://localhost:5001/make-move`, {
        move,
        agent: selectedAgent
      });

      setPosition(response.data.board);

      if (response.data.game_over) {
        setGameOver(true);
        setGameResult(response.data.result);
      } else {
        await delay(1000);
        const botMoveResponse = await axios.get(`http://localhost:5001/bot-move?agent=${selectedAgent}`);
        setPosition(botMoveResponse.data.board);

        if (botMoveResponse.data.game_over) {
          setGameOver(true);
          setGameResult(botMoveResponse.data.result);
        } else {
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

  const handleAgentChange = (e) => {
    setSelectedAgent(e.target.value);
    startNewGame();
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

      <div style={{
        marginBottom: '20px',
        padding: '10px',
        backgroundColor: '#f5f5f5',
        borderRadius: '5px',
        maxWidth: '400px'
      }}>
        <select
          value={selectedAgent}
          onChange={handleAgentChange}
          style={{
            padding: '8px',
            fontSize: '16px',
            width: '200px'
          }}
        >
          {AGENTS.map(agent => (
            <option key={agent.id} value={agent.id}>
              {agent.name}
            </option>
          ))}
        </select>
        <p style={{ margin: '10px 0 0 0', fontSize: '14px', color: '#666' }}>
          {AGENTS.find(agent => agent.id === selectedAgent)?.description}
        </p>
      </div>

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
          <button
            onClick={startNewGame}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              cursor: 'pointer',
              backgroundColor: '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: '5px'
            }}
          >
            New Game
          </button>
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