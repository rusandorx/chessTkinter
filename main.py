import tkinter
from tkinter import Button, Label, Text, END

from ChessLib import Board, BLACK


def main():
    def drawBoard(board):
        temp = True
        for x in range(0, 600, 75):
            for y in range(0, 600, 75):
                canvas.create_rectangle(x, y, x + 75, y + 75, fill='#eeeed2' if temp else '#769656')
                temp = not temp
            temp = not temp
        for i, x in enumerate(range(0, 600, 75)):
            for j, y in enumerate(range(0, 600, 75)):
                piece = board.field[7 - i][j]
                if piece:
                    my_img = tkinter.PhotoImage(file=piece.get_image())
                    my_img.img = my_img

                    resized_img = my_img.subsample(8, 8)
                    resized_img.img = resized_img
                    canvas.create_image(y + 5, x + 5, image=resized_img, anchor='nw')

    canvas_width, canvas_height = 600, 600
    master = tkinter.Tk()
    canvas = tkinter.Canvas(master, bg='white', height=canvas_height, width=canvas_width)
    board = Board()

    def Take_input():
        INPUT = inputtxt.get("1.0", "end-1c").split()
        try:
            if not INPUT:
                raise ValueError
            action = INPUT[0]
            if len(INPUT) == 1:
                if action == 'exit':
                    quit()
                elif action == '00':
                    if not board.castling7():
                        wrong_move_text()
                        return
                elif action == '000':
                    if not board.castling0():
                        wrong_move_text()
                        return
            else:
                rest = INPUT[1:]
                if len(rest) == 4:
                    rest = list(map(lambda x: int(x) - 1, rest))
                else:
                    rest = list(map(lambda x: int(x) - 1, rest[:-1]))
                    rest.append(INPUT[-1].upper())
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
            print('??????:', action, *INPUT[1:])
            Output.delete(0.0, END)
            Output.insert(END, '?????? ????????????????')
            if res := board.winner():
                Output.delete(0.0, END)
                if res == 'Equal':
                    Output.insert(END, '??????????')
                else:
                    Output.insert(END, '???????????? ????????????????' if res == BLACK else '?????????? ????????????????')
                    inputtxt.destroy()
        except ValueError:
            wrong_move_text()
            return
        finally:
            drawBoard(board)
            drawBoard(board)

    def wrong_move_text():
        Output.delete(0.0, END)
        Output.insert(END, '???????????????? ??????')

    l = Label(text="??????????????:\n"
                   "    exit                               -- ??????????\n"
                   "    move <row> <col> <row1> <col1>     -- ?????? ???? ???????????? (row, col)\n"
                   "                                          ?? ???????????? (row1, col1)\n"
                   "    promote <row> <col> <row1> <col1> <char> -- ???????????? ???????????? ?? ???????????????????? ?????????? ?? ???????????? ????????????"
                   " (char - ???????????? ????????????)\n"
                   "    00                           -- ?????????????????? ?? ???????????????? ??????????????\n"
                   "    000                          -- ?????????????????? ?? ?????????????? ??????????????")

    inputtxt = Text(master, height=2,
                    width=17,
                    bg="light yellow")

    Output = Text(master, height=5,
                  width=25,
                  bg="light cyan")

    Display = Button(master, height=2,
                     width=20,
                     text="?????????????????????? ??????",
                     command=lambda: Take_input())
    b = Button(master, height=2,
               width=40,
               text="?????????? ???? ???????? ???????? ???????????? ??????????????",
               command=lambda: drawBoard(board))

    canvas.pack()
    drawBoard(board)
    drawBoard(board)
    b.pack()
    l.pack()
    inputtxt.pack()
    Display.pack()
    Output.pack()
    master.mainloop()


if __name__ == '__main__':
    main()
