# launch_game.py

from board import *

class ChessGame:
    def __init__(self):
        self.board = Chessboard()
        self.current_player = 'white'

    def convert_position(self, pos):
        # Convert user input position to board coordinates
        # For example, 'a1' => (0, 0)
        column = ord(pos[0]) - ord('a')
        row = int(pos[1]) - 1
        return row, column

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def is_game_over(self):
        # Add game over conditions (e.g., checkmate, stalemate)
        return False

    def is_check(self, color):
        # Get the position of the king of the specified color
        king_position = self.board.find_king(color)

        # Iterate over all opponent's pieces
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece is not None and piece.color != color:
                    if piece.validate_move((row, col), king_position, self.board):
                        print(f"{color.capitalize()} king is in check!")
                        return True
        return False
    
    def simulate_move(self, start, end):
        # Implement logic to simulate a move without modifying the board's state
        pass 
    
    # Endgame functions ---------------------
    def is_checkmate(self, color):
        # Check if the king is in check
        if self.is_check(color):
            # Iterate over all the player's pieces
            for row in range(8):
                for col in range(8):
                    piece = self.board.get_piece((row, col))
                    if piece is not None and piece.color == color:
                        # Check if the piece has any legal moves
                        for move in self.board.get_legal_moves((row, col)):
                            # Simulate the move and check if the king is still in check
                            if not self.simulate_move((row, col), move):
                                return False  # The king is not in checkmate
            return True  # Checkmate
        return False  # The king is not in check

    def is_stalemate(self):
        # Check if the current player's king is in check
        if self.is_check(self.current_player):
            return False  # Not stalemate if the king is in check

        # Iterate over all the player's pieces
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece is not None and piece.color == self.current_player:
                    # Check if the piece has any legal moves
                    for move in self.board.get_legal_moves((row, col)):
                        # Simulate the move and check if the king is still not in check
                        if not self.simulate_move((row, col), move):
                            return False  # The player has at least one legal move
        return True  # Stalemate: No legal moves available
    # ---------------------------------------

    # Castle functions ----------------------
    def is_castle(self, start, end):
        # Check if the move is a castle
        # Get the piece at the start position
        piece = self.board.get_piece(start)

        # Check if the piece is a king and if the move is a castle
        if isinstance(piece, King):
            # Determine if it's a kingside or queenside castle based on the end position
            if end == (0, 6) and piece.color == 'white':
                return True
            elif end == (0, 2) and piece.color == 'white':
                return True
            elif end == (7, 6) and piece.color == 'black':
                return True
            elif end == (7, 2) and piece.color == 'black':
                return True

        return False
    # ---------------------------------------

    # Promotion functions -------------------
    def create_piece(self, piece_type, color):
        if piece_type == 'queen':
            return Queen(color)
        elif piece_type == 'rook':
            return Rook(color)
        elif piece_type == 'bishop':
            return Bishop(color)
        elif piece_type == 'knight':
            return Knight(color)
        else:
            return Queen(color)  # Default to queen if an invalid choice is made

    def promote(self, piece, position):
        if isinstance(piece, Pawn) and (piece.color == 'white' and position[0] == 7) or (piece.color == 'black' and position[0] == 0):
            print("Pawn promotion!\n")
            promotion_options = ['queen', 'rook', 'bishop', 'knight']
            print("Choose a piece to promote to: queen, rook, bishop, knight\n")
            choice = input("Enter your choice: ").lower()
            if choice in promotion_options:
                promoted_piece = self.create_piece(choice, piece.color)
                self.board.set_piece(position, promoted_piece)
                print(f"Promoted pawn to {choice.capitalize()}")
            else:
                print("Invalid choice. Pawn will be promoted to a queen by default.")
                self.board.set_piece(position, Queen(piece.color))
                print("Promoted pawn to Queen")
    # ---------------------------------------
    
    # En passant ----------------------------
    def en_passant(self, current_pos, new_pos):
        # Get the piece at the new position
        piece = self.board.get_piece(new_pos)

        # Check if the moving piece is a pawn
        if isinstance(piece, Pawn):
            # Check if the pawn moved two squares forward from its starting position
            if abs(new_pos[0] - current_pos[0]) == 2:
                # Determine the position of the square where the opposing pawn can capture en passant
                capture_pos = (current_pos[0], new_pos[1])

                # Check if there is a pawn of the opposing color at the capture position
                if self.board.get_piece(capture_pos) is not None and self.board.get_piece(capture_pos).color != piece.color:
                    # Remove the captured pawn from the board
                    self.board.set_piece(capture_pos, None)
                    print("En passant capture successful!")
                    return True

        return False
    # ---------------------------------------

    def move_piece(self, start_pos, end_pos):
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
            print(f"{piece}, Invalid move.")
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
            self.promote(piece, end_pos)
            self.en_passant(start_pos, end_pos)
            return True

    def play(self):
        while not self.is_game_over():
            self.board.display_board()
            print(f"It's {self.current_player}'s turn.")
            start = input("Enter the start position (e.g., 'a2'): \n")
            end = input("Enter the end position (e.g., 'a4'): \n")

            # Convert input positions to board coordinates
            start_pos = self.convert_position(start)
            end_pos = self.convert_position(end)

            # Check if the move is a castle
            if self.is_castle(start_pos, end_pos):
                if self.board.castle(self.current_player, end_pos):
                    print("Castle successful!")
                    self.switch_player()
                else:
                    print("Castle unsuccessful. Try again.")
                continue

            if self.move_piece(start_pos, end_pos):
                self.switch_player()
                # if self.is_checkmate(self.current_player):
                #     print(f"Checkmate! {self.current_player.capitalize()} wins!")
                #     return
                # elif self.is_stalemate():
                #     print("Stalemate! The game is a draw.")
                #     return

if __name__ == "__main__":
    
    # Play the game
    game = ChessGame()
    game.play()