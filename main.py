from gui import Gui
n = 25
board = [["." for i in range(n)] for j in range(n)]

if __name__ == "__main__":
    gui = Gui(board, n)
    gui.run()