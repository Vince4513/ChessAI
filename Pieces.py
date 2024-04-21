import numpy as np

class Piece:
    def __init__(self, color) -> None:
        self.color = color
    
    def __str__(self):
        return type(self).__name__
    
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)

    def validate_move(self, current_pos, new_pos, board):
        # Check if the move is valid for a queen
        delta_x = new_pos[0] - current_pos[0]
        delta_y = new_pos[1] - current_pos[1]

        if delta_x == 0 or delta_y == 0 :
            # Check if there are any obstacles along the trajectory
            step_x = 0 if delta_x == 0 else delta_x // abs(delta_x)
            step_y = 0 if delta_y == 0 else delta_y // abs(delta_y)
            x, y = current_pos[0] + step_x, current_pos[1] + step_y

            while (x, y) != new_pos:
                if board.get_piece((x, y)) is not None:
                    print("Obstacle in the way")
                    return False
                x += step_x
                y += step_y

            return True
        else:
            print("Rook: Illegal move")
            return False

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    def validate_move(self, current_pos, new_pos, board):
        # Check if the move is valid for a bishop
        delta_x = new_pos[0] - current_pos[0]
        delta_y = new_pos[1] - current_pos[1]

        if abs(delta_x) == abs(delta_y):
            # Check if there are any obstacles along the trajectory
            step_x = 0 if delta_x == 0 else delta_x // abs(delta_x)
            step_y = 0 if delta_y == 0 else delta_y // abs(delta_y)
            x, y = current_pos[0] + step_x, current_pos[1] + step_y

            while (x, y) != new_pos:
                if board.get_piece((x, y)) is not None:
                    print("Obstacle in the way")
                    return False
                x += step_x
                y += step_y

            return True
        else:
            print("Bishop: Illegal move")
            return False

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)

    def validate_move(self, current_pos, new_pos, board):
        # Check if the move is valid for a queen
        delta_x = new_pos[0] - current_pos[0]
        delta_y = new_pos[1] - current_pos[1]

        if delta_x == 0 or delta_y == 0 or abs(delta_x) == abs(delta_y):
            # Check if there are any obstacles along the trajectory
            step_x = 0 if delta_x == 0 else delta_x // abs(delta_x)
            step_y = 0 if delta_y == 0 else delta_y // abs(delta_y)
            x, y = current_pos[0] + step_x, current_pos[1] + step_y

            while (x, y) != new_pos:
                if board.get_piece((x, y)) is not None:
                    print("Obstacle in the way")
                    return False
                x += step_x
                y += step_y

            return True
        else:
            print("Queen: Illegal move")
            return False

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

    def validate_move(self, new_pos, current_pos, _):
        # Check if the move is valid for a knight
        delta_x = abs(new_pos[0] - current_pos[0])
        delta_y = abs(new_pos[1] - current_pos[1])

        if (delta_x == 2 and delta_y == 1) or (delta_x == 1 and delta_y == 2):
            return True
        else:
            print("Knight: Illegal move")
            return False

class King(Piece):
    def __init__(self, color):
        super().__init__(color)

    def validate_move(self, current_pos, new_pos, _):
        # Logic to validate king's movement
        # Check if the new position is valid for the king
        if abs(new_pos[0] - current_pos[0]) <= 1 and abs(new_pos[1] - current_pos[1]) <= 1:
            return True
        else:
            print("King: Illegal move")
            return False

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_not_moved = True

    def validate_move(self, current_pos, new_pos, _):
        # Logic to validate pawn's movement
        x = new_pos[0] - current_pos[0] # Row
        y = new_pos[1] - current_pos[1] # Col

        if self.color == 'black':
            if 0 < -x <= (2 if self.has_not_moved else 1) and abs(y) == 0:
                self.has_not_moved = False
                return True
            else:
                print("Pawn: Illegal move")
                return False
        
        elif self.color == 'white':
            if 0 < x <= (2 if self.has_not_moved else 1) and abs(y) == 0:
                self.has_not_moved = False
                return True
            else:
                print("Pawn: Illegal move")
                return False
        else:
            print("Pawn color not determined")

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

    def get_piece(self, pos):
        return self.board[pos]

    def move_piece(self, start, end):
        # Move a piece from start to end coordinates
        self.board[end] = self.board[start]
        self.board[start] = None

    def remove_piece(self, pos):
        # Move a piece from start to end coordinates
        self.board[pos] = None
        
class ChessGame:
    def __init__(self):
        self.board = Chessboard()
        self.current_player = 'white'

    def play(self):
        while not self.is_game_over():
            self.board.display_board()
            print(f"It's {self.current_player}'s turn.")
            start = input("Enter the start position (e.g., 'a2'): ")
            end = input("Enter the end position (e.g., 'a4'): ")
            if self.move_piece(start, end):
                self.switch_player()

    def move_piece(self, start, end):
        # Convert input positions to board coordinates
        start_pos = self.convert_position(start)
        end_pos = self.convert_position(end)

        # Perform the move
        piece = self.board.get_piece(start_pos)
        target_piece = self.board.get_piece(end_pos)

        if piece is None:
            print("No piece at the start position.")
            return False
        elif piece.color != self.current_player:
            print("It's not your turn.")
            return False
        elif not piece.validate_move(start_pos, end_pos, self.board):
            print("Invalid move.")
            return False
        elif target_piece is not None and target_piece.color == piece.color:
            print("Cant capture your own pieces !")
            return False
        else:
            # Check if the end position is occupied by an opponent's piece
            if target_piece is not None and target_piece.color != piece.color:
                print("Piece captured:",target_piece.color, target_piece)
                self.board.remove_piece(end_pos)  # Remove the captured piece from the board
            
            # Perform the move on the board
            self.board.move_piece(start_pos, end_pos)
            return True

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def is_game_over(self):
        # Add game over conditions (e.g., checkmate, stalemate)
        return False

    def convert_position(self, pos):
        # Convert user input position to board coordinates
        # For example, 'a1' => (0, 0)
        column = ord(pos[0]) - ord('a')
        row = int(pos[1]) - 1
        return row, column

# Usage
game = ChessGame()
game.play()


"""
Done: Plateau 8x8

Deplacement pieces 
Done: - Règle de chaque pièce
Done: - Pas pouvoir se poser sur une case prise 
Done - Pas pouvoir traverser si pièce sur chemin sauf cavalier

- capture une pièce
- échec au roi 
- en passant
- rock (2 cotés)
- promotion

"""