import tkinter as tk
import random
import time
from PIL import Image, ImageTk


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
    
class Enemy(Gameobject):
    def __init__(self, canvas, image_path, size):
       
        random_x = random.randint(0 + size, WIDTH - size) 
        random_y = random.randint(0 + size, HEIGHT - size)
        super().__init__(canvas, image_path, size, random_x, random_y)

    @staticmethod
    def create_enemies(canvas, image_path, size):
        enemy = Enemy(canvas, image_path, size)
        return enemy

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Game")
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{int(SCREEN_WIDTH/4)}+{int(SCREEN_HEIGHT/4)}")
        self.root.iconbitmap(f"{DIRECTORY}/image/game_icon.ico")
        self.canvas = tk.Canvas(self.root,width=WIDTH,height=HEIGHT,bg="white")
        self.canvas.pack()

        self.game_over = False
        self.player = Player(self.canvas, f"{DIRECTORY}/image/player.png", PLAYER_SIZE, WIDTH/2, HEIGHT/2)
        self.enemies = []
        for i in range(ENEMY_COUNT):
            self.enemies.append(Enemy(self.canvas, f"{DIRECTORY}/image/enemy.png", PLAYER_SIZE))
        
        self.root.bind("<Key>",self.player.move_player)
        self.main_loop()
        self.root.mainloop()

    def check_collision(self):
        player_coords = self.player.get_position()
        for enemy in self.enemies:
            enemy_coords = enemy.get_position()
            if player_coords[0] - PLAYER_SIZE/2 <= enemy_coords[0] + ENEMY_SIZE/2 and \
                player_coords[1] - PLAYER_SIZE/2 <= enemy_coords[1] + ENEMY_SIZE/2 and \
                player_coords[0] + PLAYER_SIZE/2 >= enemy_coords[0] - ENEMY_SIZE/2 and \
                player_coords[1] + PLAYER_SIZE/2 >= enemy_coords[1] - ENEMY_SIZE/2:
                return True
        return False
         
    def main_loop(self):
        #檢測碰撞
        self.game_over = self.check_collision()
        if not self.game_over:
            for enemy in self.enemies:
                enemy_coords = enemy.get_position()
                enemy.move(0,5)
                if enemy_coords[1]>HEIGHT-ENEMY_SIZE/2:
                    self.canvas.delete(enemy)
                    self.enemies.remove(enemy)
                    enemy = Enemy.create_enemies(self.canvas, f"{DIRECTORY}/image/enemy.png", ENEMY_SIZE)
                    self.enemies.append(enemy)
        else:
            self.canvas.create_text(200,250,text="Game Over",fill="#00A600",font=("blazed",40))
            self.root.unbind("<Key>")

        self.root.after(50,self.main_loop)

if __name__ == "__main__":
    root = tk.Tk()
    DIRECTORY = "C:/Users/admin/Desktop/coding/python/assignment"
    PLAYER_SIZE = 20
    ENEMY_SIZE = 20
    WIDTH = 400
    HEIGHT = 600
    SCREEN_WIDTH = root.winfo_screenwidth()
    SCREEN_HEIGHT = root.winfo_screenheight()
    ENEMY_SPEED = 5
    ENEMY_COUNT = 10
    game = Game(root)
    
