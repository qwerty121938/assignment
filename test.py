import tkinter as tk
import random
import time
from PIL import Image, ImageTk

current_directory = "D:/python code"
root = tk.Tk()

PLAYER_SIZE = 20
ENEMY_SIZE = 20
WIDTH = 400
HEIGHT = 600
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
ENEMY_SPEED = 5
ENEMY_COUNT = 10

class Gameobject:
    def __init__(self, canvas, image_path, size, x, y):
        self.canvas = canvas
        self.size = size 
        img = Image.open(image_path).resize((size,size))
        self.image_tk = ImageTk.PhotoImage(img)
        self.object = self.canvas.create_image(x,y,image=self.image_tk)

    def move(self, dx, dy):
        self.canvas.move(self.object, dx, dy)

    def get_position(self):
        return self.canvas.coords(self.object)
    
class Player(Gameobject):
    def __init__(self, canvas, image_path, size, x, y):
        super().__init__(canvas, image_path, size, x, y)

    def move_player(self, event):
        key = event.keysym
        x, y = 0, 0
        player_coords = self.canvas.coords(self.object)
        if key == "Up" and player_coords[1] - PLAYER_SIZE/2 > 0:
            y = -10
        elif key == "Down" and player_coords[1] + PLAYER_SIZE/2 < HEIGHT:
            y = 10
        elif key == "Left" and player_coords[0] - PLAYER_SIZE/2 > 0:
            x = -10
        elif key == "Right" and player_coords[0] + PLAYER_SIZE/2 < WIDTH:
            x = 10
        self.canvas.move(self.object,x,y)           
    


if __name__ == "__main__":
    root.title("Game")
    root.geometry(f"{WIDTH}x{HEIGHT}+{int(SCREEN_WIDTH/4)}+{int(SCREEN_HEIGHT/4)}")
    root.iconbitmap(f"{current_directory}/image/game_icon.ico")

    canvas = tk.Canvas(root,width=WIDTH,height=HEIGHT,bg="white")
    canvas.pack()
    player = Player(canvas, f"{current_directory}/image/player.png", PLAYER_SIZE, WIDTH/2, HEIGHT/2)
    root.bind("<Key>",player.move_player)
    root.mainloop()
