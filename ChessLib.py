WHITE = 1
BLACK = 2


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def main():
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    while True:
        # Выводим положение фигур на доске
        print_board(board)
        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <row1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход чёрных:')
        command = input()
        if command == 'exit':
            break
        try:
            move_type, row, col, row1, col1 = command.split()
            row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        except ValueError:
            print('Неверные координаты хода.')
            continue

        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')


def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if isinstance(piece, Pawn) and (row1 == 7 or row1 == 0):
            return False
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color)
        return True

    def winner(self):
        if all(p is None or isinstance(p, King) for row in self.field for p in row):
            return 'Equal'
        if all(not isinstance(p, King) or p.get_color() != WHITE for row in self.field for p in row):
            return BLACK
        if all(not isinstance(p, King) or p.get_color() != BLACK for row in self.field for p in row):
            return WHITE

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        pawn = self.field[row][col]
        if pawn is None or not isinstance(pawn, Pawn):
            return False
        if (row1 != len(self.field) - 1 and pawn.get_color() == WHITE) \
                or (row1 != 0 and pawn.get_color() == BLACK):
            return False
        if self.field[row1][col1] is None:
            if not pawn.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(pawn.get_color()):
            if not pawn.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False

        self.field[row][col] = None  # Снять фигуру.
        chars_to_figures = {'Q': Queen, 'R': Rook, 'B': Bishop, 'N': Knight}
        if char not in chars_to_figures:
            return False
        self.field[row1][col1] = chars_to_figures[char](self.color)
        self.color = opponent(self.color)
        return True

    def castle_check(self, king, rook):
        if rook is None or king is None:
            return False
        if not (isinstance(rook, Rook) and isinstance(king, King)):
            return False
        if rook.moved or king.moved:
            return False
        if rook.get_color() != self.color or king.get_color() != self.color:
            return False
        return True

    def castling0(self):
        coords = ((0, 0), (0, 4)) if self.color == WHITE else ((7, 0), (7, 4))
        rook = self.field[coords[0][0]][coords[0][1]]
        king = self.field[coords[1][0]][coords[1][1]]
        if not self.castle_check(king, rook):
            return False
        if not rook.can_move(self, coords[0][0], 0, coords[1][0], 4):
            return False

        self.field[coords[0][0]][coords[0][1]] = None
        self.field[coords[1][0]][coords[1][1]] = None
        self.field[coords[0][0]][2] = King(self.color)
        self.field[coords[0][0]][2].moved = True
        self.field[coords[0][0]][3] = Rook(self.color)
        self.field[coords[0][0]][3].moved = True
        self.color = opponent(self.color)
        return True

    def castling7(self):
        coords = ((0, 7), (0, 4)) if self.color == WHITE else ((7, 7), (7, 4))
        rook = self.field[coords[0][0]][coords[0][1]]
        king = self.field[coords[1][0]][coords[1][1]]
        if not self.castle_check(king, rook):
            return False
        if not rook.can_move(self, coords[0][0], 7, coords[1][0], 4):
            return False
        self.field[coords[0][0]][coords[0][1]] = None
        self.field[coords[1][0]][coords[1][1]] = None
        self.field[coords[0][0]][6] = King(self.color)
        self.field[coords[0][0]][6].moved = True
        self.field[coords[0][0]][5] = Rook(self.color)
        self.field[coords[0][0]][5].moved = True
        self.color = opponent(self.color)
        return True


class Figure:

    def __init__(self, color):
        self.color = color
        self.character = None

    def char(self):
        return self.character

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        return correct_coords(row, col) and correct_coords(row1, col1)

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def get_image(self):
        return f'Icons/{"Black" if self.color == BLACK else "White"}/{self.character.lower()}.png'


class Rook(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.character = 'R'
        self.moved = False

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(row, c) is None):
                return False
        self.moved = True
        return True


class Pawn(Figure):

    def __init__(self, color):
        super().__init__(color)
        self.character = 'P'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Knight(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.character = 'N'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        return abs(col - col1) == 2 and abs(row - row1) == 1 \
               or abs(col - col1) == 1 and abs(row - row1) == 2


class King(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.character = 'K'
        self.moved = False

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if not super().can_move(board, row, col, row1, col1):
            return False
        if abs(row - row1) <= 1 and abs(col - col1) <= 1:
            self.moved = True
            return True


class Queen(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.character = 'Q'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if not (abs(row - row1) == abs(col - col1) or row == row1 or col == col1):
            return False

        if row != row1:
            normalized_row = -(row - row1) // abs(row - row1)
        else:
            normalized_row = 0

        if col != col1:
            normalized_col = -(col - col1) // abs(col - col1)
        else:
            normalized_col = 0

        cur_row, cur_col = row, col
        while True:
            cur_row += normalized_row
            cur_col += normalized_col
            if cur_row == row1 and cur_col == col1:
                return True
            if board.field[cur_row][cur_col] is not None:
                return False


class Bishop(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.character = 'B'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if not (abs(row - row1) == abs(col - col1)):
            return False

        if row != row1:
            normalized_row = -(row - row1) // abs(row - row1)
        else:
            normalized_row = 0

        if col != col1:
            normalized_col = -(col - col1) // abs(col - col1)
        else:
            normalized_col = 0

        cur_row, cur_col = row, col
        while True:
            cur_row += normalized_row
            cur_col += normalized_col
            if cur_row == row1 and cur_col == col1:
                return True
            if board.field[cur_row][cur_col] is not None:
                return False


if __name__ == "__main__":
    main()
