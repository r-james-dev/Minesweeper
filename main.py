import random, time, tkinter.messagebox, sys, os


def rectify_path(path):
    if hasattr(sys, "_MEIPASS"):
        path = os.path.join(sys._MEIPASS, path)

    else:
        path = os.path.join(os.path.dirname(__file__), path)

    return path


class Minefield(object):
    def __init__(self, width=20, height=20, percentage=0.125):
        self.bombs = [[0] * width for _ in range(height)]
        self.uncovered = [[0] * width for _ in range(height)]
        self.flagged = [[0] * width for _ in range(height)]

        self.percentage = percentage

        self.width = width
        self.height = height

        self.state = 0  # 0=playing, 1=lost, 2=won

        # generate bombs
        self.total = round(width * height * percentage)
        if percentage > 1:
            self.total = width * height

        random.seed(time.time())
        count = 0
        while count < self.total:
            for y in range(self.height):
                for x in range(self.width):
                    if random.random() < percentage:
                        self.bombs[y][x] = 1
                        count += 1

                    if count == self.total:
                        break

                else:
                    continue

                break

        self.root = tkinter.Tk()
        self.root.title("Minesweeper")

        # images
        self.root.iconbitmap(rectify_path("assets/bomb-128x128.ico"))
        self.bomb_image = tkinter.PhotoImage(
            file=rectify_path("assets/bomb-20x20.gif")
        )
        self.flag_image = tkinter.PhotoImage(
            file=rectify_path("assets/flag-20x20.gif")
        )
        self.flag_large_image = tkinter.PhotoImage(
            file=rectify_path("assets/flag-50x50.gif")
        )
        self.flag_large_circled_image = tkinter.PhotoImage(
            file=rectify_path("assets/flag-circled-50x50.gif")
        )
        self.restart_image = tkinter.PhotoImage(
            file=rectify_path("assets/restart-50x50.gif")
        )

        # top bar
        self.controls = tkinter.Frame(self.root)

        self.flag_count_msg = tkinter.StringVar(self.root)
        self.flag_count_msg.set(f"0/{self.total}")
        self.flag_counter = tkinter.Label(
            self.controls, textvariable=self.flag_count_msg,
            font=("sans-serif", 16)
        )
        self.flag_counter.pack(side="left")

        self.flag_state = 0  # 0=uncover, 1=place flag
        self.flag_count = 0
        self.flag_toggle = tkinter.Button(
            self.controls, image=self.flag_large_image, command=self.toggle
        )
        self.flag_toggle.pack(side="left")

        self.restart_button = tkinter.Button(
            self.controls, image=self.restart_image, command=self.restart
        )
        self.restart_button.pack(side="left")

        self.controls.pack()

        # button array
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
        self.mainloop = self.root.mainloop

    def restart(self):
        self.bombs = [[0] * self.width for _ in range(self.height)]
        self.uncovered = [[0] * self.width for _ in range(self.height)]

        self.state = 0

        # generate bombs
        self.total = round(self.width * self.height * self.percentage)
        if self.percentage > 1:
            self.total = self.width * self.height

        random.seed(time.time())
        count = 0
        while count < self.total:
            for y in range(self.height):
                for x in range(self.width):
                    if random.random() < self.percentage:
                        self.bombs[y][x] = 1
                        count += 1

                    if count == self.total:
                        break

                else:
                    continue

                break

        # reset button array
        for y in range(self.height):
            for x in range(self.width):
                self.grid_objects[y][x][1].configure(image="")
                if len(self.grid_objects[y][x]) == 3:
                    self.grid_objects[y][x][2].grid_forget()
                    self.grid_objects[y][x].pop()
                    self.grid_objects[y][x][1].grid(sticky="nesw")

        self.flag_count = 0
        self.flag_state = 0
        self.flag_count_msg.set(f"0/{self.total}")
        self.flag_toggle.configure(image=self.flag_large_image)
        self.flagged = [[0] * self.width for _ in range(self.height)]

    def toggle(self):
        if self.flag_state:
            self.flag_state = 0
            self.flag_toggle.configure(image=self.flag_large_image)

        else:
            self.flag_state = 1
            self.flag_toggle.configure(image=self.flag_large_circled_image)

    def event_loop(self):
        self.flag_count_msg.set(f"{self.flag_count}/{self.total}")
        if self.state == 0:
            if all(map(lambda x: x[0] == x[1], zip(self.bombs, self.flagged))):
                # all bombs flagged - win
                self.state = 2
                tkinter.messagebox.showinfo("Minesweeper", "You Win!")

            if all(map(lambda x: x[0] == x[1], zip(self.bombs, (
                        list(map(lambda x: not x, row)) for row in self.uncovered
                    )))):
                # all non-bomb squares uncovered - win
                self.state = 2
                tkinter.messagebox.showinfo("Minesweeper", "You Win!")

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
        if self.state == 2:
            return

        if self.flag_state:
            if self.flagged[y][x]:
                self.flag_count -= 1
                self.flagged[y][x] = 0
                self.grid_objects[y][x][1].configure(image="")

            elif self.flag_count < self.total:
                self.flag_count += 1
                self.flagged[y][x] = 1
                self.grid_objects[y][x][1].configure(image=self.flag_image)

        elif not self.flagged[y][x]:
            self.grid_objects[y][x][1].grid_remove()
            self.uncovered[y][x] = 1
            if self.bombs[y][x]:
                # landed on bomb
                self.state = 1
                canvas = tkinter.Canvas(self.grid_objects[y][x][0])
                canvas.create_image(0, 0, anchor="nw", image=self.bomb_image)
                canvas.grid(sticky="nesw")
                self.grid_objects[y][x].append(canvas)

            else:
                adj = self.count_adj_bombs(x, y)
                if adj != 0:
                    label = tkinter.Label(
                        self.grid_objects[y][x][0], text=str(adj)
                    )
                    label.grid(sticky="nesw")
                    self.grid_objects[y][x].append(label)

                else:
                    self.uncover_adjacent(x, y)

                    # placeholder label
                    label = tkinter.Label(self.grid_objects[y][x][0])
                    label.grid(sticky="nesw")
                    self.grid_objects[y][x].append(label)

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
    example.mainloop()
