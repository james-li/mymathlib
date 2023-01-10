#!/usr/bin/env python3

import numpy as np


def neighbor_area(clicked_x: int, clicked_y: int, width: int, height: int) -> list:
    x_area = [x for x in [clicked_x - 1, clicked_x, clicked_x + 1] if 0 <= x < width]
    y_area = [x for x in [clicked_y - 1, clicked_y, clicked_y + 1] if 0 <= x < height]
    return np.array(np.meshgrid(x_area, y_area)).T.reshape(-1, 2)


def expand_area(arr: np.ndarray, mines: dict, clicked_x: int, clicked_y: int, blank_area: dict = {}) -> dict:
    if mines[(clicked_x, clicked_y)] != 0:
        return blank_area
    neighbor = neighbor_area(clicked_x, clicked_y, arr.shape[1], arr.shape[0])
    for x, y in neighbor:
        if (x, y) != (clicked_x, clicked_y):
            if (x, y) not in blank_area:
                blank_area[(x, y)] = 1
                blank_area.update(expand_area(arr, mines, x, y, blank_area))
        else:
            blank_area[(x, y)] = 2
    return blank_area


def generate_mine_map(width: int, height: int, mine_number: int, clicked_x: int = 0, clicked_y: int = 0,
                      blank_size: int = 9):
    while True:
        choice = np.random.choice(width * height, mine_number, replace=False)
        # print(choice)
        arr = np.zeros((height, width)).astype(int)
        for i in choice:
            arr[i // width, i % width] = 1
        # print(arr)
        # print("\n")
        if arr[clicked_y, clicked_x]:
            continue
        mines = {}
        for x in range(arr.shape[1]):
            for y in range(arr.shape[0]):
                if arr[y, x]:
                    mines[(x, y)] = 9
                else:
                    neighbor = neighbor_area(x, y, width, height)
                    n = 0
                    for _x, _y in neighbor:
                        if arr[_y, _x]:
                            n += 1
                    mines[(x, y)] = n
        blank_area = expand_area(arr, mines, clicked_x, clicked_y)
        if len(blank_area) < blank_size:
            continue
        return (mines, blank_area)


WHITE = '\033[0m'
RED = '\033[91m'
GRAY = '\033[37m'
BLUE = '\033[94m'


def colored_mine(mines, blank_area, x, y):
    if (x, y) in blank_area:
        return WHITE + "%02d" % (mines[(x, y)])
    elif mines[(x, y)] == 9:
        return RED + "%02d" % (mines[(x, y)])
    else:
        return GRAY + "%02d" % (mines[(x, y)])


def mine_sweeper(mines, width, height, init_blank_area: dict):
    revealed_area = {x: (mines[x], 0) for x in init_blank_area.keys()}
    while True:
        investigate_area = {}
        for p in list(revealed_area.keys()):
            mine_number, revealed_number = revealed_area[p]
            if mine_number == revealed_number:  # all mines revealed
                continue
            x, y = p
            neighbor = neighbor_area(x, y, width, height)
            revealed_mines = 0
            for _x, _y in neighbor:
                if (_x, _y) not in revealed_area:
                    i_lst = investigate_area.get(p, [])
                    i_lst.append((_x, _y))
                    investigate_area[p] = i_lst
                elif revealed_area[(_x, _y)][0] == 9:  # revealed_mine
                    revealed_mines += 1
            if (mine_number - revealed_number - revealed_mines) == len(investigate_area.get(p, [])):
                for mine in list(investigate_area.get(p, [])):
                    revealed_area[mine] = (9, 9)
                    revealed_number += 1
                    investigate_area.pop(mine)
                revealed_area[p] = (mine_number, revealed_number)


if __name__ == "__main__":
    mines, blank_area = generate_mine_map(30, 16, 99, 10, 10, 9)
    print(BLUE + "    " + " ".join(["%02d" % x for x in range(30)]))
    for y in range(16):
        line = [colored_mine(mines, blank_area, x, y) for x in range(30)]
        print("%02d" % y + ": " + " ".join(line))
    mine_sweeper(mines, 30, 16, blank_area)
