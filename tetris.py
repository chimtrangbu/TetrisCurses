#!/usr/bin/env python3
import curses
import random
import time
import os

class Cell(object):
    def __init__(self,screen, x, y):
        self.x = x
        self.y = y
        self.screen = screen

    def move(self, event):
        # if event == chr(curses.KEY_UP):
        #     self.x -= 1
        if event == curses.KEY_DOWN and self.x < MAX_X and not self.hit_():
            self.x += 1
            return True
        elif event == curses.KEY_LEFT and self.y > 1 and not self.has_colide():
            self.y -= 1
            return True
        elif event == curses.KEY_RIGHT and self.y < MAX_Y and not self.has_colide():
            self.y += 1
            return True
        return False

    def render(self):
        self.screen.addstr(self.x, self.y, 'X')

    def touch_down(self):
        if BRICKS:
            return self.x+1 in [b.x for b in BRICKS if b.y == self.y]

    def touch_bottom(self):
        return self.x == MAX_X

    def has_colide(self):
        if self.y+1 in [b.y for b in BRICKS if b.x == self.x]:
            return True
        if self.y-1 in [b.y for b in BRICKS if b.x == self.x]:
            return True
        return False

    def hit_(self):
        if BRICKS and self.x+1 in [b.x for b in BRICKS if b.y == self.y]:
            return True
        if self.touch_bottom():
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
                brick.x += 1

def game_over(block):
    return block in BRICKS

def show_score(window):
    window.clear()
    window.addstr(HEIGHT//2, WIDTH - 5, 'GAME OVER')
    window.addstr(HEIGHT//2+2, WIDTH - 7, ' your score: ' + str(SCORE))
    window.refresh()
    time.sleep(2)


if __name__ == '__main__':
    window = curses.initscr()
    width, height = os.get_terminal_size()
    HEIGHT, WIDTH = height, width//2
    MAX_X, MAX_Y = HEIGHT - 2, WIDTH - 1
    TIMEOUT = 100
    # curses.beep()
    # curses.flash()
    curses.noecho()
    curses.curs_set(0)  # invisible cursor
    window.timeout(TIMEOUT)
    window.keypad(True)
    SCORE = 0
    block = Cell(window, 1, random.randint(1, MAX_Y))
    BRICKS = []
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
        if block.hit_():
            if block.x <= 1:
                show_score(window)
                break
            BRICKS.append(block)
            block = Cell(window, 1, random.randint(1, MAX_Y))
            # block = Cell(window, 1, 5)
        else:
            block.x += 1
        event = window.getch()
        if event == 27 or event == 410:
            show_score(window)
            break
        block.move(event)
        time.sleep(1/20)
    curses.endwin()
