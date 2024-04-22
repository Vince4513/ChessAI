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

    def set_piece(self, position, piece):
        self.board[position] = piece
    
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
    
    def castle(self, color, end_pos):
        # Determine the positions of the king and rook involved in castling
        king_position = self.find_king(color)
        
        if end_pos[1] > king_position[1]:
            rook_position = (king_position[0], 7)
            new_king_position = (king_position[0], king_position[1] + 2)
            new_rook_position = (king_position[0], king_position[1] + 1)
        
        elif end_pos[1] < king_position[1]:
            rook_position = (king_position[0], 0)
            new_king_position = (king_position[0], king_position[1] - 2)
            new_rook_position = (king_position[0], king_position[1] - 1)
        else:
            print("Invalid castle direction.")
            return False

        # Check if the king and rook are in their initial positions
        king = self.board[king_position]
        rook = self.board[rook_position]
        if not isinstance(king, King) or not isinstance(rook, Rook):
            print("Invalid castle: King or rook has moved before.")
            return False

        # Check if the squares between the king and rook are empty
        for col in range(min(rook_position[1], new_king_position[1]) + 1, max(rook_position[1], new_king_position[1])):
            if self.board[new_king_position[0], col] is not None:
                print("Invalid castle: Squares between king and rook are not empty.")
                return False

        # Check if the king is in check or if it moves through or lands on a square attacked by an opponent's piece
        # Implement this check based on your existing check detection logic

        # Perform the castle by moving the king and rook to their new positions
        self.move_piece(king_position, new_king_position)
        self.move_piece(rook_position, new_rook_position)

        return True

if __name__ == "__main__":
    pass