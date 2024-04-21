# board.py

import numpy as np
from pieces import *

class Chessboard:
    def __init__(self):
        # Initialize an 8x8 chessboard with None (empty squares)
        self.board = np.full((8, 8), None, dtype=object)
        
        # Define the order of pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        # Place black pieces (row 0)
        for i, piece_class in enumerate(piece_order):
            self.board[0, i] = piece_class('white')

        # Place black pawns (row 1)
        self.board[1, :] = [Pawn('white') for _ in range(8)]

        # Place white pieces (row 7)
        for i, piece_class in enumerate(piece_order):
            self.board[7, i] = piece_class('black')

        # Place white pawns (row 6)
        self.board[6, :] = [Pawn('black') for _ in range(8)]

    def display_board(self):
        # Display the current state of the board
        display_board = np.array([[str(piece)[0:2] if piece is not None else ' .' for piece in row] for row in self.board])
        print(display_board)

    def get_piece(self, position):
        return self.board[position]
    
    def find_king(self, color):
        # Iterate over the board to find the king of the specified color
        for row in range(8):
            for col in range(8):
                piece = self.board[row, col]
                if isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None

    def get_legal_moves(self, position):
        # Implement logic to determine legal moves for a piece at the given position
        piece = self.board[position]

        if isinstance(piece, Pawn):
            return self.valid_move(position)
        if isinstance(piece, Rook):
            return self.valid_move(position)
        if isinstance(piece, Knight):
            return self.valid_move(position)
        if isinstance(piece, Bishop):
            return self.valid_move(position)
        if isinstance(piece, Queen):
            return self.valid_move(position)
        if isinstance(piece, King):
            return self.valid_move(position)
        
    def move_piece(self, start, end):
        # Move a piece from start to end coordinates
        self.board[end] = self.board[start]
        self.board[start] = None

    def remove_piece(self, position):
        # Move a piece from start to end coordinates
        self.board[position] = None
        
