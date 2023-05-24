import tkinter as tk
from random import randint, choice
from time import sleep, time
from math import sqrt
from constants import *

# Setup
window = tk.Tk()
window.title("Bubble Blaster")
screen = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg='darkblue')
screen.pack()

# Creating ship
ship_id: int = screen.create_polygon(5, 5, 5, 25, 30, 15, fill='red') # Draw triangle
ship_id2: int = screen.create_oval(0, 0, 30, 30, outline='red') # Draw circle
screen.move(ship_id, MID_X, MID_Y)
screen.move(ship_id2, MID_X, MID_Y)
# Controlling the submarine

def move_ship(event: object):
    if event.keysym == "Up":
        screen.move(ship_id, 0, -SHIP_SPEED)
        screen.move(ship_id2, 0, -SHIP_SPEED)
    elif event.keysym == "Down":
        screen.move(ship_id, 0, SHIP_SPEED)
        screen.move(ship_id2, 0, SHIP_SPEED)
    elif event.keysym == "Left":
        screen.move(ship_id, -SHIP_SPEED, 0)
        screen.move(ship_id2, -SHIP_SPEED, 0)
    elif event.keysym == "Right":
        screen.move(ship_id, SHIP_SPEED, 0)
        screen.move(ship_id2, SHIP_SPEED, 0)
screen.bind_all("<Key>", move_ship)

# Creating Bubbles
bub_id = []
bubR = []
bub_speed = []

# Create bubbles
def create_bubble():
    x: int = WIDTH + GAP
    y: int = randint(0, HEIGHT)
    r: int = randint(MIN_BUB_R, MAX_BUB_R)
    id1 = screen.create_oval(x - r, y - r, x + r, y + r, outline=choice(colors))
    bub_id.append(id1)
    bubR.append(r)
    bub_speed.append(randint(1, MAX_BUB_SPEED))

# Moving bubbles
def move_bubbles():
    for i, _ in enumerate(bub_id):
        screen.move(bub_id[i], -bub_speed[i], 0)

# Getting the position of bubbles
def get_coords(idNum: int) -> tuple[float, float]:
    pos: list[float] = screen.coords(idNum)
    x: float = (pos[0] + pos[2]) / 2
    y: float = (pos[1] + pos[3]) / 2
    return x, y

# Making the bubbles pop and cleaning up bubbles
def del_bubble(i: int):
    del bubR[i]
    del bub_speed[i]
    screen.delete(bub_id[i])
    del bub_id[i]
def clean_up_bubs():
    for i in range(len(bub_id) -1, -1, -1):
        x, _ = get_coords(bub_id[i])
        if x < -GAP:
            del_bubble(i)

# Working out the distance between points
def distance(id1: int, id2: int) -> float:
    x1, y1 = get_coords(id1)
    x2, y2 = get_coords(id2)
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Detecting Collision
def collision() -> int:
    points: int = 0
    for bub in range(len(bub_id) -1, -1, -1):
        if distance(ship_id2, bub_id[bub]) < SHIP_RADIUS + bubR[bub]:
            # Collision occurred
            points += (bubR[bub] + bub_speed[bub])
            del_bubble(bub)
    return points

# Display player's score and time left
screen.create_text(50, 30, text="TIME", fill='yellow')
screen.create_text(150, 30, text="SCORE", fill='yellow')
time_text: int = screen.create_text(50, 50, fill='yellow')
score_text: int = screen.create_text(150, 50, fill='yellow')
def show_score(score: int):
    screen.itemconfig(score_text, text=str(score))
def show_time(timeLeft: int):
    screen.itemconfig(time_text, text=str(timeLeft))

score: int = 0
end: float = time() + TIME_LIMIT

# Main gam loop
while time() < end:
    if randint(1, BUB_CHANCE) == 1:
        create_bubble()
    move_bubbles()
    clean_up_bubs()
    score += collision()
    show_score(score)
    show_time(int(end - time()))
    window.update()
    sleep(0.01)

# GAME OVER
screen.create_text(MID_X, MID_Y, text="GAME OVER", fill='white', font=('Arial', 30))
screen.create_text(MID_X, MID_Y + 30, text=f"Score: {score}", fill='white')
screen.create_text(MID_X, MID_Y + 45, text=f"Bonus time: {TIME_LIMIT}", fill='white')