# Chess Game Against Ollama (Llama 3.1) with GUI

This is a Python-based chess application with a graphical user interface (GUI) that allows you to play against the Llama 3.1 model using Ollama.

## Prerequisites

1. Python 3.6 or higher
2. Ollama installed and running on your system
3. Llama 3.1 model loaded in Ollama

## Installation

1. Clone this repository or download the `chess_ollama.py` and `chess_gui.py` files.
2. Install the required Python packages:

```bash
pip install chess requests pygame cairosvg
```

3. Download chess piece images and place them in a `chess_pieces` folder within the project directory. You can find free chess piece images online or use a chess piece font.

## How to Play

1. Make sure Ollama is running on your system.
2. Open a terminal and navigate to the directory containing `chess_gui.py`.
3. Run the script:

```bash
python3 chess_gui.py
```

4. The game window will open, displaying the chess board.
5. You play as White, and Ollama (Llama 3.1) plays as Black.
6. To make a move:
   - Click on the piece you want to move
   - Click on the square you want to move the piece to
7. After each of your moves, Ollama will make its move automatically.
8. The game continues until there's a checkmate, stalemate, or draw.

## Notes

- If Ollama generates an invalid move, the program will make a random legal move for Black.
- The chess board is displayed using a graphical interface.
- Make sure you have a good understanding of chess rules before playing.

Enjoy your game against Llama 3.1!