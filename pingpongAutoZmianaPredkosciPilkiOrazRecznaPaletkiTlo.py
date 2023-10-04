import tkinter as tk
from PIL import Image, ImageTk


class PingPong:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Pong @Szymon Guzik")
        self.setup_ui()
        self.setup_game()

    def setup_ui(self):
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.speed_label = tk.Label(self.root)
        self.speed_label.pack(side=tk.LEFT)

        self.restart_button = tk.Button(self.root, text="Restart", command=self.setup_game)
        self.restart_button.pack(side=tk.LEFT, padx=10)

        self.bounce_counter_label = tk.Label(self.root, text="Odbicia: 0")
        self.bounce_counter_label.pack(side=tk.RIGHT)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_countdown)
        self.start_button.pack(side=tk.LEFT, padx=10)

    def setup_game(self):
        self.bounces = 0
        self.bounce_counter_label.config(text="Odbicia: 0")
        self.canvas.delete("all")
        self.start_button.config(state=tk.NORMAL)

        # Wczytywanie i skalowanie obrazu tła
        self.load_background()

        # Wczytywanie i skalowanie obrazu piłki
        self.load_ball_image()

        # Wczytywanie i skalowanie obrazu paletki
        self.load_paddle_image()

        self.speed = 5
        self.acceleration = 5
        self.ball_dx = self.speed
        self.ball_dy = -self.speed

        self.paddle_dx = 10
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Up>", self.increase_paddle_speed)
        self.root.bind("<Down>", self.decrease_paddle_speed)
        self.root.bind("<R>", lambda event: self.setup_game())
        self.root.bind("<r>", lambda event: self.setup_game())
        self.root.bind("<S>", lambda event: self.start_countdown())
        self.root.bind("<s>", lambda event: self.start_countdown())

        self.speed_label.config(text="Precyzja domyślna: {}".format(self.paddle_dx))



    def load_background(self):
        image_bg = Image.open("tlo.jpg")
        ratio_bg = min(self.canvas_width / image_bg.width, self.canvas_height / image_bg.height)
        new_width_bg = int(image_bg.width * ratio_bg)
        new_height_bg = int(image_bg.height * ratio_bg)
        image_bg = image_bg.resize((new_width_bg, new_height_bg), Image.LANCZOS)
        self.background = ImageTk.PhotoImage(image_bg)
        bg_x = (self.canvas_width - new_width_bg) / 2
        bg_y = (self.canvas_height - new_height_bg) / 2
        self.canvas.create_image(bg_x, bg_y, image=self.background, anchor=tk.NW)

    def load_ball_image(self):
        image_ball = Image.open("pilka.png")
        image_ball = image_ball.resize((25, 20), Image.LANCZOS)
        self.ball_img = ImageTk.PhotoImage(image_ball)
        self.ball = self.canvas.create_image(295, 195, image=self.ball_img)

    def load_paddle_image(self):
        image_paddle = Image.open("paletka.png")
        image_paddle = image_paddle.resize((100, 10), Image.LANCZOS)
        self.paddle_img = ImageTk.PhotoImage(image_paddle)
        self.paddle = self.canvas.create_image(300, 390, image=self.paddle_img)

    def start_countdown(self):
        self.count = 5
        self.countdown_id = self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2, text=self.count,
                                                    font=("Arial", 30), fill="limegreen")
        self.root.after(1000, self.update_countdown)
        self.start_button.config(state=tk.DISABLED)

    def update_countdown(self):
        if self.count > 0:
            self.count -= 1
            self.canvas.itemconfig(self.countdown_id, text=self.count)
            self.root.after(1000, self.update_countdown)
        else:
            self.canvas.delete(self.countdown_id)
            self.move_ball()

    def move_ball(self):
        x, y = self.canvas.coords(self.ball)
        if x <= 10 or x >= self.canvas_width - 10:
            self.ball_dx = -self.ball_dx
        if y <= 10:
            self.ball_dy = -self.ball_dy
        if y >= self.canvas_height - 10:
            self.end_game()
            return

        paddle_x, paddle_y = self.canvas.coords(self.paddle)
        if (x >= paddle_x - 50 and x <= paddle_x + 50) and y + 10 >= paddle_y - 5:
            self.ball_dy = -self.ball_dy
            self.bounces += 1
            self.bounce_counter_label.config(text="Odbicia: {}".format(self.bounces))
            self.speed += self.acceleration
            self.ball_dx = self.speed if self.ball_dx > 0 else -self.speed
            self.ball_dy = self.speed if self.ball_dy > 0 else -self.speed

        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        self.root.after(30, self.move_ball)

    def move_left(self, event):
        x, y = self.canvas.coords(self.paddle)
        if x - 50 - self.paddle_dx >= 0:
            self.canvas.move(self.paddle, -self.paddle_dx, 0)

    def move_right(self, event):
        x, y = self.canvas.coords(self.paddle)
        if x + 50 + self.paddle_dx <= self.canvas_width:
            self.canvas.move(self.paddle, self.paddle_dx, 0)

    def increase_paddle_speed(self, event):
        self.paddle_dx += 2
        self.speed_label.config(text="Precyzja zmniejszona: {}".format(self.paddle_dx))

    def decrease_paddle_speed(self, event):
        if self.paddle_dx > 2:
            self.paddle_dx -= 2
            self.speed_label.config(text="Precyzja zwiększona: {}".format(self.paddle_dx))

    def end_game(self):
        self.canvas.create_text(self.canvas_width / 2, self.canvas_height / 2, text="Koniec gry", font=("Arial", 24),
                                fill="limegreen")


if __name__ == "__main__":
    root = tk.Tk()
    game = PingPong(root)
    root.mainloop()
