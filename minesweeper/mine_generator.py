#!/usr/bin/env python3

import numpy as np


class BoomException(BaseException):
    pass


class mine_generator(object):
    _revealed_area: dict
    _mines: dict

    def __init__(self, width: int, height: int, mine_number: int, clicked_x: int = 0, clicked_y: int = 0,
                 blank_size: int = 9):
        self._width = width
        self._height = height
        self._mine_number = mine_number
        self._mines, self._revealed_area = generate_mine_map(width, height, mine_number, clicked_x, clicked_y,
                                                             blank_size)
        self._clear_area = {}
        self._revealed_mines = 0

    def get_mine_info(self):
        return u"%d/%d" % (self._revealed_mines, self._mine_number)

    def get_squares(self):
        return self._mines.keys()

    def get_square_mines(self, p):
        return self._mines.get(p)

    def neighbor_area(self, p) -> list:
        return neighbor_area(p[0], p[1], self._width, self._height)

    def get_revealed_area(self):
        return self._revealed_area

    def get_size(self) -> tuple:
        return self._width, self._height

    def intersection_neighbor(self, p1: tuple, p2: tuple) -> tuple:
        p1_neighbor = self.neighbor_area(p1)
        p2_neighbor = self.neighbor_area(p2)
        return self.intersection_area(p1_neighbor, p2_neighbor)

    def intersection_area(self, area1: iter, area2: iter) -> tuple:
        p1_p2 = {}
        p1np2 = {}
        p2_p1 = {}
        for p in area1:
            if p in area2:
                p1np2[p] = 1
            else:
                p1_p2[p] = 1
        for p in area2:
            if p not in area1:
                p2_p1[p] = 1
        return p1_p2, p1np2, p2_p1

    def sweep_mine(self, area: iter) -> bool:
        print("sweep mine at %s" % str(area))
        for mine in area:
            self._revealed_area[mine] = 9
            self._revealed_mines += 1
        return len(area) > 0

    def clear_safe_area(self, area: iter) -> bool:
        unrevealed_area = [x for x in area if x not in self._revealed_area]
        if not unrevealed_area:
            return False
        print("clear safe area at %s" % str(unrevealed_area))
        updated = False
        for pos in unrevealed_area:
            if self.get_square_mines(pos) == 9:
                raise BoomException("Boom!!!!! at " + str(pos))
            self._revealed_area[pos] = self.get_square_mines(pos)
            updated = True
        return updated

    def simple_resolve(self) -> bool:
        print("Start to sweep mine by single square")
        revealed_area = self._revealed_area
        updated = False
        for p in list(revealed_area.keys()):
            if p in self._clear_area.keys():
                continue
            mine_number = revealed_area[p]
            if mine_number == 9:
                self._clear_area[p] = 9
                continue
            neighbor = self.neighbor_area(p)
            unrevealed_neighbor = [x for x in neighbor if x not in self._revealed_area]
            revealed_mines = [x for x in neighbor if x in self._revealed_area and self.get_square_mines(x) == 9]

            if (mine_number - len(revealed_mines)) == len(unrevealed_neighbor):
                # dig mine
                if unrevealed_neighbor:
                    updated = self.sweep_mine(unrevealed_neighbor)
                # reveal safe area
            if self.get_unrevealed_mines(p) == 0:
                updated |= self.clear_safe_area(neighbor)
                self._clear_area[p] = mine_number
            if self.get_unrevealed_mines(p) == (self._mine_number - self._revealed_mines):
                updated |= self.clear_safe_area(
                    [x for x in self._mines.keys() if x not in self._revealed_area and x not in self.neighbor_area(p)])
        if updated:
            return True
        return False

    def combo_resolve(self) -> bool:
        print("Start to sweep mine by combo square")
        p1_lst = {}
        updated = False
        for p1 in list(self._revealed_area.keys()):
            p1_lst[p1] = 1
            m1 = self.get_unrevealed_mines(p1)
            if m1 == 0:
                continue
            for p2 in list(self._revealed_area.keys()):
                if p2 in p1_lst:
                    continue
                m2 = self.get_unrevealed_mines(p2)
                if m2 == 0:
                    continue
                p1_p2, p1np2, p2_p1 = self.intersection_neighbor(p1, p2)
                if not p1np2:
                    continue
                unrevealed_area = lambda lst: [p for p in lst if p not in self._revealed_area]
                p1_p2_unrevealed = unrevealed_area(p1_p2)
                p2_p1_unrevealed = unrevealed_area(p2_p1)
                p1np1_unrevealed = unrevealed_area(p1np2)
                mine_area = {}
                safe_area = {}
                if len(p1_p2_unrevealed) == m1 - m2:
                    mine_area = p1_p2_unrevealed
                if len(p2_p1_unrevealed) == m2 - m1:
                    mine_area = p2_p1_unrevealed
                if m2 <= (m1 - len(p1_p2_unrevealed)):
                    safe_area = p2_p1_unrevealed
                if m1 <= (m2 - len(p2_p1_unrevealed)):
                    safe_area = p1_p2_unrevealed
                if mine_area:
                    updated = self.sweep_mine(mine_area)
                if safe_area:
                    updated |= self.clear_safe_area(safe_area)
        if updated:
            return True
        return False

    def get_unrevealed_mines(self, p: tuple) -> int:
        m = self.get_square_mines(p)
        if m == 0 or m == 9:
            return 0
        for n in self.neighbor_area(p):
            if n != p and n in self._revealed_area.keys():
                if self._mines.get(n) == 9:
                    m -= 1
        return m


def neighbor_area(clicked_x: int, clicked_y: int, width: int, height: int) -> list:
    x_area = [x for x in [clicked_x - 1, clicked_x, clicked_x + 1] if 0 <= x < width]
    y_area = [x for x in [clicked_y - 1, clicked_y, clicked_y + 1] if 0 <= x < height]
    r = [tuple(x) for x in np.array(np.meshgrid(x_area, y_area)).T.reshape(-1, 2)]
    # r.remove((clicked_x, clicked_y))
    return r


def expand_area(mines: dict, clicked_x: int, clicked_y: int, width, height, init_blank_area: dict = None) -> dict:
    if init_blank_area is None:
        init_blank_area = {}
    if mines[(clicked_x, clicked_y)] != 0:
        return init_blank_area
    neighbor = neighbor_area(clicked_x, clicked_y, width, height)
    for x, y in neighbor:
        if (x, y) != (clicked_x, clicked_y):
            if (x, y) not in init_blank_area:
                init_blank_area[(x, y)] = 1
                init_blank_area.update(expand_area(mines, x, y, width, height, init_blank_area))
        else:
            init_blank_area[(x, y)] = 2
    return init_blank_area


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
        blank_area = expand_area(mines, clicked_x, clicked_y, width, height)
        if len(blank_area) < blank_size:
            continue
        return mines, {p: mines[p] for p in blank_area.keys() if mines[p] != 9}


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


if __name__ == "__main__":
    mines, blank_area = generate_mine_map(30, 16, 99, 10, 10, 9)
    print(BLUE + "    " + " ".join(["%02d" % x for x in range(30)]))
    for y in range(16):
        line = [colored_mine(mines, blank_area, x, y) for x in range(30)]
        print("%02d" % y + ": " + " ".join(line))
