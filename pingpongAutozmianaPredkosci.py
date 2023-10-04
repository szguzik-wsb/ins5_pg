import tkinter as tk


class PingPong:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Pong - zmiana predkosci")

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='black')
        self.canvas.pack()

        self.speed = 1  # Prędkość piłki (1px na klatkę)
        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill='white')
        self.ball_dx = self.speed
        self.ball_dy = -self.speed

        self.paddle = self.canvas.create_rectangle(250, 390, 350, 400, fill='blue')
        self.paddle_dx = 20

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        self.animate()

    def move_left(self, event):
        self.canvas.move(self.paddle, -self.paddle_dx, 0)

    def move_right(self, event):
        self.canvas.move(self.paddle, self.paddle_dx, 0)

    def animate(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)

        ball_coords = self.canvas.coords(self.ball)
        paddle_coords = self.canvas.coords(self.paddle)

        if ball_coords[1] <= 0 or (
                ball_coords[3] >= 390 and ball_coords[2] >= paddle_coords[0] and ball_coords[0] <= paddle_coords[2]):
            self.ball_dy = -self.ball_dy
            if ball_coords[3] >= 390 and ball_coords[2] >= paddle_coords[0] and ball_coords[0] <= paddle_coords[
                2]:  # Jeżeli piłka dotknie paletki
                self.speed += 1  # Przyspiesz piłkę
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
