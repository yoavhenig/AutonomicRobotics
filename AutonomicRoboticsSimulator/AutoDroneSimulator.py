from pygame.locals import *
import pygame
import math
import random

def stop(degree, direction):
    fullRotation = 0;
    maxDistance = 0;
    maxDirection = 0
    while True:
        # What coordinates will the static image be placed:
        where = x, y

        screenData = fillScreen(where)
        blittedRect = screenData[0]
        drone = screenData[1]

        ranges = drawSensors()
        rangeToRight = ranges[0]
        rangeToLeft = ranges[1]
        rangeToWall = ranges[2]

        if rangeToWall > maxDistance:
            maxDistance = rangeToWall
            maxDirection = degree
        # #ROTATED
        # get center of drone for later
        oldCenter = blittedRect.center

        # rotate drone by DEGREE amount degrees
        rotatedSurf = pygame.transform.rotate(drone, degree)

        # get the rect of the rotated drone and set it's center to the oldCenter
        rotRect = rotatedSurf.get_rect()
        rotRect.center = oldCenter

        # draw rotatedSurf with the corrected rect so it gets put in the proper spot
        screen.blit(rotatedSurf, rotRect)

        # change the degree of rotation
        degree += rotate
        if degree > 360:
            degree = 0

        direction -= dRotate
        if direction > 360:
            direction = 0

        fullRotation += rotate
        if fullRotation > 360:
            return maxDirection

    # show the screen surface
    pygame.display.flip()

    # wait ? ms until loop restarts
    pygame.time.wait(20)

def drawSensors():
    begin = (x, y)

    rightData = get_end(direction + 0.9)
    leftData = get_end(direction - 0.9)
    middleData = get_end(direction)

    RsensorEnd = rightData[0]
    LsensorEnd = leftData[0]
    MsensorEnd = middleData[0]

    rangeToRight = rightData[1]
    rangeToLeft = leftData[1]
    rangeToWall = middleData[1]

    pygame.draw.line(screen, green, begin, RsensorEnd, 1)
    pygame.draw.line(screen, green, begin, LsensorEnd, 1)
    pygame.draw.line(screen, green, begin, MsensorEnd, 1)

    print("Range to right: " + str(rangeToRight))
    print("Range to left: " + str(rangeToLeft))
    print("Range to wall: " + str(rangeToWall))

    lines.append((begin, RsensorEnd))
    lines.append((begin, LsensorEnd))
    lines.append((begin, MsensorEnd))
    walls.append(RsensorEnd)
    walls.append(LsensorEnd)
    path.append(where)

    return [rangeToRight, rangeToLeft, rangeToWall]


def fillScreen(where):
    screen.fill((255, 255, 255))

    # # create new surface with white BG
    drone = pygame.Surface((1, 1))
    drone.fill((0, 0, 0))
    # drone = pygame.image.load('drone.png')
    # drone = pygame.draw.rect(drone, (0, 255, 0), (x, y, x+50, y+50), 2)

    # draw the previous sensors
    for i in lines:
        pygame.draw.line(screen, gray, i[0], i[1], 1)
    for i in walls:
        pygame.draw.circle(screen, red, i, 1, 0)
    for i in path:
        pygame.draw.circle(screen, blue, i, 1, 0)


    # draw drone to screen and catch the rect that blit returns
    blittedRect = screen.blit(drone, where)
    return [blittedRect, drone]


def get_end(direction):
    last_color = (255, 255, 255, 255)
    for i in range(20, 100000):
        range_to_wall = i
        blackPos = int(x + i * math.cos(direction)), int(y + i * math.sin(direction))
        try:
            color = background.get_at(blackPos)
            if last_color != color:
                # last_color = color
                return [blackPos, range_to_wall]
        except IndexError:
            return [(int(x + (i - 1) * math.cos(direction)), int(y + (i - 1) * math.sin(direction))), range_to_wall]


# necessary pygame initializing
pygame.init()

# create a surface that will be seen by the user
background = pygame.image.load('backgrounds/p14.png')
screen = pygame.display.set_mode(background.get_rect().size)

# create a varibles for initial coordinates
x = 100
y = 100
surfR = 8

# create a varible for degrees pf rotation
degree = 0
rotate = 2.5
direction = 0
dRotate = rotate / 58

# create lines and points lists for prescan sensors
lines = []
walls = []
path = []

# create variable for colors
white = (255, 255, 255)
green = (0, 255, 0)
gray = (224, 238, 238)
red = (223, 223, 0)
blue = (135, 206, 235)
orange = (255, 69, 0)

# create fail counter
failure = 0

while True:
    # What coordinates will the static image be placed:
    where = int(x), int(y)

    screenData = fillScreen(where)
    blittedRect = screenData[0]
    drone = screenData[1]

    pygame.draw.circle(screen, orange, where, 7, 0)

    ranges = drawSensors()
    rangeToRight = ranges[0]
    rangeToLeft = ranges[1]
    rangeToWall = ranges[2]

    pygame.event.pump()
    keys = pygame.key.get_pressed()

    if rangeToWall <= 40 and abs(rangeToLeft - rangeToRight) <= 3:
        direction = stop(degree, direction)

    if rangeToWall <= 40 and rangeToLeft > 10 and rangeToRight > 10:
        if random.randint(1, 100) < 50:
            direction = direction + 0.9
        else:
            direction = direction - 0.9

    if keys[K_w] or rangeToWall > 40:
        # moveForward(x, y, )
        if background.get_at((int(x + surfR + math.cos(direction)), int(y + surfR + math.sin(direction)))) != white:
            failure += 1
            print("Failure: ", failure)
            # step back
            x -= math.cos(direction)
            y -= math.sin(direction)
            continue
        # #FORWARD
        x += math.cos(direction)
        y += math.sin(direction)

    if (keys[K_s]):
        # #BACKWARD
        x -= math.cos(direction)
        y -= math.sin(direction)

    if keys[K_a] or rangeToLeft > rangeToRight:
        # #ROTATED
        # get center of drone for later
        oldCenter = blittedRect.center

        # rotate drone by DEGREE amount degrees
        rotatedSurf = pygame.transform.rotate(drone, degree)

        # get the rect of the rotated drone and set it's center to the oldCenter
        rotRect = rotatedSurf.get_rect()
        rotRect.center = oldCenter

        # draw rotatedSurf with the corrected rect so it gets put in the proper spot
        screen.blit(rotatedSurf, rotRect)

        # change the degree of rotation
        degree += rotate
        if degree > 360:
            degree = 0

        direction -= dRotate
        if direction > 360:
            direction = 0

    if keys[K_d] or rangeToRight > rangeToLeft:
        # # ROTATED
        # get center of drone for later
        oldCenter = blittedRect.center

        # rotate drone by DEGREE amount degrees
        rotatedSurf = pygame.transform.rotate(drone, degree)

        # get the rect of the rotated drone and set it's center to the oldCenter
        rotRect = rotatedSurf.get_rect()
        rotRect.center = oldCenter

        # draw rotatedSurf with the corrected rect so it gets put in the proper spot
        screen.blit(rotatedSurf, rotRect)

        # change the degree of rotation
        degree -= rotate
        if degree > 360:
            degree = 0

        direction += dRotate
        if direction > 360:
            direction = 0

    # show the screen surface
    pygame.display.flip()

    # wait 60 ms until loop restart
    pygame.time.wait(10)


# pix = 2.5 cm
# RES 40 pix = 1.0 meter
# ft = 60.5
# mqx speed = 3m/s
# max acc = 2
# max ang = pi/sec
