from sense_hat import SenseHat, ACTION_PRESSED
from time import sleep
import random
from random import randint
import dbconnection
import os

sense = SenseHat()

sense.low_light = True

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255,255,255)
score = 0
x = 4

bullet_frame = 1
bullet = False

ticks = 0
tick_state = 70
loading = 0

matrix = [[BLUE for column in range(8)] for row in range(8)]


def flatten(matrix):
    flattened = [pixel for row in matrix for pixel in row]
    return flattened

def gen_asteroids(matrix):
    for row in matrix:
        row[-1] = BLUE
    set_of_enemies = (random.sample(range(0,8),random.randint(1,4)))
    for d in set_of_enemies:
        matrix[d][-1] = RED
    return matrix

def move_asteroids(matrix):
    for row in matrix:
        for i in range(7):
            row[i] = row[i + 1]
        row[-1] = BLUE
    return matrix

def draw_astronaut(event):
    global y
    global x
    if x >= 1 and x <=6:
        sense.set_pixel(0,x,  BLUE)
        sense.set_pixel(1,x,  BLUE)
        sense.set_pixel(0,x+1, BLUE)
        sense.set_pixel(0,x-1, BLUE)
    elif x == 0:
        sense.set_pixel(1,x, BLUE)
        sense.set_pixel(0,x,  BLUE)
        sense.set_pixel(0,x+1, BLUE)
    elif x == 7:
        sense.set_pixel(0,x, BLUE)
        sense.set_pixel(1,x,  BLUE)
        sense.set_pixel(0,x-1, BLUE)

    if event.action == "pressed":
        if event.direction == "up" and x < 7:
            x += 1
        elif event.direction == "down" and x > 0:
            x -= 1
    draw_tank(x)


def draw_tank(x):
    if x >= 1 and x <=6:
        sense.set_pixel(0,x,  YELLOW)
        sense.set_pixel(1,x,  YELLOW)
        sense.set_pixel(0,x+1, YELLOW)
        sense.set_pixel(0,x-1, YELLOW)
    elif x == 0:
        sense.set_pixel(1,x, YELLOW)
        sense.set_pixel(0,x,  YELLOW)
        sense.set_pixel(0,x+1, YELLOW)
    elif x == 7:
        sense.set_pixel(0,x, YELLOW)
        sense.set_pixel(1,x,  YELLOW)
        sense.set_pixel(0,x-1, YELLOW)

def bullet_trajectory(matrix):
    global bullet
    global bullet_x
    global score
    if bullet == True:
        global bullet_frame
        bullet_frame += 1
        if matrix[bullet_x][bullet_frame-1] != RED and bullet_frame < 8:
            sense.set_pixel( bullet_frame,bullet_x, WHITE)
            sense.set_pixel( bullet_frame-1,bullet_x, BLUE)
                
        else:
            if matrix[bullet_x][bullet_frame-1] == RED :
                score += 1
                print ("score: ",score)
            sense.set_pixel( bullet_frame-1,bullet_x, BLUE)
            matrix[bullet_x][bullet_frame-1] = BLUE           
            bullet = False 
            bullet_frame=1
            return matrix

def shoot(event):
    global bullet_x
    global bullet
    if bullet == False:
        bullet = True
        bullet_x = x

def layer_collistion(matrix):
    global score
    for row in matrix:
        if row[1] != BLUE:
            sense.set_rotation(270)
            sense.show_message("TANK DESTROYED")
            dbconnection.establishConnection(int(score))
            os.system('/usr/bin/python3 /home/pi/tanks/tankGameWebApp/tankGameWeb.py')
            quit()



sense.stick.direction_middle = shoot
sense.stick.direction_any = draw_astronaut

sense.set_rotation(270)

sense.show_message("SPACE TANKS")

sense.set_rotation(180)

sense.set_pixels(flatten(matrix))
matrix = gen_asteroids(matrix)

while True:
    draw_tank(x)
    bullet_trajectory(matrix)
    sleep(0.35)
    ticks += 5
    if ticks == (tick_state):
        bullet_trajectory(matrix)
        loading += 1
        if loading == 5:
            tick_state -= 5
            loading = 0
        matrix = move_asteroids(matrix)
        matrix = gen_asteroids(matrix)
        sense.set_pixels(flatten(matrix))
        ticks = 0
        if layer_collistion(matrix):
            break 