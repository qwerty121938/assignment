import tkinter as tk
import random
import time
import math
from PIL import Image, ImageTk

PLAYER_SIZE = 20
ENEMY_SIZE = 20
WIDTH = 500
HEIGHT = 600
ENEMY_SPEED = 5
ENEMY_COUNT = 10

class Game():
    def __init__(self):
        self.root = tk.Tk()
        self.root.bind("<Key>", self.key_pressed)
        self.root.bind("<Button-1>", self.mouse_clicked)
        self.canvas = tk.Canvas(self.root, width = WIDTH, height = HEIGHT, bg = "#161823")
        self.canvas.config(highlightthickness=0)

        player_img = Image.open("./image/player.png").resize((PLAYER_SIZE,PLAYER_SIZE))
        player = ImageTk.PhotoImage(player_img)
        player = self.canvas.create_image(100,100,image=player)
        self.enemies = []
        self.create_player()
        for _ in range(ENEMY_COUNT):
            self.create_enemy()
            time.sleep(0.1)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.canvas.pack() 

        self.enemy_random_move()
        self.root.mainloop()
        
        
    def enemy_random_move(self):
        if not self.check_collision():
            for enemy in self.enemies:
                self.canvas.move(enemy,0,5)
                if self.canvas.coords(enemy)[1]>HEIGHT-20:
                    self.canvas.delete(enemy)
                    self.enemies.remove(enemy)
                    self.create_enemy()
        else:
            self.canvas.create_text(200,250,text="Game Over",fill="#00A600",font=("blazed",40))
            self.root.unbind("<Key>")
        self.root.after(50,self.enemy_random_move)
    
    def create_player(self):
        x = random.randint(0,WIDTH-20)
        y = random.randint(300,HEIGHT-20)
        self.player = self.canvas.create_image(x,y,image=tk.PhotoImage(file="./image/player.png"))

    def create_enemy(self):
        x = random.randint(0,WIDTH-20)
        y = random.randint(0,100)
        self.enemies.append(self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="#EA8899"))

    def mouse_clicked(self, event):
        print(event)

    def key_pressed(self, event):
        x=0
        y=0
        if event.keysym == "Right":
            x=10
        elif event.keysym == "Left":
            x=-10
        elif event.keysym == "Up":
            y=-10
        elif event.keysym == "Down":
            y=10
        self.canvas.move(self.player, x, y)
        

    def check_collision(self):
        for enemy in self.enemies:
            player_coords = self.canvas.coords(self.player) # 获取玩家坐标
            enemy_coords = self.canvas.coords(enemy) # 获取敌人坐标
            if player_coords[0] <= enemy_coords[2] and \
               player_coords[1] <= enemy_coords[3] and \
               player_coords[2] >= enemy_coords[0] and \
               player_coords[3] >= enemy_coords[1]:
                return True
        return False
    

    def on_closing(self):
        self.root.destroy()

if __name__ == "__main__":
    Game() 