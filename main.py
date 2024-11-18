import tkinter as tk
import random
import time
from PIL import Image, ImageTk
root = tk.Tk()

PLAYER_SIZE = 20
ENEMY_SIZE = 20
WIDTH = 400
HEIGHT = 600
ENEMY_SPEED = 5
ENEMY_COUNT = 10

canvas = tk.Canvas(root,width=WIDTH,height=HEIGHT,bg="white")
canvas.pack()
x = random.uniform(PLAYER_SIZE/2,WIDTH-PLAYER_SIZE/2)
y = random.uniform(PLAYER_SIZE/2,HEIGHT-PLAYER_SIZE/2)

img = Image.open("D:/python code/image/player.png").resize((PLAYER_SIZE,PLAYER_SIZE))
player_img = ImageTk.PhotoImage(img)
player = canvas.create_image(x,y,image=player_img)

img = Image.open("D:/python code/image/enemy.png").resize((ENEMY_SIZE,ENEMY_SIZE))
enemy_img = ImageTk.PhotoImage(img)


enemies=[]

#隨機
def create_enemy():
    x = random.uniform(ENEMY_SIZE/2,WIDTH-ENEMY_SIZE/2)
    y = random.uniform(ENEMY_SIZE/2,HEIGHT-ENEMY_SIZE/2)
    
    enemy = canvas.create_image(x,y,image=enemy_img)

    enemies.append(enemy)
    
#移動
def move_player(event):
    key = event.keysym
    x, y = 0, 0
    player_coords = canvas.coords(player)
    if key == "Up" and player_coords[1] - PLAYER_SIZE/2 > 0:
        y = -10
    elif key == "Down" and player_coords[1] + PLAYER_SIZE/2 < HEIGHT:
        y = 10
    elif key == "Left" and player_coords[0] - PLAYER_SIZE/2 > 0:
        x = -10
    elif key == "Right" and player_coords[0] + PLAYER_SIZE/2 < WIDTH:
        x = 10
    canvas.move(player,x,y)

#創造敵人
for _ in range(ENEMY_COUNT):
    create_enemy()
    time.sleep(0.1)

def check_collision():
    for enemy in enemies:
        player_coords = canvas.coords(player)
        enemy_coords = canvas.coords(enemy)
        if player_coords[0] - PLAYER_SIZE/2 <= enemy_coords[0] + ENEMY_SIZE/2 and \
        player_coords[1] - PLAYER_SIZE/2 <= enemy_coords[1] + ENEMY_SIZE/2 and \
        player_coords[0] + PLAYER_SIZE/2 >= enemy_coords[0] - ENEMY_SIZE/2 and \
        player_coords[1] + PLAYER_SIZE/2 >= enemy_coords[1] - ENEMY_SIZE/2:
            return True
    return False

def main_loop():
    #檢測碰撞
    if not check_collision():
        for enemy in enemies:
            canvas.move(enemy,0,5)
            if canvas.coords(enemy)[1]>HEIGHT-ENEMY_SIZE/2:
                canvas.delete(enemy)
                enemies.remove(enemy)
                create_enemy()
    else:
        canvas.create_text(200,250,text="Game Over",fill="#00A600",font=("blazed",40))
        root.unbind("<Key>")
    root.after(50,main_loop)
    
root.bind("<Key>",move_player)
main_loop()
root.mainloop()