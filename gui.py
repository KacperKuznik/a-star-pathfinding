import tkinter as tk
from PIL import ImageTk, Image
from a_star import A_Star
import time
class Gui:
    def __init__(self, board: list, size: int):
        self.board = board
        self.step = 0
        self.colors = ["blue", "deep pink", "grey"]
        self.labels = ["Place starting point", "Place ending point", "Place walls"]
        self.frame_size = 30
        self.n = size
        self.font = ("Helvetica", 16)
        self.started = False
        self.algorithm = None

        self.cat_img = Image.open("cat.png")
        self.mouse_img = Image.open("mouse.png")
        self.window = tk.Tk()
        self.window.configure(bg="black")
        self.label = tk.LabelFrame(self.window, text=self.labels[self.step],
                      height=self.frame_size, bg="white", border=0, font=self.font, labelanchor="w")
        self.label.grid(row=0, column=0, columnspan=self.n-4, padx=1, pady=1, sticky="we")
        self.start_button = tk.LabelFrame(
            master=self.window,
            background="gray",
            width=self.frame_size,
            height=self.frame_size,
            text="start",
            border=0,
            font=self.font,
            labelanchor="w"
        )
        self.start_button.grid(row=0, column=self.n-4, columnspan=self.n, padx=1, pady=1, sticky="we")
        
        self.frames = board = [[None for i in range(self.n)] for j in range(self.n)]
        for row in range(self.n):
            for col in range(self.n):
                frame = tk.Frame(
                    master=self.window,
                    background="white",
                    width=self.frame_size,
                    height=self.frame_size
                )
                self.frames[row][col] = frame
                frame.grid(row=row+1, column=col, padx=1, pady=1)
                frame.bind("<Button-1>", lambda event,
                        row=row, col=col: self.update(event, row, col),)

        self.window.maxsize((self.frame_size + 2) * self.n, (self.frame_size + 2) * (self.n + 1))

    def run(self):
        while True:
            self.window.update_idletasks()
            self.window.update()
            if self.started:
                status, nodes = self.algorithm.do_single_step()
                self.label.config(text=status)
                if status == "Found":
                    self.started = False
                    for node_pos in nodes[::-1]:
                        self.frames[node_pos[0]][node_pos[1]].config(bg='purple')
                        self.window.update_idletasks()
                        self.window.update()
                        time.sleep(0.01)
                elif status == "Searching":
                    for node in nodes:
                        node_pos = node.pos
                        green = max(255 - node.g * 10, 50)
                        self.frames[node_pos[0]][node_pos[1]].config(bg=f'#{255:02x}{green:02x}{0:02x}')

                else:
                    self.started = False

    def update(self, event, row: int, col: int):
        if event.widget["background"] == "white":
            event.widget.config(bg=self.colors[self.step])

            if self.step == 0:
                self.start_pos = (row, col)
                self.step += 1
                self.label.config(text=self.labels[self.step])
                self.add_image(self.cat_img, event.widget)

            elif self.step == 1:
                self.end_pos = (row, col)
                self.step += 1
                self.label.config(text=self.labels[self.step])
                self.add_image(self.mouse_img, event.widget)
                self.start_button.config(bg="green")
                self.start_button.bind("<Button-1>", lambda event: self.start_algorithm())
            else:
                self.board[row][col] = "X"

    def start_algorithm(self):
        self.algorithm = A_Star(self.board, self.start_pos, self.end_pos)
        self.started = True
        self.start_button.unbind("<Button-1>")
    
    def add_image(self, image: ImageTk, element):
            canvas_for_image = tk.Canvas(element, height=self.frame_size, width=self.frame_size, borderwidth=0, highlightthickness=0)
            canvas_for_image.grid(row=0, column=0, sticky='nesw', padx=0, pady=0)
            canvas_for_image.image = ImageTk.PhotoImage(image.resize((self.frame_size, self.frame_size), Image.ANTIALIAS))
            canvas_for_image.create_image(0, 0, image=canvas_for_image.image, anchor='nw')


