# pieces.py 

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
            # print("Rook: Illegal move")
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
            # print("Bishop: Illegal move")
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
            # print("Queen: Illegal move")
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
            # print("Knight: Illegal move")
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
            # print("King: Illegal move")
            return False

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_not_moved = True

    def validate_move(self, current_pos, new_pos, board):
        # Logic to validate pawn's movement
        delta_x = new_pos[0] - current_pos[0] # Row
        delta_y = new_pos[1] - current_pos[1] # Col

        if self.color == 'black':
            if 0 < -delta_x <= (2 if self.has_not_moved else 1) and abs(delta_y) == 0 and board.get_piece(new_pos) == None:
                self.has_not_moved = False
                return True
            elif delta_x == -1 and abs(delta_y) == 1:
                if board.get_piece(new_pos) is not None and board.get_piece(new_pos).color != self.color:
                    self.has_not_moved = False
                    return True
            else:
                # print("Pawn: Illegal move")
                return False
        
        elif self.color == 'white':
            if 0 < delta_x <= (2 if self.has_not_moved else 1) and abs(delta_y) == 0 and board.get_piece(new_pos) == None:
                self.has_not_moved = False
                return True
            elif delta_x == 1 and abs(delta_y) == 1:
                if board.get_piece(new_pos) is not None and board.get_piece(new_pos).color != self.color:
                    self.has_not_moved = False
                    return True
            else:
                # print("Pawn: Illegal move")
                return False
        else:
            print("Pawn color not determined")