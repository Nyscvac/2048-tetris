import os

import pygame as pg
# import copy
from math import ceil

import pygame.image
from pygame import freetype
from random import randint
from time import sleep

pg.init()
screen = pg.display.set_mode((255, 355), pg.SCALED)
pg.display.set_caption("2048 TETRIS")
pg.display.set_icon(pygame.image.load("2048.ico"))
clock = pg.time.Clock()

animing = False

off = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (232,106,128)
PURPLE128 = (125,142,212)
BLUE256 = (111,209,254)
BLUE16 = (89,190,234)
BLUE512 = (79,94,189)
GREEN = (145,224,84)
GREEN2 = (78,212,175)
YELLOW = (255,198,62)
ORANGE = (237,149,75)
RED1024 = (213,95,95)
RED = (255, 0, 0)
BACKGROUND1 = (42,173,217)
BACKGROUND2 = (45,182,228)

COLORS = {
    "2": GREEN2,
    "4": GREEN,
    "8": ORANGE,
    "16": BLUE16,
    "32": YELLOW,
    "64": PURPLE,
    "128": PURPLE128,
    "256": BLUE256,
    "512": BLUE512,
    "1024": RED1024,
    "2048": RED,
    "4096": BLACK
}

ITEMS = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, 4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4, 8,8,8,8,8,8,8,8,8, 16,16,16,16, 32,32, 64] #128, 256, 512, 1024, 2048, 4096]
my_font = freetype.SysFont("Times New Roman", 15, bold=True)

start = ITEMS[randint(0,len(ITEMS)-1)]
#start = 2

GRID_SIZE = [5, 7]

main_grid = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 32, 0, 0, 0],
    [0, 64, 0, 0, 0],
    [0, 128, 0, 0, 0],
]

STEP = 51
STEP_BACK = 50

tetris = 0

# БЛОК ПАДАЕТ -> update_matrix -> draw_anim -> calc_physics -> update_matrix -> ЕСЛИ ЕСТЬ ИЗМЕНЕНИЯ -> draw_anim -> calc_physics -> update_matrix.......

sq_pos = [1, 0, start]

def draw_background():
    c = 0
    for x in range(5):
        for y in range(7):
            if c == 0 or c == 2:
                pg.draw.rect(screen, BACKGROUND1, (x * STEP, y * STEP, 51, 51))
                #c = 0
            else:
                pg.draw.rect(screen, BACKGROUND2, (x * STEP, y * STEP, 51, 51))
                c = 1
        c += 1

def calc_physics(tetris_coords=0):
    again = False
    anim_grid = [[0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]]
    for i in range(len(anim_grid)):
        for x in range(5):
            anim_grid[i][x] += int(main_grid[i][x])
    global animing
    #global main_grid
    pr_coords = []
    anim_coords = []
    changed = False
    for x in range(GRID_SIZE[0]):
        place = []
        target = []
        for y in range(GRID_SIZE[1]):
            # time.sleep(0.3)
            if main_grid[GRID_SIZE[1] - y - 1][x] == 0 and place == []:
                place = [GRID_SIZE[1] - y - 1, x]
            if main_grid[GRID_SIZE[1] - y - 1][x] != 0:
                    if place != []:
                        if GRID_SIZE[1] - y - 1 < place[0]:
                            if target == []:
                                target = [GRID_SIZE[1] - y - 1, x]
                            else:
                                again = True
        if target != [] and place != []:
            if place[0] > target[0]:
                num1 = main_grid[target[0]][target[1]]
                #print(num1)
                #anim_grid[place[0]][place[1]] = anim_grid[target[0]][target[1]]
                anim_grid[target[0]][target[1]] = 0
                if tetris_coords == 0:
                    anim_coords.append([target[1] * STEP, target[1] * STEP, target[0] * STEP, place[0] * STEP])
                else:
                    #print("TETRIS!")
                    anim_coords.append([target[1] * STEP, target[1] * STEP, tetris_coords+50, place[0] * STEP+50])
                if tetris_coords == 0:
                    for i in range(place[0]*STEP - target[0]*STEP):
                        draw_background()
                        print("anim_coords:", len(anim_coords))
                        for x in anim_coords:
                            draw_anim(x, str(num1), "y", i, oldm=anim_grid)
                        pg.display.update()
                else:
                    for i in range(place[0]*STEP - tetris_coords-50):
                        draw_background()
                        print("anim_coords:", len(anim_coords))
                        for x in anim_coords:
                            draw_anim(x, str(num1), "y", i, oldm=anim_grid)
                        pg.display.update()
                sleep(0.05)
                main_grid[place[0]][place[1]] = main_grid[target[0]][target[1]]
                main_grid[target[0]][target[1]] = 0
                pr_coords.append([place[1], place[0]])
                animing = False
                changed = True


    if again:
        calc_physics()
    else:
        update_matrix(pr_coords)
    return changed

def height_to_coords(height):
    return ceil(height/STEP)

