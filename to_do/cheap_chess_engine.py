import chess
import chess.engine

# Create a new chess board
board = chess.Board()

# Print the board
print(board)

# Make a move
move = chess.Move.from_uci("e2e4")
board.push(move)

# Print the board after the move
print(board)

# Check if the game is over
if board.is_game_over():
    print("Game over")
else:
    print("Game continues")#engine that only sees like 3-4 moves ahead