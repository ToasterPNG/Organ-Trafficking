import pygame, random

last_shake = (0, 0)

def shake(points, shake_ammount):

    point_1 = points[0] - random.randint(1, shake_ammount)
    point_2 = points[1] - random.randint(1, shake_ammount)

    shake = (point_1, point_2)

    return shake

def smoothshake(points, shake_ammount, radius=175):
    global last_shake

    point_1 = points[0] - random.randint(1, int(shake_ammount / 12)) - last_shake[0] / radius
    point_2 = points[1] - random.randint(1, int(shake_ammount / 12)) - last_shake[1] / radius

    shake = (point_1, point_2)

    last_shake = (point_1, point_2)

    return shake