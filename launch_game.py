# launch_game.py

from board import Chessboard

class ChessGame:
    def __init__(self):
        self.board = Chessboard()
        self.current_player = 'white'

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
    
    def play(self):
        while not self.is_game_over():
            self.board.display_board()
            print(f"It's {self.current_player}'s turn.")
            start = input("Enter the start position (e.g., 'a2'): ")
            end = input("Enter the end position (e.g., 'a4'): ")

            if self.move_piece(start, end):
                self.switch_player()
                if self.is_checkmate(self.current_player):
                    print(f"Checkmate! {self.current_player.capitalize()} wins!")
                    return
                elif self.is_stalemate():
                    print("Stalemate! The game is a draw.")
                    return
    
    def simulate_move(self, start, end):
        # Implement logic to simulate a move without modifying the board's state
        pass 

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

# Play the game
game = ChessGame()
game.play()