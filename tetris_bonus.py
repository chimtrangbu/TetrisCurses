#!/usr/bin/env python3
import curses
import random
import time
import os


class Cell(object):
    def __init__(self,window, x, y):
        self.x = x
        self.y = y
        self.window = window

    def move(self, event):
        # if event == curses.KEY_UP:
        #     self.x -= 1
        if event == curses.KEY_DOWN and self.x < MAX_X and not self.hit_():
            self.x += 1
        elif event == curses.KEY_LEFT and self.y > 1 and not self.has_colide():
            self.y -= 1
        elif event == curses.KEY_RIGHT and self.y < MAX_Y and not self.has_colide():
            self.y += 1

    def render(self):
        self.window.addstr(self.x, self.y, 'X')

    def touch_down(self):
        if BRICKS:
            return self.x+1 in [b.x for b in BRICKS if b.y == self.y]
        return False

    def touch_bottom(self):
        return self.x == MAX_X

    def has_colide(self):
        if self.y+1 in [b.y for b in BRICKS if b.x == self.x] or self.y+1 not in range(1, MAX_Y+1):
            return True
        if self.y-1 in [b.y for b in BRICKS if b.x == self.x] or self.y-1 not in range(1, MAX_Y+1):
            return True
        return False

    def hit_(self):
        if BRICKS and self.x+1 in [b.x for b in BRICKS if b.y == self.y]:
            return True
        if self.touch_bottom():
            return True
        return False

    def create_new(self, tuple):
        return Cell(self.window, self.x + tuple[0], self.y + tuple[1])


class Block(object):

    def __init__(self, window):
        self.anchor = Cell(window, 2, WIDTH//2)
        block_shapes = [
            # T Block
            [(0,0), (0,-1), (0,1), (1,0)],
            # L Block
            [(-1,0), (0,0), (1,0), (1,1)],
            # J Block
            [(-1,0), (0,0), (1,0), (1,-1)],
            # S Block
            [(0,0), (0,1), (1,0), (1,-1)],
            # Z Block
            [(0,0), (0,-1), (1,0), (1,1)],
            # O Block
            [(0,0), (0,-1), (1,0), (1,-1)],
            # I Block
            [(0,0), (-1,0), (1,0), (2,0)],
        ]
        self.shape = block_shapes[random.randint(0,6)]
        self.block = []
        for tup in self.shape:
            self.block.append(self.anchor.create_new(tup))

    def render(self):
        for cell in self.block:
            cell.render()

    def rotate(self):
        new_block = []
        new_shape = []
        for tup in self.shape:
            new_tup = (tup[1], -tup[0])
            new_shape.append(new_tup)
            new_block.append(self.anchor.create_new(new_tup))
        return new_shape, new_block

    def can_rotate(self):
        shape, block = self.rotate()
        for cell in block:
            if cell.hit_() or cell.has_colide():
                return False
        return True

    def move(self, d='D'):
        new_block = []
        if d == 'D':
            new_anchor = self.anchor.create_new((1,0))
            for tup in self.shape:
                new_tup = (tup[0]+1, tup[1])
                new_block.append(self.anchor.create_new(new_tup))
        elif d == 'L':
            new_anchor = self.anchor.create_new((0,-1))
            for tup in self.shape:
                new_tup = (tup[0], tup[1]-1)
                new_block.append(self.anchor.create_new(new_tup))
        elif d == 'R':
            new_anchor = self.anchor.create_new((0,1))
            for tup in self.shape:
                new_tup = (tup[0], tup[1]+1)
                new_block.append(self.anchor.create_new(new_tup))
        else:
            new_anchor = self.anchor
            new_block = self.block
        return new_anchor, new_block

    def can_move(self, d='D'):
        if d=='D':
            for cell in self.block:
                if cell.hit_():
                    return False
        else:
            for cell in self.block:
                if cell.has_colide():
                    return False
        return True

    def update(self, event):
        if event == curses.KEY_UP and self.can_rotate():
            self.shape, self.block = self.rotate()
        elif event == curses.KEY_DOWN and self.can_move('D'):
            self.anchor, self.block = self.move('D')
        elif event == curses.KEY_LEFT and self.can_move('L'):
            self.anchor, self.block = self.move('L')
        elif event == curses.KEY_RIGHT and self.can_move('R'):
            self.anchor, self.block = self.move('R')

    def hit_(self):
        # if not BRICKS:
        #     return False
        for cell in self.block:
            if cell.hit_():
                return True

        return False


def draw_horizon(window):
    for i in range(1,HEIGHT-1):
        window.addstr(i, WIDTH, '|')

def update_score():
    global SCORE, BRICKS
    for i in range(MAX_X + 1,1,-1):
        row = []
        for brick in BRICKS:
            if i == brick.x:
                row.append(brick)
        if len(row) == MAX_Y:
            SCORE += 1
            BRICKS = [b for b in BRICKS if b not in row]
            for brick in BRICKS:
                if brick.x < i:
                    brick.x += 1

# def game_over(block):
#     return (block.hit_() and block.anchor.x <= 1)

def show_score(window):
    window.clear()
    window.addstr(HEIGHT//2, WIDTH - 5, 'GAME OVER')
    window.addstr(HEIGHT//2+2, WIDTH - 7, ' your score: ' + str(SCORE))
    window.refresh()
    time.sleep(2)


if __name__ == '__main__':
    window = curses.initscr()
    width, height = os.get_terminal_size()
    # width, height = 20, 20
    HEIGHT, WIDTH = height, width//2
    MAX_X, MAX_Y = HEIGHT - 2, WIDTH - 1
    TIMEOUT = 1000
    # curses.beep()
    # curses.flash()
    curses.noecho()
    curses.curs_set(0)  # invisible cursor
    window.timeout(TIMEOUT)
    window.keypad(True)
    SCORE = 0
    # block = Cell(window, 1, random.randint(1, MAX_Y))
    BRICKS = []
    block = Block(window)
    while True:
        window.clear()
        window.border(0)
        draw_horizon(window)
        update_score()
        window.addstr(HEIGHT//2-2, WIDTH+5, 'Score:')
        window.addstr(HEIGHT//2, WIDTH+7, str(SCORE))
        block.render()
        for b in BRICKS:
            b.render()

        # touch = False
        # for cell in block.block:
        #     if cell.x >= MAX_X-1:
        #         touch = True
        # if touch:
        #     if block.anchor.x <= 1:
        #         show_score(window)
        #         break
        #     BRICKS += block.block
        #     block = Block(window)
        # else:
        #     block.update(curses.KEY_DOWN)
        if block.hit_():
            if block.anchor.x <= 1:
                show_score(window)
                break
            BRICKS += block.block
            block = Block(window)
            if not block.can_move():
                show_score(window)
                break
        else:
            block.update(curses.KEY_DOWN)
        event = window.getch()
        if event == 27 or event == 410:
            show_score(window)
            break
        block.update(event)
    curses.endwin()
