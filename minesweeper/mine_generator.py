#!/usr/bin/env python3

import numpy as np


class BoomException(BaseException):
    pass


def neighbor_area(clicked_x: int, clicked_y: int, width: int, height: int) -> list:
    x_area = [x for x in [clicked_x - 1, clicked_x, clicked_x + 1] if 0 <= x < width]
    y_area = [x for x in [clicked_y - 1, clicked_y, clicked_y + 1] if 0 <= x < height]
    r = [tuple(x) for x in np.array(np.meshgrid(x_area, y_area)).T.reshape(-1, 2)]
    r.remove((clicked_x, clicked_y))
    return r


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
    return {p: mines[p] for p in blank_area.keys()}


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


def get_common_neighbor(p1_neighbor, p2_neighbor):
    common_neighbor = []
    for p in p1_neighbor:
        if p in p2_neighbor:
            common_neighbor.append(tuple(p))
    return common_neighbor


def mine_sweeper(mines, width, height, init_blank_area: dict):
    revealed_area = {x: mines[x] for x in init_blank_area.keys()}
    while True:
        for p in list(revealed_area.keys()):
            mine_number = revealed_area[p]
            revealed_number = 0
            revealed_mines = 0
            if mine_number == 9:
                continue
            x, y = p
            neighbor = neighbor_area(x, y, width, height)
            i_lst = []
            for _pos in neighbor:
                pos = tuple(_pos)
                if pos not in revealed_area:
                    i_lst.append(pos)
                elif revealed_area[pos] == 9:
                    revealed_mines += 1
            if (mine_number - revealed_mines) == len(i_lst):
                # dig mine
                for mine in i_lst:
                    revealed_area[mine] = 9
                    revealed_mines += 1
                # reveal safe area
            if mine_number == revealed_mines:
                for _pos in neighbor:
                    pos = tuple(_pos)
                    if pos not in revealed_area:
                        if mines[pos] == 9:
                            raise BoomException("Boom!!!!!")
                        revealed_area[pos] = mines[pos]
        ## TODO: 比较相邻两个位置，标识
        p1_lst = []
        for p1 in list(revealed_area.keys()):
            p1_lst.append(p1)
            for p2 in list(revealed_area.keys()):
                if p2 in p1_lst or not get_common_neighbor(p1, p2, width, height):
                    continue


if __name__ == "__main__":
    mines, blank_area = generate_mine_map(30, 16, 99, 10, 10, 9)
    print(BLUE + "    " + " ".join(["%02d" % x for x in range(30)]))
    for y in range(16):
        line = [colored_mine(mines, blank_area, x, y) for x in range(30)]
        print("%02d" % y + ": " + " ".join(line))
    mine_sweeper(mines, 30, 16, blank_area)
