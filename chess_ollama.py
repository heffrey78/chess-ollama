import chess
import random
import requests

def get_ollama_move(board, model="llama3.1"):
    prompt = f"You are playing as Black in a chess game. The current board state in FEN notation is: {board.fen()}. What is your next move? Respond with the move in UCI notation (e.g., 'e7e5' for moving a piece from e7 to e5)."
    
    response = requests.post('http://localhost:11434/api/generate', 
                             json={
                                 "model": model,
                                 "prompt": prompt,
                                 "stream": False
                             })
    
    if response.status_code == 200:
        move = response.json()['response'].strip()
        try:
            chess_move = chess.Move.from_uci(move)
            if chess_move in board.legal_moves:
                return chess_move
        except ValueError:
            pass
    
    # If Ollama's move is invalid, make a random move
    return random.choice(list(board.legal_moves))

def get_ollama_commentary(board, model="llama3.1"):
    prompt = f"""You are a chess master AI providing commentary on a chess game. The current board state in FEN notation is: {board.fen()}. 
    Provide a brief, witty comment (max 2 sentences) that includes both a friendly taunt and some master-level advice about the current game state or potential future moves. 
    Be creative and entertaining, but also insightful."""
    
    response = requests.post('http://localhost:11434/api/generate', 
                             json={
                                 "model": model,
                                 "prompt": prompt,
                                 "stream": False
                             })
    
    if response.status_code == 200:
        commentary = response.json()['response'].strip()
        return commentary
    else:
        return "Hmm, interesting move. Let's see how this plays out!"

if __name__ == "__main__":
    print("This module is not meant to be run directly. Please run chess_gui.py instead.")