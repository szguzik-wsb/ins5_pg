import tkinter as tk
import tkinter.simpledialog as simpledialog


class PingPong:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Pong")

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='black')
        self.canvas.pack()

        self.speed = 1  # Initial ball speed (1px per frame)
        self.acceleration = 5  # Acceleration of ball for each paddle hit
        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill='white')
        self.ball_dx = self.speed
        self.ball_dy = -self.speed

        self.paddle_dx = 10  # Initial paddle speed
        self.paddle = self.canvas.create_rectangle(250, 390, 350, 400, fill='blue')

        self.moving_left = False
        self.moving_right = False

        self.root.bind("<Left>", self.start_move_left)
        self.root.bind("<Right>", self.start_move_right)
        self.root.bind("<KeyRelease-Left>", self.stop_move_left)
        self.root.bind("<KeyRelease-Right>", self.stop_move_right)

        self.speed_label = tk.Label(self.root, text="Prędkość paletki:")
        self.speed_label.pack()

        self.speed_entry = tk.Entry(self.root)
        self.speed_entry.pack()
        self.speed_entry.insert(0, "10")

        self.update_button = tk.Button(self.root, text="Aktualizuj prędkość", command=self.update_paddle_speed)
        self.update_button.pack()

        self.animate()

    def start_move_left(self, event):
        self.moving_left = True
        self.move_left()

    def start_move_right(self, event):
        self.moving_right = True
        self.move_right()

    def stop_move_left(self, event):
        self.moving_left = False

    def stop_move_right(self, event):
        self.moving_right = False

    def move_left(self):
        if self.moving_left:
            self.canvas.move(self.paddle, -self.paddle_dx, 0)
            self.root.after(10, self.move_left)

    def move_right(self):
        if self.moving_right:
            self.canvas.move(self.paddle, self.paddle_dx, 0)
            self.root.after(10, self.move_right)

    def update_paddle_speed(self):
        try:
            new_speed = float(self.speed_entry.get())
            self.paddle_dx = new_speed
        except ValueError:
            simpledialog.messagebox.showerror("Błąd", "Wprowadź poprawną wartość dla prędkości paletki!")

    def animate(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)

        ball_coords = self.canvas.coords(self.ball)
        paddle_coords = self.canvas.coords(self.paddle)

        if ball_coords[1] <= 0 or (
                ball_coords[3] >= 390 and ball_coords[2] >= paddle_coords[0] and ball_coords[0] <= paddle_coords[2]):
            self.ball_dy = -self.ball_dy
            if ball_coords[3] >= 390 and ball_coords[2] >= paddle_coords[0] and ball_coords[0] <= paddle_coords[2]:
                self.speed += self.acceleration
                if self.ball_dx > 0:
                    self.ball_dx = self.speed
                else:
                    self.ball_dx = -self.speed
                if self.ball_dy > 0:
                    self.ball_dy = self.speed
                else:
                    self.ball_dy = -self.speed

        if ball_coords[0] <= 0 or ball_coords[2] >= 600:
            self.ball_dx = -self.ball_dx

        if ball_coords[3] > 400:
            self.canvas.create_text(300, 200, text="Koniec gry", fill='red', font=('Arial', 24))
            return

        self.root.after(20, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    game = PingPong(root)
    root.mainloop()
