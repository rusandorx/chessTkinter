import tkinter
from tkinter import Button, Label, Text, END

from ChessLib import Board


def drawBoard(canvas, board):
    canvas.delete('all')
    temp = True
    for x in range(0, 725, 75):
        for y in range(00, 600, 75):
            canvas.create_rectangle(x, y, x + 75, y + 75, fill='#eeeed2' if temp else '#769656')
            temp = not temp
        temp = not temp


def main():
    canvas_width, canvas_height = 600, 600
    master = tkinter.Tk()
    canvas = tkinter.Canvas(master, bg='white', height=canvas_height, width=canvas_width)
    board = Board()
    drawBoard(canvas, board)
    canvas.pack()

    def Take_input():
        INPUT = inputtxt.get("1.0", "end-1c").split()
        try:
            if INPUT[0] == 'exit':
                quit()
            action, rest = INPUT[0], list(map(int, INPUT[1:]))
            print(action, rest)
            if len(rest) == 5 and action == 'promote':
                if not board.move_and_promote_pawn(*rest):
                    wrong_move_text()
                    return
            elif len(rest) == 4 and action == 'move':
                if not board.move_piece(*rest):
                    wrong_move_text()
                    return
            else:
                wrong_move_text()
                return
            drawBoard(canvas, board)
            Output.delete(0.0, END)
            Output.insert(END, 'Ход совершен')
        except ValueError:
            wrong_move_text()
            return

    def wrong_move_text():
        Output.delete(0.0, END)
        Output.insert(END, 'Неверный ход')

    l = Label(text="Команды:\n"
                   "    exit                               -- выход\n"
                   "    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)\n"
                   "                                          в клетку (row1, col1)\n"
                   "    promote <row> <col> <row1> <col1> <char> -- ходить пешкой и превратить пешку в другую фигуру"
                   " (char - символ фигуры)")

    inputtxt = Text(master, height=2,
                    width=15,
                    bg="light yellow")

    Output = Text(master, height=5,
                  width=25,
                  bg="light cyan")

    Display = Button(master, height=2,
                     width=20,
                     text="Подтвердить ход",
                     command=lambda: Take_input())

    l.pack()
    inputtxt.pack()
    Display.pack()
    Output.pack()
    master.mainloop()


if __name__ == '__main__':
    main()