def update_matrix(pr=[]):
    anim_grid = [[0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]]
    #draw_grid(main_grid)
    for i in range(len(anim_grid)):
        for x in range(5):
            anim_grid[i][x] += int(main_grid[i][x])
    #global main_grid
    global animing
    changed = False
    anim_coords = []
    anim_vals = []
    if pr != []:
        for i in range(len(pr)):
            k = 1
            if pr[i][0] - 1 in range(len(main_grid[pr[i][1]])):
                if main_grid[pr[i][1]][pr[i][0] - 1] == main_grid[pr[i][1]][pr[i][0]]:
                    if main_grid[pr[i][1]][pr[i][0] - 1] != 0:
                        anim_coords.append([(pr[i][0]-1)*STEP,pr[i][0]*STEP, pr[i][1]*STEP, pr[i][1]*STEP, "x", main_grid[pr[i][1]][pr[i][0] - 1]])

                        main_grid[pr[i][1]][pr[i][0] - 1] = 0
                        k *= 2

            if pr[i][0] + 1 in range(len(main_grid[pr[i][1]])):
                if main_grid[pr[i][1]][pr[i][0] + 1] == main_grid[pr[i][1]][pr[i][0]]:
                    if main_grid[pr[i][1]][pr[i][0] + 1] != 0:
                        anim_coords.append([(pr[i][0] + 1) * STEP, pr[i][0] * STEP, pr[i][1] * STEP, pr[i][1] * STEP, "x", main_grid[pr[i][1]][pr[i][0] + 1]])
                        #anim_vals.append(main_grid[pr[i][1]][pr[i][0] + 1])
                        main_grid[pr[i][1]][pr[i][0] + 1] = 0
                        k *= 2

            if pr[i][1] + 1 in range(len(main_grid)):
                if main_grid[pr[i][1] + 1][pr[i][0]] == main_grid[pr[i][1]][pr[i][0]]:
                    if main_grid[pr[i][1]+ 1][pr[i][0]] != 0:
                        anim_coords.append([pr[i][0] * STEP, pr[i][0] * STEP, (pr[i][1]+1) * STEP, pr[i][1] * STEP, "y", main_grid[pr[i][1]+1][pr[i][0]]])
                        #anim_vals.append(main_grid[pr[i][1]+1][pr[i][0]])
                        main_grid[pr[i][1] + 1][pr[i][0]] = 0
                        k *= 2

            main_grid[pr[i][1]][pr[i][0]] = main_grid[pr[i][1]][pr[i][0]] * k


        if k != 1:
            changed = True
    if changed == False:
        #changed = True
        for x in range(5):
            for y in range(7):
                k = 1
                if x + 1 in range(5):
                    if main_grid[y][x] == main_grid[y][x+1] and main_grid[y][x+1] != 0:
                        anim_coords.append([(x + 1) * STEP, x * STEP, y * STEP, y * STEP, "x", main_grid[y][x + 1]])
                        main_grid[y][x + 1] = 0
                        k *= 2
                if x-1 in range(5):
                    if main_grid[y][x] == main_grid[y][x-1] and main_grid[y][x-1] != 0:
                        anim_coords.append([(x - 1) * STEP, x * STEP, y * STEP, y * STEP, "x", main_grid[y][x - 1]])
                        main_grid[y][x - 1] = 0
                        k *= 2
                if y+1 in range(7):
                    if main_grid[y][x] == main_grid[y+1][x] and main_grid[y+1][x] != 0:
                        anim_coords.append([x * STEP, x * STEP, (y+1) * STEP, y * STEP, "y", main_grid[y+1][x]])
                        main_grid[y+1][x] = 0
                        k *= 2
                main_grid[y][x] = main_grid[y][x] * k
                if k != 1:
                    changed = True

    if anim_coords != []:

        for x in range(50):
            draw_background()
            for i in anim_coords:
                draw_anim(i, str(i[5]), i[4], x, main_grid)
            #pg.display.flip()
            pg.display.update()
            #time.sleep(0.001)
        sleep(0.2)
        animing = False
    if changed:
        calc_physics()
    global off
    #draw_grid(main_grid)
    for i in range(5):
        c = 0
        for y in range(7):
            if main_grid[y][i] != 0:
                c += 1
        if c == 7:
            off = True
            #print("LOSE")
    return changed

def draw_anim(coords, val, mode, speed=3, oldm=[]):
    #print("awe")
    global animing
    #global main_grid
    animing = True
    if mode == "x":
        if coords[0] < coords[1]:
            #print("x")
            #draw_background()
            pg.draw.rect(screen, COLORS[val],(coords[0]+(speed), coords[2],50,50))
            my_font.render_to(screen, (coords[0]+(speed) + 13, coords[2] + 18), str(val), WHITE)
            draw_grid_anim(oldm)
        else:
            #draw_background()
            pg.draw.rect(screen, COLORS[val],(coords[0]-(speed), coords[2],50,50))
            my_font.render_to(screen, (coords[0]-(speed) + 13, coords[2] + 18), str(val), WHITE)
            draw_grid_anim(oldm)
    if mode == "y":
        #print("y")
        if coords[3] > coords[2]:

            #draw_background()
            pg.draw.rect(screen, COLORS[val],(coords[0], coords[2]+(speed),50,50))
            my_font.render_to(screen, (coords[0] + 13, coords[2]+(speed) + 18), str(val), WHITE)
            draw_grid_anim(oldm)
        else:
            #print("yy")
            #draw_background()
            pg.draw.rect(screen, COLORS[val],(coords[0], coords[2]-(speed),50,50))
            my_font.render_to(screen, (coords[0] + 13, coords[2] - (speed) + 18), str(val), WHITE)
            draw_grid_anim(oldm)

