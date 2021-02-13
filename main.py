import random, time, tkinter


class Minefield(object):
    def __init__(self, width=20, height=20, percentage=0.125):
        self.bombs = [[0] * width for _ in range(height)]
        self.uncovered = [[0] * width for _ in range(height)]

        self.width = width
        self.height = height

        self.state = 0  # 0=playing, 1=lost, 2=won

        # generate bombs
        self.total = round(width * height * percentage)
        if percentage > 1:
            self.total = width * height

        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < percentage and count < self.total:
                    self.bombs[y][x] = 1
                    count += 1

        self.root = tkinter.Tk()
        self.root.title("Minesweeper")

        # images
        self.bomb_image = tkinter.PhotoImage(file="assets/bomb.gif")
        self.flag_image = tkinter.PhotoImage(
            file="assets/Minesweeper Flag 20x20.gif"
        )
        self.flag_large_image = tkinter.PhotoImage(
            file="assets/Minesweeper Flag 50x50.gif"
        )
        self.flag_large_circled_image = tkinter.PhotoImage(
            file="assets/Minesweeper Flag (Circled) 50x50.gif"
        )

        self.controls = tkinter.Frame(self.root)
        self.flag_state = 0  # 0=uncover, 1=place flag
        self.flag_toggle = tkinter.Button(
            self.controls, image=self.flag_large_image, command=self.toggle
        )
        self.flag_toggle.pack()
        self.controls.pack()

        self.field = tkinter.Frame(self.root)

        self.grid_objects = []
        for i in range(height):
            row_objects = []
            for j in range(width):
                frame = tkinter.Frame(self.field, width=20, height=20)
                frame.grid_propagate(False)
                frame.columnconfigure(0, weight=1)
                frame.rowconfigure(0, weight=1)
                frame.grid(row=i, column=j)

                button = tkinter.Button(
                    frame, command=lambda i=i, j=j: self.uncover(j, i)
                )
                button.grid(sticky="nesw")

                row_objects.append([frame, button])

            self.grid_objects.append(row_objects)

        self.field.pack(side="top", expand=1)
        self.root.after(0, self.event_loop)

    def toggle(self):
        if self.flag_state:
            self.flag_state = 0
            self.flag_toggle.configure(image=self.flag_large_image)

        else:
            self.flag_state = 1
            self.flag_toggle.configure(image=self.flag_large_circled_image)

    def event_loop(self):
        if self.state == 1:
            for y, row in enumerate(self.uncovered):
                for x, val in enumerate(row):
                    if val == 0:
                        self.uncover(x, y)

        self.root.after(100, self.event_loop)

    def count_adj_bombs(self, x, y):
        adj = 0
        if y:
            rows = self.bombs[y - 1 : y + 2]

        else:
            rows = self.bombs[0 : 2]

        for row in rows:
            if x:
                adj += row[x - 1 : x + 2].count(1)

            else:
                adj += row[0 : 2].count(1)

        if self.bombs[y][x]:
            adj -= 1

        return adj

    def uncover(self, x, y):
        self.grid_objects[y][x][1].grid_forget()
        self.uncovered[y][x] = 1
        if self.bombs[y][x]:
            # landed on bomb
            self.state = 1
            canvas = tkinter.Canvas(self.grid_objects[y][x][0])
            canvas.create_image(0, 0, anchor="nw", image=self.bomb_image)
            canvas.grid(sticky="nesw")

        else:
            adj = self.count_adj_bombs(x, y)
            if adj != 0:
                label = tkinter.Label(
                    self.grid_objects[y][x][0], text=str(adj)
                )
                label.grid(sticky="nesw")

            else:
                self.uncover_adjacent(x, y)

    def uncover_adjacent(self, x, y):
        rows = cols = []
        if y:
            if y == self.height - 1:
                rows = range(y - 1, y + 1)

            else:
                rows = range(y - 1, y + 2)

        elif self.height:
            rows = range(2)

        if x:
            if x == self.width - 1:
                cols = range(x - 1, x + 1)

            else:
                cols = range(x - 1, x + 2)

        elif self.width:
            cols = range(2)

        for y2 in rows:
            for x2 in cols:
                if not (self.uncovered[y2][x2] or self.bombs[y2][x2]):
                    self.uncover(x2, y2)

if __name__ == "__main__":
    example = Minefield()
    example.root.mainloop()