def draw_grid_anim(grid):
    #global main_grid
    #grid = main_grid
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != 0:
                pg.draw.rect(screen, COLORS[str(grid[y][x])], (x * STEP, y * STEP, 50, 50))
                my_font.render_to(screen, (x * STEP + 13, y * STEP + 18), str(grid[y][x]), WHITE)

def draw_grid(grid):
    for y in range(len(main_grid)):
        for x in range(len(main_grid[y])):
            if main_grid[y][x] != 0:
                pg.draw.rect(screen, COLORS[str(main_grid[y][x])], (x * STEP, y * STEP, 50, 50))
                my_font.render_to(screen, (x * STEP + 13, y * STEP + 18), str(main_grid[y][x]), WHITE)
    pg.display.flip()

draw_grid(main_grid)
draw_background()

going = True
while going:
    draw_background()

    draw_anim([sq_pos[0]* STEP, sq_pos[0] * STEP, 0 * STEP, 6 * STEP], str(sq_pos[2]), "y", tetris)
    draw_grid(main_grid)
    last_block = -1
    for i in range(7):
        if main_grid[i][sq_pos[0]] != 0:
            if last_block == -1:
                last_block = i-1
                if last_block < 0:
                    last_block = 0
                break
    print(last_block)
    if (tetris >= (last_block * STEP) and last_block != -1) or tetris >= 300:
        for i in range(len(main_grid)):
            if main_grid[GRID_SIZE[1] - 1 - i][sq_pos[0]] == 0:
                main_grid[0][sq_pos[0]] = sq_pos[2]
                num = ITEMS[randint(0, len(ITEMS) - 1)]

                calc_physics(tetris_coords=tetris)
                sq_pos[2] = num
                main_grid[0][sq_pos[0]] = 0
                draw_grid(main_grid)
                tetris = 0
                #print(last_block)
                break
        #print("HERE")
    #draw_grid(main_grid)
   # pg.display.update()
    #draw_grid(main_grid)
    sleep(0.01)
    if off == True:
        exit()
    tetris += 1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            going = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            going = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            if sq_pos[0]+1 in range(5):
                if main_grid[height_to_coords(tetris)][sq_pos[0]+1] == 0:
                    # screen.fill(BLACK)
                    if sq_pos[0] < 4:
                        sq_pos[0] += 1
                    main_grid[0][sq_pos[0] - 1] = 0
                    # num =  ITEMS[random.randint(0,len(ITEMS)-1)]
                    #main_grid[0][sq_pos[0]] = sq_pos[2]
                    draw_anim([sq_pos[0]*STEP , sq_pos[0]*STEP, 0 * STEP, 6 * STEP], str(sq_pos[2]), "y", tetris)
                    # sq_pos[2] = num
                    #draw_grid(main_grid)

            #print(main_grid[0])
        elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
            if sq_pos[0] - 1 in range(5):
                if main_grid[height_to_coords(tetris)][sq_pos[0]-1] == 0:

                    #

                    #print(height_to_coords(tetris),"AEFAEFF")
                    # screen.fill(BLACK)
                    if sq_pos[0] > 0:
                        sq_pos[0] -= 1
                    main_grid[0][sq_pos[0] + 1] = 0
                    # num = ITEMS[random.randint(0,len(ITEMS)-1)]
                    draw_anim([sq_pos[0]*STEP, sq_pos[0]*STEP, 0 * STEP, 6 * STEP], str(sq_pos[2]), "y", tetris)
                    #print("123")
                    #main_grid[0][sq_pos[0]] = sq_pos[2]
                    # sq_pos[2] = num
                    #draw_grid(main_grid)
        elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:

            for i in range(len(main_grid)):
                if main_grid[GRID_SIZE[1] - 1 - i][sq_pos[0]] == 0:
                    #print(main_grid)
                    main_grid[0][sq_pos[0]] = sq_pos[2]
                    num = ITEMS[randint(0, len(ITEMS) - 1)]

                    calc_physics(tetris_coords=tetris)
                    sq_pos[2] = num
                    main_grid[0][sq_pos[0]] = 0
                    #draw_grid(main_grid)
                    tetris = 0
                    break
    #draw_grid(main_grid)
    #print(main_grid)
    #update_matrix()
    #time.sleep(0.2)
    clock.tick(60)
